"""Deterministic standalone checks for the Phase 1 JARVIS Core facade."""
import asyncio
import ast
import importlib.util
import sys
from pathlib import Path

from jarvis_core import (CommandRequest, CommandResponse, JarvisCore,
                         LegacyAdapter, StructuredError, dispatch, is_enabled)


def test_request_normalizes_and_freezes_contract_data():
    request = CommandRequest(
        "  check the calendar  ", "hud", metadata={"typed": True},
        output_targets=["hud"],
    )

    assert request.command == "check the calendar"
    assert request.output_targets == ("hud",)
    try:
        request.metadata["changed"] = True
    except TypeError:
        pass
    else:
        raise AssertionError("request metadata must be immutable")


def test_response_structure_and_cancellation_representation():
    response = CommandResponse(
        "stopped", chunks=["stop", "ped"], provider="claude",
        error=StructuredError("Cancelled", "stopped"),
        output_targets=["hud", "speech"], cancelled=True,
    )

    assert response.chunks == ("stop", "ped")
    assert response.error and response.error.kind == "Cancelled"
    assert response.cancelled is True


def test_legacy_delegation_preserves_source_and_output_targets():
    async def legacy(request):
        assert request.source == "telegram"
        assert request.session_id is None
        assert request.output_targets == ("hud", "telegram")
        return CommandResponse("sent", provider="claude",
                               output_targets=request.output_targets)

    request = CommandRequest("send this", "telegram",
                             output_targets=("hud", "telegram"))
    response = asyncio.run(JarvisCore(LegacyAdapter(legacy)).dispatch(request))

    assert response.response_text == "sent"
    assert response.provider == "claude"
    assert response.output_targets == ("hud", "telegram")


def test_hud_text_route_normalizes_and_delegates_once_unmodified():
    handler_calls = []
    adapter_calls = []
    expected_response = CommandResponse(
        "calendar opened", chunks=("calendar", " opened"), provider="claude",
        metadata={"legacy": True}, output_targets=("hud",),
    )

    async def legacy_harvis_handler(request):
        handler_calls.append(request)
        assert request.command == "open calendar"
        assert request.source == "hud"
        assert request.metadata == {"typed": True, "origin": "hud-input"}
        return expected_response

    class TrackingLegacyAdapter(LegacyAdapter):
        async def dispatch(self, request):
            adapter_calls.append(request)
            return await super().dispatch(request)

    request = CommandRequest(
        "  open calendar  ", "hud",
        metadata={"typed": True, "origin": "hud-input"}, output_targets=("hud",),
    )
    response = asyncio.run(
        JarvisCore(TrackingLegacyAdapter(legacy_harvis_handler)).dispatch(request))

    assert request.command == "open calendar"
    assert adapter_calls == [request]
    assert handler_calls == [request]
    assert response is expected_response


def test_core_returns_structured_response_when_legacy_raises():
    async def legacy(_request):
        raise RuntimeError("legacy failed")

    response = asyncio.run(JarvisCore(LegacyAdapter(legacy)).dispatch(
        CommandRequest("run", "voice", output_targets=("hud", "speech"))))

    assert response.error == StructuredError("RuntimeError", "legacy failed")
    assert response.output_targets == ("hud", "speech")


def test_disabled_default_and_enabled_flag():
    assert is_enabled({}) is False
    assert is_enabled({"jarvis_core": {}}) is False
    assert is_enabled({"jarvis_core": {"enabled": True}}) is True

    calls = []

    async def legacy(request):
        calls.append(request.source)
        return CommandResponse("legacy")

    request = CommandRequest("run", "voice")
    assert asyncio.run(dispatch({}, request, legacy)) is None
    assert asyncio.run(dispatch({"jarvis_core": {"enabled": True}},
                                request, legacy)).response_text == "legacy"
    assert calls == ["voice"]


def test_load_config_defaults_core_to_disabled():
    from kloom import load_config

    assert load_config()["jarvis_core"]["enabled"] is False


def test_core_preserves_cancellation_from_legacy():
    async def legacy(_request):
        return CommandResponse("[cortado]", cancelled=True)

    response = asyncio.run(JarvisCore(LegacyAdapter(legacy)).dispatch(
        CommandRequest("stop", "voice", output_targets=("hud", "speech"))))

    assert response.response_text == "[cortado]"
    assert response.cancelled is True
    assert response.output_targets == ("hud", "speech")


def test_core_has_no_harvis_runtime_imports():
    source = Path(importlib.util.find_spec("jarvis_core").origin).read_text(
        encoding="utf-8")
    imported_roots = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])

    forbidden_roots = {
        "kloom", "hud", "oido", "boca", "cerebro", "tools",
        "hermes", "claude", "claude_code", "claudecode",
    }
    assert not imported_roots & forbidden_roots
    assert not imported_roots - sys.stdlib_module_names


if __name__ == "__main__":
    test_request_normalizes_and_freezes_contract_data()
    test_response_structure_and_cancellation_representation()
    test_legacy_delegation_preserves_source_and_output_targets()
    test_hud_text_route_normalizes_and_delegates_once_unmodified()
    test_core_returns_structured_response_when_legacy_raises()
    test_disabled_default_and_enabled_flag()
    test_load_config_defaults_core_to_disabled()
    test_core_preserves_cancellation_from_legacy()
    test_core_has_no_harvis_runtime_imports()
    print("jarvis core checks OK")
