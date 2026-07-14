# Architecture

`aoa-discord-connector` turns authorized Discord conversation snapshots into
local evidence packets.

```text
gateway/rest/data-package snapshot
  -> normalize conversations/messages
  -> build local keyword index
  -> build conversation graph
  -> query evidence packet
  -> answer packet
```

Modes:

- `bot_gateway`
- `bot_gateway_message_content`
- `rest_history`
- `data_package`

Message Content is a permission boundary. A message can exist as metadata while
its text remains unavailable to the connector.

## Statistical port

`stats/` derives a reference-only ratio from the public fixture and normalizer
for each of the paired Gateway modes. The fixture owns the fixed guild-message
population, normalization owns text-availability behavior, and the packets
retain only counts, mode, and portable provenance. The port does not consume
or reproduce the permission eval verdict.
