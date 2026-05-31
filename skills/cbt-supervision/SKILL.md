---
name: cbt-supervision
description: Use when a CBT therapist wants a structural self-check of their own session — whether the standard protocol elements were present (agenda, mood check, bridge, homework review, Socratic dialogue, hot-thought work, experiment, new homework, feedback, summary) — with an adherence score and supervision questions. Triggers on "supervision check", "did I follow the CBT protocol", "protocol adherence", "self-supervision", "rate my session structure", "CBT checklist", "supervision memo".
---

# CBT Self-Supervision

## Overview
A structural audit of the therapist's own work against the 10-element CBT session protocol (Beck). Core principle: this is a **reflection tool, not a judgment of the therapist as a person**. Structure is an orientation, not dogma — flexibility for the sake of alliance can be justified and should be named as such. Therapists systematically rate their own adherence higher than independent observers (Hogue et al., 2015), which is exactly why an evidence-quoted external pass is useful.

## When to use
Use on one anonymized session to check protocol adherence. NOT for: client-side analysis (use `cbt-session-analysis`), trends (use `multi-session-patterns`), diagnosis, or treatment recommendations. Run a safety-boundary scan first.

## Input
One anonymized session transcript.

## Steps
Operate ONLY on already-anonymized text. Inference is cloud unless run on a local model; if cloud, the text must already be redacted and human-reviewed.

Check each of the 10 CBT protocol elements — for each give status (present / partial / absent) + a quote + a quality note:
1. Agenda · 2. Mood check · 3. Bridge from last session · 4. Homework review · 5. Socratic dialogue (questions, not a lecture) · 6. Hot-thought work · 7. Experiment / plan · 8. New homework · 9. Client feedback · 10. Session summary.

Score: present = 1.0, partial = 0.5, absent = 0. Sum to **X / 10**. Then write a short qualitative comment (strengths, structural growth areas, and whether low scores reflect a justified relational/exploratory style rather than failure). Then write **5 supervision questions** (open questions to take to supervision — NOT treatment recommendations, NOT "do X"). For each material observation use the mandatory schema:

> Доказательство (цитата) → Интерпретация → Альтернатива → Уверенность (высокая/средняя/низкая) → Действие → Граница.

Analysis output language: **Russian**. Confidence in words, not percentages.

## Example
On `sessions-ru/client-b/session-02.md` (Игорь, S2): present — bridge, homework review (with barrier analysis, not just done/not-done), Socratic dialogue, hot-thought work, experiment, new homework; partial — mood check, summary; absent — agenda (#1), client feedback (#9). Adherence ≈ **7/10**. Supervision question example: «Игорь хронически "додумывает" чужое недовольство — не упустил ли терапевт ранний сигнал разрыва, не запросив обратную связь в S2?»

## Safety & limits
No diagnoses of the client, no suicide-risk scoring, no treatment decisions. This audits the therapist's structure, not their personality. Absence of an element is a structural observation for reflection, not a verdict. Borrowing the protocol as a checklist, not reproducing a validated competence scale (e.g. CTS-R).
