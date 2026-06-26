# Agent Install Route

1. Read `AGENTS.md`, `BOUNDARIES.md`, and `connector/SOURCE_POLICY.md`.
2. Run `python scripts/validate_connector.py`.
3. Run `PYTHONPATH=src python -m pytest -q`.
4. Run the no-network starter proof.
5. Configure external roots before real Discord data.
6. Never place Discord bot tokens, user tokens, Data Packages, private
   messages, or message exports in Git.
