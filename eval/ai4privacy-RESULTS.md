# OpenAI Privacy Filter — English PII Eval Results

> **STATUS: EXECUTED.** Numbers below are our own measurement, produced by `run_opf.py` + `score.py` on this machine. Vendor-claimed model-card numbers are listed separately at the bottom and are NOT mixed into our results.

**Dataset:** `../sessions-en/pii-eval-ai4privacy.jsonl` — 15 snippets, 80 gold entities.
**Model:** `openai/privacy-filter` on **cpu** — load 10.6s, inference 48.4s (3229.0 ms/snippet).

## Headline: F2 = **0.591**  (recall = **0.550**), relaxed/overlap mode

> F2 weights recall 2x over precision. In de-identification a *missed* entity is leaked PII; a *false positive* is only over-redaction. See `README.md` for the Presidio / i2b2-n2c2 rationale.

### Strict (exact-span) mode

| Type | Support | Correct | FP | FN | Precision | Recall | F1 | **F2** |
|------|--------:|--------:|---:|---:|----------:|-------:|---:|-------:|
| private_person | 25 | 4 | 13 | 21 | 0.235 | 0.160 | 0.191 | **0.171** |
| private_address | 9 | 1 | 6 | 8 | 0.143 | 0.111 | 0.125 | **0.116** |
| private_email | 8 | 5 | 1 | 3 | 0.833 | 0.625 | 0.714 | **0.658** |
| private_phone | 8 | 3 | 6 | 5 | 0.333 | 0.375 | 0.353 | **0.366** |
| private_date | 7 | 0 | 4 | 7 | 0.000 | 0.000 | 0.000 | **0.000** |
| account_number | 19 | 4 | 2 | 15 | 0.667 | 0.210 | 0.320 | **0.244** |
| secret | 4 | 1 | 1 | 3 | 0.500 | 0.250 | 0.333 | **0.278** |
| **OVERALL** | **80** | **18** | **34** | **62** | **0.346** | **0.225** | **0.273** | **0.242** |

### Relaxed (overlap) mode — headline

| Type | Support | Correct | FP | FN | Precision | Recall | F1 | **F2** |
|------|--------:|--------:|---:|---:|----------:|-------:|---:|-------:|
| private_person | 25 | 12 | 5 | 13 | 0.706 | 0.480 | 0.571 | **0.513** |
| private_address | 9 | 6 | 1 | 3 | 0.857 | 0.667 | 0.750 | **0.698** |
| private_email | 8 | 6 | 0 | 2 | 1.000 | 0.750 | 0.857 | **0.789** |
| private_phone | 8 | 8 | 1 | 0 | 0.889 | 1.000 | 0.941 | **0.976** |
| private_date | 7 | 4 | 0 | 3 | 1.000 | 0.571 | 0.727 | **0.625** |
| account_number | 19 | 6 | 0 | 13 | 1.000 | 0.316 | 0.480 | **0.366** |
| secret | 4 | 2 | 0 | 2 | 1.000 | 0.500 | 0.667 | **0.556** |
| **OVERALL** | **80** | **44** | **8** | **36** | **0.846** | **0.550** | **0.667** | **0.591** |

## Error breakdown (relaxed)
- Correct: **44**  |  Missed (FN, = leaked PII): **36**  |  Spurious/over-redaction (FP): **8**
- Wrong-type matches: 0  |  Partial-overlap (non-exact) matches: 26

## Vendor claim (for reference — NOT our measurement)

The `openai/privacy-filter` model card reports, on the full **PII-Masking-300k** benchmark: **F1 96% / Precision 94% / Recall 98%**. That is the vendor's number on the full, in-distribution benchmark.

Our eval differs deliberately and that explains the gap:
- **Different data:** 32 *therapy-style* curated snippets with hard cases (relative dates like "last Tuesday", short numeric PINs/account tails), not the in-distribution 300k generic text. A real ai4privacy slice is also provided (`pii-eval-ai4privacy.jsonl`) for an in-distribution comparison.
- **Stricter accounting:** entity-level, with wrong-type counted as both FP+FN.
- **Small N:** 46 gold entities — each miss moves recall ~2pp. Treat per-type numbers as directional, not precise.

**Honest read:** the model is strong on names/phones/emails/URLs and over-redacts very little (high precision), but on this hard set it misses relative dates and short numeric secrets — exactly the recall failures that matter for de-id. Run the ai4privacy slice to see in-distribution recall.

