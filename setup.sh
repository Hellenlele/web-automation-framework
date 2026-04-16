#!/bin/bash
set -e

echo "==> Setting up web-automation-framework"

# ── .env ──────────────────────────────────────────────────────────────────────
if [ -f .env ]; then
    echo "[SKIP] .env already exists, not overwriting"
else
    cp .env.example .env
    echo "[OK]   .env created from .env.example"
fi

# ── Python virtual environment ────────────────────────────────────────────────
if [ -d .venv ]; then
    echo "[SKIP] .venv already exists"
else
    python3 -m venv .venv
    echo "[OK]   .venv created"
fi

# ── Activate and install dependencies ────────────────────────────────────────
source .venv/bin/activate
echo "[OK]   virtual environment activated"

pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "[OK]   dependencies installed"

# ── Output dirs ───────────────────────────────────────────────────────────────
mkdir -p reports screenshots
echo "[OK]   reports/ and screenshots/ directories ready"

echo ""
echo "Setup complete. To get started:"
echo "  source .venv/bin/activate"
echo "  pytest"
