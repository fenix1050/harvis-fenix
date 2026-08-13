# HARVIS to JARVIS Migration Plan

## Strategy

Migrate behind small, reversible seams. HARVIS is not being replaced by a new application, and the existence of a target architecture does not authorize its early implementation.

The current path is:

```text
HARVIS legacy runtime
  -> default-off Phase 1 Core facade
  -> validated compatibility boundary
  -> policy gateway and other focused migration slices
```

## Verified State

| Fact | Status |
|---|---|
| Current-architecture and security baseline | Documented in committed JARVIS docs |
| Phase 1 Core implementation | Commit `09fa39c` on `feat/jarvis-core` |
| Default behavior | Legacy-compatible; Core flag is off by default |
| Manual microphone/HUD smoke check | Pending |
| `harvis-stable` | Not created |
| OpenRouter, Supabase, Web Speech API runtime use | Not present |
| Final framework, database, or provider | Not selected |

Do not turn these facts into claims of a stable tag, a release, production readiness, a push, or completed manual validation.

## Phase 1: Current Slice

Phase 1 adds contracts and a compatibility facade without replacing the existing provider, tool, memory, voice, or HUD implementations. The switch is default-off, so rollback is disabling `jarvis_core.enabled` and continuing through the unchanged legacy route.

The outstanding validation is manual compatibility smoke testing of microphone and typed HUD input, including expected HUD and speech output behavior. The result must be recorded before the enabled route is treated as operationally validated.

## Phase 2: Blocked Until Entry Criteria

Phase 2 runtime work is blocked pending:

1. Recorded manual Phase 1 compatibility validation.
2. A deliberate baseline decision. `harvis-stable` may be created only after selecting and validating the intended commit; it does not exist today.
3. An approved policy-gateway design matching `SECURITY_MODEL.md`.
4. A narrow, feature-flagged implementation plan with an explicit rollback boundary.

The first Phase 2 concern is not a broad tools rewrite. It is a compatibility-mode `ToolGateway` design that can eventually centralize typed validation, authorization, risk classification, transaction-bound approval, redacted audit events, timeouts, and cancellation.

## Migration Rules

- Keep existing behavior unless a focused slice deliberately replaces it.
- Preserve legacy code until its replacement has evidence of equivalent behavior.
- Move dependencies behind contracts before selecting or changing vendors.
- Keep local-file storage operational while storage and tracing ports are introduced.
- Use explicit channel and identity metadata before expanding remote authority.
- Enforce allowlisted operations and targets; do not authorize arbitrary commands with regex denylists or conversational confirmation alone.
- Build UI after the underlying state and controls exist.

## Later Work, Subject to Evidence

After Phase 2 gates are met, candidate slices include provider normalization, storage/tracing ports, runtime context and lifecycle ownership, memory retrieval, planning, agents, evolved voice interfaces, and a Command Center. Their ordering and implementation are intentionally undecided until prerequisites, risks, and acceptance evidence are known.

## Completion Evidence

For each slice, the review record should state the feature-flag default, behavior preserved, exact validation performed, validation not performed, rollback boundary, and any remaining security or operational risk. Do not infer test, manual, release, or deployment outcomes from the presence of code or documentation.
