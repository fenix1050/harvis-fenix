# JARVIS Target Architecture

## Scope and Status

This document describes the target direction, not an implemented runtime architecture. HARVIS remains a local Python-composed assistant with microphone, HUD, and Telegram ingress; provider/tool turns; and local-file persistence. See `CURRENT_ARCHITECTURE.md` for the evidence-backed current state.

Phase 1 is implemented as a default-off, legacy-compatible Core facade in commit `09fa39c` on `feat/jarvis-core`. Its manual microphone/HUD smoke validation is pending. It does not introduce a new runtime provider, database, web stack, or full orchestration pipeline.

## Architectural Direction

JARVIS should own stable orchestration contracts while replaceable components remain behind adapters:

```text
Ingress adapters
  -> Core turn contract
  -> policy-controlled provider, tool, storage, and output adapters
  -> response
```

The intended separation is:

| Boundary | Responsibility | Current state |
|---|---|---|
| Ingress | Carry command text, source, session, and metadata | Shared queue remains legacy; Phase 1 defines request metadata |
| Core | Coordinate a turn through stable contracts | Compatibility facade delegates to legacy behavior |
| Provider | Normalize model requests, responses, errors, and cancellation | Existing provider logic remains in HARVIS |
| Tool gateway | Validate, authorize, approve, execute, and audit effectful operations | Required design; not implemented |
| Storage and tracing | Persist state with retention and redaction policy | Local files remain the runtime implementation |
| Output | Send response to HUD and speech adapters | Existing HARVIS output path remains active |

## Phase 1 Boundary

The implemented Core provides immutable request and response contracts, structured failures, cancellation representation, output targets, a `LegacyAdapter`, and a feature-gated dispatcher. `jarvis_core.enabled` defaults to `false`.

When disabled, the existing HARVIS dispatch route is used. When enabled, the facade delegates to injected legacy behavior. This preserves compatibility while creating a narrow seam; it is not a replacement for the legacy runtime.

## Future Pipeline

The following pipeline is a target shape only:

```text
Input
  -> normalize and identify source
  -> build bounded context
  -> choose response, provider, or approved operation
  -> enforce policy before effectful execution
  -> execute with timeout and cancellation
  -> verify when required
  -> emit a redacted trace and response
```

Memory retrieval, multi-step planning, agent delegation, event handling, and UI state may join this pipeline only after their contracts and controls are designed and implemented. A request does not need every stage.

## Security Boundary

All effectful operations must eventually cross `ToolGateway`, as defined by `SECURITY_MODEL.md`. The gateway is responsible for typed validation, risk classification, authorization, transaction-bound approval where required, allowlists, bounded execution, cancellation, and redacted audit records.

No provider, model, HUD, dynamic skill, or remote ingress receives direct execution authority. A denylist for arbitrary commands is not a sufficient authorization model.

## Replaceable Components

JARVIS must not make its Core depend directly on a particular LLM provider, agent runtime, database, UI, voice engine, or human-facing knowledge tool. Claude Code, Hermes, Obsidian, and prospective provider or storage products are possible adapters or interfaces, not the Core.

OpenRouter, Supabase, and the Web Speech API are not current HARVIS runtime integrations. No final JavaScript framework, database, or provider has been selected.

## Deferred Capabilities

The following remain future architecture, not Phase 1 implementation:

- provider routing and model profiles;
- a policy-enforced tools and skills layer;
- structured and durable memory beyond current local files;
- context, planning, and verification services;
- agent supervision, desktop/VPS operations, and remote workflows;
- Voice v2, vision, browser automation, events, routines, and proactivity;
- a JARVIS Command Center or replacement HUD.

The HUD must represent verified capabilities and must not be used to simulate unfinished architecture.

## Invariants

1. Preserve a runnable legacy path until equivalent behavior is validated.
2. Keep feature flags default-safe and each migration slice reversible.
3. Separate policy and execution from model reasoning and UI presentation.
4. Keep durable human knowledge distinct from operational machine state.
5. Record evidence before claiming validation, readiness, or completion.
