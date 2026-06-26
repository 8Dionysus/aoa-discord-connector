# aoa-discord-connector

`aoa-discord-connector` is a GitHub-publishable AoA connector skeleton for
permissioned Discord conversation evidence.

It proves a small no-network path:

```bash
python scripts/validate_connector.py
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m aoa_discord_connector.cli doctor
PYTHONPATH=src python -m aoa_discord_connector.cli materialize fixture --mode bot_gateway_message_content
PYTHONPATH=src python -m aoa_discord_connector.cli build-index
PYTHONPATH=src python -m aoa_discord_connector.cli build-graph
PYTHONPATH=src python -m aoa_discord_connector.cli answer "vendor_boot bootloop warning"
```

## Modes

| Mode | Coverage | Boundary |
| --- | --- | --- |
| `bot_gateway` | bot-visible events/metadata | message text can be unavailable without privileged Message Content |
| `bot_gateway_message_content` | bot-visible messages with content | requires configured/approved Message Content intent |
| `rest_history` | channel history | bot permissions and pagination apply |
| `data_package` | account-owned offline export | import-only, no selfbot/user-token route |

The repository stores method, code, schemas, synthetic fixtures, evals, and docs.
It does not store bot tokens, user tokens, Data Packages, private messages,
indexes, graph databases, or media downloads.
