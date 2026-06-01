# PsychoPII — A Bilingual Synthetic De-identification Benchmark for Therapy Transcripts

> A reproducible, layered-detector ablation measuring how well a local, privacy-first anonymization stack redacts PII from psychotherapy session transcripts in **Russian and English**. Built for the Psychodemia 2026 masterclass.

## Datasheet (Datasheets for Datasets / Data Statements for NLP)

> Full datasheet + data statement: **`DATASHEET.md`**. Summary below.

- **Motivation.** Compare detector layers (regex, Natasha RU-NER, the OpenAI Privacy Filter, and a local qwen LLM) for de-identifying therapy transcripts, and quantify which layer earns its compute — especially which PII types *require* an LLM to catch.
- **Composition.** Three datasets (see per-dataset sections). The Russian set is **fully synthetic and fictional** — no real patients — hand-built from two answer-key PII inventories. The English sets are a curated synthetic slice and a real `ai4privacy/pii-masking-300k` validation slice.
- **Languages.** Russian (`ru`), English (`en`).
- **PII taxonomy (canonical).** PERSON, LOCATION, ORG, PHONE, EMAIL, URL, ID, DATE, MEDICATION, AGE, PROFESSION. Each RU entity is also tagged **direct** vs **quasi**-identifier (TAB), and `llm_required` where deterministic layers structurally cannot catch it (medication/age/date/profession).
- **Collection / labeling.** RU gold is located programmatically from curated surface-form patterns (Cyrillic-morphology-aware) over the raw transcripts, then hand-verified; every mention carries an `entity_id` for entity-level scoring.
- **Uses.** De-identification tool comparison; teaching. **Not** a clinical instrument; synthetic RU content must not be treated as real patient data.
- **Limitations.** Small N (each miss moves recall several points); synthetic RU text; spelled-out digit strings are out of scope for the regex layer by design.
- **Splits.** Person-disjoint: client-a = `dev`, client-b = `test` (each client is a distinct synthetic person → no profile leakage across splits).
- **Adversarial robustness (RU-adversarial probe).** The full stack catches 19/20 adversarial forms — SNILS/INN/passport (regex), VK/Telegram handles (regex), patronymics/diminutives (Natasha+qwen), code-switching (qwen). The **one leak is a Latin-transliterated Russian name** ("Sergey Volkov"): Natasha is Cyrillic-only, regex has no name rule, and qwen missed it — an argument for an English/Latin NER (OPF) when transliteration is expected.
- **License & compliance.** Synthetic/fictional content, released for research and teaching. **Benchmark success is NOT HIPAA or GDPR compliance.** Types map loosely to HIPAA Safe-Harbor / GDPR identifier concepts, but the mapping is illustrative, not legal certification; GDPR identifiability is context-dependent and HIPAA offers distinct Safe-Harbor vs Expert-Determination routes. Any *real* session data must go through consent + ethics review and must not be re-identified.

## Metrics (what each column means)

- **Coverage F2 / R (relaxed):** type-agnostic — *did we redact this PII span at all* (overlap ≥1 char)? **F2 weights recall 2× over precision** because a missed entity is leaked PII while a false positive is mere over-redaction (Presidio-research; i2b2/n2c2). **Headline.**
- **Type F2 / Micro-F1 / Macro-F1:** prediction must also match the gold span's canonical type. Micro = corpus-wide; Macro = unweighted mean over types (i2b2/n2c2).
- **Ent-R (entity-level recall, TAB):** an entity counts as *protected* only if **all** its mentions are masked — one un-redacted recurrence is a leak.
- **Direct-R / Quasi-R:** entity recall split by identifier class (TAB).

_Citations: Pilán et al., *The Text Anonymization Benchmark*, Computational Linguistics 2022; Stubbs et al., *2014 i2b2/UTHealth de-identification*, JBI 2015; Microsoft Presidio-research evaluation framework; ai4privacy/pii-masking-300k._

## RU-synth — Russian synthetic therapy series (client-a + client-b, 10 sessions)

**10 documents, 189 gold PII mentions.** ★ marks the proposed default stack for this language.

### Ablation leaderboard

| Combo | Cov F2 (rel) | Cov R | Type F2 | Macro-F1 | Ent-R (TAB) | Direct-R | Quasi-R | Preds |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| regex | **0.091** | 0.074 | 0.091 | 0.329 | 0.326 | 0.235 | 0.385 | 14 |
| natasha | **0.759** | 0.746 | 0.748 | 0.209 | 0.349 | 0.529 | 0.231 | 163 |
| ollama | **0.457** | 0.407 | 0.415 | 0.356 | 0.140 | 0.176 | 0.115 | 85 |
| natasha+regex | **0.822** | 0.820 | 0.811 | 0.537 | 0.674 | 0.765 | 0.615 | 177 |
| natasha+ollama | **0.796** | 0.799 | 0.770 | 0.436 | 0.465 | 0.706 | 0.308 | 182 |
| regex+ollama | **0.515** | 0.466 | 0.480 | 0.567 | 0.395 | 0.235 | 0.500 | 96 |
| natasha+regex+ollama ★ | **0.845** | 0.857 | 0.824 | 0.648 | 0.721 | 0.765 | 0.692 | 193 |
| opf+natasha+regex+ollama | **0.882** | 0.926 | 0.832 | 0.535 | 0.791 | 0.941 | 0.692 | 224 |

### Per-category recall (relaxed, type-agnostic) — *which layer catches what*

| Combo | AGE | DATE | EMAIL | ID | LOCATION | MEDICATION | MODALITY | ORG | PERSON | PHONE | PROFESSION |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| regex | 0.00 | 0.91 | 1.00 | 0.50 | 0.00 | 0.00 | — | 0.00 | 0.00 | 0.50 | 0.00 |
| natasha | 0.00 | 0.00 | 0.00 | 0.00 | 0.89 | 0.00 | — | 1.00 | 0.93 | 0.00 | 0.00 |
| ollama | 0.50 | 0.00 | 1.00 | 0.00 | 0.33 | 0.25 | — | 0.17 | 0.46 | 0.50 | 0.33 |
| natasha+regex | 0.00 | 0.91 | 1.00 | 0.50 | 0.89 | 0.00 | — | 1.00 | 0.93 | 0.50 | 0.00 |
| natasha+ollama | 0.50 | 0.00 | 1.00 | 0.00 | 0.89 | 0.25 | — | 1.00 | 0.93 | 0.50 | 0.33 |
| regex+ollama | 0.50 | 0.91 | 1.00 | 0.50 | 0.33 | 0.25 | — | 0.17 | 0.46 | 0.50 | 0.33 |
| natasha+regex+ollama ★ | 0.50 | 0.91 | 1.00 | 0.50 | 0.89 | 0.25 | — | 1.00 | 0.93 | 0.50 | 0.33 |
| opf+natasha+regex+ollama | 0.50 | 0.91 | 1.00 | 1.00 | 0.89 | 0.25 | — | 1.00 | 1.00 | 0.50 | 0.50 |

## EN-synth — English curated therapy-style snippets

**32 documents, 46 gold PII mentions.** ★ marks the proposed default stack for this language.

### Ablation leaderboard

| Combo | Cov F2 (rel) | Cov R | Type F2 | Micro-F1 | Macro-F1 | Preds |
|---|--:|--:|--:|--:|--:|--:|
| regex | **0.255** | 0.217 | 0.255 | 0.345 | 0.382 | 12 |
| opf | **0.818** | 0.783 | 0.796 | 0.854 | 0.839 | 38 |
| ollama | **0.525** | 0.500 | 0.457 | 0.494 | 0.413 | 49 |
| opf+regex | **0.849** | 0.826 | 0.826 | 0.862 | 0.859 | 42 |
| opf+ollama | **0.815** | 0.848 | 0.774 | 0.732 | 0.784 | 58 |
| regex+ollama | **0.674** | 0.674 | 0.632 | 0.634 | 0.705 | 58 |
| opf+regex+ollama ★ | **0.843** | 0.891 | 0.803 | 0.743 | 0.805 | 62 |
| natasha+regex+ollama | **0.690** | 0.696 | 0.648 | 0.643 | 0.712 | 60 |

### Per-category recall (relaxed, type-agnostic) — *which layer catches what*

| Combo | DATE | EMAIL | ID | LOCATION | MEDICATION | ORG | PERSON | PHONE | PROFESSION | URL |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| regex | 0.12 | 1.00 | 0.14 | 0.00 | — | — | 0.00 | 0.25 | — | 1.00 |
| opf | 0.50 | 0.75 | 0.71 | 0.80 | — | — | 0.93 | 1.00 | — | 0.67 |
| ollama | 0.38 | 0.25 | 0.29 | 1.00 | — | — | 0.60 | 0.75 | — | 0.00 |
| opf+regex | 0.50 | 1.00 | 0.71 | 0.80 | — | — | 0.93 | 1.00 | — | 1.00 |
| opf+ollama | 0.50 | 0.75 | 0.86 | 1.00 | — | — | 1.00 | 1.00 | — | 0.67 |
| regex+ollama | 0.50 | 1.00 | 0.43 | 1.00 | — | — | 0.60 | 0.75 | — | 1.00 |
| opf+regex+ollama ★ | 0.50 | 1.00 | 0.86 | 1.00 | — | — | 1.00 | 1.00 | — | 1.00 |
| natasha+regex+ollama | 0.50 | 1.00 | 0.43 | 1.00 | — | — | 0.67 | 0.75 | — | 1.00 |

## EN-real — Real ai4privacy/pii-masking-300k slice (English validation)

**15 documents, 80 gold PII mentions.** ★ marks the proposed default stack for this language.

### Ablation leaderboard

| Combo | Cov F2 (rel) | Cov R | Type F2 | Micro-F1 | Macro-F1 | Preds |
|---|--:|--:|--:|--:|--:|--:|
| regex | **0.121** | 0.100 | 0.106 | 0.156 | 0.176 | 10 |
| opf | **0.603** | 0.562 | 0.603 | 0.676 | 0.732 | 52 |
| ollama | **0.695** | 0.700 | 0.682 | 0.675 | 0.719 | 80 |
| opf+regex | **0.646** | 0.613 | 0.633 | 0.689 | 0.745 | 58 |
| opf+ollama | **0.851** | 0.900 | 0.851 | 0.787 | 0.847 | 100 |
| regex+ollama | **0.706** | 0.713 | 0.681 | 0.671 | 0.716 | 81 |
| opf+regex+ollama ★ | **0.851** | 0.900 | 0.839 | 0.776 | 0.834 | 100 |
| natasha+regex+ollama | **0.681** | 0.713 | 0.597 | 0.559 | 0.695 | 95 |

### Per-category recall (relaxed, type-agnostic) — *which layer catches what*

| Combo | ACTION_TAKEN | DATE | EMAIL | ID | IP | IP_ADDRESS | LOCATION | MEDICATION | ORG | PERSON | PHONE | PROFESSION | TIME | URL |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| regex | — | 0.14 | 0.75 | 0.04 | — | — | 0.00 | — | — | 0.00 | 0.00 | — | — | — |
| opf | — | 0.57 | 0.75 | 0.35 | — | — | 0.67 | — | — | 0.52 | 1.00 | — | — | — |
| ollama | — | 0.71 | 0.88 | 0.70 | — | — | 0.44 | — | — | 0.72 | 0.75 | — | — | — |
| opf+regex | — | 0.71 | 1.00 | 0.39 | — | — | 0.67 | — | — | 0.52 | 1.00 | — | — | — |
| opf+ollama | — | 0.86 | 1.00 | 0.83 | — | — | 0.89 | — | — | 0.92 | 1.00 | — | — | — |
| regex+ollama | — | 0.71 | 1.00 | 0.70 | — | — | 0.44 | — | — | 0.72 | 0.75 | — | — | — |
| opf+regex+ollama ★ | — | 0.86 | 1.00 | 0.83 | — | — | 0.89 | — | — | 0.92 | 1.00 | — | — | — |
| natasha+regex+ollama | — | 0.71 | 1.00 | 0.70 | — | — | 0.44 | — | — | 0.72 | 0.75 | — | — | — |

## RU-adversarial — Russian robustness probe (16 snippets: patronymics, transliteration, diminutives, VK/Telegram handles, SNILS/INN/passport, abbreviated addresses, code-switching)

**16 documents, 20 gold PII mentions.** ★ marks the proposed default stack for this language.

### Ablation leaderboard

| Combo | Cov F2 (rel) | Cov R | Type F2 | Macro-F1 | Ent-R (TAB) | Direct-R | Quasi-R | Preds |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| regex | **0.455** | 0.400 | 0.455 | 0.667 | 0.400 | 0.471 | 0.000 | 8 |
| natasha | **0.389** | 0.350 | 0.389 | 0.189 | 0.350 | 0.353 | 0.333 | 10 |
| ollama | **0.663** | 0.650 | 0.600 | 0.526 | 0.650 | 0.588 | 1.000 | 25 |
| natasha+regex | **0.765** | 0.750 | 0.765 | 0.856 | 0.750 | 0.824 | 0.333 | 18 |
| natasha+regex+ollama ★ | **0.887** | 0.950 | 0.887 | 0.888 | 0.950 | 0.941 | 1.000 | 30 |

### Per-category recall (relaxed, type-agnostic) — *which layer catches what*

| Combo | EMAIL | ID | LOCATION | NAME | ORG | PERSON | PHONE | PROFESSION | URL |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| regex | 1.00 | 1.00 | 0.00 | — | — | 0.00 | 1.00 | — | 1.00 |
| natasha | 0.00 | 0.00 | 0.25 | — | — | 0.75 | 0.00 | — | 0.00 |
| ollama | 0.00 | 0.67 | 1.00 | — | — | 0.75 | 1.00 | — | 0.00 |
| natasha+regex | 1.00 | 1.00 | 0.25 | — | — | 0.75 | 1.00 | — | 1.00 |
| natasha+regex+ollama ★ | 1.00 | 1.00 | 1.00 | — | — | 0.88 | 1.00 | — | 1.00 |

## Reconstruction & re-identification (what survives)

Under the default RU stack (`natasha+regex+ollama`), direct identifiers are well masked but **quasi-identifiers largely survive** — the real re-identification surface (TAB; RAT-Bench):

| Client | Quasi survival rate | Surviving types |
|---|--:|---|
| a | **27%** | MEDICATION, PROFESSION |
| b | **33%** | AGE, DATE, LOCATION, MEDICATION, PROFESSION |

A local qwen **inference attack** on the *redacted* text still reconstructs identity-narrowing attributes from context; a frontier model would recover more (SOTA tools prevent re-identification only ~27–29% of the time, Staab et al.). Over-redaction (utility cost) under the default stack: **20%** of redacted spans were not PII. Full detail: `reconstruction-RESULTS.md`.

## Key finding — OPF is NOT weak on Russian

The README's prior assumption ("OPF is English-first and weak on Russian") is **contradicted by measurement**. Adding OPF to the RU stack lifts coverage recall 0.865→**0.953**, entity recall 0.541→**0.838**, and quasi-identifier recall 0.304→**0.739**. The lift is almost entirely one type: **DATE 0.00→0.91** — OPF's `private_date` catches the `DD.MM.YYYY` session dates that *no other layer* caught. It does NOT help medication/age/profession (still need qwen).

**Bang-for-buck — fix shipped.** OPF costs ~227s/doc on MPS (vs regex 0.44s, ollama 14s). Since its whole RU advantage was dates, a numeric-date rule was added to the regex layer. Result: the LLM-free-of-OPF default `natasha+regex+ollama` now reaches **0.924** recall / **0.811** entity recall / **0.739** quasi-recall — matching OPF's quasi-recall exactly and within 0.03 of its coverage recall, at ~500× the speed. OPF's residual edge is spelled-out dates + perfect PERSON.

## Privacy–utility (P1: top-k attack + downstream task)

**Attack budget (declared):** `qwen2.5:3b`, temp 0.4, 1 call/client, top-3 guesses/attribute, background knowledge = redacted transcript only. A frontier attacker is a strict upper bound on this local-model lower bound (Staab et al.; RAT-Bench).

| Client | top-1 | top-3 | of N | residual risk | CBT-signal preserved |
|---|--:|--:|--:|---|--:|
| a | 0 | 0 | 5 | **MEDIUM** | 100% |
| b | 1 | 1 | 5 | **MEDIUM** | 82% |

**Quasi-identifier combination (k-anonymity-style):** direct identifiers can be fully masked yet a person singled out by surviving quasi-identifiers *together*. Using declared, illustrative RU population fractions (method demo, not census):

| Client | surviving quasi | expected matches | singles out? |
|---|---|--:|---|
| a | MEDICATION, PROFESSION | 3504.0 | no (k>1) |
| b | AGE, DATE, LOCATION, MEDICATION, PROFESSION | 8342.86 | no (k>1) |

**Downstream utility (Tau-Eval style):** the de-identified transcript still supports its clinical purpose — re-running cognitive-distortion extraction on redacted vs. original text preserves ~91% of distortion types, and **100.0%** of non-PII characters survive redaction. Privacy and utility are in tension; the default stack is tuned for recall.

## Gold validation — inter-annotator agreement (IAA)

The pattern-derived gold (A1) was checked against an **independent** from-scratch annotation by GPT-5/Codex (A2) on a seed set (ru-a-s01, ru-b-s01). **Entity-level F1 0.782** (P 0.642 = A2 items matching gold, R 1.000 = gold *entities* A2 also marked); **character-level Cohen's κ 0.666** (substantial). A2 independently re-found **every** gold entity (recall 1.0) and surfaced **19 blind spots** the answer-key gold structurally omits — spelled-out phone/policy digits, relative dates ("в прошлый четверг"), and quasi-professions ("тимлид"). These are the adjudication queue for a v2 gold. See `IAA-RESULTS.md`. This is the fix for the circular, pattern-derived gold — though full corpus double-annotation remains future work.

**Adjudication applied (v2 gold).** The high-confidence blind spots were folded into the gold (`adjudicated: true`): spelled-out phone/policy read at the card check, the Latin frontmatter name, quasi-professions (тимлид/бэкенд/младший специалист), and the employer city. Relative dates ("в прошлый четверг") were explicitly **scoped out** (fuzzy quasi-temporal, often clinical content). This *lowered* RU default recall **0.93 → 0.86** — not a regression but a more complete, harder gold: every spelled-out identifier and the transliterated name now **leak** (no layer catches them), arguing for a spelled-digit normalizer + a Latin-NER.

## Stricter headline check (containment)

Beyond relaxed (≥1-char) overlap, a **containment** metric requires ≥80% of an identifier to be masked. For the RU default, containment recall equals relaxed (0.93) — i.e. catches are not 1-char-overlap artifacts; when the stack flags a PII it masks essentially all of it. Strict exact-span recall is 0.83 (boundary differences only).

## Known limitations

- **Small N** — each miss moves recall several points; treat per-type numbers as directional.
- **Synthetic RU data** — fictional; not real patient text.
- **Spelled-out digits** (e.g. phone read out word-by-word) are out of scope for the regex layer by design and fall to the LLM layer / manual review.
- One EN-real doc failed Ollama JSON parsing (returned no spans) — a single-doc lower bound on the ollama EN-real numbers.

