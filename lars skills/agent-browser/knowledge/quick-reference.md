# agent-browser Quick Reference

## Most Common Commands

```bash
# Navigate
agent-browser open "https://example.com"

# Get accessibility snapshot (ALWAYS do this first)
agent-browser snapshot

# Click, type, fill
agent-browser click @5
agent-browser fill @3 "hello world"
agent-browser press Enter

# Get info
agent-browser get text @7
agent-browser get url
agent-browser get title

# Screenshot
agent-browser screenshot output.png

# Wait
agent-browser wait @5          # Wait for element
agent-browser wait 2000        # Wait 2 seconds

# Close
agent-browser close
```

## Selector Types

1. **@ref** - From snapshot (preferred)
2. **CSS selector** - `agent-browser click "button.submit"`
3. **Text** - `agent-browser click "Submit"`

## Key Names for `press`
- `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`
- `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`
- `Control+a`, `Control+c`, `Control+v`
- `Shift+Tab`, `Alt+F4`

## State Checks
```bash
agent-browser is visible @5
agent-browser is enabled @3
agent-browser is checked @7
```

## Scroll
```bash
agent-browser scroll down 500
agent-browser scroll up
agent-browser scrollintoview @15
```

## Find Elements
```bash
agent-browser find role button click
agent-browser find text "Submit" click
agent-browser find testid "login-btn" click
```
