from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "index.md",
    "article.md",
    "publication-plan.md",
    "demo.md",
    "releases/v0.1-publication.md",
    "examples/document-triage/demo_cases.json",
    "examples/document-triage/demo_results.json",
    "assets/document-triage-demo-overview.svg",
    "assets/decision-pga-decision-state-diagnostics.pdf",
    "assets/decision-pga-diagnostic-loop.svg",
    "_config.yml",
    "_layouts/default.html",
    "assets/styles.css",
    "LICENSE.md",
    "scripts/build_pdf.py",
]


ARTICLE_REQUIRED_PHRASES = [
    "Decision-PGA and the Need for Decision-State Diagnostics",
    "Zachary D. Michels, PhD",
    "May 18, 2026",
    "personal technical perspective, not an institutional statement",
    "no patient data",
    "not clinical validation",
    "does not describe a medical device or clinical decision support product",
    "a decision-state is a probability-like distribution over an explicit set of candidate decisions",
    "does not assume that every agent trace lives on a smooth behavioral manifold",
    "Healthcare is not the only place this matters",
    "The geometric framing should be treated as a hypothesis to test",
    "where the geometric assumptions fail",
    "not a claim made by the current prototype",
    "not the inevitable geometry of agent cognition",
    "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices",
    "https://www.fda.gov/medical-devices/software-medical-device-samd/clinical-decision-support-software-frequently-asked-questions-faqs",
    "https://healthit.gov/regulations/hti-rules/hti-1-final-rule/",
    "https://www.who.int/publications/i/item/9789240029200",
]


PLAN_REQUIRED_PHRASES = [
    "One-week publication path",
    "GitHub Pages or repository Markdown",
    "Substack or Medium",
    "OSF Preprints",
    "Zenodo",
    "arXiv",
]


DEMO_REQUIRED_ACTIONS = [
    "accept_extraction",
    "ask_for_clarification",
    "retrieve_more_context",
    "flag_for_review",
    "defer",
]


DEMO_REQUIRED_STATES = [
    "stable",
    "binary_ambiguous",
    "diffuse",
    "boundary_sensitive",
    "drifting",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        require(path.exists(), f"Missing required file: {relative}")
        require(path.stat().st_size > 0, f"Required file is empty: {relative}")

    article = (ROOT / "article.md").read_text(encoding="utf-8")
    normalized_article = " ".join(article.split())
    for phrase in ARTICLE_REQUIRED_PHRASES:
        require(
            phrase in article or phrase in normalized_article,
            f"Article missing required phrase/link: {phrase}",
        )
    require("Document Extraction Triage Demo" in article, "Article should link to the demo page")
    removed_terms = ["Ma" + "yo", "Ma" + "yo Clinic"]
    for term in removed_terms:
        require(term not in article, "Active article should not name removed institutions")
    placeholder_terms = ["TO" + "DO", "T" + "BD"]
    for term in placeholder_terms:
        require(term not in article, "Active article contains placeholder text")

    plan = (ROOT / "publication-plan.md").read_text(encoding="utf-8")
    for phrase in PLAN_REQUIRED_PHRASES:
        require(phrase in plan, f"Publication plan missing required phrase: {phrase}")

    index = (ROOT / "index.md").read_text(encoding="utf-8")
    require("Read the article" in index, "Landing page missing article call to action")
    require("Try the demo" in index, "Landing page missing demo call to action")
    require("Download PDF" in index, "Landing page missing PDF call to action")
    require(
        "assets/decision-pga-decision-state-diagnostics.pdf" in index,
        "Landing page should link to the current PDF asset",
    )

    layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
    require("styles.css?v=20260519-demo-responsive" in layout, "Layout should version the stylesheet")

    pdf = ROOT / "assets/decision-pga-decision-state-diagnostics.pdf"
    require(pdf.read_bytes().startswith(b"%PDF"), "PDF asset does not look like a PDF")
    require(pdf.stat().st_size > 100_000, "PDF asset is unexpectedly small")

    demo = (ROOT / "demo.md").read_text(encoding="utf-8")
    for phrase in [
        "Document Extraction Triage Demo",
        "synthetic demonstration data",
        "accept_extraction",
        "ask_for_clarification",
        "retrieve_more_context",
        "flag_for_review",
        "defer",
        "stable",
        "binary ambiguous",
        "diffuse",
        "boundary-sensitive",
        "drifting",
        "not clinical validation",
        "Visual Walkthrough",
        "document-triage-demo-overview.svg",
        "How to read the matrices",
        "Each row is one synthetic observation",
        "The columns always follow this order",
        "Decision-PGA reads the full matrix",
        "Try one case as a diagnostic payload",
        "Generated diagnostic readout",
        "Probability table columns",
    ]:
        require(phrase in demo, f"Demo page missing required phrase: {phrase}")

    fixture_path = ROOT / "examples/document-triage/demo_cases.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    require(fixture["schema_version"] == "decision-pga-document-triage-demo-v1", "Unexpected demo fixture schema")
    require(fixture["labels"] == DEMO_REQUIRED_ACTIONS, "Demo fixture labels changed unexpectedly")
    scenarios = fixture["scenarios"]
    require(len(scenarios) == 5, "Demo fixture should contain five scenarios")
    states = [scenario["expected_state"] for scenario in scenarios]
    require(states == DEMO_REQUIRED_STATES, "Demo fixture should cover the expected decision states in order")
    actions = [scenario["expected_action"] for scenario in scenarios]
    require(actions == DEMO_REQUIRED_ACTIONS, "Demo fixture should cover the expected actions in order")
    for scenario in scenarios:
        observations = scenario["observations"]
        require(len(observations) >= 6, f"Scenario has too few observations: {scenario['id']}")
        for row in observations:
            require(len(row) == len(DEMO_REQUIRED_ACTIONS), f"Observation width mismatch in {scenario['id']}")
            require(abs(sum(row) - 1.0) < 1e-9, f"Observation probabilities do not sum to 1 in {scenario['id']}")
            require(all(value > 0 for value in row), f"Observation contains nonpositive value in {scenario['id']}")

    results = json.loads((ROOT / "examples/document-triage/demo_results.json").read_text(encoding="utf-8"))
    require(results["source_fixture"] == "examples/document-triage/demo_cases.json", "Unexpected demo result source")
    diagnostic_states = [scenario["diagnostic_state"] for scenario in results["scenarios"]]
    require(
        diagnostic_states
        == ["stable", "binary_ambiguity", "diffuse_uncertainty", "boundary_sensitive", "regime_shift"],
        "Demo diagnostic results should cover the current Decision-PGA states in order",
    )
    workflow_actions = [scenario["workflow_action"] for scenario in results["scenarios"]]
    require(workflow_actions == DEMO_REQUIRED_ACTIONS, "Demo result workflow actions should match the public action vocabulary")
    for scenario in results["scenarios"]:
        require("mean_probability" in scenario, f"Demo result missing mean probability: {scenario['id']}")
        require("metrics" in scenario, f"Demo result missing metrics: {scenario['id']}")

    svg = (ROOT / "assets/document-triage-demo-overview.svg").read_text(encoding="utf-8")
    for phrase in [
        "Document extraction triage demo",
        "Clean invoice due date",
        "Two plausible contract dates",
        "Missing attachment reference",
        "Near-threshold total",
        "Contradictory revision packet",
    ]:
        require(phrase in svg, f"Demo SVG missing required text: {phrase}")

    print("publication site validation passed")


if __name__ == "__main__":
    main()
