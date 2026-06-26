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
