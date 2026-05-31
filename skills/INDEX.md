# Skills Index — Therapy Session Analysis Package

Portable skills (agentskills.io `SKILL.md` spec) for privacy-safe analysis of therapy/coaching session transcripts. Each skill is self-contained, plain-prose, and runs on **both** Claude Code and Codex. Analysis output is in **Russian** (audience language).

> **Privacy first (the rule that protects the whole package):** *Local tools ≠ local inference.* What matters is where the **model** computes. By default these agents send reasoning to the **cloud**, so every analysis skill operates ONLY on **already-anonymized, human-reviewed** text. Pipeline: raw transcript → local anonymization → manual quasi-identifier check → green folder → analysis. Run a safety-boundary scan (markers needing a human protocol) **before** any analysis — it flags, it does not score risk.

## Skills

| Skill | Use when… |
|---|---|
| `session-anonymizer` | …you need to strip PII from a transcript locally before any cloud analysis (3-layer: Natasha + OpenAI Privacy Filter + local LLM). |
| `synthetic-session-generator` | …you need realistic fictional session transcripts for evals, demos, or training data. |
| `cbt-session-analysis` | …you have ONE anonymized session and want client cognitive distortions named with quoted evidence (Diagnosis of Thought). |
| `multi-session-patterns` | …you have a client's whole corpus and want distortion trends, theme evolution, avoidance themes, and homework assigned-vs-checked. |
| `cbt-supervision` | …a therapist wants a structural self-check of their own session (10-element CBT protocol, X/10) + 5 supervision questions. |
| `act-lens` | …you want the same corpus read through ACT psychological flexibility (hexaflex, towards/away moves). |
| `psychodynamic-lens` | …you want a cautious psychodynamic reading (CCRT wish/response-of-other/response-of-self, coarse defenses, transference hints). |
| `cognitive-toolkit` | …a client/user wants to *do* a guided CBT/DBT exercise (thought record, opposite action) — intervention, not analysis. |
| `mental-toolkit` | …a user wants structured self-management (timed worry processing, scenario planning, anxiety check-in). |
| `meeting-processor` | …you want to auto-detect a transcript's type and apply type-specific extraction (incl. coaching/therapy). |

## Recommended pipeline order

1. **Anonymize** — `session-anonymizer` (local). Then manually check quasi-identifiers.
2. **Safety scan** — flag any material needing a human clinical protocol (self-harm, harm to others, safeguarding, forensic). This flags only; it does not score risk and "no flag" never means "safe."
3. **Analyze single session** — `cbt-session-analysis`.
4. **Multi-session** — `multi-session-patterns` (distortion trend → themes → avoidance → homework).
5. **Supervision** — `cbt-supervision` (protocol adherence on the therapist's own work).
6. **Other lenses** — `act-lens`, then `psychodynamic-lens` (most interpretive last; lowest confidence).

`synthetic-session-generator` feeds the pipeline test data; `cognitive-toolkit` / `mental-toolkit` are client-facing interventions, not part of the analysis chain.

## Shared discipline (all analysis skills)

- Operate ONLY on already-anonymized text. Inference is cloud unless run on a local model.
- Mandatory per-observation schema: **Доказательство → Интерпретация → Альтернатива → Уверенность (высокая/средняя/низкая) → Действие → Граница.**
- Confidence in words, never percentages. Lower it where context is thin.
- No diagnoses, no suicide-risk scoring, no treatment decisions. AI is a microscope, not a clinician.
- `act-lens` / `psychodynamic-lens` are exploratory, low-confidence, hypotheses-only — borrowing construct definitions, not reproducing psychometrics.

## Install (both agents)

Each skill is a folder containing a single `SKILL.md`. Copy or symlink the folders.

**Claude Code** — into `~/.claude/skills`:
```sh
cp -R cbt-session-analysis multi-session-patterns cbt-supervision act-lens psychodynamic-lens ~/.claude/skills/
# or symlink (stays in sync with the repo):
ln -s "$PWD"/cbt-session-analysis ~/.claude/skills/cbt-session-analysis
```

**Codex** — into `~/.agents/skills`:
```sh
mkdir -p ~/.agents/skills
cp -R cbt-session-analysis multi-session-patterns cbt-supervision act-lens psychodynamic-lens ~/.agents/skills/
# or symlink:
ln -s "$PWD"/cbt-session-analysis ~/.agents/skills/cbt-session-analysis
```

The already-bundled skills (`session-anonymizer`, `synthetic-session-generator`, `cognitive-toolkit`, `mental-toolkit`, `meeting-processor`) install the same way. No agent-specific tooling is assumed by any of the five analysis skills — they are plain-prose instructions.
