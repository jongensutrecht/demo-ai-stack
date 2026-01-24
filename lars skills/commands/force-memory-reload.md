# Memory Recovery & Injection Command

Forcefully restore Claude's memory when it starts ignoring CLAUDE.md and MCP servers.

**Use this when Claude:**
- Ignores project CLAUDE.md files
- Forgets MCP server connections  
- Loses context from previous messages
- Acts like it's starting fresh despite being mid-conversation

**What this does:**
1. Forces reload of ALL CLAUDE.md files in project hierarchy
2. Re-injects project-specific instructions
3. Refreshes MCP server connections
4. Creates persistent context anchors
5. Provides memory injection payload

**Arguments:** $ARGUMENTS (optional context to preserve)

**Critical:** This command FORCES Claude to acknowledge injected memory content.