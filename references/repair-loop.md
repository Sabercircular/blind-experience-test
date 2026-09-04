# Authorized repair loop

Read this reference only after the user explicitly authorizes product changes.
Testing permission alone is not repair permission.

## Freeze the repair scope

Record:

- the accepted finding or root-cause cluster being repaired;
- the immutable tested revision;
- the isolated successor branch, worktree, or equivalent revision;
- files and behaviors in scope;
- regression evidence required for completion;
- actions still excluded, especially merge, publish, deploy, production data,
  credentials, legal acceptance, and unrelated cleanup.

One repair pass addresses one coherent root cause. If several findings share
the same verified cause, they may travel together. Do not use the authorization
to redesign unrelated experience improvements.

## Make the smallest durable change

Reproduce the accepted finding before editing when the environment still
permits it. Fix the cause rather than only the visible instance.

Add a deterministic regression when the evidence establishes a stable product
contract, such as:

- object count stays unchanged after empty enter/exit;
- committed identity survives the declared lifecycle transition;
- failed work remains recognizable and recoverable;
- retry is idempotent;
- a critical control has a unique accessible name and state.

Do not encode an unresolved product preference as a test. If the finding is
`human_decision`, wait for the user to choose the intended behavior first.

Run the smallest relevant existing test set, the new regression, and any
build/lint checks needed for the changed surface. Preserve unrelated user
changes and do not broaden cleanup for a green check.

## Require a fresh tester

The agent that authored the change cannot certify the experience. Give a fresh
executor only:

- the successor revision and reset route;
- the same persona and core goal;
- the shortest path needed to test the repaired behavior;
- the original surface, plus a narrower native surface only if the claim
  requires it;
- the same information restrictions as the original blind run.

Do not give the tester the patch explanation or expected screen-by-screen
answer. The controller may name the behavior to retest, but the executor must
still observe and report what happens.

Classify the retest as:

- `pass`: the original finding no longer reproduces and the intended journey
  still completes;
- `fail`: the finding remains, changed form, or a regression blocks the
  journey;
- `blocked`: apparatus or isolation cannot prove the result.

## Stop after one pass

Append the repair receipt to `RESULT.md` with the original and successor
revisions, tests, fresh-tester result, and remaining items. Stop after one
bounded repair pass. A failure may be reported with a recommended next step;
it does not automatically authorize another repair cycle.

Never merge, publish, deploy, delete real data, or touch production because a
repair or retest passed. Those actions require their own authorization.
