---
description: Fast, native browser automation CLI for AI agents. Use for quick web interactions, screenshots, and token-efficient browser tasks.
---

# agent-browser Skill

Fast, native browser automation for AI agents using Vercel's agent-browser CLI.

## When to Use
- Quick web interactions (open, click, fill, screenshot)
- Token-efficient browser automation (uses accessibility snapshots)
- AI agent workflows needing minimal context overhead
- Speed-critical browser tasks (native Rust binary)

## When NOT to Use
- Complex test scenarios needing full Playwright features
- Network interception, request mocking
- Long-running autonomous workflows (use playwright-browser instead)

## Installation
Already installed globally: `agent-browser@0.15.1`

## Headed Mode (browser zichtbaar)
Environment variable `AGENT_BROWSER_HEADED=true` is ingesteld in fish config.
Browser window is altijd zichtbaar - geen headless mode.

## Core Workflow

### 1. Open page and get snapshot
```bash
agent-browser open "https://example.com"
agent-browser snapshot
```

The snapshot returns an accessibility tree with `@ref` identifiers for each element.

### 2. Interact using refs from snapshot
```bash
agent-browser click @ref           # Click element by ref
agent-browser fill @ref "text"     # Fill input
agent-browser type @ref "text"     # Type into element
agent-browser press Enter          # Press key
```

### 3. Get information
```bash
agent-browser get text @ref        # Get element text
agent-browser get html @ref        # Get element HTML
agent-browser get url              # Get current URL
agent-browser get title            # Get page title
```

### 4. Screenshots
```bash
agent-browser screenshot           # To stdout (base64)
agent-browser screenshot path.png  # To file
```

## Command Reference

| Command | Description |
|---------|-------------|
| `open <url>` | Navigate to URL |
| `snapshot` | Get accessibility tree with refs |
| `click @ref` | Click element |
| `fill @ref "text"` | Clear and fill input |
| `type @ref "text"` | Type into element |
| `press <key>` | Press key (Enter, Tab, etc.) |
| `hover @ref` | Hover over element |
| `scroll up/down` | Scroll page |
| `wait @ref` | Wait for element |
| `wait 1000` | Wait milliseconds |
| `screenshot` | Capture screenshot |
| `get text @ref` | Get element text |
| `get url` | Get current URL |
| `eval "js code"` | Run JavaScript |
| `close` | Close browser |

## Best Practices

1. **Always snapshot first** - Get refs before interacting
2. **Use refs, not selectors** - `@ref` from snapshot is more reliable
3. **Minimal interactions** - Native speed means less waiting needed
4. **Check state when needed** - `agent-browser is visible @ref`

## Example: Login Flow
```bash
agent-browser open "https://app.example.com/login"
agent-browser snapshot
# Find refs for username, password, submit button
agent-browser fill @3 "user@example.com"
agent-browser fill @5 "password123"
agent-browser click @7
agent-browser wait 2000
agent-browser snapshot  # Verify logged in
```

## Comparison with playwright-browser
- **Speed**: agent-browser is faster (native Rust)
- **Tokens**: agent-browser uses fewer tokens (minimal snapshots)
- **Features**: playwright-browser has more features (network, PDF, complex waits)
- **Use case**: agent-browser for quick tasks, playwright-browser for complex automation
