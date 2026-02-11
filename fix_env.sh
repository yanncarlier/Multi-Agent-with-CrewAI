#!/bin/bash

# ==============================================================================
# Script: fix_env.sh
# Description: Resolves the ".venv does not match project environment" error
#              by clearing stale environment paths and re-syncing.
# ==============================================================================

echo "----------------------------------------------------------"
echo "Starting environment reconciliation..."
echo "----------------------------------------------------------"

# 1. Deactivate any currently "zombie" virtual environments in the shell
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Detected active environment variable. Deactivating..."
    # We use a subshell approach or direct unset to ensure the variable is cleared
    unset VIRTUAL_ENV
    unset PYTHONHOME
    echo "Done: Environment variables cleared."
fi

# 2. Remove the existing .venv folder that is being ignored
if [ -d ".venv" ]; then
    echo "Removing the mismatched .venv directory..."
    rm -rf .venv
    echo "Done: .venv removed."
else
    echo "No .venv directory found to remove."
fi

# 3. Re-initialize the environment
# We use the '--active' flag logic if you want to keep the current state,
# but a fresh sync is usually safer for project consistency.
if command -v uv &> /dev/null; then
    echo "Using 'uv' to recreate the environment..."
    uv sync
elif command -v python3 &> /dev/null; then
    echo "Falling back to standard venv..."
    python3 -m venv .venv
    source .venv/bin/activate
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
else
    echo "Error: No environment manager (uv or python3) found."
    exit 1
fi

echo "----------------------------------------------------------"
echo "Success! Your environment has been reset."
echo "To activate it, run: source .venv/bin/activate"
echo "----------------------------------------------------------"