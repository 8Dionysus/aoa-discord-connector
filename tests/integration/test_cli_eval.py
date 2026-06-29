import json
import os
import subprocess
import sys


def _run(*args: str, env: dict[str, str] | None = None) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "aoa_discord_connector.cli", *args],
        check=True,
        text=True,
        capture_output=True,
        env=env,
    )
    return json.loads(completed.stdout)


def test_cli_materialize_build_query_answer_and_eval() -> None:
    materialize = _run("materialize", "fixture", "--run", "pytest-fixture", "--mode", "bot_gateway_message_content")
    assert materialize["network_touched"] is False
    index = _run("build-index", "--run", "pytest-fixture")
    assert index["doc_count"] >= 2
    graph = _run("build-graph", "--run", "pytest-fixture")
    assert graph["edge_count"] >= 6
    query = _run("query-graph", "vendor_boot bootloop warning", "--run", "pytest-fixture")
    assert query["network_touched"] is False
    assert query["read_only"] is True
    assert query["results"]
    answer = _run("answer", "vendor_boot bootloop warning", "--run", "pytest-fixture")
    assert answer["network_touched"] is False
    assert answer["read_only"] is True
    assert answer["answer_report"]["answer_status"] == "answered"
    assert _run("eval", "permissions")["status"] == "pass"
    assert _run("eval", "answer-packets")["status"] == "pass"


def test_cli_sources_registry_plans_discord_scope(tmp_path) -> None:
    env = os.environ.copy()
    env["CONNECTOR_DATA_ROOT"] = str(tmp_path / "data")
    env["CONNECTOR_CACHE_ROOT"] = str(tmp_path / "cache")
    env["CONNECTOR_ARTIFACT_ROOT"] = str(tmp_path / "artifacts")

    channel = _run("sources", "add", "guild:aoa-lab/channel:android", "--kind", "guild_channel", "--tags", "android,firmware", "--trust-score", "0.8", env=env)
    assert channel["status"] == "ok"
    assert channel["source"]["access"] == "bot_visible"
    package = _run("sources", "add", "account:self", "--kind", "data_package", "--tags", "self,archive", "--trust-score", "1.0", env=env)
    assert package["source"]["access"] == "account_owned_export"

    listed = _run("sources", "list", env=env)
    assert listed["selected_count"] == 2
    plan = _run("sources", "plan", "--run", "pytest-discord-sources", "--limit", "50", env=env)
    assert plan["schema"] == "aoa_discord_source_sync_plan_v1"
    assert plan["selected_count"] == 2
    assert plan["network_touched"] is False
    assert all(step["operation"] == "sync" for step in plan["steps"])
