#!/usr/bin/env python3
"""Build the dependency-free Learn Napplets static learning site from one JSON record."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTENT = ROOT / "site" / "content" / "site.json"
DEFAULT_TEMPLATE = ROOT / "site" / "templates" / "page.html"
DEFAULT_STYLES = ROOT / "site" / "assets" / "styles.css"
DEFAULT_SCRIPT = ROOT / "site" / "assets" / "site.js"
DEFAULT_OUTPUT = ROOT / "site" / "dist"
PAGE_ORDER = ("home", "learn", "architecture", "sources")
REQUIRED_STATUS_FIELDS = (
    "authorityTier",
    "evidenceClass",
    "maturity",
    "state",
    "uncertainty",
    "uncertaintyReason",
    "refreshTrigger",
)
SAFE_URL = re.compile(r"^https://github\.com/[A-Za-z0-9._/-]+$")


class ContentError(ValueError):
    """A deterministic content-contract validation error."""


def fail(message: str) -> None:
    raise ContentError(message)


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def identifiers(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        fail(f"{label} must be an array of non-empty IDs")
    return value


def reject_markup(value: Any, label: str = "content") -> None:
    if isinstance(value, str):
        if "<" in value or ">" in value:
            fail(f"unsafe markup in {label}")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_markup(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_markup(item, f"{label}[{index}]")


def validate_status(record: dict[str, Any], label: str) -> None:
    for field in REQUIRED_STATUS_FIELDS:
        text(record.get(field), f"{label}.{field}")


def validate_content(content: dict[str, Any]) -> None:
    if content.get("schemaVersion") != 1:
        fail("schemaVersion must equal 1")
    reject_markup(content)
    site = mapping(content.get("site"), "site")
    for field in ("title", "strapline", "edition", "scopeNote"):
        text(site.get(field), f"site.{field}")

    sources = mapping(content.get("sources"), "sources")
    facts = mapping(content.get("facts"), "facts")
    terms = mapping(content.get("terms"), "terms")
    relationships = mapping(content.get("relationships"), "relationships")
    blockers = mapping(content.get("blockers"), "blockers")
    pages = mapping(content.get("pages"), "pages")

    for source_id, source_value in sources.items():
        source = mapping(source_value, f"sources.{source_id}")
        if source_id != text(source.get("id"), f"sources.{source_id}.id"):
            fail(f"source key and ID disagree: {source_id}")
        for field in ("label", "sourceIdentity", "digest", "retrievedAt"):
            text(source.get(field), f"sources.{source_id}.{field}")
        url = text(source.get("immutableUrl"), f"sources.{source_id}.immutableUrl")
        if not SAFE_URL.fullmatch(url):
            fail(f"sources.{source_id}.immutableUrl must be a GitHub immutable URL")
        validate_status(source, f"sources.{source_id}")

    for fact_id, fact_value in facts.items():
        fact = mapping(fact_value, f"facts.{fact_id}")
        if fact_id != text(fact.get("id"), f"facts.{fact_id}.id"):
            fail(f"fact key and ID disagree: {fact_id}")
        text(fact.get("label"), f"facts.{fact_id}.label")
        text(fact.get("statement"), f"facts.{fact_id}.statement")
        validate_status(fact, f"facts.{fact_id}")
        for source_id in identifiers(fact.get("sourceIds"), f"facts.{fact_id}.sourceIds"):
            if source_id not in sources:
                fail(f"facts.{fact_id} references unknown source ID {source_id}")

    for term_id, term_value in terms.items():
        term = mapping(term_value, f"terms.{term_id}")
        if term_id != text(term.get("id"), f"terms.{term_id}.id"):
            fail(f"term key and ID disagree: {term_id}")
        for field in ("label", "classification", "state", "definition"):
            text(term.get(field), f"terms.{term_id}.{field}")
        for source_id in identifiers(term.get("sourceIds"), f"terms.{term_id}.sourceIds"):
            if source_id not in sources:
                fail(f"terms.{term_id} references unknown source ID {source_id}")

    for relationship_id, relationship_value in relationships.items():
        relationship = mapping(relationship_value, f"relationships.{relationship_id}")
        if relationship_id != text(relationship.get("id"), f"relationships.{relationship_id}.id"):
            fail(f"relationship key and ID disagree: {relationship_id}")
        for field in ("label", "classification", "state", "transcript", "refreshTrigger"):
            text(relationship.get(field), f"relationships.{relationship_id}.{field}")
        for source_id in identifiers(relationship.get("sourceIds"), f"relationships.{relationship_id}.sourceIds"):
            if source_id not in sources:
                fail(f"relationships.{relationship_id} references unknown source ID {source_id}")
        steps = relationship.get("steps")
        if not isinstance(steps, list) or not steps:
            fail(f"relationships.{relationship_id}.steps must be a non-empty array")
        for index, step in enumerate(steps):
            step_map = mapping(step, f"relationships.{relationship_id}.steps[{index}]")
            for field in ("id", "actor", "action"):
                text(step_map.get(field), f"relationships.{relationship_id}.steps[{index}].{field}")

    for blocker_id, blocker_value in blockers.items():
        blocker = mapping(blocker_value, f"blockers.{blocker_id}")
        if blocker_id != text(blocker.get("id"), f"blockers.{blocker_id}.id"):
            fail(f"blocker key and ID disagree: {blocker_id}")
        for field in ("label", "state", "statement"):
            text(blocker.get(field), f"blockers.{blocker_id}.{field}")
        if blocker.get("state") != "blocked":
            fail(f"blockers.{blocker_id}.state must be blocked")
        for source_id in identifiers(blocker.get("sourceIds"), f"blockers.{blocker_id}.sourceIds"):
            if source_id not in sources:
                fail(f"blockers.{blocker_id} references unknown source ID {source_id}")

    if set(pages) != set(PAGE_ORDER):
        fail("pages must contain exactly home, learn, architecture, and sources")
    expected_routes = {
        "home": "index.html",
        "learn": "learn/index.html",
        "architecture": "architecture/index.html",
        "sources": "sources/index.html",
    }
    for page_key in PAGE_ORDER:
        page = mapping(pages[page_key], f"pages.{page_key}")
        for field in ("id", "route", "title", "eyebrow", "lead"):
            text(page.get(field), f"pages.{page_key}.{field}")
        if page["route"] != expected_routes[page_key]:
            fail(f"pages.{page_key}.route must be {expected_routes[page_key]}")
        safe_route(page["route"])
        for collection, valid_ids, noun in (
            ("factIds", facts, "fact"),
            ("termIds", terms, "term"),
            ("blockerIds", blockers, "blocker"),
            ("relationshipIds", relationships, "relationship"),
        ):
            for item_id in identifiers(page.get(collection), f"pages.{page_key}.{collection}"):
                if item_id not in valid_ids:
                    fail(f"pages.{page_key} references unknown {noun} ID {item_id}")


def safe_route(route: str) -> PurePosixPath:
    candidate = PurePosixPath(route)
    if candidate.is_absolute() or ".." in candidate.parts or route.startswith("/"):
        fail(f"unsafe output path {route}")
    if candidate.suffix != ".html":
        fail(f"output path must be HTML: {route}")
    return candidate


def escaped(value: Any) -> str:
    return html.escape(str(value), quote=True)


def route_link(from_route: str, to_route: str) -> str:
    start = PurePosixPath(from_route).parent
    relative = os.path.relpath(to_route, start.as_posix() or ".")
    return relative.replace(os.sep, "/")


def source_links(source_ids: list[str], route: str) -> str:
    return ", ".join(
        f'<a href="{escaped(route_link(route, "sources/index.html"))}#source-{escaped(source_id)}">{escaped(source_id)}</a>'
        for source_id in source_ids
    ) or "No pinned source record"


def render_status(record: dict[str, Any], route: str) -> str:
    fields = (
        ("Authority tier", record["authorityTier"]),
        ("Evidence class", record["evidenceClass"]),
        ("Maturity", record["maturity"]),
        ("Claim/record state", record["state"]),
        ("Uncertainty", record["uncertainty"]),
        ("Source identity", source_links(record["sourceIds"], route)),
        ("Refresh trigger", record["refreshTrigger"]),
    )
    rows = []
    for label, value in fields:
        rendered = value if label == "Source identity" else escaped(value)
        rows.append(f"<dt>{escaped(label)}</dt><dd>{rendered}</dd>")
    return '<dl class="status-grid">' + "".join(rows) + "</dl>"


def render_fact(fact: dict[str, Any], route: str) -> str:
    return (
        f'<article class="fact-record state-{escaped(fact["state"])}" id="fact-{escaped(fact["id"])}">'
        f'<p class="record-id">{escaped(fact["id"])}</p>'
        f'<h3>{escaped(fact["label"])}</h3>'
        f'<p>{escaped(fact["statement"])}</p>'
        f'{render_status(fact, route)}'
        f'</article>'
    )


def render_term(term: dict[str, Any], route: str) -> str:
    return (
        f'<article class="term-record state-{escaped(term["state"])}" id="term-{escaped(term["id"])}">'
        f'<p class="record-id">{escaped(term["id"])}</p>'
        f'<h3>{escaped(term["label"])}</h3>'
        f'<p><strong>{escaped(term["classification"])}</strong> · {escaped(term["state"])}</p>'
        f'<p>{escaped(term["definition"])}</p>'
        f'<p class="source-line">Source identity: {source_links(term["sourceIds"], route)}</p>'
        f'</article>'
    )


def render_blocker(blocker: dict[str, Any], route: str) -> str:
    return (
        f'<article class="blocker-record" id="blocker-{escaped(blocker["id"])}">'
        f'<p class="record-id">{escaped(blocker["id"])}</p>'
        f'<h3>{escaped(blocker["label"])}</h3>'
        f'<p><strong>blocked</strong> — {escaped(blocker["statement"])}</p>'
        f'<p class="source-line">Source identity: {source_links(blocker["sourceIds"], route)}</p>'
        f'</article>'
    )


def render_relationship(relationship: dict[str, Any], page_key: str) -> str:
    steps = relationship["steps"]
    ordered_steps = "".join(
        f'<li id="{escaped(step["id"])}"><strong>{escaped(step["actor"])}</strong><span>{escaped(step["action"])}</span></li>'
        for step in steps
    )
    if page_key == "architecture":
        table_rows = "".join(
            f'<tr><th scope="row">{escaped(step["id"])}</th><td>{escaped(step["actor"])}</td><td>{escaped(step["action"])}</td></tr>'
            for step in steps
        )
        return (
            f'<section class="relationship architecture-model" id="relationship-{escaped(relationship["id"])}">'
            f'<p class="record-id">{escaped(relationship["id"])}</p>'
            f'<h2 id="architecture-title">{escaped(relationship["label"])}</h2>'
            f'<p class="model-label">{escaped(relationship["classification"])} · {escaped(relationship["state"])}</p>'
            '<figure class="authority-diagram" aria-labelledby="architecture-title">'
            '<div class="diagram-visual" aria-hidden="true"><span>note</span><span>guest request</span><span>host policy</span><span>bounded result</span></div>'
            '<figcaption>Request → mediated capability → result. The visual repeats the ordered text model below; it carries no unique meaning.</figcaption>'
            '</figure>'
            '<h3>Ordered request/result steps</h3>'
            f'<ol class="relationship-steps">{ordered_steps}</ol>'
            '<details class="transcript" open><summary>Read the static transcript</summary>'
            f'<p id="architecture-transcript">{escaped(relationship["transcript"])}</p></details>'
            '<div class="table-wrap"><table><caption>Static comparison table</caption><thead><tr><th>Step</th><th>Actor</th><th>Bounded action</th></tr></thead>'
            f'<tbody>{table_rows}</tbody></table></div>'
            f'<p class="source-line">Source identity: {source_links(relationship["sourceIds"], "architecture/index.html")}</p>'
            f'<p class="refresh-line">Refresh trigger: {escaped(relationship["refreshTrigger"])}</p>'
            '</section>'
        )
    return (
        f'<section class="relationship" id="relationship-{escaped(relationship["id"])}">'
        f'<p class="record-id">{escaped(relationship["id"])}</p><h2>{escaped(relationship["label"])}</h2>'
        f'<ol class="relationship-steps">{ordered_steps}</ol></section>'
    )


def render_sources(content: dict[str, Any], route: str) -> str:
    records = []
    for source_id, source in content["sources"].items():
        fields = (
            ("Authority tier", source["authorityTier"]),
            ("Evidence class", source["evidenceClass"]),
            ("Maturity", source["maturity"]),
            ("Claim/record state", source["state"]),
            ("Uncertainty", source["uncertainty"]),
            ("Source identity", source["sourceIdentity"]),
            ("Digest", source["digest"]),
            ("Retrieved", source["retrievedAt"]),
            ("Refresh trigger", source["refreshTrigger"]),
        )
        metadata = "".join(f"<dt>{escaped(label)}</dt><dd>{escaped(value)}</dd>" for label, value in fields)
        records.append(
            f'<article class="source-record state-{escaped(source["state"])}" id="source-{escaped(source_id)}">'
            f'<p class="record-id">{escaped(source_id)}</p><h2>{escaped(source["label"])}</h2>'
            f'<p><a href="{escaped(source["immutableUrl"])}" rel="noreferrer">Open immutable source identity</a></p>'
            f'<dl class="status-grid">{metadata}</dl>'
            f'<p class="uncertainty-line">Uncertainty detail: {escaped(source["uncertaintyReason"])}</p></article>'
        )
    return '<section class="source-ledger" aria-label="Immutable source ledger">' + "".join(records) + "</section>"


def render_page(content: dict[str, Any], page_key: str, template: str) -> tuple[str, str]:
    page = content["pages"][page_key]
    route = page["route"]
    nav_items = []
    for candidate in PAGE_ORDER:
        target = content["pages"][candidate]
        current = ' aria-current="page"' if candidate == page_key else ""
        nav_items.append(
            f'<li><a href="{escaped(route_link(route, target["route"]))}"{current}>{escaped(candidate.title())}</a></li>'
        )
    fact_html = "".join(render_fact(content["facts"][item], route) for item in page["factIds"])
    term_html = "".join(render_term(content["terms"][item], route) for item in page["termIds"])
    blocker_html = "".join(render_blocker(content["blockers"][item], route) for item in page["blockerIds"])
    relationship_html = "".join(render_relationship(content["relationships"][item], page_key) for item in page["relationshipIds"])

    actions = ""
    if page_key == "home":
        actions = (
            '<p class="path-actions"><a class="action-link" href="learn/">Begin the reading path</a>'
            '<a class="action-link" href="sources/">Inspect the source ledger</a></p>'
        )
    if page_key == "learn":
        actions = '<p class="path-actions"><a class="action-link" href="../architecture/">Continue to the authority model</a></p>'
    if page_key == "architecture":
        actions = '<p class="path-actions"><a class="action-link" href="../sources/">Inspect the evidence limits</a></p>'
    sources_html = render_sources(content, route) if page_key == "sources" else ""

    body = (
        '<article class="page-shell">'
        f'<header class="page-intro"><p class="eyebrow">{escaped(page["eyebrow"])}</p>'
        f'<h1>{escaped(page["title"])}</h1><p class="lede">{escaped(page["lead"])}</p>{actions}</header>'
        f'{relationship_html}'
        f'<section class="facts" aria-label="Evidence-labeled statements"><h2>What this page can say</h2>{fact_html}</section>'
        f'<section class="terms" aria-label="Terms and status"><h2>Terms, named carefully</h2>{term_html}</section>'
        f'<section class="blockers" aria-label="Open blockers"><h2>What remains blocked</h2>{blocker_html}</section>'
        f'{sources_html}'
        '</article>'
    )
    substitutions = {
        "{{site_strapline}}": escaped(content["site"]["strapline"]),
        "{{page_title}}": escaped(page["title"]),
        "{{site_title}}": escaped(content["site"]["title"]),
        "{{page_key}}": escaped(page_key),
        "{{styles_link}}": escaped(route_link(route, "assets/styles.css")),
        "{{script_link}}": escaped(route_link(route, "assets/site.js")),
        "{{home_link}}": escaped(route_link(route, "index.html")),
        "{{site_edition}}": escaped(content["site"]["edition"]),
        "{{navigation}}": "".join(nav_items),
        "{{page_body}}": body,
        "{{site_scope_note}}": escaped(content["site"]["scopeNote"]),
        "{{sources_link}}": escaped(route_link(route, "sources/index.html")),
    }
    document = template
    for token, value in substitutions.items():
        document = document.replace(token, value)
    if "{{" in document or "}}" in document:
        fail("template contains an unknown placeholder")
    return route, document + "\n"


def render_all(content: dict[str, Any], template: str, styles: str, script: str) -> dict[str, str]:
    outputs = dict(render_page(content, page_key, template) for page_key in PAGE_ORDER)
    outputs["assets/styles.css"] = styles
    outputs["assets/site.js"] = script
    knowledge = {
        "schemaVersion": content["schemaVersion"],
        "site": content["site"],
        "sources": content["sources"],
        "facts": content["facts"],
        "terms": content["terms"],
        "relationships": content["relationships"],
        "blockers": content["blockers"],
        "pages": content["pages"],
    }
    outputs["knowledge.json"] = json.dumps(knowledge, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    return outputs


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".site-build-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def build(content_path: Path, template_path: Path, output_dir: Path, check: bool) -> int:
    try:
        content = json.loads(content_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"build-site: cannot read content: {error}", file=sys.stderr)
        return 1
    try:
        validate_content(mapping(content, "root"))
        template = template_path.read_text(encoding="utf-8")
        styles = DEFAULT_STYLES.read_text(encoding="utf-8")
        script = DEFAULT_SCRIPT.read_text(encoding="utf-8")
        outputs = render_all(content, template, styles, script)
    except (OSError, ContentError) as error:
        print(f"build-site: {error}", file=sys.stderr)
        return 1

    output_dir = output_dir.resolve()
    if output_dir == output_dir.parent:
        print("build-site: unsafe output root", file=sys.stderr)
        return 1
    for route, document in outputs.items():
        safe_route(route) if route.endswith(".html") else None
        target = (output_dir / route).resolve()
        if target != output_dir and output_dir not in target.parents:
            print(f"build-site: unsafe output path {route}", file=sys.stderr)
            return 1
        if check:
            if not target.is_file() or target.read_text(encoding="utf-8") != document:
                print(f"build-site: output is out of date: {route}", file=sys.stderr)
                return 1
        else:
            atomic_write(target, document)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=DEFAULT_CONTENT)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if generated files differ")
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    return build(arguments.content, arguments.template, arguments.output, arguments.check)


if __name__ == "__main__":
    raise SystemExit(main())
