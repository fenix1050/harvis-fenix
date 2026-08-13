# JARVIS Development Plan

This plan turns the Phase 0 audit into small, evidence-driven migration slices. It does not prescribe a final framework, database, provider, or JavaScript source layout.

## Phase 0: Completed Audit

**Outcome:** a verified current-state baseline and a reversible migration shape.

The completed evidence is in [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md). It confirms a Python runtime centered on `kloom.py`, current ingress/output/provider paths, coupling points, risks, component dispositions, and Phase 1 entry criteria.

Phase 0 does not claim that OpenRouter, Supabase, or Web Speech API are current integrations. It does not create a stable tag because the worktree is dirty and no intentional baseline commit has yet been selected and validated.

## Phase 1: Safe Core Entry

**Outcome:** introduce the first JARVIS boundary without changing the user-visible HARVIS behavior.

### Implemented slice

`jarvis_core.py` supplies stdlib-only immutable request/response contracts and a `JarvisCore` facade with an injected `LegacyAdapter`. It imports no HARVIS runtime modules. The current command dispatcher remains the only execution implementation in this phase; this boundary does not claim provider-neutral tools, providers, persistence, UI, or lifecycle execution.

The seam is in `kloom.py` immediately after an accepted command is constructed and `hud.heard(...)` runs, before the Telegram or local dispatch branches. Voice, typed HUD, and Telegram commands construct the same contract there. Telegram deliberately has no fabricated user or session identity.

| Topic | Phase 1 behavior |
|---|---|
| Feature flag | `jarvis_core.enabled` defaults to `false` in `load_config`; omitted configuration uses legacy dispatch. No user-specific `config.yaml` change is required. |
| Enabled route | The shared facade invokes the injected legacy Telegram/local dispatcher exactly once; disabled mode invokes that dispatcher directly. |
| Scope | Queue controls, raw audio, microphone/HUD startup, Telegram audio download, providers, tools, storage, and UI stay outside the core. |
| Cancellation | The contract represents cancellation without changing the existing abort event or turn behavior. |
| Rollback | Keep `jarvis_core.enabled` absent or `false`; removing the facade call and root module/test restores the prior direct route without touching runtime subsystems. |

### Evidence

Run `.venv\Scripts\python.exe test_jarvis_core.py` for deterministic contract and delegation checks. Run `.venv\Scripts\python.exe test_startup.py` for the existing focused startup checks. Manual microphone and HUD smoke validation remains pending and is required before treating this compatibility route as operationally proven.

**Acceptance conditions:** HARVIS remains runnable; the legacy route remains available; the facade does not change provider, tool, persistence, or output behavior; rollback is explicit.

## Phase 2: Controlled Capabilities

**Outcome:** all effectful tool calls have a single policy boundary.

1. Introduce `ToolGateway` in compatibility/observation mode.
2. Add typed validation, risk classification, authorization, transaction-bound approval, audit events, timeouts, and cancellation.
3. Migrate tools by risk class, beginning with low-risk read-only operations.
4. Replace SSH regex-denylist handling and prompt-only confirmations with allowlisted operations and bound approvals.

**Acceptance conditions:** no migrated effectful tool bypasses the gateway; UI actions cannot grant execution authority; approval evidence identifies one exact operation and expires.

## Phase 3: Replaceable Runtime Dependencies

**Outcome:** providers, state, tracing, and lifecycle can evolve without expanding the orchestrator.

1. Wrap the current Claude and OpenAI-compatible provider paths behind a normalized provider interface.
2. Place local file persistence and traces behind storage and tracing ports; retain file-backed adapters initially.
3. Introduce injected runtime context and lifecycle supervision for audio, providers, skills, and watchers.

**Acceptance conditions:** current providers remain usable; no database migration is required; lifecycle ownership and cancellation are explicit.

## Deferred Decisions

The following require later evidence and a focused decision record:

| Topic | Phase 0 status |
|---|---|
| Framework and language layout | Unselected |
| Database or hosted persistence | Unselected; local files remain current |
| Provider expansion or replacement | Unselected; current providers remain Claude, Ollama, Groq, Kimi, OpenAI, and Gemini |
| OpenRouter, Supabase, Web Speech API | Not current runtime integrations; future options only |
| Planner, agents, proactive events, vision, and broader automation | Deferred until the core boundaries and policy gateway are proven |

## Global Completion Rule

A slice completes only with documented scope, runnable legacy fallback, validation evidence, explicit rollback, updated security posture, and no unreviewed expansion into unrelated architecture decisions.
