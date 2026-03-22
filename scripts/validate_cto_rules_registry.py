#!/usr/bin/env python3
"""Validate docs/CTO_RULES.md as a CTO Rule Registry (fail-closed).

Contract:
- docs/CTO_RULES.md MUST contain exactly one fenced YAML block under the heading "## Registry (SSOT)".
- YAML MUST parse and match the minimal schema.

Exit codes:
- 0: OK
- 2: contract/schema violation
- 3: parse error
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Failure:
    code: int
    msg: str


FACET_VOCAB = {
    "Architecture",
    "Code Quality",
    "Complexity & Bugs",
    "Testing",
    "Dependencies",
    "Security",
    "Ops/Reliability",
    "Documentation",
    "Developer Experience",
    "Feature Flags",
    "Domain/Spec Compliance",
}


def _extract_registry_yaml(md: str) -> str:
    # Ensure the marker exists and extract the first yaml fenced block after it.
    marker = "## Registry (SSOT)"
    idx = md.find(marker)
    if idx == -1:
        raise Failure(2, f"Missing required heading: {marker}")

    tail = md[idx:]
    m = re.search(r"```yaml\n(.*?)\n```", tail, flags=re.DOTALL)
    if not m:
        raise Failure(2, "Missing fenced ```yaml block under '## Registry (SSOT)'")

    # Fail closed if there is a second yaml block under the marker.
    rest = tail[m.end() :]
    if re.search(r"```yaml\n", rest):
        raise Failure(2, "Found more than one ```yaml block under '## Registry (SSOT)'")

    return m.group(1).strip() + "\n"


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise Failure(2, msg)


def _as_list(val: Any, *, path: str) -> list[Any]:
    _require(isinstance(val, list), f"{path} must be a list")
    return val


def _as_dict(val: Any, *, path: str) -> dict[str, Any]:
    _require(isinstance(val, dict), f"{path} must be a mapping")
    return val


def validate_registry(doc: dict[str, Any]) -> None:
    _require(doc.get("version") == 1, "version must be 1")

    facet_vocab = doc.get("facet_vocab")
    _require(isinstance(facet_vocab, list), "facet_vocab must be a list")
    unknown_facets = sorted({f for f in facet_vocab if f not in FACET_VOCAB})
    _require(not unknown_facets, f"facet_vocab contains unknown facets: {unknown_facets}")

    rules = _as_list(doc.get("rules"), path="rules")
    _require(len(rules) > 0, "rules must be non-empty")

    ids: set[str] = set()

    for i, rule_any in enumerate(rules):
        rule = _as_dict(rule_any, path=f"rules[{i}]")

        rid = rule.get("id")
        _require(isinstance(rid, str) and rid.strip(), f"rules[{i}].id must be a non-empty string")
        _require(re.fullmatch(r"[A-Z]{2,5}-\d{3}", rid) is not None, f"rules[{i}].id must match PREFIX-### (got {rid!r})")
        _require(rid not in ids, f"Duplicate rule id: {rid}")
        ids.add(rid)

        title = rule.get("title")
        _require(isinstance(title, str) and title.strip(), f"{rid}.title must be a non-empty string")

        facets = _as_list(rule.get("facets"), path=f"{rid}.facets")
        _require(len(facets) > 0, f"{rid}.facets must be non-empty")
        bad_facets = sorted({f for f in facets if f not in FACET_VOCAB})
        _require(not bad_facets, f"{rid}.facets contains unknown facets: {bad_facets}")

        intent = rule.get("intent")
        _require(isinstance(intent, str) and intent.strip(), f"{rid}.intent must be a non-empty string")

        dod = _as_list(rule.get("definition_of_done"), path=f"{rid}.definition_of_done")
        _require(all(isinstance(x, str) and x.strip() for x in dod), f"{rid}.definition_of_done must be list of non-empty strings")
        _require(len(dod) > 0, f"{rid}.definition_of_done must be non-empty")

        verifs = _as_list(rule.get("verification"), path=f"{rid}.verification")
        _require(len(verifs) > 0, f"{rid}.verification must be non-empty")
        for j, v_any in enumerate(verifs):
            v = _as_dict(v_any, path=f"{rid}.verification[{j}]")
            manual = v.get("manual") is True
            has_cmd = isinstance(v.get("command"), str) and v.get("command").strip()
            has_exp = isinstance(v.get("expected"), str) and v.get("expected").strip()
            has_check = isinstance(v.get("check"), str) and v.get("check").strip()

            if manual:
                _require(has_check, f"{rid}.verification[{j}] manual=true requires non-empty 'check'")
            else:
                _require(has_cmd and has_exp, f"{rid}.verification[{j}] requires 'command' + 'expected' (or set manual:true + check)")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    rules_path = repo_root / "docs" / "CTO_RULES.md"

    if not rules_path.exists():
        print(f"ERROR: missing {rules_path}")
        return 2

    md = rules_path.read_text(encoding="utf-8")

    try:
        y = _extract_registry_yaml(md)
    except Failure as e:
        print(f"ERROR: {e.msg}")
        return e.code

    try:
        doc = yaml.safe_load(y)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: YAML parse error: {e}")
        return 3

    try:
        _require(isinstance(doc, dict), "Top-level YAML must be a mapping")
        validate_registry(doc)
    except Failure as e:
        print(f"ERROR: {e.msg}")
        return e.code

    print("OK: CTO Rule Registry is valid")
    print(f"rules_count={len(doc.get('rules', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
