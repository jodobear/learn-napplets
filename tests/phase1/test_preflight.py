"""Deterministic tests for the Phase 1 execution-convergence preflight."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


VALIDATOR_PATH = Path(__file__).resolve().parents[2] / "tools" / "validate-planning.py"
spec = importlib.util.spec_from_file_location("validate_planning", VALIDATOR_PATH)
validate_planning = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validate_planning)


REVIEW_TEMPLATE = """# Phase 1 Review

## Codex Review
# Fresh Codex Review
Fresh disposition: CONVERGED; HIGH=0; actionable=0

## Current HIGH
None.

## Execution authorization
- Decision: authorized
- Authorized date: 2026-07-24
- Successful reviewer: Codex (`CONVERGED; HIGH=0; actionable=0`)
"""


class Phase1ExecutionPreflightTests(unittest.TestCase):
    def test_failed_expired_or_transport_only_reviewer_lanes_fail(self) -> None:
        review = """# Phase 1 Review

## Review run record
- Codex lane: transport error
- Gemini lane: expired authentication
- Local lane: failed

## Current HIGH
None.

## Execution authorization
- Decision: authorized
- Authorized date: 2026-07-24
"""

        errors = validate_planning.phase1_execution_preflight_errors(review)

        self.assertIn("PRE001: missing successful reviewer response", errors)

    def test_current_high_without_disposition_and_rationale_fails(self) -> None:
        review = REVIEW_TEMPLATE.replace(
            "None.",
            "| Finding | Description |\n| --- | --- |\n| HIGH-001 | Unresolved source provenance |",
        )

        errors = validate_planning.phase1_execution_preflight_errors(review)

        self.assertIn("PRE002: current HIGH finding HIGH-001 lacks disposition with rationale", errors)

    def test_missing_authorized_dated_convergence_decision_fails(self) -> None:
        review = REVIEW_TEMPLATE.replace(
            "- Decision: authorized\n- Authorized date: 2026-07-24\n", "",
        )

        errors = validate_planning.phase1_execution_preflight_errors(review)

        self.assertIn("PRE003: missing authorized dated convergence decision", errors)

    def test_successful_reviewer_complete_disposition_and_authorization_passes(self) -> None:
        review = REVIEW_TEMPLATE.replace(
            "None.",
            "| Finding | Description |\n| --- | --- |\n| HIGH-001 | Unresolved source provenance |\n\n"
            "## Finding Dispositions\n"
            "| Finding | Disposition | Rationale |\n"
            "| --- | --- | --- |\n"
            "| HIGH-001 | addressed | Immutable source record was added. |",
        )

        self.assertEqual(validate_planning.phase1_execution_preflight_errors(review), [])


if __name__ == "__main__":
    unittest.main()
