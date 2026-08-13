# HARVIS to JARVIS Documentation

This package defines an incremental, reversible path from the runnable HARVIS runtime to a safer JARVIS core. It does not authorize a rewrite or select a final framework, database, provider, or JavaScript source layout.

## Start Here

1. Read [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md). It is the completed, evidence-based Phase 0 audit and the source of truth for the current system.
2. Review [JARVIS_ARCHITECTURE.md](JARVIS_ARCHITECTURE.md) for the proposed boundaries, not a selected implementation stack.
3. Use [MIGRATION_PLAN.md](MIGRATION_PLAN.md) and [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) to sequence reversible work.
4. Apply [SECURITY_MODEL.md](SECURITY_MODEL.md) to every tool and ingress migration.

## Documents

| Document | Purpose | Status |
|---|---|---|
| `CURRENT_ARCHITECTURE.md` | Verified runtime inventory, risks, dispositions, and Phase 1 entry criteria. | Completed Phase 0 evidence |
| `JARVIS_ARCHITECTURE.md` | Target boundaries and invariants for an incremental core. | Proposed migration shape |
| `MIGRATION_PLAN.md` | Safe baseline process, rollout order, and rollback rules. | Planning guidance |
| `DEVELOPMENT_PLAN.md` | Outcome-based phases and acceptance conditions. | Planning guidance |
| `SECURITY_MODEL.md` | Required ToolGateway and authorization controls. | Required design constraints |

## Current Runtime Facts

HARVIS is currently a Python runtime centered on `kloom.py`. Microphone input uses `sounddevice`, VAD, an `asyncio` queue, and `faster-whisper`; the HUD uses `pywebview` with embedded HTML/JavaScript; Telegram long-polls the Bot API; and speech output uses Edge TTS, in-memory MP3, and `pygame`. `cerebro.py` and `cerebro_jarvis.py` support Claude, Ollama, Groq, Kimi, OpenAI, and Gemini.

OpenRouter, Supabase, and the Web Speech API are not current runtime integrations. They are future, unselected options only and must not appear as current architecture.

## Non-Negotiable Migration Rules

- Keep HARVIS runnable. Route each migrated capability through a feature flag that selects legacy behavior or the JARVIS-core path.
- Start with `InboundTurn` adapters and a `TurnOrchestrator` facade that delegates to the legacy turn behavior.
- Do not remove legacy behavior until its replacement has validated rollback and equivalence criteria.
- Do not create or distribute a stable tag from the current dirty worktree. Select and validate an intentional baseline commit first.
- Treat Phase 0 boundaries as reversible. Final framework, storage, provider, and source-layout choices remain open.
