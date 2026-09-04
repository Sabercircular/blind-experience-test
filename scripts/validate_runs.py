#!/usr/bin/env python3
"""Validate blind-experience-test executor JSON without judging findings."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
VALID_ARMS = {"A", "B", "C"}
VALID_ROLES = {
    "user_simulation",
    "semantic_coverage",
    "state_audit",
    "native_confirmation",
}
VALID_COMPLETIONS = {"success", "blocked", "gave_up"}
VALID_CLAIM_SCOPES = {"shared", "platform_candidate", "platform_specific"}
VALID_COVERAGE_STATUSES = {"covered", "unobserved", "blocked"}
VALID_LEGACY_COVERAGE_STATUSES = VALID_COVERAGE_STATUSES | {"partial", "not_reached"}

LEGACY_COMMON_FIELDS = {
    "arm",
    "seed",
    "surface",
    "surface_fidelity",
    "persona",
    "goal",
    "completion",
    "steps",
    "findings",
    "unknowns",
    "action_count",
}
ROLE_COMMON_FIELDS = {
    "run_id",
    "role",
    "seed",
    "surface",
    "surface_fidelity",
    "persona",
    "goal",
    "completion",
    "steps",
    "findings",
    "unknowns",
    "action_count",
    "elapsed_time_ms",
    "environment_blockers",
    "reset_receipt",
    "evidence_refs",
}
FINDING_FIELDS = {
    "title",
    "claim",
    "visible_evidence",
    "impact",
    "severity",
    "confidence",
    "inference",
    "reproduction_steps",
    "claim_scope",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_receipt(value: object) -> bool:
    return nonempty_string(value) or (isinstance(value, dict) and bool(value))


def validate_coverage(
    coverage: object,
    label: str,
    errors: list[str],
    *,
    legacy: bool,
) -> None:
    require(isinstance(coverage, list), f"{label} requires coverage", errors)
    if not isinstance(coverage, list):
        return
    for position, row in enumerate(coverage, 1):
        require(isinstance(row, dict), f"coverage {position} must be an object", errors)
        if not isinstance(row, dict):
            continue
        statuses = VALID_LEGACY_COVERAGE_STATUSES if legacy else VALID_COVERAGE_STATUSES
        require(
            row.get("status") in statuses,
            f"coverage {position} has invalid status",
            errors,
        )
        require(
            nonempty_string(row.get("item"))
            or nonempty_string(row.get("anchor"))
            or nonempty_string(row.get("state"))
            or (legacy and isinstance(row.get("rule"), int)),
            f"coverage {position} needs item, anchor, state or legacy rule",
            errors,
        )


def validate(
    path: Path,
    expected_sha: str | None,
    max_actions: int | None,
    allow_legacy_surface: bool,
) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read JSON: {exc}"]

    require(isinstance(data, dict), "top level must be an object", errors)
    if not isinstance(data, dict):
        return errors

    has_arm = "arm" in data
    has_role = "role" in data
    require(has_arm != has_role, "provide exactly one selector: role or arm", errors)

    role = data.get("role") if has_role else None
    arm = data.get("arm") if has_arm else None
    if has_role:
        require(role in VALID_ROLES, "invalid role", errors)
        common_fields = set(ROLE_COMMON_FIELDS)
        if allow_legacy_surface:
            errors.append("--allow-legacy-surface applies only to legacy arm runs")
    elif has_arm:
        require(arm in VALID_ARMS, "arm must be A, B or C", errors)
        common_fields = set(LEGACY_COMMON_FIELDS)
        if allow_legacy_surface:
            common_fields -= {"surface", "surface_fidelity"}
    else:
        common_fields = set()

    missing = sorted(common_fields - data.keys())
    require(not missing, f"missing fields: {', '.join(missing)}", errors)

    sha = data.get("subject_sha")
    digest = data.get("artifact_digest")
    valid_sha = isinstance(sha, str) and SHA_RE.fullmatch(sha) is not None
    valid_digest = nonempty_string(digest)
    require(
        valid_sha or valid_digest,
        "provide a full lowercase subject_sha or artifact_digest",
        errors,
    )
    if expected_sha is not None:
        require(valid_sha, "--expected-sha requires subject_sha", errors)
        require(sha == expected_sha, f"subject_sha differs from {expected_sha}", errors)

    require(data.get("completion") in VALID_COMPLETIONS, "invalid completion", errors)
    require(nonempty_string(data.get("persona")), "persona must be non-empty", errors)
    require(nonempty_string(data.get("goal")), "goal must be non-empty", errors)
    require(isinstance(data.get("unknowns"), list), "unknowns must be a list", errors)

    if "surface" in data:
        require(nonempty_string(data.get("surface")), "surface must be non-empty", errors)
    if "surface_fidelity" in data:
        require(
            nonempty_string(data.get("surface_fidelity")),
            "surface_fidelity must be non-empty",
            errors,
        )

    if has_role:
        require(nonempty_string(data.get("run_id")), "run_id must be non-empty", errors)
        elapsed = data.get("elapsed_time_ms")
        require(
            isinstance(elapsed, int) and elapsed >= 0,
            "elapsed_time_ms must be a non-negative integer",
            errors,
        )
        require(
            isinstance(data.get("environment_blockers"), list),
            "environment_blockers must be a list",
            errors,
        )
        require(
            nonempty_receipt(data.get("reset_receipt")),
            "reset_receipt must be a non-empty string or object",
            errors,
        )
        require(
            isinstance(data.get("evidence_refs"), list),
            "evidence_refs must be a list",
            errors,
        )

    steps = data.get("steps")
    require(isinstance(steps, list) and bool(steps), "steps must be a non-empty list", errors)
    visible_steps: list[dict] = []
    lifecycle_steps: list[dict] = []
    if isinstance(steps, list):
        for position, step in enumerate(steps, 1):
            require(isinstance(step, dict), f"step {position} must be an object", errors)
            if not isinstance(step, dict):
                continue
            require(
                step.get("index") == position,
                f"step {position} has non-sequential index",
                errors,
            )
            missing_step = {"observation", "action", "result"} - step.keys()
            require(
                not missing_step,
                f"step {position} missing {', '.join(sorted(missing_step))}",
                errors,
            )
            if step.get("kind") == "lifecycle":
                lifecycle_steps.append(step)
            else:
                visible_steps.append(step)

    action_count = data.get("action_count")
    require(
        isinstance(action_count, int) and action_count >= 0,
        "action_count must be a non-negative integer",
        errors,
    )
    if isinstance(action_count, int):
        require(
            action_count == len(visible_steps),
            f"action_count={action_count}, visible steps={len(visible_steps)}",
            errors,
        )
        if max_actions is not None:
            require(
                action_count <= max_actions,
                f"action_count exceeds shared limit {max_actions}",
                errors,
            )

    findings = data.get("findings")
    require(isinstance(findings, list), "findings must be a list", errors)
    if isinstance(findings, list):
        for position, finding in enumerate(findings, 1):
            require(isinstance(finding, dict), f"finding {position} must be an object", errors)
            if not isinstance(finding, dict):
                continue
            finding_fields = set(FINDING_FIELDS)
            if allow_legacy_surface and has_arm:
                finding_fields.discard("claim_scope")
            missing_finding = sorted(finding_fields - finding.keys())
            require(
                not missing_finding,
                f"finding {position} missing {', '.join(missing_finding)}",
                errors,
            )
            if "claim_scope" in finding:
                require(
                    finding.get("claim_scope") in VALID_CLAIM_SCOPES,
                    f"finding {position} has invalid claim_scope",
                    errors,
                )

    needs_coverage = arm in {"B", "C"} or role == "semantic_coverage"
    if needs_coverage:
        validate_coverage(
            data.get("coverage"),
            str(role or f"arm {arm}"),
            errors,
            legacy=has_arm,
        )

    needs_state_audit = arm == "C" or role == "state_audit"
    if needs_state_audit:
        require(
            isinstance(data.get("object_ledgers"), list)
            and bool(data.get("object_ledgers")),
            f"{role or 'arm C'} requires non-empty object_ledgers",
            errors,
        )
        lifecycle_count = data.get("lifecycle_action_count")
        require(
            isinstance(lifecycle_count, int)
            and lifecycle_count == len(lifecycle_steps),
            "lifecycle_action_count must match lifecycle steps",
            errors,
        )

    if role == "native_confirmation":
        require(
            nonempty_string(data.get("confirmation_target")),
            "native_confirmation requires confirmation_target",
            errors,
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate product-round role runs and legacy A/B/C runs."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--expected-sha")
    parser.add_argument(
        "--max-actions",
        type=int,
        help="visible-action cap for every supplied run",
    )
    parser.add_argument(
        "--allow-legacy-surface",
        action="store_true",
        help="accept registered historical arm runs without surface metadata",
    )
    args = parser.parse_args()

    if args.max_actions is not None and args.max_actions < 0:
        parser.error("--max-actions must be non-negative")

    failed = False
    for path in args.paths:
        errors = validate(
            path,
            args.expected_sha,
            args.max_actions,
            args.allow_legacy_surface,
        )
        if errors:
            failed = True
            for error in errors:
                print(f"FAIL {path}: {error}", file=sys.stderr)
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
