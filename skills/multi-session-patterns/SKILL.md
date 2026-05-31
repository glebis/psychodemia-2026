---
name: multi-session-patterns
description: Use when a clinician has several anonymized sessions from one client and wants cross-session patterns — how cognitive distortions trend over time, how themes shift, which topics the client avoids, and whether homework assigned was later checked. Triggers on "compare these sessions", "distortion trend across sessions", "what is the client avoiding", "did the homework get checked", "theme evolution", "multi-session analysis", "across the whole corpus".
---

# Multi-Session Pattern Analysis

## Overview
The highest-value lens: a single client's whole corpus read longitudinally. Core principle: **direction of trend and the dominant/substitute distortion matter more than exact counts** — live counts vary ±1–2, especially on borderline cases. Surfaces what a human cannot hold across many transcripts at once: a distortion fading while another rises, a topic that surfaces and gets blocked every session, homework assigned but never checked.

## When to use
Use with 2+ anonymized sessions from the SAME client. NOT for: a single session (use `cbt-session-analysis`), protocol adherence (use `cbt-supervision`), diagnosis, or risk scoring. Run a safety-boundary scan on each file first.

## Input
All anonymized sessions for one client (e.g. `sessions-ru/client-a/session-01..05.md`).

## Steps
Operate ONLY on already-anonymized text. Inference is cloud unless run on a local model; if cloud, files must already be redacted and human-reviewed. Produce four analyses:

1. **Distortion trend** — per session, count each distortion type (CLEAR instances) in CLIENT speech. Table: types × S1..Sn + Trend (↑/↓/→). Flag borderline cases separately, do not count them silently.
2. **Theme evolution** — name the dominant theme per session and how focus shifts.
3. **Avoidance themes** — topics the client starts then steers away from. Per topic: every instance with quote + session number, the exit pattern, a cautious hypothesis. Do not interpret beyond the text.
4. **Homework assigned-vs-checked** — table [Session | Assigned | Checked? (yes/no/partial) | Where | Done?]. Flag items assigned but never checked later.

Summarize: what decreases (progress), what GROWS (possible substitute distortion), recommendation for the next block. For EACH observation use the mandatory schema:

> Доказательство (цитата) → Интерпретация → Альтернатива → Уверенность (высокая/средняя/низкая) → Действие → Граница.

Analysis output language: **Russian**. Confidence in words, not percentages. Use cautious causal language for consequences ("может ослаблять преемственность; стоит вынести в супервизию"), never causal claims about outcome.

## Example
On `sessions-ru/client-a` (Марина, S1–S5): catastrophizing 7→2 (↓↓), overgeneralization 5→1 (↓), **mind reading 2→5 (↑ — substitute distortion, dominant by S4–S5)**, should-statements → (mixed; some are values-consistent). Themes shift work → relationships → self-worth. Avoidance topic «отец»: 4 escalating episodes S2→S5, unresolved. Homework gaps: behavioral experiment (assigned S2, never properly checked); support circle (assigned S4, not checked in S5).

## Safety & limits
No diagnoses, no suicide-risk scoring, no treatment decisions. Counts are an orientation, not a measurement. Avoidance hypotheses stay close to the text — no reconstruction of "repressed" material. Borrowing construct frameworks, not reproducing psychometrics.
