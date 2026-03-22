# playwright-browser Quick Reference

## CLI Commands

```bash
# Navigate
npx @playwright/cli open "https://example.com"

# Get snapshot (do this first)
npx @playwright/cli snapshot

# Interact
npx @playwright/cli click ref1
npx @playwright/cli fill ref2 "text"
npx @playwright/cli type "text"
npx @playwright/cli press Enter
npx @playwright/cli select ref3 "option"

# Checkboxes
npx @playwright/cli check ref4
npx @playwright/cli uncheck ref4

# Navigation
npx @playwright/cli go-back
npx @playwright/cli go-forward
npx @playwright/cli reload

# Dialogs
npx @playwright/cli dialog-accept
npx @playwright/cli dialog-dismiss

# Viewport
npx @playwright/cli resize 1920 1080

# JavaScript
npx @playwright/cli eval "document.title"
npx @playwright/cli eval "el => el.value" ref2

# Close
npx @playwright/cli close
```

## MCP Server

```bash
# Start MCP server (for Claude integration)
npx @playwright/mcp

# With restrictions
npx @playwright/mcp --allowed-hosts "example.com,api.example.com"
npx @playwright/mcp --blocked-origins "ads.example.com"
```

## Key Names for `press`
- `a`-`z`, `0`-`9`
- `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`
- `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`
- `Control+a`, `Control+c`, `Control+v`
- `Shift+Tab`

## Drag and Drop
```bash
npx @playwright/cli drag ref1 ref2
```

## File Upload
```bash
npx @playwright/cli upload "/path/to/file.pdf"
```
