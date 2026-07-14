# AGENTS.md

Route card for owner-local statistical questions in
`aoa-discord-connector`. Read the root `AGENTS.md` first.

## Applies To

Everything under `stats/`.

## Role

This directory owns bounded statistics over Discord connector evidence. Shared
measurement grammar and cross-owner composition remain owned by `aoa-stats`;
permission policy and connector behavior remain owned by this repository, eval
verdicts remain owned by `aoa-evals`, and private or live Discord data remains
outside Git in configured storage.

## Read Before Editing

1. Root `AGENTS.md`, `CHARTER.md`, and `BOUNDARIES.md`.
2. `connector/SOURCE_POLICY.md` and `connector/STORAGE_POLICY.md`.
3. The fixture, normalizer, schema, and owner evidence relevant to the measure.
4. `evals/AGENTS.md` when the same evidence is also consumed by an eval.
5. `stats/README.md`, `stats/port.manifest.json`, and the central contracts
   under `aoa-stats/stats/`.

## Boundaries

- The reference population is the non-empty set of unique public starter
  guild messages declared visible in both paired Gateway modes.
- A message enters the numerator only when the normalizer emits the same
  message with authorized, non-empty text under the packet's `source_mode`.
- Explicit Message Content denial across a valid complete population is an
  observed zero, not missing evidence or eval failure.
- A missing normalized message is an observed observability gap. Malformed,
  empty, duplicate, unexpected, contradictory, or unpaired populations are
  unknown.
- The reference packets are weaker than the fixture, normalizer, permission
  policy, executable audits, eval results, and live Discord evidence.
- Text observability does not prove live authorization, guild coverage,
  connector readiness, retrieval or answer quality, eval success, or runtime
  health.

## Validation

Inspect the fixture, normalized outputs for both paired modes, and packets
first. The port validator requires a compatible `aoa-stats` checkout through
`AOA_STATS_ROOT`, `.deps/aoa-stats`, or the workspace sibling route. Then run:

```bash
AOA_STATS_ROOT=/path/to/aoa-stats python scripts/validate_local_stats_port.py
PYTHONPATH=src python -m pytest -q tests/unit/test_local_stats_port.py
```

Use the root route for repository-wide validation.

## Closeout

Report both mode-specific ratios, the manual positive and negative cases,
unknown handling, packet posture, central validation, and repository
validation.
