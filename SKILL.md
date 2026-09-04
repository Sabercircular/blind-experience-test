---
name: blind-experience-test
description: Test an app's core journey like a first-time user using isolated agent tasks, semantic coverage, and state ledgers, then return a reproducible product improvement list. Use for pre-release product discovery on Web, Flutter, iOS, Android, or desktop, and for explicit blind A/B/C recall benchmarks; do not use for ordinary known-bug regression tests.
---

# Blind Experience Test

Start from a request as small as “test this app.” The controller discovers the
testable context, asks only for information it cannot verify, tests one core
journey through isolated executor tasks, and returns one decision-ready
`RESULT.md`. The default round tests and stops; it does not edit the product.

## Discover before asking

Inspect the current project before questioning the user. Resolve as much as
possible from repository files, product notes, launch instructions, existing
tests, semantic anchors, and available runtimes:

- the exact product, source revision or artifact, and production entrypoint;
- the product promise and the single journey that delivers first value;
- the cheapest surfaces that may faithfully contain that journey;
- an isolated account, namespace, storage location, and clean reset;
- available Test IDs, Semantics, ARIA, accessibility tree, or other stable
  anchors;
- action/time budgets and actions that need separate authorization.

Track each required item internally as `required`, `discovered`, `missing`, and
`source`. Ask the user only about `missing` items that would change the run or
its safety. If nothing material is missing, state the chosen journey, surface,
isolation, no-edit default, and start. Ask when multiple products or promises
remain genuinely ambiguous; do not guess across them.

Use these defaults unless the user says otherwise:

- one core journey;
- one first-time-user task, one semantic-coverage task, and one state-audit
  task;
- isolated synthetic or test data;
- the lowest-cost behavior-faithful surface;
- audit only, followed by one product improvement list;
- no production mutation, code edit, merge, publish, or deploy.

## Freeze the subject and prove the apparatus

Before dispatch, create an immutable subject lock for the exact revision or
artifact and chosen journey. After launch, collect runtime identity and
capability evidence in a separate action. Expected identity and observed
identity must not come from the same claim.

Choose the lowest-cost surface that preserves the behavior under test and
passes a controller-owned capability probe. A production Web entrypoint is a
good candidate; a test-only Web projection that changes object creation,
identity, storage, or lifecycle is a different subject. Escalate only the
narrow claim that requires Simulator, Emulator, or device evidence.

If identity or state-changing bindings differ, mark the run `excluded`. If the
correct subject lacks a required capability, mark it `apparatus_blocked` with
`findings_allowed=false`. Do not turn either condition into a product finding.

Keep one run directory with:

```text
subject-lock.json
apparatus.json
runs/
evidence/
RESULT.md
```

Read [references/result-schema.md](references/result-schema.md) when creating
these files.

## Run one journey through three isolated tasks

Read [references/protocol.md](references/protocol.md) before dispatching the
executor tasks.

1. `user_simulation` pursues the user's goal without source, known bugs, a
   checklist, expected answers, or another executor's findings.
2. `semantic_coverage` follows stable semantic anchors through the critical
   destinations, actions, and empty/loading/success/failure/recovery states.
3. `state_audit` records object, identity, persistence, asynchronous ownership,
   Back/resume, and relevant lifecycle transitions before and after actions.

Prefer lower-cost executors that can reliably operate the chosen surface. The
controller keeps source, subject identity, known-fault information, and final
adjudication. Run tasks concurrently only when each has a fresh context,
isolated mutable state, and an independent reset. With one Simulator or test
account, run serially.

If fresh isolated executor contexts are unavailable, do not claim a blind
round. Complete only the intake and apparatus work, then report executor
isolation as the blocker.

Add a second user seed only when the first run suggests persona or seed
sensitivity. Add a `native_confirmation` task only when an accepted candidate
crosses the current surface's proven boundary. Do not replay every journey on
every platform.

## Adjudicate into one product improvement list

Executor observations and candidate findings remain immutable. The controller:

1. validates run files with `scripts/validate_runs.py`;
2. excludes wrong-subject and apparatus-blocked evidence;
3. reproduces each candidate from a clean reset and waits for a stable state;
4. deduplicates findings and separates product problems from testability gaps;
5. classifies accepted findings as `release_blocker`, `core_fix`,
   `experience_improvement`, or `human_decision`;
6. writes one `RESULT.md` with the release recommendation, product improvement
   list, coverage and limits, apparatus gaps, and evidence links.

The product improvement list is not an automatically approved requirements
list. State what happened, who it affects, why it matters, the supporting
evidence, a suggested change, a regression entry, confidence, and surface
scope. Let the user decide when more than one product behavior is valid.

Raw JSON, screenshots, and ledgers are evidence attachments. `RESULT.md` is the
only primary artifact the user should need to read.

## Stop, then repair only with authorization

Stop after delivering `RESULT.md`. Summarize the counts by class and recommend
the smallest useful next action. Do not continue testing until no defects can
be found.

Only after the user authorizes product changes, read
[references/repair-loop.md](references/repair-loop.md). Repair one root-cause
cluster on an isolated successor revision, add deterministic regression
coverage where the evidence establishes a stable contract, and use a fresh
tester for targeted verification. Repair authorization does not authorize
merge, publish, or deploy.

## Use benchmark mode only when requested

When the user explicitly asks to compare discovery methods, control budgets,
or measure added defect recall, use the A/B/C benchmark appendix in
[references/protocol.md](references/protocol.md). Keep subject, surface, reset,
persona, goal, model, effort, and budget comparable, and keep hidden ground
truth outside executor-visible context.

Ordinary “test this app” requests use the three-task product round, not the
A/B/C benchmark.

## Safety and stopping conditions

- Use isolated accounts, storage, browser contexts, devices, and synthetic or
  minimized inputs. Define evidence retention and cleanup for private content.
- Do not mutate production, accept legal terms, enter private credentials, or
  delete non-test data without separate authorization.
- Stop when the action/time budget, persona give-up point, apparatus blocker,
  or unresolved product decision is reached.
- UI-only evidence cannot prove hidden object, API, storage, or lifecycle
  effects; use the smallest relevant oracle from
  [references/oracle-catalog.md](references/oracle-catalog.md).
- Keep product-specific promises, adapters, and defects in the product
  repository rather than growing this generic Skill around one app.
