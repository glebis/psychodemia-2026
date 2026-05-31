# Evidence Base & Benchmarks — citable science for the masterclass

Confirmed via live URLs (2026-05-29). Use these to (a) cite real work on slides and (b) make our
own eval credible. **Verification flags at the end — read before presenting anything as
peer-reviewed.**

## One-line credibility frame
> **Recite-vs-reason gap (CBT-Bench) · recall-is-safety (Presidio/i2b2) · validate-the-judge-first
> (TherapyJudgeBench)** — the three principles that separate a credible eval from a demo.

---

## 1. Cognitive distortion detection

- **CBT-Bench** — arXiv 2410.13218, **NAACL 2025**. Three levels: CBT-knowledge MCQ; distortion
  classification (CBT-CD, 146 ex.) + core-belief classification (CBT-PC, 184 ex.); response
  generation. **Headline:** LLMs recite CBT knowledge but fail at deep cognitive-structure
  analysis → the "not ready to replace clinicians" slide. (Sets are small — citation, not eval set.)
- **Diagnosis of Thought (DoT)** — Chen, Lu & Wang, **Findings of EMNLP 2023** (`2023.findings-emnlp.284`),
  arXiv 2310.07146. 3 stages: subjectivity → contrastive reasoning → **schema analysis**. Eval on
  **TherapistQA** (Shreevastava & Foltz 2021; 2,531 ex., 10 distortion types). Metrics: binary
  Assessment = **F1**, typing = **weighted-F1**, + expert rating (Comprehensive/Partial/Invalid).
  Numbers: ChatGPT 73.5/19.2 → +DoT 81.2/22.3. **The ~22 classification F1 is an honest slide:
  fine-grained typing is genuinely hard.**
- **Distortion-classification datasets** (from the 2025 survey, arXiv 2508.09878): TherapistQA (EN,
  2.5k, 10), **C2D2** (Mandarin, 7.5k, 7; EMNLP-F 2023), SocialCD-3K (Mandarin), Koko (EN, expert,
  15), PatternReframe (EN, 9.7k), Thinking Traps (EN, expert), KoACD (Korean, 108k). **Survey
  warning:** metric inconsistency across papers → fix one metric and report it transparently.

## 2. Alliance / process inference

- **COMPASS** — Lin et al., arXiv 2402.14701, **Translational Psychiatry 2025**. Infers turn-by-turn
  Task/Bond/Goal alliance from transcripts using WAI items as semantic anchors; >950 sessions
  (Alexander Street). **CAVEAT (flag):** **not validated against ground-truth clinician WAI** —
  validates indirectly (condition classification, replicating known over/under-estimation). Cite as
  a *method for mapping alliance language*, **not** a validated alliance measure.
- **AnnoMI** — Wu et al., ICASSP 2022 / *Future Internet* 2023. 133 expert-annotated MI dialogues,
  ~8.8k utterances; MISC-based **Change Talk / Sustain Talk / Neutral** + therapist codes.
  Best real dataset for an MI/process-coding eval slide. github.com/uccollab/AnnoMI.
- Standard instrument behind all this: **Working Alliance Inventory (Horvath & Greenberg)** /
  **Bordin** (bond–tasks–goals). Use these instead of the deck's "COMPASS framework."

## 3. Fidelity / protocol-adherence scoring

- **TherapyGym + TherapyJudgeBench** — arXiv 2603.18008 (Stanford). Automates the **CTRS** (Cognitive
  Therapy Rating Scale) into an LLM pipeline scoring *adherence* + *competence* across multi-turn
  sessions, with a safety scheme. **TherapyJudgeBench:** 116 dialogues, 1,270 expert ratings to
  calibrate LLM-as-judge against clinicians. **Directly copyable methodology for our fidelity eval.**
  (⚠ arXiv "2603" = March 2026 — verify peer-review status.)
- **CTS-R / CTRS** — Revised Cognitive Therapy Scale manual (Univ. Edinburgh, Blackburn et al. 2001);
  factor structure Muse et al. (PMC6997919). Defines adherence vs competence.
- **Hogue et al. 2015** (PMID 24711046) — therapists over-report fidelity vs observers by ~0.4 scale
  points. The honest replacement for the deck's fabricated "Garland 78/42."

## 4. PII / de-identification

- **PII-Masking-300k / Ai4Privacy** (HF) — the set OpenAI Privacy Filter reports 96% F1 on, but
  collapsing 54+ entity types to **8 categories** (IBAN/card/routing → one `account_number`).
  Cautionary slide: **high headline F1 ≠ fine-grained coverage.**
- **Presidio / presidio-research** — per-entity P/R/F; correct/partial/missed; **strict vs relaxed**
  scoring; uses **recall-weighted F2/F2.5** because "in PII detection recall matters more than
  precision — avoid missing any PII." **Our authoritative citation for recall-is-the-safety-metric.**
- **i2b2/n2c2 2014 de-identification** — 1,304 clinical notes, 805k tokens; entity-level micro-P/R/F1;
  top systems ~92% strict-entity F1. Canonical clinical de-id reference; **PHI recall = breach risk**.
- **MultiGraSCCo** — arXiv 2603.08879 — multilingual anonymization benchmark **including Russian**
  (+DE/EN/IT/FR/AR/PL/UK/TR/FA). Nearest thing to a Russian PII benchmark. (⚠ "2603" = March 2026;
  verify.) **Genuine gap:** no mature standalone Russian clinical de-id benchmark → we may build/annotate
  our own small RU eval slice (a real contribution opportunity).

## 5. Surveys / position papers (anchor citations)

1. **"A Survey of LLMs in Psychotherapy"** — arXiv 2502.11095, **Findings of ACL 2025**. The survey to
   anchor the talk (assessment/diagnosis/treatment taxonomy; linguistic-bias warning).
2. **"A Systematic Review of LLMs in Mental Health"** — *Electronics* 2025; 205 studies; "evidence base
   is thin / mostly single-session, non-longitudinal" — supports *our* multi-session angle.
3. **The Lancet Psychiatry 2025** — "LLMs as mental health providers" (prestige clinical position piece).
4. **Suicide-risk safety evals** — arXiv 2510.27521 (clinician-graded), arXiv 2505.13480 (C-SSRS +
   human-in-the-loop tiered triage), ScienceDirect S2772598726000206 (2026 simulation). Back the
   "suicide-risk = never AI-only" boundary with real evidence.
5. **"Evaluating LLMs on mental health: knowledge test → illness diagnosis"** — PMC12365771 (2025);
   mirrors CBT-Bench's recite-vs-reason gap.

## 6. How WE score our demo credibly

- **Distortion detection:** report **binary F1** + **macro-F1 AND weighted-F1** (weighted alone hides
  rare-class failure); report **Cohen's κ** vs clinician labels on a held-out subset; copy DoT's
  Comprehensive/Partial/Invalid rationale rating. Expect ~20–25 weighted-F1 on fine-grained typing —
  say so.
- **PII redaction:** **entity-level recall is the headline** (false negative = leak); report strict +
  relaxed P/R/F per entity type (Presidio framework); use **F2** as headline; build a small **Russian**
  eval slice (MultiGraSCCo RU = nearest reference).
- **Alliance/fidelity:** correlate model scores with human raters (Pearson/Spearman/ICC vs CTRS/WAI);
  **validate the LLM-judge against a small clinician-rated set first** (TherapyJudgeBench move); never
  claim "measurement" for semantic inference — claim "mapping."

## Verification flags
- DoT = EMNLP-2023 **Findings** (not arXiv-only). Hogue = **2015** (epub 2014).
- **TherapyGym (2603.18008) & MultiGraSCCo (2603.08879): arXiv "2603" = March 2026 — recent; verify
  peer-review status before calling them published.**
- COMPASS: published (Transl. Psychiatry 2025) but **not validated vs ground-truth WAI**.
- CrossLinCD / Indonesian distortion set: exist but outside the main survey — verify before slide use.
- Real gaps: no mature standalone Russian clinical de-id benchmark; no validated "WAI-from-NLP vs
  human-WAI" benchmark. Both = contribution opportunities for Gleb.
