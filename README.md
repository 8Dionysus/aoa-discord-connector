# aoa-discord-connector

`aoa-discord-connector` is a GitHub-publishable AoA connector skeleton for
permissioned Discord conversation evidence.

It proves a small no-network path from the synthetic fixture through
normalization, local index and graph construction, evidence query, answer
packets, and permission-aware evals. The bounded operator route is owned by
`AGENTS.md`; exact behavior and syntax remain with the CLI parser, validator,
tests, and CI workflow.

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

## Local statistics

The root `stats/` port compares text observability for the same public starter
guild-message population under the paired Gateway modes with and without
Message Content intent. It exports only reference counts and source links;
permission policy, raw content, eval verdicts, and live state stay with their
owners. See `stats/README.md` for the measurement boundary.
