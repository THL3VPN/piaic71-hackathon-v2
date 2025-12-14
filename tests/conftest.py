from __future__ import annotations

import os
import sys
from pathlib import Path


# Ensure project root is importable in tests.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Default DB env so DB tests run locally without extra exports.
os.environ.setdefault("RUN_DB_TESTS", "1")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
