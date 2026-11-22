#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_CMD="python3"
if ! "$PYTHON_CMD" --version >/dev/null 2>&1; then
  PYTHON_CMD="/usr/bin/python3"
fi

echo "Running unit and integration tests in $(basename "$SCRIPT_DIR")..."
"$PYTHON_CMD" -m unittest discover -s tests -p "test_*.py" -v
