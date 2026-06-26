# Runtime Contract

Future stack service name:

```text
aoa-discord-connector-mcp
```

The MCP wrapper belongs in `abyss-stack` and must stay read-only and stdio-first.

Required packet fields:

- `agent_answer`
- `evidence_chain`
- `permission_report`
- `conflict_report`
- `freshness_report`
- `applicability_report`
- `warning_report`
- `network_touched=false`
- `read_only=true`
- `internal-search source route` remains local-only; Discord internal search is
  not a crawler source

Return `insufficient_permission` when Message Content, guild, channel, or thread
permissions are missing.
