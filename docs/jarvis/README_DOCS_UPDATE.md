# JARVIS Documentation Package

This package separates verified HARVIS facts from the prospective JARVIS direction so the migration can be reviewed without treating plans as completed runtime work.

## Review Order

1. Read `CURRENT_ARCHITECTURE.md` for the evidence-backed HARVIS baseline.
2. Read `SECURITY_MODEL.md` for the required policy-gateway boundary.
3. Read `DEVELOPMENT_PLAN.md` and `MIGRATION_PLAN.md` for the current Phase 1 status and Phase 2 gates.
4. Read `JARVIS_ARCHITECTURE.md` and `JARVIS_VISION.md` as target-direction documents.

## Current Facts

- Phase 1 Core is committed as `09fa39c` on `feat/jarvis-core`.
- The compatibility flag is off by default and legacy behavior remains the default route.
- Manual microphone/HUD smoke validation remains pending.
- `harvis-stable` has not been created.
- OpenRouter, Supabase, and the Web Speech API are not runtime integrations.
- No final JavaScript framework, database, or provider is selected.
- Phase 2 is blocked pending manual compatibility evidence, an intentional baseline decision, and policy-gateway design.

## Documentation Rule

Treat future architecture as conditional design. Record implementation, validation, release, tag, push, or production claims only when repository evidence supports them.
