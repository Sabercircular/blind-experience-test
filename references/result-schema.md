# Result contracts

Use one run directory. Raw executor files are immutable evidence; the
controller's final disposition belongs in `RESULT.md`.

```text
subject-lock.json
apparatus.json
runs/
evidence/
RESULT.md
```

## Subject lock

Create `subject-lock.json` before build or launch. Include:

- `locked_at` and a stable lock digest;
- source revision or non-Git artifact identity;
- production entrypoint and expected runtime identity;
- the one frozen journey: name, persona, goal, start state, and success
  evidence;
- expected state-changing bindings;
- required runtime capabilities;
- isolated data namespace and reset route;
- visible-action and elapsed-time budgets.

Expected identity must be declared before the observed runtime evidence is
collected.

## Apparatus receipt

Create `apparatus.json` after launch from a separate controller action. Include:

- observed source revision and artifact digest;
- executable/runtime identity, surface, and context;
- observed production entrypoint and state-changing bindings;
- required capabilities with evidence references;
- reset receipt and isolated namespace;
- `disposition`: `score`, `excluded`, or `apparatus_blocked`;
- `findings_allowed`: `true` only for `score`;
- reasons for every mismatch or blocker.

Compare source identity and bindings before capabilities. An artifact digest
supports identity but is not sufficient by itself. Wrong identity or bindings
are `excluded`; missing capability on the correct subject is
`apparatus_blocked` with `findings_allowed=false`.

## Default role run

Each file under `runs/` is one executor JSON document. New product-round runs
use exactly one `role`:

- `user_simulation`
- `semantic_coverage`
- `state_audit`
- `native_confirmation`

Common required fields:

- `run_id`: unique non-empty string;
- `role`;
- `seed`;
- `subject_sha`: full lowercase Git SHA, or a non-empty `artifact_digest`;
- `surface`: exact runtime such as `production_web`, `ios_simulator`,
  `android_emulator`, or `ios_device`;
- `surface_fidelity`: executor receipt naming the production entrypoint and
  any replaced boundary; controller evidence remains authoritative;
- `persona`, `goal`;
- `completion`: `success`, `blocked`, or `gave_up`;
- `steps`: ordered objects with `index`, `observation`, `action`, and `result`;
- `findings`: candidate finding objects;
- `unknowns`;
- `action_count`: visible steps only;
- `elapsed_time_ms`;
- `environment_blockers`;
- `reset_receipt`;
- `evidence_refs`.

A lifecycle step adds `"kind": "lifecycle"` and does not count toward
`action_count`.

Each candidate finding contains:

- `title`
- `claim`
- `visible_evidence`
- `impact`
- `severity`
- `confidence`
- `inference`
- `reproduction_steps`
- `claim_scope`: `shared`, `platform_candidate`, or `platform_specific`

JSON validity does not accept a finding. Acceptance requires apparatus checks
and clean-reset controller reproduction.

### Role-specific fields

- `semantic_coverage` requires `coverage`, a list of rows with an anchor/state,
  `status` (`covered`, `unobserved`, or `blocked`), and step/evidence
  references.
- `state_audit` requires non-empty `object_ledgers` and
  `lifecycle_action_count`, which must equal the number of lifecycle steps.
- `native_confirmation` requires a non-empty `confirmation_target` naming the
  narrow claim being checked.

`user_simulation` has no extra required field. It should not receive coverage
or state-audit prompts merely to make its JSON look complete.

## Legacy A/B/C run

The validator remains backward compatible with files using `arm: A|B|C`
instead of `role`. A run must contain exactly one selector: `role` or `arm`.

Legacy B and C require `coverage`; C also requires non-empty
`object_ledgers` and a matching `lifecycle_action_count`. Historical artifacts
that predate surface routing may use `--allow-legacy-surface`; never use that
flag for new runs.

## RESULT.md

`RESULT.md` is the only primary artifact. Write for the product owner, not the
test harness. Use this compact shape:

```markdown
# Blind Experience Test — <product / journey>

## Recommendation
<One paragraph: release, fix first, or needs a human decision.>

## What was tested
- Subject: <revision / artifact>
- Journey: <one core journey>
- Surfaces: <where the evidence applies>
- Executors: <completed / blocked tasks>

## Product improvement list
| Class | User scenario | Reproduced evidence | Impact | Suggested change | Regression entry | Confidence / scope |
|---|---|---|---|---|---|---|

## Testability and apparatus gaps
<Wrong builds, missing capabilities, unreachable states, or tool failures.>

## Coverage and limits
<What was covered, what was not, budgets, and unresolved product decisions.>

## Evidence
<Links to immutable runs, screenshots, ledgers, and controller reproduction.>
```

Use one of four product classes:

- `release_blocker`: core task failure, data loss/corruption, security/privacy,
  identity/payment failure, or no recovery from a common failure;
- `core_fix`: the journey may complete, but state, lifecycle, recovery, or a
  critical action clearly violates the product promise;
- `experience_improvement`: the user can complete the journey, but entry,
  steps, feedback, language, accessibility, or layout should improve;
- `human_decision`: more than one product behavior may be valid.

Do not put wrong builds, missing accounts, unfaithful surfaces, permission
setup, or tool failures into the product improvement list. Put them under
testability and apparatus gaps.

Every product row states the user scenario, controller-reproduced evidence,
impact, suggested change, deterministic regression entry when justified,
confidence, and surface scope. Suggestions are not approved requirements.

## Repair receipt

If the user authorizes repair, append a short section to the same `RESULT.md`:

```markdown
## Repair and retest
- Authorized scope: <root-cause cluster>
- Tested revision: <immutable original>
- Successor revision: <changed revision>
- Regression added: <test or reason none was added>
- Fresh-tester result: pass / fail / blocked
- Remaining items: <not changed>
```

Do not overwrite the original finding, evidence, or tested revision after a
repair passes.
