# AGENTS.md — Psychodemia 2026 (therapy-session analysis package)

Repo for the masterclass «Паттерны в массиве сессий»: a reproducible, privacy-first workflow
for generating **supervision hypotheses** from therapy-session corpora. This file orients any
coding/clinical agent (Claude Code, Codex, etc.). All session data here is **synthetic**
(fictional clients) — an instrumentation demo, **not** clinical validation.

## Layout
- `skills/` — portable skills (one `SKILL.md` per folder, agentskills.io spec). See `skills/INDEX.md`.
- `prompts/PROMPTS.md` — the canonical prompt pack the skills are derived from.
- `sessions-ru/` — synthetic RU transcripts (client-a = Марина, client-b = Игорь) + `ANSWER-KEY.md`.
- `reference-outputs/` — precomputed analyses (the "answer" to each prompt/skill).
- `eval/` — anonymizer evaluation (real numbers) + method.
- `briefing/` — fact-check corrections, evidence base, deck-revision notes, external reviews.
- `demo/` — `red_raw_local_only/` (never read) vs `green_anon_reviewed/` (agent-readable).

## How the skills work (cross-agent)
Each `skills/<name>/SKILL.md` is a **self-contained instruction set** with YAML frontmatter
(`name`, `description`) and a prose body. No agent-specific tooling is assumed. To use a skill:
read its `SKILL.md` and follow the Steps.

**Install (optional):**
- Claude Code: copy or symlink `skills/<name>` into `~/.claude/skills/`.
- Codex: copy or symlink `skills/<name>` into `~/.agents/skills/`.

## Hard rules (for ANY agent operating on this material)
1. **Only anonymized text leaves the machine.** Raw transcripts → local anonymization
   (`skills/session-anonymizer`) → human review → only then a cloud model. Never read
   `demo/red_raw_local_only/`.
2. **Terminal ≠ local inference.** Claude Code / Codex are cloud by default; inference is local
   only when pointed at a local model (Ollama/LM Studio). State which path is in use.
3. **No diagnosis. No suicide-risk scoring.** Absence of a model flag means nothing. Risk
   decisions are human-only. Every output is a **hypothesis for supervision**, not a fact.
4. **ACT / psychodynamic lenses are exploratory** — low confidence, hypotheses only; the skills
   borrow construct definitions, they do not reproduce psychometrics.
5. Confidence is expressed in words (high/medium/low), never fabricated percentages.

## Recommended pipeline
`session-anonymizer` → `cbt-session-analysis` (+ output audit) → `multi-session-patterns`
→ `cbt-supervision` → optional lenses (`act-lens`, `psychodynamic-lens`). Generate practice data
with `synthetic-session-generator`; route transcripts → reports with `meeting-processor`.

## For an auditing agent (e.g. Codex `codex exec`)
Audit `skills/**/SKILL.md` for: (a) agentskills.io spec compliance (valid `name`, "Use when…"
description with no workflow summary, < 1024-char frontmatter); (b) portability (no Claude-only
tool assumptions; runnable from prose alone); (c) the hard rules above present in each skill;
(d) clinical-claim accuracy against `briefing/02-corrections-factcheck.md` and
`briefing/05-evidence-and-benchmarks.md` (e.g. DoT step 3 = schema analysis; Beck 1976 + Burns
1980; WAI/Bordin not "COMPASS framework"; Miller & Rollnick; ACT/psychodynamic = exploratory).
Report issues per skill; do not edit clinical content without flagging.
