"""Lock the cycle check green. Does not assert `tach check`."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECK_CYCLES = REPO / "scripts" / "check_cycles.py"


def test_no_package_level_import_cycle():
    result = subprocess.run(
        [sys.executable, str(CHECK_CYCLES)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
