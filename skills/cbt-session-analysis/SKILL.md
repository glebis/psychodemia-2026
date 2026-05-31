---
name: cbt-session-analysis
description: Use when a clinician has one anonymized CBT therapy session transcript and wants the client's statements examined for cognitive distortions with quoted evidence — e.g. catastrophizing, mind reading, overgeneralization, should-statements, labeling. Triggers on "analyze this session for distortions", "what cognitive distortions show up", "DoT analysis", "Diagnosis of Thought", "cognitive distortion analysis of a transcript".
---

# CBT Single-Session Analysis (Diagnosis of Thought)

## Overview
Transparent, evidence-first analysis of one session through the **Diagnosis of Thought (DoT)** framework (Chen, Lu & Wang, Findings of EMNLP 2023). Core principle: every claim is anchored to a direct client quote, distortions are named only after a schema-level reading, and uncertainty is stated in words, not numbers. The tool surfaces *candidate* distortions for clinician review — it does not classify a person.

## When to use
Use when you have a single anonymized session and want distortions named with evidence. NOT for: multi-session trends (use `multi-session-patterns`), protocol adherence (use `cbt-supervision`), diagnosis, or suicide-risk scoring. Run a safety-boundary scan first (see `INDEX.md`).

## Input
One anonymized session transcript (Russian or English).

## Steps
Operate ONLY on already-anonymized text. Inference is cloud unless you run a local model; if cloud, the text must already be redacted and human-reviewed. Analyze CLIENT speech only.

1. **Subjectivity** — split each significant client statement into facts vs. interpretations.
2. **Contrastive reasoning** — list arguments FOR and AGAINST the interpretation, plus an alternative reading.
3. **Schema analysis** (not mere classification) — name the deeper belief behind the pattern, then map to a distortion type per **Beck (1976)** (arbitrary inference, overgeneralization, magnification/minimization, personalization, dichotomous thinking) and **Burns (1980)** (mind reading, fortune telling, should statements, labeling, emotional reasoning, discounting the positive). State which distortion dominates and why.

Output a table (Quote | Facts | Interpretation | Alternative | Type | Confidence) plus a short schema-analysis paragraph. Then, for EACH observation, follow the mandatory schema:

> Доказательство (цитата) → Интерпретация → Альтернатива → Уверенность (высокая/средняя/низкая) → Действие (вынести в супервизию / уточнить у клиента / проверить записи) → Граница.

Analysis output language: **Russian**. Confidence in words, never percentages. Where context is thin, lower confidence and say so. Mark borderline cases (e.g. a "reading" that might be accurate perception) as borderline, not as confirmed distortions.

## Example
On `sessions-ru/client-a/session-01.md` (Марина, S1): «если хоть одну презентацию сдам с ошибкой — это катастрофа, меня сразу спишут со счетов» → факт: ошибки иногда бывают; интерпретация: одна ошибка = конец карьеры; альтернатива: 6 лет роста, «спишут» ни разу не случалось; тип: катастрофизация; уверенность: высокая; действие: вынести в супервизию схему условной самоценности; граница: гипотеза, не диагноз. Dominant distortion S1 = catastrophizing (7 clear episodes); «по лицу поняла» is flagged **borderline** (medium, not high).

## Safety & limits
No diagnoses, no suicide-risk scoring, no treatment decisions. Outputs are hypotheses for joint review with the client, not labels. Russian use of DoT is exploratory (the framework was validated in English). Borrowing a construct framework, not reproducing a psychometric instrument.
