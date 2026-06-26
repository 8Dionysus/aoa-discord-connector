"""Discord source-route policy helpers."""

from __future__ import annotations


ALLOWED_PREFIXES = (
    "discord:bot_gateway:guild:",
    "discord:rest_history:guild:",
    "discord:data_package:account:",
)

DENIED_MARKERS = ("user_token", "selfbot", "write:", "send_message", "download:", "attachment")


def route_decision(route: str) -> dict[str, object]:
    lowered = route.casefold()
    if any(marker in lowered for marker in DENIED_MARKERS):
        return _deny(route, "forbidden_user_token_selfbot_write_or_download_route")
    if route.startswith(ALLOWED_PREFIXES):
        mode = route.split(":", 2)[1]
        return {
            "route": route,
            "allowed": True,
            "mode": mode,
            "requires_explicit_allowlist": mode != "data_package",
            "operator_local": mode == "data_package",
            "reason": "authorized_discord_source_mode",
        }
    return _deny(route, "unknown_or_unconfigured_discord_route")


def _deny(route: str, reason: str) -> dict[str, object]:
    return {"route": route, "allowed": False, "reason": reason}
