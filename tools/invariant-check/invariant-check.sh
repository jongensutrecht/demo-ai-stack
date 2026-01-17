#!/bin/bash
# =============================================================================
# INVARIANT-CHECK - Bash Version
# =============================================================================
# Validates that all invariants have corresponding NEVER-tests.
#
# Usage:
#   ./invariant-check.sh [options]
#
# Options:
#   -r, --repo-root PATH       Repository root (default: current directory)
#   -i, --invariants PATH      Path to invariants.md
#   -d, --dry-run              Show what would be checked without failing
#   -v, --verbose              Show detailed output
#   -h, --help                 Show this help
#
# Exit codes:
#   0 - All invariants have tests
#   1 - Uncovered invariants found
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
INVARIANTS_PATH=""
DRY_RUN=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--repo-root)
            REPO_ROOT="$2"
            shift 2
            ;;
        -i|--invariants)
            INVARIANTS_PATH="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
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

if [[ -z "$INVARIANTS_PATH" ]]; then
    INVARIANTS_PATH="$REPO_ROOT/invariants.md"
fi

# Check invariants file exists
if [[ ! -f "$INVARIANTS_PATH" ]]; then
    echo -e "${RED}[ERROR] Invariants file not found: $INVARIANTS_PATH${NC}"
    exit 2
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  INVARIANT-CHECK${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "[INFO] Repo root: $REPO_ROOT"
echo -e "[INFO] Invariants: $INVARIANTS_PATH"
if $DRY_RUN; then
    echo -e "${YELLOW}[INFO] DRY RUN MODE${NC}"
fi
echo ""

cd "$REPO_ROOT"

# Arrays to track results
declare -a ALL_INVARIANTS=()
declare -a COVERED_INVARIANTS=()
declare -a UNCOVERED_INVARIANTS=()

# Parse invariants from markdown
# Format: - [ ] **INV-XXX-000**: Description
# Or:     - [x] **INV-XXX-000**: Description (already has test)
parse_invariants() {
    local current_category=""

    while IFS= read -r line; do
        # Detect category headers
        if [[ "$line" =~ ^##[[:space:]]+(Security|Business|Performance|Reliability) ]]; then
            current_category="${BASH_REMATCH[1]}"
            $VERBOSE && echo -e "[INFO] Category: $current_category"
        fi

        # Match invariant lines: - [ ] **INV-SEC-001**: Description
        # or: - [x] **INV-SEC-001**: Description
        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*\[([x[:space:]])\][[:space:]]*\*\*(INV-[A-Z]+-[0-9]+)\*\*:[[:space:]]*(.+)$ ]]; then
            local checked="${BASH_REMATCH[1]}"
            local inv_id="${BASH_REMATCH[2]}"
            local description="${BASH_REMATCH[3]}"

            ALL_INVARIANTS+=("$inv_id|$description|$current_category")

            $VERBOSE && echo "  Found: $inv_id - $description"
        fi
    done < "$INVARIANTS_PATH"
}

# Search for NEVER-tests
find_never_test() {
    local inv_id="$1"
    local description="$2"

    # Search patterns
    local found=false

    # Pattern 1: Test file named after invariant
    # e.g., test_inv_sec_001.py, inv-sec-001.test.ts
    local inv_lower=$(echo "$inv_id" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
    local inv_dash=$(echo "$inv_id" | tr '[:upper:]' '[:lower:]')

    if find tests -name "*${inv_lower}*" -o -name "*${inv_dash}*" 2>/dev/null | grep -q .; then
        found=true
    fi

    # Pattern 2: Test with "NEVER" in name + related keywords
    local keywords=$(echo "$description" | tr ' ' '\n' | grep -E '^[A-Za-z]{4,}$' | head -3 | tr '\n' '|' | sed 's/|$//')

    if [[ -n "$keywords" ]]; then
        if grep -rliE "(NEVER|never).*(${keywords})" tests/ 2>/dev/null | grep -q .; then
            found=true
        fi
    fi

    # Pattern 3: Look for invariant ID in test file comments
    if grep -rli "$inv_id" tests/ 2>/dev/null | grep -q .; then
        found=true
    fi

    # Pattern 4: Check tests/invariants/ directory
    if [[ -d "tests/invariants" ]]; then
        if find tests/invariants -name "*.py" -o -name "*.ts" 2>/dev/null | grep -q .; then
            # Check if any test mentions the invariant
            if grep -rli "$inv_id" tests/invariants/ 2>/dev/null | grep -q .; then
                found=true
            fi
        fi
    fi

    echo $found
}

# Check each invariant
check_invariants() {
    echo -e "[INFO] Checking ${#ALL_INVARIANTS[@]} invariants..."
    echo ""

    for invariant in "${ALL_INVARIANTS[@]}"; do
        IFS='|' read -r inv_id description category <<< "$invariant"

        local has_test=$(find_never_test "$inv_id" "$description")

        if [[ "$has_test" == "true" ]]; then
            COVERED_INVARIANTS+=("$inv_id")
            echo -e "  ${GREEN}[COVERED]${NC} $inv_id: $description"
        else
            UNCOVERED_INVARIANTS+=("$inv_id|$description|$category")
            echo -e "  ${RED}[MISSING]${NC} $inv_id: $description"
        fi
    done
}

# Run checks
parse_invariants

if [[ ${#ALL_INVARIANTS[@]} -eq 0 ]]; then
    echo -e "${YELLOW}[WARN] No invariants found in $INVARIANTS_PATH${NC}"
    echo -e "[INFO] Expected format: - [ ] **INV-SEC-001**: Description"
    exit 0
fi

check_invariants

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  RESULTS${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "Total invariants: ${#ALL_INVARIANTS[@]}"
echo -e "Covered: ${#COVERED_INVARIANTS[@]}"
echo -e "Uncovered: ${#UNCOVERED_INVARIANTS[@]}"
echo ""

# Calculate coverage
if [[ ${#ALL_INVARIANTS[@]} -gt 0 ]]; then
    coverage=$((${#COVERED_INVARIANTS[@]} * 100 / ${#ALL_INVARIANTS[@]}))
    echo -e "Coverage: ${coverage}%"
    echo ""
fi

if [[ ${#UNCOVERED_INVARIANTS[@]} -gt 0 ]]; then
    echo -e "${RED}[FAIL] Uncovered invariants:${NC}"
    echo ""

    # Group by category
    declare -A by_category

    for uncovered in "${UNCOVERED_INVARIANTS[@]}"; do
        IFS='|' read -r inv_id description category <<< "$uncovered"
        by_category["$category"]+="  - $inv_id: $description\n"
    done

    for category in "${!by_category[@]}"; do
        echo -e "${YELLOW}$category:${NC}"
        echo -e "${by_category[$category]}"
    done

    echo -e "${YELLOW}To fix:${NC}"
    echo "  1. Create tests in tests/invariants/<category>/"
    echo "  2. Name test after invariant ID (e.g., test_inv_sec_001.py)"
    echo "  3. Include NEVER in test name for clarity"
    echo ""

    if $DRY_RUN; then
        echo -e "${YELLOW}[DRY RUN] Would fail with exit code 1${NC}"
        exit 0
    else
        exit 1
    fi
else
    echo -e "${GREEN}[PASS] All invariants have NEVER-tests${NC}"
    exit 0
fi
