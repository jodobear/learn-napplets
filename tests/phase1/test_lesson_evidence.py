"""Keep LES-005 through LES-009 tied to post-consolidation canonical evidence."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / ".planning/research"
PACKETS = tuple(
    RESEARCH / "lesson-packets" / filename
    for filename in (
        "05-one-request-across-boundary.md",
        "06-capabilities-not-ambient-authority.md",
        "07-identity-and-distribution.md",
        "08-apps-that-cooperate.md",
        "09-designing-a-good-napplet.md",
    )
)
ID_PATTERN = re.compile(r"(?<![A-Z0-9-])(?P<family>CMP|DRF|OQ)-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
UNSETTLED_STATES = {"disputed", "provisional", "blocked", "stale"}
AUDIT_TARGETS = ("compatibility-matrix.yaml", "drift-register.yaml", "open-questions.yaml")


def load_records(filename: str, key: str) -> dict[str, dict[str, object]]:
    document = yaml.safe_load((RESEARCH / filename).read_text(encoding="utf-8"))
    return {record["id"]: record for record in document[key]}


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError(f"missing required section: {heading}")
    return match.group("body")


class LessonEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compatibility = load_records("compatibility-matrix.yaml", "compatibility")
        cls.drift = load_records("drift-register.yaml", "drift")
        cls.questions = load_records("open-questions.yaml", "questions")
        cls.audit_path = RESEARCH / "reports/spike-consolidation.md"

    def test_canonical_collections_and_consolidation_audit_exist(self) -> None:
        self.assertTrue(self.audit_path.is_file(), "Plan 01-28 consolidation audit is required")
        audit = self.audit_path.read_text(encoding="utf-8")
        self.assertIn("Canonical targets:", audit)
        for target in AUDIT_TARGETS:
            self.assertIn(target, audit)
        self.assertTrue(self.compatibility, "canonical compatibility records are required")
        self.assertTrue(self.drift, "canonical drift records are required")
        self.assertTrue(self.questions, "canonical open-question records are required")

    def test_packet_citations_resolve_to_their_canonical_collection(self) -> None:
        records = {"CMP": self.compatibility, "DRF": self.drift, "OQ": self.questions}
        for packet in PACKETS:
            text = packet.read_text(encoding="utf-8")
            citations = list(ID_PATTERN.finditer(text))
            self.assertTrue(citations, f"{packet.name} must cite canonical evidence IDs")
            malformed = re.findall(r"(?<![A-Z0-9-])(?:CMP|DRF|OQ)-[^\s`*),.;:]+", text)
            self.assertEqual(
                {citation.group(0) for citation in citations},
                set(malformed),
                f"{packet.name} replaces a canonical evidence ID with malformed prose",
            )
            for citation in citations:
                evidence_id = citation.group(0)
                self.assertIn(
                    evidence_id,
                    records[citation.group("family")],
                    f"{packet.name} cites missing canonical evidence {evidence_id}",
                )

    def test_unsettled_citations_are_bounded_in_both_required_sections(self) -> None:
        records = {"CMP": self.compatibility, "DRF": self.drift, "OQ": self.questions}
        for packet in PACKETS:
            text = packet.read_text(encoding="utf-8")
            blocked = section(text, "Do not teach as settled")
            follow_up = section(text, "Follow-up research")
            for citation in ID_PATTERN.finditer(text):
                evidence_id = citation.group(0)
                record = records[citation.group("family")][evidence_id]
                state = record.get("status")
                if state not in UNSETTLED_STATES:
                    continue
                for required_section in (blocked, follow_up):
                    self.assertIn(evidence_id, required_section, f"{packet.name} omits {evidence_id} from an uncertainty section")
                    self.assertRegex(required_section, rf"{re.escape(evidence_id)}.*?state: {re.escape(str(state))}")
                    self.assertRegex(required_section, rf"{re.escape(evidence_id)}.*?Reason:")
                    self.assertRegex(required_section, rf"{re.escape(evidence_id)}.*?Impact:")


if __name__ == "__main__":
    unittest.main()
