#!/usr/bin/env python3
"""Residual-gap gallery across a folder of REAL sessions (LOCAL / private).

Runs the CONFIDE detector stack on each session, renders the GREEN (redacted) text
with caught PII placeholders highlighted, and gives a browser tool to MARK survivors
the stack missed (select text -> choose type -> harvest). Export the marked cases to a
JSON the harvester turns into (a) a local private gold and (b) synthetic bench cases.

PRIVACY: the HTML embeds GREEN text, which can still contain survivors (real PII).
It is written LOCALLY, gitignored, banner-marked private, never shipped. This script
(code) is public; its OUTPUT is not. Stats printed to stdout are counts only.

Usage:
  python3 eval/gap_gallery.py [--sessions DIR] [--out DIR] [--layers regex,natasha]
"""
import os, sys, re, json, html, argparse, glob

CONFIDE_SHARED = os.path.expanduser("~/ai_projects/claude-skills/confide/shared")
sys.path.insert(0, CONFIDE_SHARED)
import confide_core as C  # noqa: E402

SENTINEL = re.compile(r"\[CONFIDE_[A-Z]+_\d{4}\]|\[(?:PERSON|EMAIL|PHONE|URL|ID|DATE|AGE|LOCATION|ORG|MEDICATION|PROFESSION|OTHER)\]")
HARVEST_TYPES = ["PERSON", "AGE", "LOCATION", "ORG", "PROFESSION", "MEDICATION", "DATE", "PHONE", "EMAIL", "URL", "ID", "OTHER"]


def detect_all(text, layers):
    spans = []
    if "regex" in layers:
        spans += C.detect_regex(text)
    if "natasha" in layers:
        try:
            spans += C.detect_natasha(text)
        except Exception:
            pass
    return C.merge_spans(spans)


def render_session(doc_id, text, layers):
    spans = detect_all(text, layers)
    green, _map = C.redact_reversible(text, spans)
    # highlight sentinels in the green; everything else is plain (survivors hide there)
    out, last = [], 0
    for m in SENTINEL.finditer(green):
        out.append(html.escape(green[last:m.start()]))
        typ = re.search(r"CONFIDE_([A-Z]+)_|\[([A-Z]+)\]", m.group())
        t = (typ.group(1) or typ.group(2)) if typ else "PII"
        out.append(f'<mark class="t-{t}" title="caught: {t}">{html.escape(m.group())}</mark>')
        last = m.end()
    out.append(html.escape(green[last:]))
    by_type = {}
    for s in spans:
        by_type[s.type] = by_type.get(s.type, 0) + 1
    return "".join(out), len(spans), by_type


def build(sessions_dir, out_dir, layers):
    files = sorted(glob.glob(os.path.join(sessions_dir, "*.md")))
    os.makedirs(out_dir, exist_ok=True)
    cards, total_spans = [], 0
    agg = {}
    for i, f in enumerate(files):
        doc_id = "own-%02d" % (i + 1)            # anonymized id, never the filename/date
        text = open(f, encoding="utf-8").read()
        body, n, by_type = render_session(doc_id, text, layers)
        total_spans += n
        for t, c in by_type.items():
            agg[t] = agg.get(t, 0) + c
        badges = " ".join(f'<span class="badge t-{t}">{t}:{c}</span>' for t, c in sorted(by_type.items()))
        cards.append(
            f'<section class="card" data-doc="{doc_id}">'
            f'<h2>{doc_id} <small>({n} caught)</small></h2><div class="badges">{badges}</div>'
            f'<pre class="green" data-doc="{doc_id}">{body}</pre></section>'
        )
    nav = " ".join(f'<a href="#{("own-%02d"%(i+1))}">{i+1}</a>' for i in range(len(files)))
    aggbadges = " ".join(f'<span class="badge t-{t}">{t}:{c}</span>' for t, c in sorted(agg.items()))
    html_doc = TEMPLATE.replace("__NAV__", nav).replace("__CARDS__", "\n".join(cards)) \
        .replace("__AGG__", aggbadges).replace("__N__", str(len(files))).replace("__TOTAL__", str(total_spans)) \
        .replace("__TYPES__", json.dumps(HARVEST_TYPES))
    out = os.path.join(out_dir, "own-sessions-gap-gallery.html")
    open(out, "w", encoding="utf-8").write(html_doc)
    # anchor ids
    doc = open(out, encoding="utf-8").read()
    for i in range(len(files)):
        d = "own-%02d" % (i + 1)
        doc = doc.replace(f'<section class="card" data-doc="{d}">', f'<section class="card" id="{d}" data-doc="{d}">', 1)
    open(out, "w", encoding="utf-8").write(doc)
    print(f"[gap-gallery] {len(files)} sessions, {total_spans} caught spans | by type: {json.dumps(agg, ensure_ascii=False)}")
    print(f"[gap-gallery] wrote {out}  (LOCAL/private — embeds green text, gitignored, do not share)")
    return out


TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CONFIDE — residual-gap gallery (PRIVATE)</title>
<style>
:root{--bg:#14110d;--fg:#e8dcc6;--mut:#9a8f78;--card:#1d1813;--line:#3a3024}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,Segoe UI,Roboto,sans-serif}
header{position:sticky;top:0;background:#0e0c09ee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:12px 18px;z-index:5}
h1{font-size:16px;margin:0 0 4px}.warn{color:#e0a96d;font-size:12px}
.nav{font-size:12px;margin-top:6px}.nav a{color:var(--mut);text-decoration:none;margin-right:7px}.nav a:hover{color:var(--fg)}
.wrap{display:grid;grid-template-columns:1fr 320px;gap:0}
main{padding:18px;max-width:none}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin:0 0 16px}
h2{font-size:14px;margin:0 0 6px;color:#d9c9a6}h2 small{color:var(--mut);font-weight:400}
.badges{margin-bottom:8px}.badge{display:inline-block;font-size:11px;padding:1px 6px;border-radius:10px;margin:0 4px 4px 0;border:1px solid var(--line);color:var(--fg)}
pre.green{white-space:pre-wrap;word-break:break-word;font:13px/1.6 ui-monospace,Menlo,monospace;margin:0;max-height:340px;overflow:auto;padding:10px;background:#100d0a;border-radius:6px}
mark{padding:0 2px;border-radius:3px;color:#0e0c09;font-weight:600}
.t-PERSON{background:#7fb3d5}.t-LOCATION{background:#82c99a}.t-ORG{background:#d6a96b}.t-AGE{background:#e08a8a}
.t-DATE{background:#c2a0d8}.t-PHONE{background:#e0c36b}.t-EMAIL{background:#9ad0d0}.t-URL{background:#9ad0d0}
.t-ID{background:#c9b08a}.t-MEDICATION{background:#e09ac0}.t-PROFESSION{background:#b0c98a}.t-OTHER{background:#b8b8b8}
aside{border-left:1px solid var(--line);padding:18px;position:sticky;top:64px;height:calc(100vh - 64px);overflow:auto}
aside h3{font-size:13px;margin:0 0 8px}.hint{color:var(--mut);font-size:12px;margin-bottom:10px}
#harvest{list-style:none;padding:0;margin:0}#harvest li{font-size:12px;border:1px solid var(--line);border-radius:6px;padding:6px 8px;margin-bottom:6px}
#harvest .x{float:right;cursor:pointer;color:#e08a8a}.surf{color:#e0a96d;font-weight:600}
button{background:#2a2218;color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:7px 10px;font-size:12px;cursor:pointer}
button:hover{background:#352a1d}.bar{position:fixed;bottom:14px;right:340px;background:#1d1813;border:1px solid var(--line);border-radius:8px;padding:8px;display:none}
.bar select{background:#100d0a;color:var(--fg);border:1px solid var(--line);border-radius:5px;padding:5px}
</style></head><body>
<header><h1>CONFIDE — residual-gap gallery · __N__ sessions · __TOTAL__ caught spans</h1>
<div class="warn">⚠ PRIVATE — embeds GREEN (redacted) text that may still contain survivors. Local only; do not share or commit.</div>
<div class="badges" style="margin-top:6px">__AGG__</div>
<div class="nav">jump: __NAV__</div></header>
<div class="wrap"><main>__CARDS__</main>
<aside><h3>Harvested gaps (<span id="count">0</span>)</h3>
<div class="hint">Highlighted = caught by the stack. To collect a MISSED case: select the survivor text in any session, pick its type, and it's added here. Export feeds the harvester (local gold + synthetic bench cases).</div>
<div><button onclick="exportSel()">⬇ Export selected (JSON)</button> <button onclick="clearSel()">clear</button></div>
<ul id="harvest"></ul></aside></div>
<div class="bar" id="bar"><select id="seltype"></select> <button onclick="addSel()">+ mark as missed PII</button> <button onclick="hideBar()">✕</button></div>
<script>
const TYPES=__TYPES__;const sel=document.getElementById('seltype');TYPES.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o)});
let cases=[],pending=null;
document.addEventListener('mouseup',e=>{const s=window.getSelection();const txt=(s+'').trim();
 if(txt.length<1||txt.length>80){return} let n=s.anchorNode;while(n&&!(n.nodeType===1&&n.dataset&&n.dataset.doc))n=n.parentNode;
 if(!n){return} const pre=n.closest? n: null; const card=(s.anchorNode.parentNode.closest)?s.anchorNode.parentNode.closest('.card'):null;
 const doc=card?card.dataset.doc:(n.dataset?n.dataset.doc:'?');
 // context: surrounding text of the green block
 const block=card?card.querySelector('pre.green').innerText:''; const idx=block.indexOf(txt);
 const ctx=idx>=0?block.slice(Math.max(0,idx-40),idx+txt.length+40):txt;
 pending={doc,surface:txt,context:ctx};
 const bar=document.getElementById('bar');bar.style.display='block';bar.style.top=(e.clientY+8)+'px';bar.style.left=(e.clientX-180)+'px';bar.style.position='fixed';bar.style.bottom='auto';bar.style.right='auto';});
function addSel(){if(!pending)return;pending.type=sel.value;cases.push(pending);render();hideBar();window.getSelection().removeAllRanges()}
function hideBar(){document.getElementById('bar').style.display='none';pending=null}
function render(){const ul=document.getElementById('harvest');ul.innerHTML='';cases.forEach((c,i)=>{const li=document.createElement('li');
 li.innerHTML=`<span class="x" onclick="del(${i})">✕</span><b class="t-${c.type}" style="padding:0 4px;border-radius:3px;color:#0e0c09">${c.type}</b> <span class="surf">${c.surface.replace(/</g,'&lt;')}</span><br><small style="color:#9a8f78">${c.doc} · …${c.context.replace(/</g,'&lt;')}…</small>`;ul.appendChild(li)});document.getElementById('count').textContent=cases.length}
function del(i){cases.splice(i,1);render()}
function clearSel(){cases=[];render()}
function exportSel(){const blob=new Blob([JSON.stringify({schema:'confide-gap-harvest/1',cases},null,2)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='gap-harvest.json';a.click()}
</script></body></html>"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", default=os.path.expanduser("~/Brains/brain/Psychotherapy/own-sessions"))
    ap.add_argument("--out", default=os.path.expanduser("~/confide-work"))
    ap.add_argument("--layers", default="regex,natasha")
    a = ap.parse_args()
    build(a.sessions, a.out, [x.strip() for x in a.layers.split(",") if x.strip()])
