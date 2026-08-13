"""Compatibility contracts for the first JARVIS Core migration slice.

This module deliberately has no HARVIS runtime imports. Phase 1 delegates every
accepted command to the existing dispatcher supplied by the composition root.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Awaitable, Callable, Literal, Mapping


CommandSource = Literal["voice", "hud", "telegram"]


def _immutable_metadata(metadata: Mapping[str, object]) -> Mapping[str, object]:
    return MappingProxyType(dict(metadata))


@dataclass(frozen=True)
class StructuredError:
    """A failure that can cross the core boundary without raising."""

    kind: str
    message: str


@dataclass(frozen=True)
class CommandRequest:
    """An accepted command, after ingress-specific processing is complete."""

    command: str
    source: CommandSource
    session_id: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)
    mode: str | None = None
    brain: str | None = None
    output_targets: tuple[str, ...] = ()
    cancelled: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "command", self.command.strip())
        object.__setattr__(self, "metadata", _immutable_metadata(self.metadata))
        object.__setattr__(self, "output_targets", tuple(self.output_targets))


@dataclass(frozen=True)
class CommandResponse:
    """The result of a command, including streaming-compatible output."""

    response_text: str = ""
    chunks: tuple[str, ...] = ()
    provider: str | None = None
    error: StructuredError | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)
    output_targets: tuple[str, ...] = ()
    cancelled: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "chunks", tuple(self.chunks))
        object.__setattr__(self, "metadata", _immutable_metadata(self.metadata))
        object.__setattr__(self, "output_targets", tuple(self.output_targets))


LegacyDispatch = Callable[[CommandRequest], Awaitable[CommandResponse]]


class LegacyAdapter:
    """Delegates one core turn to injected legacy behavior without imports."""

    def __init__(self, dispatch: LegacyDispatch):
        self._dispatch = dispatch

    async def dispatch(self, request: CommandRequest) -> CommandResponse:
        return await self._dispatch(request)


class JarvisCore:
    """Phase 1 facade. Legacy dispatch remains the sole implementation."""

    def __init__(self, legacy: LegacyAdapter):
        self._legacy = legacy

    async def dispatch(self, request: CommandRequest) -> CommandResponse:
        try:
            response = await self._legacy.dispatch(request)
        except Exception as error:
            return CommandResponse(
                error=StructuredError(type(error).__name__, str(error)),
                output_targets=request.output_targets,
                metadata={"source": request.source},
            )
        if response.cancelled or request.cancelled:
            return CommandResponse(
                response_text=response.response_text,
                chunks=response.chunks,
                provider=response.provider,
                error=response.error,
                metadata=response.metadata,
                output_targets=response.output_targets or request.output_targets,
                cancelled=True,
            )
        return response


async def dispatch(
        config: Mapping[str, object], request: CommandRequest,
        legacy: LegacyDispatch) -> CommandResponse | None:
    """Select the legacy default or the opt-in facade at the composition seam."""

    if not is_enabled(config):
        return None
    return await JarvisCore(LegacyAdapter(legacy)).dispatch(request)


def is_enabled(config: Mapping[str, object]) -> bool:
    """Return the opt-in Phase 1 flag; absent configuration stays legacy."""

    section = config.get("jarvis_core")
    return bool(section.get("enabled", False)) if isinstance(section, Mapping) else False
