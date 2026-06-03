#!/usr/bin/env python3
"""Rigorous verdict: score Presidio / Philter / CONFIDE (and CONFIDE+Presidio) on the
LABELED RU gold — precision / recall / F1, relaxed (overlap) matching. Privacy metric is
RECALL (did we catch the PII). Philter is typeless -> scored type-agnostic (span detection).

Usage: python3 eval/score_baselines.py [--gold sessions-ru/pii-eval-ru.jsonl]
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.expanduser("~/ai_projects/claude-skills/confide/shared"))
import confide_core as C  # noqa: E402
from baseline_compare import spans_presidio, spans_philter  # reuse engine wrappers

HERE = os.path.dirname(os.path.abspath(__file__))


def spans_confide(text):
    s = C.merge_spans(C.detect_regex(text) + (C.detect_natasha(text) or []))
    return [(x.start, x.end, x.type) for x in s]

def spans_confide_presidio(text):
    s = C.merge_spans(C.detect_regex(text) + (C.detect_natasha(text) or [])
                      + C.detect_presidio(text, dict(C.DEFAULTS)))
    return [(x.start, x.end, x.type) for x in s]


def overlap(a0, a1, b0, b1):
    return a0 < b1 and b0 < a1


def score(gold_docs, predict, type_aware):
    """Greedy overlap match per doc. Returns dict with precision/recall/F1 + per-type recall."""
    tp = fp = fn = 0
    type_total, type_found = {}, {}
    for d in gold_docs:
        gold = [(s["start"], s["end"], (s.get("type") or s.get("label"))) for s in d["spans"]]
        preds = list(predict(d["text"]))
        gused = [False] * len(gold); pused = [False] * len(preds)
        for gi, (g0, g1, gt) in enumerate(gold):
            type_total[gt] = type_total.get(gt, 0) + 1
            for pi, (p0, p1, pt) in enumerate(preds):
                if pused[pi]:
                    continue
                if overlap(g0, g1, p0, p1) and (not type_aware or _canon(pt) == _canon(gt)):
                    gused[gi] = pused[pi] = True
                    type_found[gt] = type_found.get(gt, 0) + 1
                    break
        tp += sum(gused); fn += sum(1 for u in gused if not u)
        fp += sum(1 for u in pused if not u)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    by_type_recall = {t: round(type_found.get(t, 0) / type_total[t], 2) for t in sorted(type_total)}
    return {"precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3),
            "tp": tp, "fp": fp, "fn": fn, "by_type_recall": by_type_recall}


_CANON = {"GPE": "LOCATION", "ORGANIZATION": "ORG", "DATE_TIME": "DATE",
          "PHONE_NUMBER": "PHONE", "EMAIL_ADDRESS": "EMAIL", "IP_ADDRESS": "ID"}
def _canon(t):
    return _CANON.get(t, t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", default=os.path.join(HERE, "..", "sessions-ru", "pii-eval-ru.jsonl"))
    ap.add_argument("--out", default=os.path.join(HERE, "baseline-gold-scores.json"))
    ap.add_argument("--presidio-model", default=None, help="override spaCy model (e.g. ru_core_news_lg)")
    ap.add_argument("--no-philter", action="store_true", help="skip Philter (known-poor on RU, slow)")
    a = ap.parse_args()
    if a.presidio_model:
        C.DEFAULTS["presidio_model"] = a.presidio_model
        print(f"[presidio model: {a.presidio_model}]")
    gold = [json.loads(l) for l in open(a.gold, encoding="utf-8")]
    n_spans = sum(len(d["spans"]) for d in gold)
    print(f"gold: {len(gold)} docs, {n_spans} labeled spans\n")
    engines = [
        ("CONFIDE (regex+natasha)", spans_confide, True),
        ("Presidio-RU",            spans_presidio, True),
        ("CONFIDE + Presidio",     spans_confide_presidio, True),
    ]
    if not a.no_philter:
        engines.append(("Philter (typeless)", spans_philter, False))  # type-agnostic span detection
    report = {}
    print(f"{'engine':26} {'prec':>6} {'recall':>7} {'F1':>6}   (relaxed/overlap; Philter type-agnostic)")
    print("-" * 72)
    for name, fn_, type_aware in engines:
        r = score(gold, fn_, type_aware)
        report[name] = r
        print(f"{name:26} {r['precision']:6.3f} {r['recall']:7.3f} {r['f1']:6.3f}")
    print("\nPer-type RECALL (privacy-critical — did we catch it):")
    for name in ["CONFIDE (regex+natasha)", "Presidio-RU", "CONFIDE + Presidio"]:
        print(f"  {name:26} {json.dumps(report[name]['by_type_recall'], ensure_ascii=False)}")
    json.dump(report, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
