# Generic oracle catalog

Choose the smallest set that can observe the claim. UI appearance alone is not
an oracle for storage, network or lifecycle effects.

## Surface routing

| Surface | Candidate use after its probe passes | Does not prove |
|---|---|---|
| Production Flutter Web | Shared UI/state discovery, object ledgers, empty/minimal/repeat/recovery, localization and browser accessibility | Native plugin, iOS/Android process lifecycle, secure storage or hardware behavior |
| Simulator/emulator | Narrow confirmation of native navigation, plugin, storage, OS lifecycle, keyboard/safe-area or packaging claims | Real microphone/audio routes, lock-screen behavior, calls, power/thermal or physical accessibility use |
| Device/TestFlight | Hardware, real authentication, install/upgrade, background audio and other OS behavior unavailable in simulation | Unrelated shared flows that were never exercised |

Choose the cheapest row that both passes its controller capability probe and
faithfully contains the claim. Moving downward is evidence escalation, not a
reason to repeat unrelated discovery.

## Stable semantic anchors

Use the product's existing user-facing accessibility and automation surface;
do not add a parallel test-only navigation model merely for this Skill.

| Product surface | Useful anchors |
|---|---|
| Web | ARIA role/name/value, labels, live regions, stable test IDs |
| Flutter | Semantics label/role/value, keys or test IDs exposed by the production build |
| iOS | accessibility identifier, label, value, trait and visible state |
| Android | content description, resource/test ID, role/state and visible text |

Prefer anchors a user-assistive surface can also understand. A test ID may
locate a control, but it does not replace checking whether the control has a
meaningful accessible name and state.

| Oracle | Evidence | Typical claim |
|---|---|---|
| Visible state | screenshot plus stable text | hierarchy, language, empty/error/success copy |
| Accessibility | role, name, value, live status | operability and status announcement |
| Object ledger | pre/post count and labels | empty creates, duplicates, retry multiplication |
| Lifecycle | before/after background or relaunch ledger | draft/history continuity |
| Identity context | visible user, tenant/workspace, role, verification and edit route | “connected/ready” is attributable |
| Network/API adapter | request count, idempotency key, response class | duplicate calls and silent failure |
| Storage adapter | durable object IDs before/after | cancellation residue and restart recovery |
| Quiescence | explicit state predicate, not fixed sleep | terminal-state and timing claims |

## Stable-state rule

Prefer an explicit predicate such as no loading/live status, target object
reached terminal state, request count stopped changing, or bounded timeout with
`stability_unproven`. A fixed sleep by itself does not prove completion.

## Fixture-fidelity rule

Record which production boundary each adapter replaces. Compare at least one
state-changing operation against production behavior or source before scoring.
If the adapter changes whether or when objects are created, listed, persisted
or restored, it is not an observation adapter; it is a different subject.

The product adapter must declare draft/commit semantics. An empty action that
creates an intentional recoverable draft is not a defect merely because the
generic ledger observed a new object.
