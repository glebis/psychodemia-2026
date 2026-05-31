# OpenAI Privacy Filter — English PII Eval Results

> **STATUS: EXECUTED.** Numbers below are our own measurement, produced by `run_opf.py` + `score.py` on this machine. Vendor-claimed model-card numbers are listed separately at the bottom and are NOT mixed into our results.

**Dataset:** `../sessions-en/pii-eval.jsonl` — 32 snippets, 46 gold entities.
**Model:** `openai/privacy-filter` on **cpu** — load 8.3s, inference 64.0s (2001.0 ms/snippet).

## Headline: F2 = **0.788**  (recall = **0.761**), relaxed/overlap mode

> F2 weights recall 2x over precision. In de-identification a *missed* entity is leaked PII; a *false positive* is only over-redaction. See `README.md` for the Presidio / i2b2-n2c2 rationale.

### Strict (exact-span) mode

| Type | Support | Correct | FP | FN | Precision | Recall | F1 | **F2** |
|------|--------:|--------:|---:|---:|----------:|-------:|---:|-------:|
| private_person | 15 | 14 | 1 | 1 | 0.933 | 0.933 | 0.933 | **0.933** |
| private_address | 5 | 2 | 4 | 3 | 0.333 | 0.400 | 0.364 | **0.385** |
| private_email | 4 | 3 | 0 | 1 | 1.000 | 0.750 | 0.857 | **0.789** |
| private_phone | 4 | 4 | 0 | 0 | 1.000 | 1.000 | 1.000 | **1.000** |
| private_url | 3 | 2 | 0 | 1 | 1.000 | 0.667 | 0.800 | **0.714** |
| private_date | 8 | 4 | 0 | 4 | 1.000 | 0.500 | 0.667 | **0.556** |
| account_number | 3 | 2 | 0 | 1 | 1.000 | 0.667 | 0.800 | **0.714** |
| secret | 4 | 2 | 0 | 2 | 1.000 | 0.500 | 0.667 | **0.556** |
| **OVERALL** | **46** | **33** | **5** | **13** | **0.868** | **0.717** | **0.786** | **0.743** |

### Relaxed (overlap) mode — headline

| Type | Support | Correct | FP | FN | Precision | Recall | F1 | **F2** |
|------|--------:|--------:|---:|---:|----------:|-------:|---:|-------:|
| private_person | 15 | 14 | 1 | 1 | 0.933 | 0.933 | 0.933 | **0.933** |
| private_address | 5 | 4 | 2 | 1 | 0.667 | 0.800 | 0.727 | **0.769** |
| private_email | 4 | 3 | 0 | 1 | 1.000 | 0.750 | 0.857 | **0.789** |
| private_phone | 4 | 4 | 0 | 0 | 1.000 | 1.000 | 1.000 | **1.000** |
| private_url | 3 | 2 | 0 | 1 | 1.000 | 0.667 | 0.800 | **0.714** |
| private_date | 8 | 4 | 0 | 4 | 1.000 | 0.500 | 0.667 | **0.556** |
| account_number | 3 | 2 | 0 | 1 | 1.000 | 0.667 | 0.800 | **0.714** |
| secret | 4 | 2 | 0 | 2 | 1.000 | 0.500 | 0.667 | **0.556** |
| **OVERALL** | **46** | **35** | **3** | **11** | **0.921** | **0.761** | **0.833** | **0.788** |

## Error breakdown (relaxed)
- Correct: **35**  |  Missed (FN, = leaked PII): **11**  |  Spurious/over-redaction (FP): **3**
- Wrong-type matches: 1  |  Partial-overlap (non-exact) matches: 2

## Vendor claim (for reference — NOT our measurement)

The `openai/privacy-filter` model card reports, on the full **PII-Masking-300k** benchmark: **F1 96% / Precision 94% / Recall 98%**. That is the vendor's number on the full, in-distribution benchmark.

Our eval differs deliberately and that explains the gap:
- **Different data:** 32 *therapy-style* curated snippets with hard cases (relative dates like "last Tuesday", short numeric PINs/account tails), not the in-distribution 300k generic text. A real ai4privacy slice is also provided (`pii-eval-ai4privacy.jsonl`) for an in-distribution comparison.
- **Stricter accounting:** entity-level, with wrong-type counted as both FP+FN.
- **Small N:** 46 gold entities — each miss moves recall ~2pp. Treat per-type numbers as directional, not precise.

**Honest read:** the model is strong on names/phones/emails/URLs and over-redacts very little (high precision), but on this hard set it misses relative dates and short numeric secrets — exactly the recall failures that matter for de-id. Run the ai4privacy slice to see in-distribution recall.

