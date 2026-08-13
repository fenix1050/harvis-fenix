"""Deterministic standalone checks for the Phase 1 JARVIS Core facade."""
import asyncio
import importlib.util
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
    forbidden = ("import kloom", "from kloom", "import hud", "from hud",
                 "import oido", "from oido", "import boca", "from boca",
                 "import cerebro", "from cerebro", "import tools", "from tools")
    assert not any(item in source for item in forbidden)


if __name__ == "__main__":
    test_request_normalizes_and_freezes_contract_data()
    test_response_structure_and_cancellation_representation()
    test_legacy_delegation_preserves_source_and_output_targets()
    test_core_returns_structured_response_when_legacy_raises()
    test_disabled_default_and_enabled_flag()
    test_load_config_defaults_core_to_disabled()
    test_core_preserves_cancellation_from_legacy()
    test_core_has_no_harvis_runtime_imports()
    print("jarvis core checks OK")
