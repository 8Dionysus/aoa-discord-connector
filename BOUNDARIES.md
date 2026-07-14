# Boundaries

Discord coverage is permission-shaped.

The connector must not model live user-token scraping as an acceptable route.
`insufficient_permission` is the correct result when the bot lacks channel
access or Message Content.

Real Data Package imports stay outside Git and are account-owned local state.

The root `stats/` port may derive privacy-bounded measurements from public
fixtures and connector outputs. It does not own Discord authorization,
permission policy, raw message content, eval verdicts, connector readiness,
or runtime truth; shared measurement grammar remains with `aoa-stats`.
