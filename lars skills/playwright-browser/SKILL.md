---
description: Full-featured browser automation using Playwright CLI and MCP server. Use for complex automation, test scenarios, and long-running workflows.
---

# playwright-browser Skill

Full-featured browser automation using Microsoft's Playwright CLI and MCP server.

## When to Use
- Complex browser automation scenarios
- Test automation with self-healing capabilities
- Long-running autonomous workflows
- Need for network interception, request mocking
- PDF generation, complex screenshot scenarios
- Exploratory web automation

## When NOT to Use
- Simple, quick browser interactions (use agent-browser instead)
- Token budget is very tight
- Speed is the primary concern

## Installation
Already installed globally:
- `@playwright/cli@0.0.63`
- `@playwright/mcp@0.0.63`

## Core Workflow

### 1. Open page and get snapshot
```bash
npx @playwright/cli open "https://example.com"
npx @playwright/cli snapshot
```

The snapshot returns element refs for interaction.

### 2. Interact using refs
```bash
npx @playwright/cli click <ref>           # Click element
npx @playwright/cli fill <ref> "text"     # Fill input
npx @playwright/cli type "text"           # Type into focused element
npx @playwright/cli press Enter           # Press key
```

### 3. Navigation
```bash
npx @playwright/cli go-back               # Navigate back
npx @playwright/cli go-forward            # Navigate forward
npx @playwright/cli reload                # Reload page
```

### 4. JavaScript evaluation
```bash
npx @playwright/cli eval "document.title"
npx @playwright/cli eval "el => el.textContent" <ref>
```

## Command Reference

| Command | Description |
|---------|-------------|
| `open [url]` | Open URL |
| `close` | Close page |
| `snapshot` | Get page snapshot with refs |
| `click <ref>` | Click element |
| `dblclick <ref>` | Double-click element |
| `fill <ref> "text"` | Fill input |
| `type "text"` | Type into editable element |
| `select <ref> <val>` | Select dropdown option |
| `check <ref>` | Check checkbox |
| `uncheck <ref>` | Uncheck checkbox |
| `hover <ref>` | Hover over element |
| `drag <start> <end>` | Drag and drop |
| `upload <file>` | Upload file |
| `press <key>` | Press keyboard key |
| `go-back` | Navigate back |
| `go-forward` | Navigate forward |
| `reload` | Reload page |
| `resize <w> <h>` | Resize browser window |
| `eval <js>` | Evaluate JavaScript |
| `dialog-accept` | Accept dialog |
| `dialog-dismiss` | Dismiss dialog |

## MCP Server Mode

For integration with Claude or other MCP-compatible tools:

```bash
npx @playwright/mcp
```

Options:
- `--allowed-hosts <hosts>` - Restrict allowed hosts
- `--allowed-origins <origins>` - Restrict allowed origins
- `--blocked-origins <origins>` - Block specific origins

## Best Practices

1. **Use snapshot for refs** - Always get current page state before interacting
2. **Handle dialogs** - Use `dialog-accept` or `dialog-dismiss` for alerts/confirms
3. **Resize for consistency** - Set viewport size for reproducible screenshots
4. **Evaluate for complex logic** - Use `eval` when CLI commands aren't enough

## Example: Form Submission
```bash
npx @playwright/cli open "https://example.com/form"
npx @playwright/cli snapshot
# Identify refs from snapshot
npx @playwright/cli fill ref1 "John Doe"
npx @playwright/cli fill ref2 "john@example.com"
npx @playwright/cli select ref3 "option1"
npx @playwright/cli check ref4
npx @playwright/cli click ref5  # Submit button
npx @playwright/cli snapshot    # Verify result
```

## Example: Screenshot with custom viewport
```bash
npx @playwright/cli open "https://example.com"
npx @playwright/cli resize 1920 1080
npx @playwright/cli eval "await new Promise(r => setTimeout(r, 1000))"  # Wait for animations
# Screenshot via eval or external tool
```

## Comparison with agent-browser
- **Features**: playwright-browser has more features (dialogs, resize, drag-drop)
- **Speed**: agent-browser is faster (native Rust vs Node.js)
- **Tokens**: agent-browser uses fewer tokens
- **Integration**: playwright-browser has MCP server for Claude integration
- **Use case**: playwright-browser for complex automation, agent-browser for quick tasks
