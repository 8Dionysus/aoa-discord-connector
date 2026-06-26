# MCP Rollout

The connector repo is not the runtime owner.

`abyss-stack` should later expose `aoa-discord-connector-mcp` as a thin,
read-only, stdio-first wrapper over this repo's JSON packets.

Forbidden MCP behavior:

- storing Discord sessions
- writing to Discord
- downloading media by default
- widening scope beyond configured allowlists
