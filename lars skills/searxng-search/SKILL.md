---
name: searxng-search
description: Local, API-style web search without paid keys using SearXNG in Docker. Use when you need to search the web for docs/facts and want fast structured results.
---

# SearXNG Search (local)

Deze skill geeft je **web search zonder betaalde API key** door lokaal **SearXNG** te draaien.

## Setup (1x)

Start de service:

```bash
docker compose -f ~/.pi/agent/services/searxng/docker-compose.yml up -d
```

Test:

```bash
curl -sS 'http://localhost:8089/search?q=test&format=json' | head
```

## Usage

Aanbevolen: gebruik het Pi command (sneller, geen LLM nodig):

- `/search glob deprecated meaning`
- `/search -n 10 nextjs dynamic server usage cookies`

Service beheren:
- `/search-start`
- `/search-stop`

## Notes

- Resultaten kunnen wisselen per zoek-engine (metasearch). Als een engine blokkeert/captcha doet, probeer een andere query of gebruik browser-tools.
- Voor interactief browsen (klik/scroll/screenshot) gebruik: `browser-tools` skill uit `pi-skills`.
