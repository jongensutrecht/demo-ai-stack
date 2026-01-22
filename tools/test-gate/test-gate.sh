#!/bin/bash
# =============================================================================
# TEST-GATE - Bash Version
# =============================================================================
# Validates that required tests exist for changed files.
#
# Usage:
#   ./test-gate.sh [options]
#
# Options:
#   -r, --repo-root PATH    Repository root (default: current directory)
#   -c, --config PATH       Path to test-requirements.yaml
#   -d, --dry-run           Show what would be checked without failing
#   -j, --json-output PATH  Write JSON report to file
#   -v, --verbose           Show detailed output
#   -h, --help              Show this help
#
# Exit codes:
#   0 - All required tests exist
#   1 - Missing required tests
#   2 - Configuration error
# =============================================================================

set -uo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Defaults
REPO_ROOT="."
CONFIG_PATH=""
DRY_RUN=false
VERBOSE=false
JSON_OUTPUT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--repo-root)
            REPO_ROOT="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_PATH="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -j|--json-output)
            JSON_OUTPUT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            head -30 "$0" | tail -25
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 2
            ;;
    esac
done

# Resolve paths
REPO_ROOT=$(cd "$REPO_ROOT" && pwd)

if [[ -z "$CONFIG_PATH" ]]; then
    CONFIG_PATH="$REPO_ROOT/test-requirements.yaml"
fi

# Check config exists
if [[ ! -f "$CONFIG_PATH" ]]; then
    echo -e "${RED}[ERROR] Config not found: $CONFIG_PATH${NC}"
    if [[ -n "$JSON_OUTPUT" ]]; then
        JSON_OUTPUT="$JSON_OUTPUT" \
        REPO_ROOT="$REPO_ROOT" \
        CONFIG_PATH="$CONFIG_PATH" \
        python - <<'PY'
import json, os
from pathlib import Path

out_path = Path(os.environ["JSON_OUTPUT"])
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "tool": "test-gate",
    "repo_root": os.environ.get("REPO_ROOT", ""),
    "config": os.environ.get("CONFIG_PATH", ""),
    "error": "missing_config",
    "exit_code": 2,
}
out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
PY
    fi
    exit 2
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  TEST-GATE${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "[INFO] Repo root: $REPO_ROOT"
echo -e "[INFO] Config: $CONFIG_PATH"
if $DRY_RUN; then
    echo -e "${YELLOW}[INFO] DRY RUN MODE${NC}"
fi
echo ""

# Get changed files (staged + unstaged)
cd "$REPO_ROOT"
CHANGED_SOURCE=""

get_changed_files() {
    local files=""

    if git rev-parse --verify HEAD >/dev/null 2>&1; then
        files=$(git diff --name-only HEAD 2>/dev/null || true)
        if [[ -n "$files" ]]; then
            CHANGED_SOURCE="git diff HEAD"
            printf '%s\n' "$files"
            return
        fi
    fi

    files=$(git diff --name-only --cached 2>/dev/null || true)
    if [[ -n "$files" ]]; then
        CHANGED_SOURCE="git diff --cached"
        printf '%s\n' "$files"
        return
    fi

    files=$(git ls-files 2>/dev/null || true)
    if [[ -n "$files" ]]; then
        CHANGED_SOURCE="git ls-files"
        printf '%s\n' "$files"
        return
    fi

    files=$(find src -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" \) 2>/dev/null | sed 's|^\./||' || true)
    if [[ -n "$files" ]]; then
        CHANGED_SOURCE="find src"
        printf '%s\n' "$files"
        return
    fi

    CHANGED_SOURCE="none"
}

CHANGED_FILES=$(get_changed_files || true)
echo -e "[INFO] Changed files source: $CHANGED_SOURCE"
CHANGED_FILES_JOINED=$(printf '%s\n' "$CHANGED_FILES")

if [[ -z "$CHANGED_FILES" ]]; then
    echo -e "${GREEN}[OK] No files to check${NC}"
    EXIT_CODE=0
    if [[ -n "$JSON_OUTPUT" ]]; then
        JSON_OUTPUT="$JSON_OUTPUT" \
        REPO_ROOT="$REPO_ROOT" \
        CONFIG_PATH="$CONFIG_PATH" \
        CHANGED_SOURCE="$CHANGED_SOURCE" \
        DRY_RUN="$DRY_RUN" \
        python - <<'PY'
import json, os
from pathlib import Path

out_path = Path(os.environ["JSON_OUTPUT"])
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "tool": "test-gate",
    "repo_root": os.environ.get("REPO_ROOT", ""),
    "config": os.environ.get("CONFIG_PATH", ""),
    "changed_source": os.environ.get("CHANGED_SOURCE", ""),
    "changed_files": [],
    "files_checked": 0,
    "tests_found": 0,
    "missing_tests": [],
    "exit_code": 0,
    "dry_run": os.environ.get("DRY_RUN", "false") == "true",
}
out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
PY
    fi
    exit 0
fi

$VERBOSE && echo -e "[INFO] Changed files:"
$VERBOSE && echo "$CHANGED_FILES" | sed 's/^/  /'
$VERBOSE && echo ""

# Simple YAML parser - extract rules
# Format expected:
# rules:
#   - pattern: "src/app/api/**"
#     required: [unit, integration]

MISSING_TESTS=()
CHECKED_COUNT=0
PASSED_COUNT=0

# Parse rules from YAML (simplified)
parse_rules() {
    local in_rules=false
    local current_pattern=""
    local current_required=""

    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// }" ]] && continue

        if [[ "$line" =~ ^rules: ]]; then
            in_rules=true
            continue
        fi

        if $in_rules; then
            # New rule
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*pattern:[[:space:]]*[\"\']?([^\"\']+)[\"\']? ]]; then
                # Process previous rule if exists
                if [[ -n "$current_pattern" && -n "$current_required" ]]; then
                    check_rule "$current_pattern" "$current_required"
                fi
                current_pattern="${BASH_REMATCH[1]}"
                current_required=""
            fi

            # Required tests
            if [[ "$line" =~ required:[[:space:]]*\[([^\]]+)\] ]]; then
                current_required="${BASH_REMATCH[1]}"
            fi

            # End of rules section (new top-level key)
            if [[ "$line" =~ ^[a-z_]+: && ! "$line" =~ ^[[:space:]] ]]; then
                in_rules=false
                # Process last rule
                if [[ -n "$current_pattern" && -n "$current_required" ]]; then
                    check_rule "$current_pattern" "$current_required"
                fi
            fi
        fi
    done < "$CONFIG_PATH"

    # Process final rule
    if [[ -n "$current_pattern" && -n "$current_required" ]]; then
        check_rule "$current_pattern" "$current_required"
    fi
}

# Check a single rule
check_rule() {
    local pattern="$1"
    local required="$2"

    $VERBOSE && echo -e "[INFO] Checking pattern: $pattern -> required: [$required]"

    # Convert glob pattern to regex
    local regex_pattern=$(echo "$pattern" | sed 's/\*\*/DOUBLESTAR/g' | sed 's/\*/[^\/]*/g' | sed 's/DOUBLESTAR/.*/g')

    # Find matching changed files
    local matched_files=$(echo "$CHANGED_FILES" | grep -E "^$regex_pattern$" 2>/dev/null || echo "")

    if [[ -z "$matched_files" ]]; then
        $VERBOSE && echo "  No files match this pattern"
        return
    fi

    $VERBOSE && echo "  Matched files: $(echo "$matched_files" | wc -l)"

    # Parse required test types
    IFS=',' read -ra TEST_TYPES <<< "$required"

    for file in $matched_files; do
        ((CHECKED_COUNT++))
        local file_ok=true
        local missing_types=()

        for test_type in "${TEST_TYPES[@]}"; do
            test_type=$(echo "$test_type" | tr -d ' "'\''')

            # Check if test exists
            local test_exists=false
            local base_name=$(basename "$file" .py)
            base_name=$(basename "$base_name" .ts)
            base_name=$(basename "$base_name" .tsx)

            case "$test_type" in
                unit)
                    # Look for unit tests
                    if [ -d tests ]; then
                        if find tests -type f \( -name "*${base_name}*" -o -name "test_${base_name}*" \) 2>/dev/null | grep -q .; then
                            test_exists=true
                        fi
                        if ! $test_exists; then
                            if command -v rg >/dev/null 2>&1; then
                                find tests -type f \( -name "*.test.ts" -o -name "*.spec.ts" \) -print0 2>/dev/null \
                                    | xargs -0 rg -l --fixed-strings "$base_name" 2>/dev/null | grep -q . && test_exists=true
                            else
                                find tests -type f \( -name "*.test.ts" -o -name "*.spec.ts" \) -print0 2>/dev/null \
                                    | xargs -0 grep -l "$base_name" 2>/dev/null | grep -q . && test_exists=true
                            fi
                        fi
                    fi
                    ;;
                integration)
                    if [ -d tests/integration ]; then
                        if find tests/integration -type f -name "*${base_name}*" 2>/dev/null | grep -q .; then
                            test_exists=true
                        fi
                    fi
                    ;;
                playwright|e2e)
                    if find tests/e2e e2e -type f -name "*.spec.ts" 2>/dev/null | grep -q .; then
                        test_exists=true
                    fi
                    ;;
                contract)
                    if [ -d tests/contract ]; then
                        if find tests/contract -type f -name "*${base_name}*" 2>/dev/null | grep -q .; then
                            test_exists=true
                        fi
                    fi
                    ;;
            esac

            if ! $test_exists; then
                file_ok=false
                missing_types+=("$test_type")
            fi
        done

        if $file_ok; then
            ((PASSED_COUNT++))
            $VERBOSE && echo -e "  ${GREEN}[OK]${NC} $file"
        else
            MISSING_TESTS+=("$file: missing ${missing_types[*]} tests")
            echo -e "  ${RED}[MISSING]${NC} $file: requires ${missing_types[*]} test(s)"
        fi
    done
}

# Run checks
parse_rules

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  RESULTS${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "Files checked: $CHECKED_COUNT"
echo -e "Tests found: $PASSED_COUNT"
echo -e "Missing tests: ${#MISSING_TESTS[@]}"
echo ""

if [[ ${#MISSING_TESTS[@]} -gt 0 ]]; then
    echo -e "${RED}[FAIL] Missing required tests:${NC}"
    for missing in "${MISSING_TESTS[@]}"; do
        echo -e "  - $missing"
    done
    echo ""

    if $DRY_RUN; then
        echo -e "${YELLOW}[DRY RUN] Would fail with exit code 1${NC}"
        EXIT_CODE=0
    else
        EXIT_CODE=1
    fi
else
    echo -e "${GREEN}[PASS] All required tests exist${NC}"
    EXIT_CODE=0
fi

if [[ -n "$JSON_OUTPUT" ]]; then
    MISSING_TESTS_JOINED=$(printf '%s\n' "${MISSING_TESTS[@]}")
    JSON_OUTPUT="$JSON_OUTPUT" \
    REPO_ROOT="$REPO_ROOT" \
    CONFIG_PATH="$CONFIG_PATH" \
    CHANGED_SOURCE="$CHANGED_SOURCE" \
    CHANGED_FILES_JOINED="$CHANGED_FILES_JOINED" \
    MISSING_TESTS_JOINED="$MISSING_TESTS_JOINED" \
    CHECKED_COUNT="$CHECKED_COUNT" \
    PASSED_COUNT="$PASSED_COUNT" \
    EXIT_CODE="$EXIT_CODE" \
    DRY_RUN="$DRY_RUN" \
    python - <<'PY'
import json, os
from pathlib import Path

out_path = Path(os.environ["JSON_OUTPUT"])
out_path.parent.mkdir(parents=True, exist_ok=True)

changed_files = [
    line for line in os.environ.get("CHANGED_FILES_JOINED", "").splitlines() if line.strip()
]
missing = [
    line for line in os.environ.get("MISSING_TESTS_JOINED", "").splitlines() if line.strip()
]

data = {
    "tool": "test-gate",
    "repo_root": os.environ.get("REPO_ROOT", ""),
    "config": os.environ.get("CONFIG_PATH", ""),
    "changed_source": os.environ.get("CHANGED_SOURCE", ""),
    "changed_files": changed_files,
    "files_checked": int(os.environ.get("CHECKED_COUNT", "0")),
    "tests_found": int(os.environ.get("PASSED_COUNT", "0")),
    "missing_tests": missing,
    "exit_code": int(os.environ.get("EXIT_CODE", "0")),
    "dry_run": os.environ.get("DRY_RUN", "false") == "true",
}

out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
PY
fi

exit "$EXIT_CODE"
