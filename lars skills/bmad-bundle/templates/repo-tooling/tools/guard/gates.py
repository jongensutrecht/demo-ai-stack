#!/usr/bin/env python3
"""Repo-native BMAD quality gates driven by tools/guard/quality_gates.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / 'tools' / 'guard' / 'quality_gates.json'


def _load_config() -> dict:
    if not CONFIG_PATH.is_file():
        raise SystemExit(f'GATES_CONFIG_MISSING: {CONFIG_PATH}')
    return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))


def _resolve_cwd(raw: str | None) -> Path:
    return (PROJECT_ROOT / (raw or '.')).resolve()


def _run(cmd: list[str], cwd: Path) -> None:
    print('[GATES] $', ' '.join(cmd), f'(cwd={cwd})')
    cp = subprocess.run(cmd, cwd=str(cwd))
    if cp.returncode != 0:
        raise SystemExit(cp.returncode)


def _ensure_install(step: dict) -> None:
    cwd = _resolve_cwd(step.get('cwd'))
    marker_dir = cwd / step.get('marker_dir', 'node_modules')
    lockfile = step.get('lockfile')
    if marker_dir.is_dir():
        return
    if lockfile and not (cwd / lockfile).is_file():
        return
    command = step.get('command')
    if not isinstance(command, list) or not command:
        raise SystemExit(f'INVALID_INSTALL_STEP: {step}')
    _run([str(part) for part in command], cwd)


def _run_steps(steps: list[dict]) -> None:
    for step in steps:
        command = step.get('command')
        if not isinstance(command, list) or not command:
            raise SystemExit(f'INVALID_GATE_STEP: {step}')
        _run([str(part) for part in command], _resolve_cwd(step.get('cwd')))


def main() -> int:
    cfg = _load_config()
    installs = cfg.get('installs', [])
    commands = cfg.get('commands', [])
    if not isinstance(installs, list) or not isinstance(commands, list) or not commands:
        raise SystemExit('INVALID_GATES_CONFIG: expected installs[] and non-empty commands[]')
    for step in installs:
        _ensure_install(step)
    _run_steps(commands)
    print('[GATES] All checks passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
