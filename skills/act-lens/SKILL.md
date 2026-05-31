---
name: act-lens
description: Use when a clinician wants the same anonymized session corpus read through an ACT (Acceptance and Commitment Therapy) lens — psychological flexibility, the six hexaflex processes (fusion/defusion, experiential avoidance/acceptance, self-as-content/context, past-future/present, unclear/clear values, inaction/committed action), and whether the client moves toward or away from values over time. Triggers on "ACT analysis", "psychological flexibility", "hexaflex", "values work", "experiential avoidance", "towards and away moves", "read this through ACT".
---

# ACT Lens (Psychological Flexibility)

## Overview
Reads a client's corpus through the ACT model of psychological (in)flexibility (Hayes / Strosahl / Wilson, six hexaflex processes). Core principle: **lead with towards/away movements** — does the client move toward stated values or away from inner experience, and does that shift across sessions? This is the most interpretive of the CBT-adjacent lenses: markers are observable in text, but the constructs are a reading frame, not a measurement.

## When to use
Use when you want an ACT reading of one client's anonymized sessions. NOT for: distortion counting (use `cbt-session-analysis` / `multi-session-patterns`), protocol adherence, diagnosis, or risk scoring. Run a safety-boundary scan first.

## Input
All anonymized sessions for one client.

## Steps
Operate ONLY on already-anonymized text. Inference is cloud unless run on a local model; if cloud, files must already be redacted and human-reviewed.

1. **Towards / away (lead with this)** — per session, table the away-moves (from inner experience) and towards-moves (toward values), with quotes. State whether a shift toward flexibility appears.
2. **Hexaflex** — for each of the 6 processes, give the inflexibility-pole marker and any opening-of-flexibility marker, with quotes: (1) fusion ↔ defusion, (2) experiential avoidance ↔ acceptance, (3) attachment to conceptualized self ↔ self-as-context, (4) dominance of past/future ↔ present-moment contact, (5) unclear values ↔ clear values, (6) inaction ↔ committed action.
3. **Summary hypothesis** — the central inflexibility and any movement toward flexibility by later sessions.

For EACH observation use the mandatory schema:

> Доказательство (цитата) → Интерпретация → Альтернатива → Уверенность (высокая/средняя/низкая) → Действие → Граница.

Analysis output language: **Russian**. Confidence ≤ medium by default; everything is exploratory hypotheses for supervision. Confidence in words, not percentages.

## Example
On `sessions-ru/client-a` (Марина): central inflexibility = experiential avoidance of rejection/loneliness, held up by fusion with conditional self-worth. Away-moves dominate S1; towards-moves emerge by S3 (named anger aloud instead of withdrawing), S4 (names her own values–action gap), S5 (wrote to an old friend first — a behavioral move toward connection). Defusion sprouts by S4–S5 («внутренний экзаменатор… он отдельно, я отдельно»). Confidence: medium — towards-steps are observable, their "values" nature is interpretation.

## Safety & limits
Exploratory, low-confidence, hypotheses-only — this lens has higher interpretive load than the CBT skills. No diagnoses, no suicide-risk scoring, no treatment decisions. These are hypotheses for supervision, not material to hand the client as "your pattern." Borrowing construct definitions, not reproducing psychometrics (this is NOT an AAQ-II score).
