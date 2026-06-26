from pathlib import Path

from aoa_discord_connector.normalize import normalize_snapshot
from aoa_discord_connector.policy.rules import route_decision


FIXTURE = Path("connector/fixtures/discord/starter_conversation.json")


def test_normalizer_redacts_message_content_without_privileged_intent(tmp_path: Path) -> None:
    output = normalize_snapshot(FIXTURE, "discord:fixture", tmp_path, mode="bot_gateway")
    text = output.read_text(encoding="utf-8")
    assert "aoa_discord_normalized_conversation_v1" in text
    assert "message_content_intent_missing" in text
    assert "vendor_boot.img" not in text


def test_normalizer_with_message_content_intent_can_index_channel_text(tmp_path: Path) -> None:
    output = normalize_snapshot(FIXTURE, "discord:fixture", tmp_path, mode="bot_gateway_message_content")
    text = output.read_text(encoding="utf-8")
    assert "guild_text_channel" in text
    assert "vendor_boot.img" in text
    assert "bootloop" in text


def test_data_package_mode_is_offline_account_owned_import(tmp_path: Path) -> None:
    output = normalize_snapshot(FIXTURE, "discord:fixture", tmp_path, mode="data_package")
    text = output.read_text(encoding="utf-8")
    assert "data_package_dm" in text
    assert "user-token selfbot collection is forbidden" in text


def test_policy_models_authorized_and_denied_routes() -> None:
    assert route_decision("discord:bot_gateway:guild:aoa-lab:channel:android")["allowed"] is True
    assert route_decision("discord:rest_history:guild:aoa-lab:channel:android")["allowed"] is True
    assert route_decision("discord:data_package:account:self")["operator_local"] is True
    assert route_decision("discord:user_token_selfbot:dm:self")["allowed"] is False
    assert route_decision("discord:write:send_message")["allowed"] is False
    assert route_decision("discord:download:attachment")["allowed"] is False
