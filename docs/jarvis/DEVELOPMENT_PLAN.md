# JARVIS Development Plan

This plan turns the Phase 0 audit into small, evidence-driven migration slices. It does not prescribe a final framework, database, provider, or JavaScript source layout.

## Phase 0: Completed Audit

**Outcome:** a verified current-state baseline and a reversible migration shape.

The completed evidence is in [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md). It confirms a Python runtime centered on `kloom.py`, current ingress/output/provider paths, coupling points, risks, component dispositions, and Phase 1 entry criteria.

Phase 0 does not claim that OpenRouter, Supabase, or Web Speech API are current integrations. It does not create a stable tag because the worktree is dirty and no intentional baseline commit has yet been selected and validated.

## Phase 1: Safe Core Entry

**Outcome:** introduce the first JARVIS boundary without changing the user-visible HARVIS behavior.

1. Define `InboundTurn` adapters for microphone, HUD text, and Telegram, including origin and identity metadata.
2. Add a `TurnOrchestrator` facade that delegates to the legacy turn loop.
3. Add a feature flag that chooses legacy behavior or the JARVIS-core facade.
4. Document the default route, rollback route, and validation evidence.

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
