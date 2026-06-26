# Permissioned Conversation Contract

Discord and Telegram connectors share a conversation-first contract.

Core records:

- `conversation`
- `message`
- `author`
- `permission_state`
- `freshness_state`
- `source_ref`
- `evidence_packet`
- `answer_packet`

Required answer statuses:

- `answered`
- `insufficient_permission`
- `insufficient_evidence`

Message Content, edits, deletes, attachments metadata, `warning_report`, and
`freshness_report` must be explicit. Later extraction may add formal
`claim_relation` records over the message graph.
