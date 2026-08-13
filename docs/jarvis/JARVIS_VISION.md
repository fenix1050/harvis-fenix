# JARVIS Vision

## Purpose

JARVIS is the intended evolution of HARVIS into a modular personal assistant that can eventually coordinate conversation, context, memory, controlled actions, verification, and multiple interfaces. It is not a renamed LLM, agent runtime, UI, database, or voice engine.

The current implementation is deliberately much smaller: a default-off Phase 1 Core compatibility facade that delegates to HARVIS. Manual microphone/HUD smoke validation is still pending.

## Product Direction

Over time, JARVIS may support:

- text, voice, HUD, Telegram, and other ingress through common turn contracts;
- bounded context and durable knowledge retrieval;
- provider-neutral model selection;
- typed tools and controlled automation;
- specialized agent delegation;
- planning, verification, events, and carefully governed routines;
- an interface that presents real system state.

These are product intentions, not delivered capabilities or implementation commitments.

## Core Principle

> JARVIS owns orchestration. Providers, agents, storage, voice, and interfaces are replaceable components.

This keeps a future provider, Claude Code, Hermes, Obsidian, a database, or a UI from becoming the architecture itself. No final JavaScript framework, database, or provider has been selected.

## Trust Model

JARVIS must distinguish a proposed action from authority to execute it. Models and interfaces can request work; a policy boundary must validate and authorize effectful operations, request transaction-bound approval when necessary, constrain execution, and write redacted audit records.

The target does not grant direct shell or infrastructure authority to a model, HUD, dynamic skill, or remote channel.

## Experience Principle

A future Command Center should help a user understand the active task, context, plan, and verified execution state. It must not simulate agents, memory, infrastructure health, or actions that do not yet exist.

## Migration Principle

HARVIS remains operational while JARVIS grows behind feature flags and tested seams. The next work begins only after the pending manual compatibility validation, baseline decision, and policy-gateway design are complete.
