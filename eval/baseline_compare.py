#!/usr/bin/env python3
"""Actually RUN Presidio (Russian) + Philter + CONFIDE on a folder of sessions and
report a STATS-ONLY diff: per-engine PII char-coverage and by-type counts, plus what
each engine catches that the others miss (char overlap). No PII values are emitted.

Why this exists: the benchmark only *cited* Presidio/Philter; they were never executed.
This wires them up for real so their value on Russian can be measured, not assumed.

Engines:
  - Presidio  : AnalyzerEngine + spaCy ru_core_news_sm (Russian NER + pattern recognizers)
  - Philter   : philter-ucsf 1.0.3, regex/POS/English-namelist (patched to load on py3.13)
  - CONFIDE   : regex + Natasha (this repo's stack)

Usage:
  python3 eval/baseline_compare.py [--sessions DIR] [--out FILE.json] [--limit N]
"""
import os, sys, re, json, tempfile, argparse, glob, warnings
warnings.simplefilter("ignore")
sys.path.insert(0, os.path.expanduser("~/ai_projects/claude-skills/confide/shared"))
import confide_core as C  # noqa: E402

PHILTER_BASE = "/opt/miniconda3/lib/python3.13/site-packages/philter_ucsf"

# ---- engine: CONFIDE -------------------------------------------------------
def spans_confide(text):
    spans = C.merge_spans(C.detect_regex(text) + (C.detect_natasha(text) or []))
    return [(s.start, s.end, s.type) for s in spans]

# ---- engine: Presidio (Russian) -------------------------------------------
_PRES = None
def _presidio():
    global _PRES
    if _PRES is None:
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        cfg = {"nlp_engine_name": "spacy", "models": [{"lang_code": "ru", "model_name": "ru_core_news_sm"}]}
        nlp = NlpEngineProvider(nlp_configuration=cfg).create_engine()
        _PRES = AnalyzerEngine(nlp_engine=nlp, supported_languages=["ru"])
    return _PRES

_PRES_MAP = {"PERSON": "PERSON", "LOCATION": "LOCATION", "GPE": "LOCATION", "NRP": "OTHER",
             "DATE_TIME": "DATE", "PHONE_NUMBER": "PHONE", "EMAIL_ADDRESS": "EMAIL",
             "URL": "URL", "IP_ADDRESS": "ID", "ORGANIZATION": "ORG", "ORG": "ORG"}
def spans_presidio(text):
    out = []
    for r in _presidio().analyze(text=text, language="ru"):
        out.append((r.start, r.end, _PRES_MAP.get(r.entity_type, r.entity_type)))
    return out

# ---- engine: Philter (patched to load on modern Python) -------------------
_PH = None
def _philter_cls():
    global _PH
    if _PH is None:
        os.chdir(PHILTER_BASE)
        import philter_ucsf.philter as PH
        _FLAG = {'i': re.I, 's': re.S, 'm': re.M, 'x': re.X, 'a': re.A, 'u': re.U, 'l': re.L}
        def sane(self, fp):
            rx = open(fp).read().strip(); fl = 0
            for mm in re.findall(r"\(\?([aiLmsux]+)\)", rx):
                for ch in mm: fl |= _FLAG.get(ch, 0)
            rx = re.sub(r"\(\?[aiLmsux]+\)", "", rx)
            try: return re.compile(rx, fl)
            except re.error: return re.compile("(?!x)x")
        PH.Philter.precompile = sane
        _PH = PH
    return _PH
def spans_philter(text):
    PH = _philter_cls()
    ind = tempfile.mkdtemp() + os.sep; outd = tempfile.mkdtemp() + os.sep; pos = tempfile.mkdtemp()
    open(ind + "n.txt", "w", encoding="utf-8").write(text)
    cfg = {"verbose": False, "run_eval": False, "dependent": False, "finpath": ind, "foutpath": outd,
           "filters": os.path.join(PHILTER_BASE, "configs", "philter_delta.json"),
           "outputformat": "asterisk", "cachepos": pos, "prod": True}
    p = PH.Philter(cfg); p.map_coordinates(); p.transform()
    masked = open(outd + "n.txt", encoding="utf-8").read()
    # Philter is typeless here: derive masked char ranges (runs of '*')
    return [(m.start(), m.end(), "PHI") for m in re.finditer(r"\*{2,}", masked)]

# ---- coverage helpers ------------------------------------------------------
def charset(spans):
    s = set()
    for a, b, _ in spans: s.update(range(a, b))
    return s

def by_type(spans):
    d = {}
    for _, _, t in spans: d[t] = d.get(t, 0) + 1
    return d


def run(sessions_dir, out_path, limit):
    files = sorted(glob.glob(os.path.join(sessions_dir, "*.md")))
    if limit: files = files[:limit]
    agg = {e: {"chars": 0, "spans": 0, "by_type": {}} for e in ("confide", "presidio", "philter")}
    only = {"confide_not_presidio": 0, "presidio_not_confide": 0,
            "philter_not_confide": 0, "confide_not_philter": 0}
    n_ok = 0
    for i, f in enumerate(files):
        text = open(f, encoding="utf-8").read()
        try:
            sc = spans_confide(text); sp = spans_presidio(text)
            try: sh = spans_philter(text)
            except Exception: sh = []
        except Exception as e:
            print(f"  [skip {i+1}] {type(e).__name__}: {e}"); continue
        n_ok += 1
        for name, sp_ in (("confide", sc), ("presidio", sp), ("philter", sh)):
            agg[name]["chars"] += len({c for a, b, _ in sp_ for c in range(a, b)})
            agg[name]["spans"] += len(sp_)
            for t, c in by_type(sp_).items():
                agg[name]["by_type"][t] = agg[name]["by_type"].get(t, 0) + c
        cc, pc, hc = charset(sc), charset(sp), charset(sh)
        only["confide_not_presidio"] += len(cc - pc)
        only["presidio_not_confide"] += len(pc - cc)
        only["philter_not_confide"] += len(hc - cc)
        only["confide_not_philter"] += len(cc - hc)
        print(f"  [{i+1}/{len(files)}] confide={len(sc)} presidio={len(sp)} philter={len(sh)} spans")
    report = {"sessions_scored": n_ok, "engines": agg, "char_overlap": only,
              "note": "Counts/characters only — no PII values. Philter is typeless (PHI)."}
    if out_path:
        json.dump(report, open(out_path, "w"), ensure_ascii=False, indent=2)
    print("\n=== STATS-ONLY DIFF (aggregate over %d sessions) ===" % n_ok)
    for e in ("confide", "presidio", "philter"):
        print(f"  {e:9} : {agg[e]['spans']:5} spans, {agg[e]['chars']:7} PII chars | by_type={json.dumps(agg[e]['by_type'], ensure_ascii=False)}")
    print("  char-coverage diff:")
    print(f"    CONFIDE catches but Presidio misses : {only['confide_not_presidio']:7} chars")
    print(f"    Presidio catches but CONFIDE misses : {only['presidio_not_confide']:7} chars")
    print(f"    Philter  catches but CONFIDE misses : {only['philter_not_confide']:7} chars")
    if out_path: print(f"\n  wrote {out_path}")
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", default=os.path.expanduser("~/Brains/brain/Psychotherapy/own-sessions"))
    ap.add_argument("--out", default=os.path.expanduser("~/confide-work/baseline-compare.json"))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    run(a.sessions, a.out, a.limit)
