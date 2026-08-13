# HARVIS to JARVIS Migration Plan

The migration is incremental and reversible. HARVIS remains runnable while a feature flag selects the legacy route or the JARVIS-core route for each migrated slice.

## Baseline Before Architecture Work

A `harvis-stable` tag cannot be created safely from the currently dirty worktree. A tag identifies a specific commit, so its baseline must be intentionally selected and validated before any tag is created or distributed.

1. Review existing modified and untracked paths without discarding intentional work.
2. Establish a clean, intentional baseline and identify its exact commit.
3. Pin and review dependencies, then run the separately agreed validation in an isolated environment.
4. Record the selected commit, worktree state, validation commands, and results.
5. Create an annotated tag only after the previous evidence is accepted. Distribution is a separate approved operation.

This document intentionally provides no blind `checkout`, `pull`, `tag`, or `push` commands.

## Migration Sequence

| Slice | Change | Legacy protection | Exit condition |
|---|---|---|---|
| 1. Ingress | Add `InboundTurn` adapters for microphone, HUD text, and Telegram. | Each adapter delegates to current turn handling. | Origin and identity metadata are available without behavioral change. |
| 2. Orchestration | Add `TurnOrchestrator` facade. | Feature flag routes to legacy or facade; facade delegates to legacy behavior. | Rollback is verified and provider/tool behavior is unchanged. |
| 3. Tools | Introduce compatibility-mode `ToolGateway`. | Observe policy decisions before enforcing selected tool classes. | All effectful tool calls can be audited at one boundary. |
| 4. Providers | Extract provider adapters from `cerebro.py` and `cerebro_jarvis.py`. | Current providers remain available through adapters. | Orchestration is provider-neutral. |
| 5. State | Add storage and tracing ports around local files. | File-backed implementations remain active. | Retention and redaction policy has one ownership point. |
| 6. Lifecycle | Introduce injected runtime context and lifecycle supervision. | Supervise legacy components before replacing them. | Startup, shutdown, watcher cancellation, and failures have explicit ownership. |
| 7. Enforcement | Enforce allowlisted operations and transaction-bound approvals by tool class. | Feature flag and staged policy rollout remain available. | Side effects cannot bypass validation or authorization. |

## Compatibility Rules

- Do not perform a wholesale rewrite.
- Do not remove a legacy component based only on source inspection; retain it until runtime and product dependency are assessed.
- Do not migrate data storage merely because a port exists; local-file adapters are the initial implementation.
- Do not assume a final database, provider, framework, or source-tree layout.
- Do not treat OpenRouter, Supabase, or Web Speech API as existing integration work. They are unselected future options.

## Rollback Conditions

Each slice must preserve a narrow rollback: disable the relevant feature flag and route affected turns to the known legacy behavior. A slice is not ready to expand when it changes provider selection, tool semantics, storage format, or user-facing output outside its stated boundary.

## Evidence to Record Per Slice

- Feature-flag scope and default route.
- Interfaces and adapters introduced.
- Behavior deliberately preserved.
- Validation performed and known gaps.
- Rollback action and owner.
- Security controls enabled, observed, or deferred.
