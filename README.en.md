<sub>🌐 <a href="README.md">中文</a> · <b>English</b></sub>

<div align="center">

# Blind Experience Test

> *“You can never use your own app for the first time. An agent can.”*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-blue)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Hand your app to agents that cannot compare notes. Let them feel their way through it like first-time users, then turn the problems they can reproduce into a product improvement list you can actually act on.**

[Why this exists](#why-this-exists) · [How it tests](#there-are-really-only-three-jobs) · [What comes back](#what-comes-back-is-not-a-test-report) · [Get started](#quick-start)

</div>

## Why this exists

Once you have built an app, you lose the ability to use it for the first time.

You know where the entry point is. You know which loading state is worth waiting for and what Back is supposed to do. However carefully you click through it, you are still proving that the author knows how to use the product. Automated tests have a similar blind spot: they are excellent at protecting expectations you have already written down, but they will not volunteer that a screen is misleading, that nobody knows which button is safe to press, or that going Back quietly creates something behind the scenes.

I wanted a stranger on demand—one that genuinely has to find the entry point, click, make mistakes, go back, retry, and sometimes give up. Then I wanted someone else to cover the important states and reconcile what existed before and after every action. The result should not be “this part feels odd.” It should be a short, reproducible list of things worth changing.

The first time this approach ran against a real Flutter app, it found exactly that kind of problem: a list fell from four items to zero after relaunch; entering and leaving a create screen produced empty objects; and a failed submission remained in detail while the list acted as if nothing existed. These were not pixel bugs. The product's world was changing incorrectly behind the user's back. The anonymized pilot evidence is [here](examples/pilot-upgrade-backlog.md).

## The whole experience should start with one sentence

```text
@blind-experience-test, test this app.
```

The agent reads the project, launch instructions, product notes, and existing tests first. If the repository already answers a question, it does not ask you again.

When it has enough, it should simply begin:

```text
I’ve looked through the project. I’ll start with the new-user journey from
creating something to seeing the first result. I’ll use isolated data and
won’t edit code. If the evidence crosses into native permissions or lifecycle,
I’ll move that part to Simulator. Starting now.
```

When something is genuinely missing, it asks for that one thing:

```text
I still need a test account or reset route that cannot touch production data.
Give me that and I’m ready.
```

No five-question intake. No need to learn about A/B/C arms, subject locks, or oracles before the test can start. The simple rule is: if the agent can find it, it should not bother you with it.

## There are really only three jobs

One round starts with one important journey. It does not launch an all-product, all-platform testing campaign.

1. **Let a stranger genuinely use the app.** It knows who the product is for and what it wants to accomplish. It does not see source, Git history, or known bugs. Wrong turns and abandonment are part of the result.
2. **Walk the critical states through semantic anchors.** Test IDs, Semantics, and ARIA make sure important destinations, primary actions, and empty, loading, success, failure, and recovery states are not missed.
3. **Check what the world became after each action.** Around create, submit, Back, failure, retry, and relaunch, compare object counts, identity, content, and persistence.

The controller freezes the build, chooses the surface, keeps task context separate, and reproduces claims from a clean reset. The other agents can be cheap. What matters is that they do not know one another's answers or share mutable accounts and device state.

These are jobs, not an org chart. Run them in parallel when there are three isolated environments. Run them serially when there is only one Simulator.

## What comes back is not a test report

It is a **product improvement list**.

I do not call it a requirements list because a test can prove what a user encountered and whether it reproduces; it cannot approve roadmap scope for you. Each entry is an evidence-backed candidate that is ready for a decision.

Every example below came from the Flutter pilot:

| Finding | What we saw | What to do next |
| --- | --- | --- |
| **Must fix before release: data continuity** | After creating several items, terminate and relaunch; the list falls from four to zero | Restore objects across relaunch; regress “create → cold launch → count and identity remain stable” |
| **Core problem: ghost objects** | Enter and leave the create screen three times; three empty rows appear on Home | Create after the first meaningful input, or discard an empty draft on exit |
| **Core problem: broken recovery** | A failed submission remains visible in detail, but the list cannot find it and offers no recognizable route to retry | Preserve failed-object identity and expose the same retry route in detail and list views |
| **Core problem: accessibility** | A screen reader and semantic tree cannot tell what the primary submit control does | Give primary actions stable, unique semantic labels |
| **Could feel better: localization** | A Chinese screen shows an English empty state and looks unfinished on first visit | Match empty-state copy to the active language |

The real result puts data loss, broken core tasks, security/privacy issues, and failed recovery first. Friction that does not block completion goes under experience improvements. When two product behaviors are both defensible, the agent shows you the evidence and asks you to decide instead of inventing product truth.

Screenshots, run logs, and object ledgers stay attached as evidence. You should be able to start with this one list.

## Why it usually starts in a browser

Because agents are fastest and cheapest there—but only when the browser is running the same product.

If a Flutter app already has a production Web version and its object creation, identity, storage, and lifecycle have not been swapped out, test the shared journey there first. Move only permission, native plugin, secure-storage, background/foreground, or process-lifecycle evidence to Simulator or Emulator. Save devices for cameras, microphones, push, install/upgrade, and behavior a simulator cannot prove.

“It compiles for Web” is not the same as “Web can prove the native behavior.” Speed is useful. Fidelity is the line that matters.

## Will it edit the code when it is done?

No.

The first round only tests. It returns the product improvement list and asks you what to do next. If you approve a repair, the agent fixes one root-cause cluster on an isolated successor revision, adds the regression that the evidence justifies, and asks a fresh agent—one that did not author the change—to walk the path again.

Permission to repair is not permission to merge, publish, or deploy. Those remain separate decisions.

## Quick start

Copy this directory into your project:

```bash
# Codex
cp -R blind-experience-test .codex/skills/

# Claude Code
cp -R blind-experience-test .claude/skills/
```

Then say:

```text
@blind-experience-test, test this app.
```

Once installed, the controller inspects the project first, asks only for what is genuinely missing, and runs one core journey through three isolated jobs. It switches to the A/B/C benchmark only when you explicitly ask to compare test methods.

## It does not replace the tests you already have

Widget tests, integration tests, XCTest, Maestro, and Playwright protect behavior you already know about. Blind Experience Test finds the behavior you did not know to write an assertion for.

In one line: blind testing discovers; deterministic testing keeps the problem from coming back.

## How this differs from Superpowers testing

[Superpowers](https://github.com/obra/superpowers) asks whether the builder agent followed the right engineering process. Its TDD starts with behavior you already know you want: write a failing test, then the minimum implementation. Its skill-testing method follows the same shape—watch an agent fail without the skill, then use pressure scenarios to see whether the agent holds the rule.

Blind Experience Test does not test the builder agent. It tests the running product. The tester does not know the source, known bugs, expected answer, or another tester's findings. It watches how a first-time user understands the product, where they go wrong, and what actually happens to objects and state after each action.

The shortest distinction is: **Superpowers makes the builder prove it implemented the known thing correctly. Blind Experience Test sends in a stranger to find what you did not know was wrong.**

They fit together naturally: Blind Experience Test discovers an unknown problem; a human chooses the intended product behavior; Superpowers / TDD turns it into a failing regression and implements the fix; then a fresh blind tester verifies the real experience.

## A few lines it will not cross

- The first-time user agent does not see source, known bugs, expected answers, or another agent's findings.
- Tests use isolated accounts, storage, and devices. Mutable environments are not shared between tasks.
- A wrong build, unavailable service, or unfaithful surface is a test-environment problem, not a product bug.
- Deleting real data, accepting terms, entering private credentials, merging, publishing, and deploying all require separate authorization.

## If you want to look inside

```text
blind-experience-test/
├── SKILL.md                 # The agent entry point
├── references/             # Protocol, state oracles, and result format
├── scripts/validate_runs.py
├── examples/               # Synthetic example and anonymized real pilot
├── agents/openai.yaml
└── README.md / README.en.md
```

Validate an existing run file with:

```bash
python3 scripts/validate_runs.py --max-actions 40 \
  --expected-sha 0123456789abcdef0123456789abcdef01234567 \
  examples/state-audit-synthetic.json examples/arm-c-synthetic.json
```

## License

[MIT](LICENSE)
