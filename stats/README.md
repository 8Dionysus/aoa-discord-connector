# aoa-discord-connector local stats port

This directory exposes statistical questions whose domain meaning belongs to
the Discord connector. It uses the shared `aoa-stats` grammar without moving
Discord permission policy, private content, eval verdicts, or runtime state
into the central stats organ.

## Current reference measurement

| Measurement | Gateway source mode | Reference value |
| --- | --- | --- |
| `aoa-discord-connector/starter-guild-message-content-observability-ratio` | `bot_gateway` | `0 / 2` |
| `aoa-discord-connector/starter-guild-message-content-observability-ratio` | `bot_gateway_message_content` | `2 / 2` |

The question is: under each paired Gateway permission posture in the canonical
public starter fixture, what fraction of the same declared guild-message
population is normalized with authorized, non-empty text?

The population is a census of unique guild messages with non-empty fixture
text that are declared visible in both paired Gateway modes. The numerator
contains only matching normalized messages whose text is available and whose
permission state is authorized in the selected `source_mode`. The two mode
observations are deliberately not aggregated: their difference is the
permission boundary being measured.

Explicit Message Content denial over the valid complete population is an
observed zero. A missing normalized message is an observed gap against the
fixed fixture population. A malformed, empty, duplicate, unexpected,
contradictory, or mode-unpaired population is unknown rather than zero or
failure.

## Evidence posture

Both packets are public, reference-only snapshots derived from the committed
synthetic fixture and normalizer at source revision
`fcac6256dbded4a8694b22f1c9cb9fb478a58347`. They contain counts and portable
source references, not message text, user content, configured storage, live
Discord state, or eval output. Terminal progress means only that the two-item
fixture census was processed for that mode.

## Authority

The ratio reports fixture text observability across two modeled Gateway
permission postures. It does not establish real bot authorization, live guild
or channel coverage, Message Content configuration, source completeness,
index or graph quality, retrieval or answer quality, connector readiness, eval
success, proof verdicts, or runtime health.

## Surfaces

- `port.manifest.json` declares the owner-local question and measurement.
- `packets/` records the two evidence-linked reference observations.
- the public starter fixture owns the declared message population;
- the normalizer and source policy own text-availability and permission
  semantics;
- `aoa-stats` owns shared validation and cross-owner composition.
