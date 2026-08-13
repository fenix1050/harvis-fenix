# JARVIS Development Plan

## Current Position

JARVIS is an incremental evolution of HARVIS, not a rewrite. The current repository state is:

| Item | Status |
|---|---|
| Phase 0 architecture audit | Documented in `CURRENT_ARCHITECTURE.md` |
| `harvis-stable` tag | Not created |
| Phase 1 Core | Implemented in commit `09fa39c` on `feat/jarvis-core` |
| Phase 1 manual microphone/HUD smoke validation | Pending |
| Runtime OpenRouter, Supabase, or Web Speech API | Not present |
| Final JavaScript framework, database, or provider | Not selected |

The Phase 1 route is disabled by default. With the flag off, HARVIS keeps its legacy behavior. Phase 1 does not authorize a wholesale rewrite or the implementation of later capabilities.

## Phase 1: Legacy-Compatible Core

**Goal:** establish a small, reversible Core boundary while retaining the existing HARVIS turn path.

Delivered scope:

- immutable command request, response, error, cancellation, and output-target contracts;
- a legacy adapter and a default-off dispatcher selection;
- a composition seam after accepted HUD input, before the existing legacy dispatch;
- configuration defaulting `jarvis_core.enabled` to `false`.

The Core is currently a compatibility facade. It delegates enabled turns to legacy behavior; it does not replace providers, tools, memory, voice, or the HUD.

### Non-Microphone Validation Evidence (2026-08-13)

- Passed with the project `.venv`: `test_hud.py`, `test_jarvis_core.py`, `test_startup.py`, `test_registry.py`, and `test_jarvis.py`; `py_compile` and diff checks also passed. `test_jarvis.py` emits expected mocked failure traces while exiting successfully.
- Passed: `git diff --check`.
- `test_hud.py` opens the real pywebview HUD test window and verifies pending messages, state, and `Hud.send_text` delivery to its sink.
- The HUD test was corrected to assert the live HUD's three `#brain-sel` options rather than stale `#brains button` controls. This was a stale test assertion, not a HUD runtime defect.
- Core tests cover request normalization and immutability; HUD/text Core -> LegacyAdapter -> injected legacy handler delegation exactly once with response preservation; disabled-default versus enabled feature flag behavior; structured error conversion; cancellation; source and output preservation; and direct stdlib-only imports. The latter confirms no direct microphone, UI, concrete provider, Hermes, or Claude Code dependencies.
- These silent checks do not validate the production `kloom.main` path from full HUD text through Core and `LegacyAdapter` to a live LLM tool and HUD response. Before its queue loop, the application unconditionally initializes STT, pygame/Boca, provider connection setup, and the Oido microphone; that chain must not be described as validated.
- `package.json` is absent, so `npm test` and `npm run lint` are not applicable and were not run.

### Pending Validation

Manual smoke validation remains required before relying on the enabled route:

- microphone ingress still reaches the expected legacy behavior;
- typed HUD ingress still reaches the expected legacy behavior;
- the HUD continues to display and speech output continues to behave as expected;
- disabling the flag restores the legacy route without behavior drift.

Manual microphone/HUD smoke validation remains pending: startup, typed HUD validation against the live runtime, real voice input, one tool, expected HUD and real TTS output, and real voice-failure recovery. Manual confirmation remains required before the Core enabled route is operationally validated. `harvis-stable` is a local provisional tag at the approved pre-Core baseline `800294c`; it has not been pushed.

## Phase 2 Entry Gate

Do not begin Phase 2 runtime work until all of the following are true:

- the manual Phase 1 compatibility smoke validation is recorded;
- an intentional HARVIS baseline commit is selected; creating `harvis-stable` remains a separate decision and has not occurred;
- the policy-gateway design is agreed, including typed operations, risk classification, authorization, transaction-bound approval, redacted audit events, timeouts, and cancellation;
- the next slice has a default-safe feature flag and a scoped rollback path.

## Sequenced Future Work

The following is order of discovery, not an implementation commitment or milestone record.

1. Route effectful capabilities through a compatibility-mode `ToolGateway` and design policy enforcement.
2. Isolate provider selection behind normalized request and response contracts.
3. Put local persistence and tracing behind storage and tracing ports before changing storage products.
4. Introduce explicit inbound metadata, runtime context, and lifecycle supervision where the existing seams support them.
5. Add memory, planning, agents, voice evolution, events, and a Command Center only when their prerequisite contracts and controls exist.

Provider choices, a JavaScript framework, a database, hosted services, and agent runtimes remain open decisions. OpenRouter, Supabase, and the Web Speech API must not be described as current runtime integrations.

## Guardrails

- Keep the legacy route available until an equivalent replacement is validated.
- Do not delete legacy code merely because a target design exists.
- Do not let a model, HUD, dynamic skill, or remote channel directly execute sensitive operations.
- Do not build a future HUD, knowledge graph, full memory engine, new agent runtime, or Voice v2 ahead of its approved phase.
- Treat completion claims as evidence-based: record validation before declaring a capability ready.

## Completion Standard

Each future slice should be independently reviewable, default-safe, documented, and removable without changing unrelated behavior. Validation must state what actually ran and what remains manual or unverified.
