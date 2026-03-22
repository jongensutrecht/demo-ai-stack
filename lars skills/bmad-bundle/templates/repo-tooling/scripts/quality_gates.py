#!/usr/bin/env python3
"""Stable BMAD quality-gates entrypoint."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == '__main__':
    target = Path(__file__).resolve().parents[1] / 'tools' / 'guard' / 'gates.py'
    runpy.run_path(str(target), run_name='__main__')
