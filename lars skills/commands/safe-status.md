# Safe Token Status Check

Check current token usage without risking session crashes.

Please check current session status by:
1. Estimating current token usage based on conversation length
2. Providing a rough percentage of context window used  
3. Recommending action if usage is high (>70%)
4. **DO NOT use /context command - it can crash sessions**

Suggest safe alternatives:
- Start new session if >80% usage
- Save important context to docs/ folder first
- Use /clear only after explicit user confirmation

**Guardian Protection Active** - Dangerous commands are automatically blocked.