from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from aoa_discord_connector.normalize import normalize_snapshot


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = REPO_ROOT / "connector" / "fixtures" / "discord" / "starter_conversation.json"
PORT_PATH = REPO_ROOT / "stats" / "port.manifest.json"
PACKET_PATHS = {
    "bot_gateway": REPO_ROOT
    / "stats"
    / "packets"
    / "starter-guild-message-content-observability-ratio.bot-gateway.reference.json",
    "bot_gateway_message_content": REPO_ROOT
    / "stats"
    / "packets"
    / "starter-guild-message-content-observability-ratio.message-content.reference.json",
}
PAIRED_MODES = ("bot_gateway", "bot_gateway_message_content")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_fixture(tmp_path: Path, mode: str) -> dict[str, object]:
    path = normalize_snapshot(FIXTURE_PATH, "discord:fixture", tmp_path / mode, mode=mode)
    return load_json(path)


def derive_content_observability_ratio(
    fixture: object,
    normalized: object,
    mode: str,
) -> dict[str, object]:
    if mode not in PAIRED_MODES:
        return {"status": "unknown", "reason": "unsupported_gateway_posture"}
    if not isinstance(fixture, dict) or fixture.get("schema") != "aoa_discord_fixture_snapshot_v1":
        return {"status": "unknown", "reason": "malformed_fixture"}
    conversations = fixture.get("conversations")
    if not isinstance(conversations, list):
        return {"status": "unknown", "reason": "malformed_fixture"}

    populations: dict[str, list[tuple[str, str]]] = {candidate: [] for candidate in PAIRED_MODES}
    for conversation in conversations:
        if not isinstance(conversation, dict) or conversation.get("conversation_type") != "guild_text_channel":
            continue
        conversation_id = conversation.get("conversation_id")
        messages = conversation.get("messages")
        if not isinstance(conversation_id, str) or not conversation_id or not isinstance(messages, list):
            return {"status": "unknown", "reason": "malformed_guild_population"}
        for message in messages:
            if not isinstance(message, dict):
                return {"status": "unknown", "reason": "malformed_guild_message"}
            message_id = message.get("message_id")
            visible_modes = message.get("visible_in_modes")
            text = message.get("text")
            if (
                not isinstance(message_id, str)
                or not message_id
                or not isinstance(visible_modes, list)
                or not isinstance(text, str)
                or not text
            ):
                return {"status": "unknown", "reason": "malformed_guild_message"}
            for candidate in PAIRED_MODES:
                if candidate in visible_modes:
                    populations[candidate].append((conversation_id, message_id))

    first, second = (populations[candidate] for candidate in PAIRED_MODES)
    if not first or set(first) != set(second):
        return {"status": "unknown", "reason": "empty_or_unpaired_gateway_population"}
    expected = populations[mode]
    expected_set = set(expected)
    if len(expected) != len(expected_set):
        return {"status": "unknown", "reason": "duplicate_fixture_message_identity"}

    if not isinstance(normalized, dict) or normalized.get("schema") != "aoa_discord_normalized_snapshot_v1":
        return {"status": "unknown", "reason": "malformed_normalized_snapshot"}
    normalized_conversations = normalized.get("conversations")
    if not isinstance(normalized_conversations, list):
        return {"status": "unknown", "reason": "malformed_normalized_snapshot"}

    materialized: dict[tuple[object, object], dict[str, object]] = {}
    for conversation in normalized_conversations:
        if not isinstance(conversation, dict) or not isinstance(conversation.get("messages"), list):
            return {"status": "unknown", "reason": "malformed_normalized_conversation"}
        for message in conversation["messages"]:
            if not isinstance(message, dict):
                return {"status": "unknown", "reason": "malformed_normalized_message"}
            identity = (message.get("conversation_id"), message.get("message_id"))
            if identity in materialized:
                return {"status": "unknown", "reason": "duplicate_normalized_message_identity"}
            if identity not in expected_set:
                return {"status": "unknown", "reason": "unexpected_normalized_message_identity"}
            permission = message.get("permission_state")
            if message.get("source_mode") != mode or not isinstance(permission, dict):
                return {"status": "unknown", "reason": "malformed_normalized_message"}
            if message.get("text_available") is False and bool(message.get("text")):
                return {"status": "unknown", "reason": "contradictory_text_visibility"}
            materialized[identity] = message

    numerator = sum(
        identity in materialized
        and materialized[identity].get("text_available") is True
        and materialized[identity]["permission_state"].get("status") == "authorized"
        and bool(materialized[identity].get("text"))
        for identity in expected
    )
    denominator = len(expected)
    return {
        "status": "observed",
        "numerator": numerator,
        "denominator": denominator,
        "ratio": numerator / denominator,
        "source_mode": mode,
    }


def test_reference_packets_match_current_paired_gateway_outputs(tmp_path: Path) -> None:
    fixture = load_json(FIXTURE_PATH)
    expected = {
        "bot_gateway": (0, 2, 0.0),
        "bot_gateway_message_content": (2, 2, 1.0),
    }

    for mode, (numerator, denominator, ratio) in expected.items():
        derived = derive_content_observability_ratio(fixture, normalized_fixture(tmp_path, mode), mode)
        packet = load_json(PACKET_PATHS[mode])

        assert derived == {
            "status": "observed",
            "numerator": numerator,
            "denominator": denominator,
            "ratio": ratio,
            "source_mode": mode,
        }
        assert packet["population"]["size"] == denominator
        assert packet["sample"]["size"] == denominator
        assert packet["dimensions"] == {"source_mode": mode}
        assert packet["value"] == {
            "status": "observed",
            "kind": "ratio",
            "unit": "1",
            "number": ratio,
            "numerator": numerator,
            "denominator": denominator,
        }
        assert packet["progress"] == {"state": "terminal", "completed": 2, "total": 2}


def test_missing_normalized_message_is_an_observed_gap(tmp_path: Path) -> None:
    fixture = load_json(FIXTURE_PATH)
    normalized = normalized_fixture(tmp_path, "bot_gateway_message_content")
    normalized["conversations"][0]["messages"].pop()

    assert derive_content_observability_ratio(fixture, normalized, "bot_gateway_message_content") == {
        "status": "observed",
        "numerator": 1,
        "denominator": 2,
        "ratio": 0.5,
        "source_mode": "bot_gateway_message_content",
    }


def test_permission_denial_over_complete_population_is_observed_zero(tmp_path: Path) -> None:
    derived = derive_content_observability_ratio(
        load_json(FIXTURE_PATH),
        normalized_fixture(tmp_path, "bot_gateway"),
        "bot_gateway",
    )

    assert derived["status"] == "observed"
    assert derived["numerator"] == 0
    assert derived["denominator"] == 2
    assert derived["ratio"] == 0.0


def test_malformed_duplicate_contradictory_and_unpaired_inputs_are_unknown(tmp_path: Path) -> None:
    fixture = load_json(FIXTURE_PATH)
    content = normalized_fixture(tmp_path, "bot_gateway_message_content")
    gateway = normalized_fixture(tmp_path, "bot_gateway")

    duplicate = deepcopy(content)
    duplicate["conversations"][0]["messages"].append(
        deepcopy(duplicate["conversations"][0]["messages"][0])
    )
    contradictory = deepcopy(gateway)
    contradictory["conversations"][0]["messages"][0]["text"] = "not redacted"
    empty = deepcopy(fixture)
    empty["conversations"] = [
        conversation
        for conversation in empty["conversations"]
        if conversation["conversation_type"] != "guild_text_channel"
    ]
    unpaired = deepcopy(fixture)
    unpaired["conversations"][0]["messages"][0]["visible_in_modes"].remove("bot_gateway")

    cases = (
        derive_content_observability_ratio(None, content, "bot_gateway_message_content"),
        derive_content_observability_ratio(fixture, {"schema": "wrong"}, "bot_gateway_message_content"),
        derive_content_observability_ratio(fixture, duplicate, "bot_gateway_message_content"),
        derive_content_observability_ratio(fixture, contradictory, "bot_gateway"),
        derive_content_observability_ratio(empty, gateway, "bot_gateway"),
        derive_content_observability_ratio(unpaired, gateway, "bot_gateway"),
        derive_content_observability_ratio(fixture, content, "rest_history"),
    )

    assert all(case["status"] == "unknown" for case in cases)


def test_measurement_stays_reference_only_and_below_permission_eval_and_runtime_authority() -> None:
    port = load_json(PORT_PATH)
    measurement = port["measurements"][0]
    ceiling = measurement["authority_ceiling"]

    assert port["evidence_posture"] == {
        "live_state": "reference_only",
        "privacy": "public",
        "raw_content_allowed": False,
    }
    assert measurement["live_state"] == {"capability": "reference_only"}
    assert measurement["aggregation"] == {"operator": "none", "across": []}
    assert measurement["dimensions"]["allowed"] == [
        {"name": "source_mode", "max_cardinality": 2, "sensitivity": "public"}
    ]
    assert "real bot authorization" in ceiling
    assert "connector readiness" in ceiling
    assert "eval success" in ceiling
    assert all(load_json(path)["posture"]["raw_content_included"] is False for path in PACKET_PATHS.values())
