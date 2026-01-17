#!/usr/bin/env python3
"""
Test type decision helper - determines which tests are needed.
Run: python decide.py <file_path>
"""

import sys
import os

def decide_test_type(file_path: str) -> dict:
    """Determine which tests are needed based on file path."""

    result = {
        "file": file_path,
        "required_tests": [],
        "reasoning": []
    }

    path_lower = file_path.lower()

    # UI/Frontend files
    if any(x in path_lower for x in [
        'component', 'page', 'view', '.tsx', '.jsx',
        'frontend', 'ui/', 'src/app/', 'pages/'
    ]):
        result["required_tests"].append("playwright")
        result["reasoning"].append("UI component → needs e2e browser test")

    # API endpoints
    if any(x in path_lower for x in [
        'api/', 'routes/', 'endpoints/', 'controller',
        'router', 'handler'
    ]):
        result["required_tests"].append("integration")
        result["reasoning"].append("API endpoint → needs integration test")

        if 'openapi' in path_lower or 'schema' in path_lower:
            result["required_tests"].append("contract")
            result["reasoning"].append("API schema → needs contract test")

    # Business logic
    if any(x in path_lower for x in [
        'service', 'domain', 'model', 'lib/', 'utils/',
        'helpers/', 'core/'
    ]):
        result["required_tests"].append("unit")
        result["reasoning"].append("Business logic → needs unit test")

    # Database/models
    if any(x in path_lower for x in [
        'models/', 'entities/', 'repository', 'database',
        'migrations/', 'schema'
    ]):
        result["required_tests"].append("integration")
        result["reasoning"].append("Database layer → needs integration test")

    # Auth/Security
    if any(x in path_lower for x in [
        'auth', 'security', 'permission', 'token',
        'session', 'login', 'password'
    ]):
        result["required_tests"].append("unit")
        result["required_tests"].append("integration")
        result["reasoning"].append("Security code → needs unit + integration tests")
        result["invariants"] = ["INV-SEC-*"]

    # Always need at least unit test
    if "unit" not in result["required_tests"]:
        result["required_tests"].append("unit")
        result["reasoning"].append("Default: every change needs unit test")

    # Deduplicate
    result["required_tests"] = list(set(result["required_tests"]))

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python decide.py <file_path>")
        print("Example: python decide.py src/components/Button.tsx")
        sys.exit(1)

    file_path = sys.argv[1]
    result = decide_test_type(file_path)

    print(f"File: {result['file']}")
    print(f"\nRequired tests: {', '.join(result['required_tests'])}")
    print(f"\nReasoning:")
    for reason in result['reasoning']:
        print(f"  - {reason}")

    if "invariants" in result:
        print(f"\nCheck invariants: {', '.join(result['invariants'])}")


if __name__ == "__main__":
    main()
