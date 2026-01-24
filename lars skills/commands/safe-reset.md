# Safe Session Reset

Safely reset session with backup protection.

Before resetting:
1. Ask user to confirm they want to reset
2. Suggest saving current progress to docs/session-summary.md
3. Create a summary of what we accomplished
4. Only then use /clear command
5. Offer to restore context from saved summary

Arguments: $ARGUMENTS (optional reason for reset)

**Guardian Active** - Automatic backup will be created before reset.