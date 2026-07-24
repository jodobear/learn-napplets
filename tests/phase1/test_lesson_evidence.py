"""Validate the fixed lesson inventory against canonical Phase 1 evidence."""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / ".planning/research"
PACKET_DIRECTORY = RESEARCH / "lesson-packets"
INDEX_PATH = PACKET_DIRECTORY / "index.yaml"
EXPECTED_INVENTORY = (
    ("LES-001", "01-nostr-client-taken-apart.md"),
    ("LES-002", "02-cast-and-mental-model.md"),
    ("LES-003", "03-nostr-underneath.md"),
    ("LES-004", "04-sandbox-boundary.md"),
    ("LES-005", "05-one-request-across-boundary.md"),
    ("LES-006", "06-capabilities-not-ambient-authority.md"),
    ("LES-007", "07-identity-and-distribution.md"),
    ("LES-008", "08-apps-that-cooperate.md"),
    ("LES-009", "09-designing-a-good-napplet.md"),
    ("LES-010", "10-anatomy-of-a-napplet.md"),
    ("LES-011", "11-build-test-and-publish.md"),
    ("LES-012", "12-inside-a-runtime.md"),
    ("LES-013", "13-evolving-the-protocol.md"),
)
CANONICAL_HEADINGS = (
    "Learner question",
    "Intended outcome",
    "Current terminology",
    "Candidate claims",
    "Implementation and runtime evidence",
    "Drift and open questions",
    "Misconceptions to address",
    "Story representation",
    "System representation",
    "Wire representation",
    "Code representation",
    "Candidate instrument",
    "Required fixtures and tests",
    "Do not teach as settled",
    "Follow-up research",
)
ID_PATTERN = re.compile(r"(?<![A-Z0-9-])(?P<family>CLM|CMP|DRF|OQ)-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
FAMILY_TOKEN_PATTERN = re.compile(r"(?<![A-Z0-9-])(?:CLM|CMP|DRF|OQ)-[^\s`*),.;:]+")
UNSETTLED_STATES = {"disputed", "provisional", "blocked", "stale"}
AUDIT_TARGETS = {
    "CMP": "compatibility-matrix.yaml",
    "DRF": "drift-register.yaml",
    "OQ": "open-questions.yaml",
}
REQUIRED_SOURCE_FIELDS = (
    "officialUrl",
    "ref",
    "commitSha",
    "path",
    "locator",
    "contentSha256",
    "retrievedAt",
    "authorityTier",
    "evidenceClass",
    "maturity",
)


def load_document(filename: str) -> dict[str, Any]:
    return yaml.safe_load((RESEARCH / filename).read_text(encoding="utf-8"))


def records_by_id(filename: str, key: str) -> dict[str, dict[str, Any]]:
    return {record["id"]: record for record in load_document(filename)[key]}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing required section: {heading}")
    return match.group("body")


def record_state(record: dict[str, Any]) -> str:
    return str(record.get("state") or record.get("status") or "")


def record_reason(record: dict[str, Any]) -> str:
    if record.get("stateReason"):
        return str(record["stateReason"])
    if record.get("statusReason"):
        return str(record["statusReason"])
    history = record.get("history") or []
    if history and history[-1].get("reason"):
        return str(history[-1]["reason"])
    return str(record.get("question") or record.get("scope") or "")


class LessonEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = yaml.safe_load(INDEX_PATH.read_text(encoding="utf-8"))
        cls.entries = cls.index["lessons"]
        cls.claims = records_by_id("claims.yaml", "claims")
        cls.sources = records_by_id("source-registry.yaml", "sources")
        cls.compatibility = records_by_id("compatibility-matrix.yaml", "compatibility")
        cls.drift = records_by_id("drift-register.yaml", "drift")
        cls.questions = records_by_id("open-questions.yaml", "questions")
        cls.records = {
            "CLM": cls.claims,
            "CMP": cls.compatibility,
            "DRF": cls.drift,
            "OQ": cls.questions,
        }
        cls.audit = (RESEARCH / "reports/spike-consolidation.md").read_text(encoding="utf-8")

    def packet_paths(self) -> tuple[Path, ...]:
        return tuple(PACKET_DIRECTORY / entry["filename"] for entry in self.entries)

    def test_fixed_thirteen_entry_inventory_is_complete_and_ordered(self) -> None:
        actual = tuple((entry["id"], entry["filename"]) for entry in self.entries)
        self.assertEqual(EXPECTED_INVENTORY, actual)
        self.assertEqual(13, len(self.entries))
        self.assertEqual("complete", self.index["inventoryStatus"])
        self.assertTrue(all(entry["status"] == "present" for entry in self.entries))
        self.assertEqual(13, len({entry["id"] for entry in self.entries}))
        self.assertEqual(13, len({entry["filename"] for entry in self.entries}))

    def test_indexed_packets_exist_once_and_declare_their_indexed_id(self) -> None:
        indexed_names = {entry["filename"] for entry in self.entries}
        packet_names = {path.name for path in PACKET_DIRECTORY.glob("*.md")}
        self.assertEqual(indexed_names, packet_names)
        for entry, path in zip(self.entries, self.packet_paths(), strict=True):
            self.assertTrue(path.is_file(), f"missing indexed packet: {path.name}")
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"**Lesson ID:** {entry['id']}", text)
            for heading in CANONICAL_HEADINGS:
                section(text, heading)

    def test_canonical_collections_and_consolidation_targets_exist(self) -> None:
        self.assertIn("Canonical targets:", self.audit)
        for target in AUDIT_TARGETS.values():
            self.assertIn(target, self.audit)
        for records in self.records.values():
            self.assertTrue(records, "canonical evidence collections are required")
        self.assertTrue(self.sources, "canonical source records are required")

    def test_family_citations_are_well_formed_resolved_and_audit_mapped(self) -> None:
        for packet in self.packet_paths():
            text = packet.read_text(encoding="utf-8")
            citations = list(ID_PATTERN.finditer(text))
            family_tokens = set(FAMILY_TOKEN_PATTERN.findall(text))
            self.assertEqual(
                {citation.group(0) for citation in citations},
                family_tokens,
                f"{packet.name} contains a malformed canonical family ID",
            )
            for citation in citations:
                family = citation.group("family")
                evidence_id = citation.group(0)
                self.assertIn(evidence_id, self.records[family], f"{packet.name} cites unknown {evidence_id}")
                target = AUDIT_TARGETS.get(family)
                if target is not None:
                    self.assertIn(target, self.audit, f"consolidation audit omits target for {evidence_id}")

    def test_claim_citations_transitively_resolve_to_complete_immutable_sources(self) -> None:
        for packet in self.packet_paths():
            text = packet.read_text(encoding="utf-8")
            for claim_id in {match.group(0) for match in ID_PATTERN.finditer(text) if match.group("family") == "CLM"}:
                claim = self.claims[claim_id]
                relations = claim.get("sourceRelations") or []
                self.assertTrue(relations, f"{claim_id} has no source relation")
                for relation in relations:
                    source_id = relation.get("sourceId")
                    self.assertIn(source_id, self.sources, f"{claim_id} has a dangling source relation")
                    source = self.sources[source_id]
                    missing = [field for field in REQUIRED_SOURCE_FIELDS if not source.get(field)]
                    self.assertFalse(missing, f"{source_id} is incomplete for {claim_id}: {missing}")
                    self.assertTrue(source.get("immutableUrl"), f"{source_id} has no immutable source URL")
                    self.assertTrue(relation.get("relation"), f"{claim_id} relation to {source_id} is untyped")
                    self.assertTrue(relation.get("locator"), f"{claim_id} relation to {source_id} has no locator")
                    self.assertTrue(relation.get("excerptSha256"), f"{claim_id} relation to {source_id} has no digest")

    def test_unsettled_citations_are_bounded_in_both_uncertainty_sections(self) -> None:
        for packet in self.packet_paths():
            text = packet.read_text(encoding="utf-8")
            blocked = section(text, "Do not teach as settled")
            follow_up = section(text, "Follow-up research")
            for citation in ID_PATTERN.finditer(text):
                evidence_id = citation.group(0)
                record = self.records[citation.group("family")][evidence_id]
                state = record_state(record)
                if state not in UNSETTLED_STATES:
                    continue
                self.assertTrue(record_reason(record), f"{evidence_id} has no canonical reason")
                self.assertTrue(record.get("impacts") or record.get("scope"), f"{evidence_id} has no canonical impact")
                for required_section in (blocked, follow_up):
                    self.assertIn(evidence_id, required_section, f"{packet.name} omits {evidence_id} from an uncertainty section")
                    self.assertRegex(required_section, rf"{re.escape(evidence_id)}.*?state: {re.escape(state)}")
                    self.assertRegex(required_section, rf"{re.escape(evidence_id)}.*?Reason:")
                    self.assertRegex(required_section, rf"{re.escape(evidence_id)}.*?Impact:")


if __name__ == "__main__":
    unittest.main()
