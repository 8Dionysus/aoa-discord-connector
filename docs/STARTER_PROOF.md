# Starter Proof

The starter proof is no-network and synthetic.

It demonstrates:

- `bot_gateway` preserves metadata but reports Message Content permission gaps.
- `bot_gateway_message_content` can answer message-content questions.
- `data_package` is modeled as offline account-owned import.
- `user_token_selfbot` is denied by policy.

The root `stats/` port records the narrower reference observation that the
same two declared guild messages expose authorized non-empty text in `0 / 2`
cases under `bot_gateway` and `2 / 2` under
`bot_gateway_message_content`. This describes fixture observability; it is not
the permission eval verdict and does not claim live Discord coverage.
