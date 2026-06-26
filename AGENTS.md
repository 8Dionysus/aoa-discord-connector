# AGENTS.md

Root route card for `aoa-discord-connector`.

## Purpose

This repository owns the Discord side of the permissioned conversation connector
family: source policy, starter schemas, synthetic fixtures, normalization, local
search, graph packets, answer packets, and local evals.

## Boundaries

- Do not commit bot tokens, user tokens, Data Packages, private messages, raw
  corpora, indexes, graph databases, vectors, or caches.
- Bot/guild/channel permissions and Message Content intent determine coverage.
- User-token/selfbot collection is forbidden.
- Data Package mode is offline account-owned import only.
- Attachment downloads and write actions are forbidden by default.
- Runtime/MCP belongs in `abyss-stack`; this repo owns connector logic.

## Validation

```bash
python scripts/validate_connector.py
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m aoa_discord_connector.cli doctor
PYTHONPATH=src python -m aoa_discord_connector.cli policy check
PYTHONPATH=src python -m aoa_discord_connector.cli eval permissions
PYTHONPATH=src python -m aoa_discord_connector.cli eval answer-packets
```
