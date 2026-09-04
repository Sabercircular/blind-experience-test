# Product round and benchmark protocol

Use this reference when the controller is ready to dispatch executor tasks.
The default is one product round. Use the benchmark appendix only when the
user explicitly asks to compare discovery methods or measure defect recall.

## Shared executor envelope

Every task names:

- one exact subject revision or artifact and production entrypoint;
- one runtime surface/context and a controller-confirmed reset receipt;
- one persona, one goal, and the same frozen core journey;
- a maximum visible-action budget and elapsed-time budget;
- one output path inside `runs/` and allowed evidence paths;
- actions that are forbidden or need separate authorization.

Executors may observe the product surface and its accessibility tree. They may
not read source, Git history, later versions, known bugs, controller findings,
another executor's run, hidden ground truth, private credentials, or backend
state. They observe fresh UI/AX after each action and label inference as
inference.

Use a fresh executor context and clean mutable state for every task. If
accounts, namespaces, storage, browser contexts, Simulators, or devices cannot
be isolated, run serially and reset between tasks. If a fresh executor context
itself is unavailable, the controller must not call the result blind.

## Default product round

### 1. First-time user (`user_simulation`)

Give the executor only the product promise, persona, goal, launch route,
surface, budget, and safety limits. Do not provide a checklist or semantic
inventory.

Ask it to:

- find the entry point without coaching;
- pursue first value naturally;
- record each observation, chosen action, and visible result;
- make ordinary mistakes, use visible recovery, go Back, retry, or give up as
  the persona would;
- report candidate confusion, friction, task breaks, and side effects without
  guessing hidden causes;
- stop at success, a believable give-up point, budget, or blocker.

The controller should learn what an unbriefed user notices, not whether the
executor can satisfy a test script.

### 2. Semantic coverage (`semantic_coverage`)

Give this executor the same journey plus the stable semantic inventory: Test
IDs, Semantics, ARIA roles/names, accessibility tree, or other user-facing
anchors. Do not give it known bugs or the first executor's discoveries.

Cover only states reachable within the frozen journey:

- each primary destination and action;
- empty and minimal-valid input;
- loading/pending and stable success;
- visible failure and available recovery;
- Back/cancel and resume;
- keyboard, focus, accessible name, live status, and blocked controls when
  relevant.

Emit one `coverage` row per assigned anchor or state. Use `covered` with step
or evidence references, `unobserved` when the state was not reachable, and
`blocked` when the environment prevented the check. Coverage is not proof
that the experience is good; it is proof of what was and was not exercised.

### 3. State and side-effect audit (`state_audit`)

Give this executor the same journey plus generic transition questions. Do not
name a suspected product defect.

For every selected create/open/new, submit, retry, cancel, Back/resume, or
asynchronous action:

1. record related visible object count, labels, identity clues, and current
   status before the action;
2. perform the action once and wait for an explicit stable state;
3. record the same ledger after the action;
4. repeat an empty or minimal transition only when it can reveal idempotency,
   draft, duplicate, or residue behavior;
5. leave and resume to check whether the same object is recognizable;
6. perform the controller-declared lifecycle transition only when continuity
   is part of the journey, then compare the ledger again.

Browser reload, fresh browser context, native background/foreground, process
terminate/relaunch, app reinstall, and device reboot are different lifecycle
actions. Record the exact one used. UI-only evidence does not prove hidden
storage or API behavior.

The product's own draft/commit semantics remain authoritative. A new empty
object is not automatically a defect; the executor records the transition and
the controller decides whether it violates the product promise.

## Conditional native confirmation (`native_confirmation`)

Dispatch this task only after a candidate finding depends on a capability the
current surface cannot prove. Name one `confirmation_target`, the narrower
native path, and the evidence needed to confirm or reject it. Do not replay the
whole product round.

Typical triggers include native authentication, secure storage, plugins,
microphone/audio, keyboard/safe areas, VoiceOver/TalkBack, OS lifecycle,
push/background execution, packaging, install/upgrade, or hardware behavior.

## Controller handoff

After every executor has stopped:

1. preserve its raw run without rewriting observations;
2. validate the file with `scripts/validate_runs.py`;
3. compare the controller apparatus receipt with the subject lock;
4. reproduce candidate findings from a clean reset on the cheapest surface
   that can prove each claim;
5. exclude wrong-subject, apparatus-blocked, intermediate-frame, duplicate,
   and unsupported claims;
6. write the accepted product items, testability gaps, coverage, and limits to
   one `RESULT.md`.

## A/B/C benchmark appendix

Use this mode only for an explicit method-comparison or added-recall question.
Keep subject, surface, reset, persona, goal, maximum visible actions,
wall-clock budget, model, and effort comparable. Report actual actions and
elapsed time; invalid apparatus runs do not enter the metrics.

- **A — semantic exploration:** product promise plus persona and goal only.
- **B — interaction grammar:** A plus empty, minimal, repeat, Back/resume,
  recovery, stability, and accessibility prompts.
- **C — state and side-effect grammar:** B plus pre/post object ledgers,
  create/open/new transitions, lifecycle comparison, and identity-context
  questions.

Run one seed per arm as a canary. Replicate with at least three independent
seeds only after the canary shows a useful, reproducible difference. Stop
scaling when C adds no accepted recall or adds only noise and cost.

The controller chooses repeat count and lifecycle transitions for the product.
Three total empty cycles and one cold relaunch are useful canary defaults, not
universal requirements. Keep the hidden fault set outside executor-visible
files until all runs are complete.
