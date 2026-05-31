#!/usr/bin/env bash
# One-command install for session-anonymizer's three layers. Idempotent.
# Each layer is OPTIONAL — the script skips missing layers at runtime and warns.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Layer 1: Natasha (Russian NER)"
pip install -r requirements.txt

echo "==> Layer 2: OpenAI Privacy Filter (opf CLI) — installed from source (no PyPI package)"
if command -v opf >/dev/null 2>&1; then
  echo "    opf already on PATH — skipping"
else
  PF_DIR="${HOME}/.local/share/privacy-filter"
  if [ ! -d "${PF_DIR}/.git" ]; then
    git clone --depth 1 https://github.com/openai/privacy-filter.git "${PF_DIR}"
  fi
  pip install -e "${PF_DIR}"   # OpenAI Privacy Filter, Apr 2026, Apache-2.0. Provides `opf redact`.
fi

echo "==> Layer 3: Ollama model (medications / dates / contextual IDs)"
if command -v ollama >/dev/null 2>&1; then
  ollama pull qwen2.5:3b       # skill's verified default (no thinking overhead; qwen3:4b returns empty)
else
  echo "    Ollama not found — install from https://ollama.com, then: ollama pull qwen2.5:3b" >&2
fi

echo "==> Done. Verify: python3 scripts/anonymize.py --help"
echo "    Memory note: opf (2.8 GB) + an Ollama model don't coexist on 16 GB — use"
echo "    --layers natasha,ollama  OR  --layers natasha,opf. All three need ~32 GB."
