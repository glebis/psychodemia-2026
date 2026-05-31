# Running order — 100 minutes (Sun 31 May, 17:20–19:00 MSK)

**Hero story:** *A clinician has many sessions. First we make the data safe. Then we ask one
useful question. Then we show what becomes visible across sessions.*
**Framing line (not "AI can analyze therapy"):** *"A reproducible, privacy-first workflow for
generating supervision hypotheses from session corpora."*

| Time | Segment | Live | Hard rule |
|---|---|---|---|
| 0:00–2:00 | Opening promise | Запись → транскрипт → анонимизация → агент → отчёт. "Demo pipeline, not clinical validation." | One sentence of bio, max. |
| 2:00–5:00 | Safety frame | AI = hypothesis generator, not diagnostician/supervisor/risk-assessor. | Suicide boundary stated here, repeated later. |
| 5:00–8:00 | Data honesty | Synthetic RU + real EN PII eval. "Synthetic demonstration, not proof." | Never say "proof". |
| 8:00–12:00 | Why it matters | Can't hold 200 sessions in working memory; AI finds review targets. | Drop unsourced "average therapist / supervision %" numbers. |
| 12:00–16:00 | **The privacy rule** | **Локальные инструменты ≠ локальный инференс.** Two paths: (A) Claude Code → Ollama/local = private but weaker; (B) cloud = anonymize+review first. Red/green folders. | This replaces the legal lecture. |
| 16:00–22:00 | PII taxonomy | Standard / contextual / therapeutic PII. "Programmer in Kostroma" quasi-id example. | No jurisdiction table. |
| 22:00–30:00 | **Live demo 1: RU anonymization** | Presidio/spaCy on one RU excerpt; show catches + misses; manually catch quasi-ids. | <8 min. No installation on stage. |
| 30:00–35:00 | Eval credibility | Precomputed EN OpenAI-Privacy-Filter eval: entity P/R/F1, **recall = safety metric**. | Show output; don't run eval live. |
| 35:00–38:00 | Transition | "Now reviewed, safe enough for cloud." Open only `green_anon_reviewed/`. | "Safe enough for this demo," not "anonymized forever." |
| 38:00–42:00 | What is an agent | Reads files, writes reports, runs scripts, asks permission — **with the cloud caveat**. | No skills lecture. |
| 42:00–45:00 | Prompt anatomy | Role + task + evidence + format + limits. One clinician-readable prompt + the 6-field output schema. | No prompt-eng theory beyond this. |
| 45:00–56:00 | **Live demo 2: single-session DoT** | Quote → interpretation → alternative → distortion → confidence (high/med/low) → "insufficient context". | >20s → open reference output. No debugging. |
| 56:00–61:00 | **Ground-truth check** | Compare 3 AI findings to the answer key: one true positive, one miss, one questionable. | This is where you earn scientific trust. |
| 61:00–69:00 | **Multi-session payoff** | Client A trend: catastrophizing↓, mind-reading↑, homework gaps, father avoidance. | Show precomputed report; don't generate live. |
| 69:00–74:00 | Clinician value | Convert to supervision questions: "What should I review?" not "What is true?" | No treatment recommendations. |
| 74:00–79:00 | Homework / fidelity | Assigned-vs-checked table + CBT self-audit checklist. | Alliance out of live demo unless time. |
| 79:00–83:00 | Alliance/process caveat | Transcript markers *may suggest* rupture/repair; alliance not measured from text. Bordin/WAI, not "COMPASS framework". | — |
| 83:00–88:00 | **Ethics red line** | Suicide/crisis/diagnosis/minors/forensic/treatment. "Absence of AI flag means nothing." | Scripted, word-for-word. |
| 88:00–92:00 | Participant artifact | Repo tour: START_HERE, prompts, reference-outputs, eval, checklists. | — |
| 92:00–95:00 | One takeaway slide | "Anonymize locally. Verify manually. Ask narrow questions. Demand quotes. Treat outputs as hypotheses." | No new concepts. |
| 95:00–100:00 | Q&A | 5 min. Cut earlier if you want more. | — |

## Three-layer fallback for every live demo
- **A: live command** (`make demo-1/2/3`).
- **B: precomputed** — if >20s, open `reference-outputs/NN-*.md`.
- **C: static** — if terminal dies, screenshot + "what to notice".

## Hard stage rules
Never install / download weights / log in / run a full eval on stage. Never let the agent see
`red_raw_local_only/`. Terminal font 22–28pt. Clean clone, synthetic data only. `.claudeignore`
in place. Demos titled as clinical questions, never as commands.
