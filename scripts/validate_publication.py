from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "index.md",
    "article.md",
    "telescoping.md",
    "kinematics.md",
    "demo.md",
    "toolkit.md",
    "robots.txt",
    "sitemap.xml",
    "llms.txt",
    "google4a9ab19a7fbfc2f9.html",
    "examples/document-triage/demo_cases.json",
    "examples/document-triage/demo_results.json",
    "assets/document-triage-demo-overview.svg",
    "assets/decision-pga-decision-state-diagnostics.pdf",
    "assets/telescoping-decision-pga.pdf",
    "assets/telescoping-zoom.svg",
    "assets/telescoping-zoom.png",
    "assets/cross-document-bridge.svg",
    "assets/cross-document-bridge.png",
    "assets/decision-pga-diagnostic-loop.svg",
    "_config.yml",
    "_layouts/default.html",
    "assets/styles.css",
    "assets/decision-pga-demo-runner.js",
    "LICENSE.md",
    "scripts/build_pdf.py",
]


ARTICLE_REQUIRED_PHRASES = [
    "Decision-PGA and the Need for Decision-State Diagnostics",
    "Zachary D. Michels, PhD",
    "May 19, 2026",
    "personal technical perspective, not an institutional statement",
    "no patient data",
    "not clinical validation",
    "does not describe a medical device or clinical decision support product",
    "Principal Geodesic Analysis: a manifold analogue of Principal Component Analysis",
    "Fletcher, Lu, Pizer, and Joshi's 2004 paper",
    "https://doi.org/10.1109/TMI.2004.831793",
    "Probabilistic Principal Geodesic Analysis",
    "https://papers.nips.cc/paper/5133-probabilistic-principal-geodesic-analysis",
    "Semantic Uncertainty: Linguistic Invariances",
    "https://arxiv.org/abs/2302.09664",
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


TELESCOPING_REQUIRED_PHRASES = [
    "Telescoping Decision-PGA: Seeing The Smaller Shape Inside The Larger One",
    "Zachary D. Michels, PhD",
    "A Diagnostic Should Be Able To Zoom",
    "What Decision-PGA Borrows From PGA",
    "The Cloud May Contain Smaller Clouds",
    "Telescoping a broad uncertainty state",
    "assets/telescoping-zoom.svg",
    "Bridging uncertainty across two source documents",
    "assets/cross-document-bridge.svg",
    "The Bridge Case: When Two Uncertainties Belong Together",
    "source-backed bridge",
    "human review",
    "Telescoping As A Workflow Pattern",
    "What To Build Next",
    "Decision-PGA offers one modest, inspectable way to help them do that",
]


KINEMATICS_REQUIRED_PHRASES = [
    "Kinematic Decision-PGA: Reading Motion in Decision States",
    "Zachary D. Michels, PhD",
    "June 10, 2026",
    "observed probability-geometry motion",
    "not hidden model physics",
    "does not prove causal internal forces",
    "does not decide whether the underlying answer is correct",
    "ambient_tangent_delta",
    "RAG/tool whiplash",
    "Jerk Is A Review Signal",
    "jerk is a review signal",
    "Quickly characterizing the trajectory",
    "review attention",
    "uncertainty has shape",
    "shape has substructure",
    "shape has motion",
    "kinematic_trajectory",
    "decision-pga diagnose --pretty examples/agent/kinematic_trajectory_rag_tool_whiplash.json",
    "canonical_path_probabilities",
    "step_kinetic_energy",
    "step_jerk",
    "systemic_kinetic_energy",
    "systemic_jerk",
    "velocity_dispersion",
    "primary_drift_labels",
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
    require("Telescoping Decision-PGA" in article, "Article should link to the telescoping companion article")
    require("{{ '/telescoping/' | relative_url }}" in article, "Article should use the relative companion article link")
    require("Kinematic Decision-PGA" in article, "Article should link to the kinematic companion article")
    require("{{ '/kinematics/' | relative_url }}" in article, "Article should use the relative kinematic article link")
    require("https://github.com/zmichels/Decision-PGA" in article, "Article should link to the public code repo")
    removed_terms = ["Ma" + "yo", "Ma" + "yo Clinic"]
    for term in removed_terms:
        require(term not in article, "Active article should not name removed institutions")
    placeholder_terms = ["TO" + "DO", "T" + "BD"]
    for term in placeholder_terms:
        require(term not in article, "Active article contains placeholder text")

    kinematics = (ROOT / "kinematics.md").read_text(encoding="utf-8")
    normalized_kinematics = " ".join(kinematics.split())
    for phrase in KINEMATICS_REQUIRED_PHRASES:
        require(
            phrase in kinematics or phrase in normalized_kinematics,
            f"Kinematic article missing required phrase/link: {phrase}",
        )
    require("schema_type: TechArticle" in kinematics, "Kinematic article should be marked as TechArticle")
    require("permalink: /kinematics/" in kinematics, "Kinematic article should use the public permalink")
    require("{{ '/article/' | relative_url }}" in kinematics, "Kinematic article should link back to the original article")
    require("{{ '/telescoping/' | relative_url }}" in kinematics, "Kinematic article should link to the telescoping companion")
    require("https://github.com/zmichels/Decision-PGA" in kinematics, "Kinematic article should link to the public code repo")

    index = (ROOT / "index.md").read_text(encoding="utf-8")
    require("Read the article" in index, "Landing page missing article call to action")
    require("Read the follow-up" in index, "Landing page missing follow-up call to action")
    require("Try the demo" in index, "Landing page missing demo call to action")
    require("Use the toolkit" in index, "Landing page missing toolkit call to action")
    require("View code" in index, "Landing page missing code call to action")
    require("https://github.com/zmichels/Decision-PGA" in index, "Landing page missing public code repo link")
    require("Download PDF" in index, "Landing page missing PDF call to action")
    require("Telescoping Decision-PGA" in index, "Landing page should mention the companion article")
    require("{{ '/telescoping/' | relative_url }}" in index, "Landing page should link to the companion article")
    require("Read kinematics" in index, "Landing page missing kinematic call to action")
    require("Kinematic Decision-PGA" in index, "Landing page should mention the kinematic companion")
    require("{{ '/kinematics/' | relative_url }}" in index, "Landing page should link to the kinematic companion")
    require(
        "assets/decision-pga-decision-state-diagnostics.pdf" in index,
        "Landing page should link to the current PDF asset",
    )

    layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
    require("styles.css?v=20260519-toolkit-pyramid" in layout, "Layout should version the stylesheet")
    for phrase in [
        "rel=\"canonical\"",
        "rel=\"sitemap\"",
        "title=\"llms.txt\"",
        "og:title",
        "twitter:card",
        "application/ld+json",
        "SoftwareSourceCode",
        "WebApplication",
        "TechArticle",
        "https://github.com/zmichels/Decision-PGA#software",
        "decision-state diagnostics",
        "principal geodesic analysis",
    ]:
        require(phrase in layout, f"Layout missing crawler metadata marker: {phrase}")
    styles = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
    require(".panel a" in styles, "Stylesheet should include panel link wrapping")
    require("overflow-wrap: anywhere" in styles, "Panel content should wrap long filenames")
    require(".toolkit-gallery" in styles, "Stylesheet should include toolkit gallery layout")
    require(".example-link" in styles, "Stylesheet should include compact example link styling")
    require("text-overflow: ellipsis" in styles, "Example links should not dangle over card edges")
    require("white-space: nowrap" in styles, "Example links should stay on one line")
    require("https://github.com/zmichels/Decision-PGA" in layout, "Nav should link to the public code repo")
    require("Toolkit" in layout, "Nav should link to the toolkit page")
    require("Telescoping" in layout, "Nav should link to the telescoping companion article")
    require("Kinematics" in layout, "Nav should link to the kinematic companion article")
    require("{{ '/kinematics/' | relative_url }}" in layout, "Nav should use the relative kinematic article link")
    for removed_nav in ["publication-plan", "Release Notes", "Plan"]:
        require(removed_nav not in layout, f"Layout should not expose old staging navigation: {removed_nav}")

    toolkit = (ROOT / "toolkit.md").read_text(encoding="utf-8")
    for phrase in [
        "Decision-PGA Agent Toolkit",
        "Diagnostic Payload Gallery",
        "Use Decision-PGA in five minutes",
        "what kind of uncertainty is it",
        "Tool/action ambiguity",
        "RAG evidence conflict",
        "Document extraction routing",
        "Multi-step agent drift",
        "Stable abstain decision",
        "toolkit-gallery",
        "example-link",
        "https://github.com/zmichels/Decision-PGA/blob/main/docs/agent-toolkit.md",
        "not a production safety layer",
    ]:
        require(phrase in toolkit, f"Toolkit page missing required phrase: {phrase}")
    for phrase in [
        "Kinematic Decision-PGA",
        "{{ '/kinematics/' | relative_url }}",
        "Kinematic trajectory whiplash",
        "kinematic_trajectory",
        "RAG/tool whiplash",
        "step_jerk",
        "kinematic_trajectory_rag_tool_whiplash.json",
    ]:
        require(phrase in toolkit, f"Toolkit page missing kinematic phrase: {phrase}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for phrase in [
        "User-agent: *",
        "Allow: /",
        "Sitemap: {{ \"/sitemap.xml\" | absolute_url }}",
    ]:
        require(phrase in robots, f"robots.txt missing required phrase: {phrase}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for phrase in [
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
        "{{ \"/\" | absolute_url }}",
        "{{ \"/article/\" | absolute_url }}",
        "{{ \"/telescoping/\" | absolute_url }}",
        "{{ \"/demo/\" | absolute_url }}",
        "{{ \"/toolkit/\" | absolute_url }}",
        "{{ \"/assets/decision-pga-decision-state-diagnostics.pdf\" | absolute_url }}",
        "{{ \"/assets/telescoping-decision-pga.pdf\" | absolute_url }}",
    ]:
        require(phrase in sitemap, f"sitemap.xml missing required phrase: {phrase}")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for phrase in [
        "# Decision-PGA",
        "Canonical Pages",
        "Best Entry Points For AI Assistants",
        "Technical Summary",
        "Important Limits",
        "Source code: https://github.com/zmichels/Decision-PGA",
        "Telescoping companion",
        "not a production safety layer",
        "no clinical-validation claim",
    ]:
        require(phrase in llms, f"llms.txt missing required phrase: {phrase}")

    google_verification = (ROOT / "google4a9ab19a7fbfc2f9.html").read_text(encoding="utf-8")
    require(
        google_verification.strip() == "google-site-verification: google4a9ab19a7fbfc2f9.html",
        "Google Search Console verification file has unexpected contents",
    )

    pdf = ROOT / "assets/decision-pga-decision-state-diagnostics.pdf"
    require(pdf.read_bytes().startswith(b"%PDF"), "PDF asset does not look like a PDF")
    require(pdf.stat().st_size > 100_000, "PDF asset is unexpectedly small")

    telescoping_pdf = ROOT / "assets/telescoping-decision-pga.pdf"
    require(telescoping_pdf.read_bytes().startswith(b"%PDF"), "Telescoping PDF asset does not look like a PDF")
    require(telescoping_pdf.stat().st_size > 40_000, "Telescoping PDF asset is unexpectedly small")
    telescoping = (ROOT / "telescoping.md").read_text(encoding="utf-8")
    normalized_telescoping = " ".join(telescoping.split())
    for phrase in TELESCOPING_REQUIRED_PHRASES:
        require(
            phrase in telescoping or phrase in normalized_telescoping,
            f"Telescoping article missing required phrase/link: {phrase}",
        )
    require("schema_type: TechArticle" in telescoping, "Telescoping article should be marked as TechArticle")
    require("permalink: /telescoping/" in telescoping, "Telescoping article should use the public permalink")
    require("{{ '/article/' | relative_url }}" in telescoping, "Telescoping article should link back to the original article")
    require("{{ '/kinematics/' | relative_url }}" in telescoping, "Telescoping article should link to the kinematic companion")
    require("shape has motion" in telescoping, "Telescoping article should point to the motion companion")
    require("{{ '/assets/telescoping-decision-pga.pdf' | relative_url }}" in telescoping, "Telescoping article should link to its PDF")
    require("SME" not in telescoping and "SMEs" not in telescoping, "Telescoping article should avoid unexplained SME acronym")
    for figure in [
        ROOT / "assets/telescoping-zoom.svg",
        ROOT / "assets/cross-document-bridge.svg",
    ]:
        svg_text = figure.read_text(encoding="utf-8")
        require("<svg" in svg_text, f"Figure does not look like SVG: {figure.name}")
        require("SME" not in svg_text and "SMEs" not in svg_text, f"Figure should avoid unexplained SME acronym: {figure.name}")

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
        "Live Diagnostic Workspace",
        "Choose a case, inspect or edit the probability rows, then run the same",
        "Generate variation",
        "Decision-state shape atlas",
        "data-manifold-map",
        "data-dpga-demo-runner",
        "decision-pga-demo-runner.js",
        "https://github.com/zmichels/Decision-PGA",
    ]:
        require(phrase in demo, f"Demo page missing required phrase: {phrase}")

    runner = (ROOT / "assets/decision-pga-demo-runner.js").read_text(encoding="utf-8")
    for phrase in [
        "diagnoseProbabilityCloud",
        "jacobiEigensystem",
        "sphereLog",
        "jacobiEigenvalues",
        "projectTangentCloud",
        "renderManifoldMap",
        "renderProbabilityBars",
        "renderPayload",
        "generateVariationRows",
        "SHAPE_ATLAS",
        "createShapeAtlasSvg",
        "threshold_band",
        "two_lobes",
        "examples/document-triage/demo_cases.json",
        "accept_extraction",
        "ask_for_clarification",
        "retrieve_more_context",
        "flag_for_review",
        "defer",
    ]:
        require(phrase in runner, f"Live demo runner missing required behavior marker: {phrase}")
    require("auto-zoom radius" not in runner, "Live demo map should not expose auto-zoom implementation details")

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

    print("site validation passed")


if __name__ == "__main__":
    main()
