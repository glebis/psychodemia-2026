---
name: session-anonymizer
description: Three-layer PII anonymization for session transcripts (therapy, coaching, consulting, mentoring). Runs Natasha (Russian NER), OpenAI Privacy Filter, and local LLM (Ollama) in sequence for maximum coverage. Fully local by default. This skill should be used when anonymizing session transcripts, notes, or any text containing client PII before AI analysis. Triggers on "anonymize", "redact PII", "anonymize session", "protect client data", "strip personal data", "anonymize transcript".
---

# Therapy Anonymizer

Three-layer PII detection and anonymization for therapy session transcripts. Supports Russian and English. Fully local by default — no data leaves the machine.

## Architecture

Three detection layers run in sequence, each catching what others miss:

| Layer | Tool | Catches | Size | Speed |
|-------|------|---------|------|-------|
| 1 | Natasha | Russian names, locations, organizations | 27 MB | instant |
| 2 | OpenAI Privacy Filter (opf) | Phones, accounts, addresses, emails | 2.8 GB | ~1.5s |
| 3 | Ollama LLM | Medications, dates, contextual IDs | 2.5-7 GB | ~10s |

Spans from all layers are merged, overlaps resolved, and a unified redacted output is produced.

## Prerequisites

One command installs all three layers (idempotent):

```bash
./setup.sh
```

Manual equivalent:

```bash
pip install -r requirements.txt                 # Layer 1: Natasha (Russian NER)
# Layer 2: OpenAI Privacy Filter — NOT on PyPI; install from source (provides the `opf` CLI):
git clone https://github.com/openai/privacy-filter.git && pip install -e ./privacy-filter
ollama pull qwen2.5:3b                           # Layer 3: local LLM (verified default model)
```

Each layer is optional — the script gracefully skips unavailable layers and warns. On 16 GB RAM,
`opf` (2.8 GB) and an Ollama model can't coexist: use `--layers natasha,ollama` or
`--layers natasha,opf`; all three need ~32 GB.

## Usage

### Single file

```bash
python3 scripts/anonymize.py session.txt
```

### Stdin pipe

```bash
cat session.txt | python3 scripts/anonymize.py
```

### Batch processing

```bash
python3 scripts/anonymize.py --batch ~/sessions/ -o ~/sessions_clean/
```

### JSON report

```bash
python3 scripts/anonymize.py session.txt --json
```

### Pseudonyms instead of tags

```bash
python3 scripts/anonymize.py session.txt --pseudonyms
```

### Select layers / model

```bash
# Fast — Natasha only
python3 scripts/anonymize.py session.txt --layers natasha

# LLM only — maximum coverage
python3 scripts/anonymize.py session.txt --layers ollama --model qwen2.5:3b
```

### Encrypt output (AES-256)

```bash
python3 scripts/anonymize.py session.txt -o clean.txt --encrypt "password"
```

## Invoking from an agent (Claude Code / Codex)

Run from the installed skill folder (`~/.claude/skills/session-anonymizer` or
`~/.agents/skills/session-anonymizer`), or use the absolute path to `scripts/anonymize.py`.
To anonymize text already in context, pipe it through the script:

```bash
echo '<text>' | python3 scripts/anonymize.py --json
```

For files, pass the path directly. Always recommend manual review after automated anonymization.

## Limitations

- Contextual identifiers ("the only red-haired architect in Kostroma") are NOT detected by any automated tool
- OPF is English-focused — Russian coverage is partial
- Medications detected only by Layer 3 (requires Ollama)
- Does not assess re-identification risk from combinations of non-PII fields

## Guardrails

- NEVER send raw transcripts to cloud services
- Cloud verification only on already-anonymized text
- Always recommend manual review for therapy data
- Never log original PII values

## Learnings

### 2026-05-05
- **Qwen2.5:3b is the right default model** — no thinking overhead, 2s response, 8/8 with medication prompt. Qwen3 4B returns empty content via Ollama chat API on longer prompts due to thinking mode.
- **Memory contention on 16 GB**: OPF (2.8 GB) + Ollama model cannot coexist. Run `--layers natasha,ollama` for max coverage or `--layers natasha,opf` for deterministic-only. All 3 layers need 32 GB.
- **Medication prompt is critical**: "Include MEDICATIONS with dosages as PII (they narrow identity)" is what takes any LLM from 7/8 to 8/8. No dedicated PII tool catches medications.
- **OPF `redact` subcommand required**: `opf` alone doesn't work, must use `opf redact --device cpu --format json`.
- **Russian morphology breaks text matching**: LLM returns "Москва" but text has "Москве" (prepositional case). Stem matching fallback needed.
- **Ollama API**: use `/api/chat` not `/api/generate`. The generate endpoint returns empty for Qwen2.5 on complex prompts.
