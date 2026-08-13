# JARVIS Security Model

All effectful runtime capabilities must cross a `ToolGateway`. The gateway replaces SSH regex-denylist controls and prompt-only confirmations with explicit, auditable authorization.

## Required Execution Path

```text
Provider or adapter request
  -> ToolGateway
  -> typed input validation
  -> risk classification
  -> authorization
  -> transaction-bound approval when required
  -> approved adapter execution with timeout and cancellation
  -> redacted audit event
```

The model proposes an operation. It does not receive direct execution authority. The same rule applies to providers, the HUD, dynamic skills, and remote ingress.

## ToolGateway Responsibilities

| Control | Required behavior |
|---|---|
| Typed inputs | Validate tool name, operation, target, and arguments before dispatch. Reject unrecognized fields and invalid values. |
| Risk | Assign risk from the declared operation and target, not model prose. |
| Authorization | Check actor, channel, policy, and permitted environment before execution. |
| Approval | Bind any approval to one transaction containing the exact action, sanitized parameters, actor, expiry, and one-time use. |
| Audit | Record a redacted event with transaction, actor, channel, tool, operation, risk, policy decision, result, duration, and cancellation status. |
| Timeouts and cancellation | Apply bounded execution and support cancellation before and during execution. |
| Allowlisting | Permit defined operations and targets. Do not filter arbitrary commands with a denylist. |

## Risk Classes

| Class | Examples | Default control |
|---|---|---|
| Observe | Read-only local status, logs, or diagnostics. | Authorization and audit. |
| Modify | Persistent local changes or service changes. | Authorization, audit, and policy-defined approval. |
| Critical | Destructive, externally visible, credential, production, or irreversible actions. | Explicit transaction-bound approval, strict timeout, audit, and cancellation. |

Risk class names and thresholds can evolve, but they must be policy decisions rather than provider prompts.

## Ingress and UI Controls

- Telegram ownership must use explicit enrollment or local approval. First-contact pairing is not sufficient authorization.
- An `InboundTurn` carries channel and identity metadata so policy can distinguish microphone, HUD, and Telegram requests.
- The HUD may submit input and render output. It must never grant or directly trigger dynamic skill execution.
- Dynamic skills require reviewed manifests, declared capabilities, lifecycle limits, and server-side authorization.
- External web pages, documents, logs, email, repositories, and tool output are untrusted data, not system instructions.

## Current Risks Requiring Migration

| Current condition | Required replacement |
|---|---|
| Model-provided SSH commands filtered by regex denylist | Typed, allowlisted operations and targets enforced by `ToolGateway`. |
| Prompt-only confirmation | Approval bound to one exact transaction with expiry and one-time use. |
| First-contact Telegram owner pairing | Explicit enrollment and identity checks. |
| HUD-selected dynamic skill execution | Reviewed, server-authorized extension model with no UI-granted authority. |
| Distributed local logs and state | Storage/tracing ports with redaction, retention, and access policy. |

## Secrets and Records

Secrets remain outside the UI, prompts, and audit events. Store only sanitized arguments and redact credentials, tokens, cookies, private keys, and sensitive content from traces. Local file storage remains the current implementation; no database or secret-store product is selected by Phase 0.

## Rollout Rule

Introduce the gateway in compatibility/observation mode, record proposed decisions, then enforce controls one tool class at a time. The legacy-versus-JARVIS-core feature flag remains the rollback path while policy coverage expands.
