# AOA-DISCORD-D-0001: Permissioned Conversation Proof

Status: accepted

Discord is modeled as a permissioned conversation source. The first public repo
proof uses synthetic data and treats Message Content as a first-class permission
boundary.

Consequences:

- Bot Gateway without Message Content can produce `insufficient_permission`.
- User-token/selfbot collection is forbidden.
- Account-owned Data Package import is offline and local.
- Heavy and sensitive data stays outside Git.
