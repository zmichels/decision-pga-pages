from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "index.md",
    "article.md",
    "publication-plan.md",
    "releases/v0.1-publication.md",
    "assets/decision-pga-decision-state-diagnostics.pdf",
    "assets/decision-pga-diagnostic-loop.svg",
    "_config.yml",
    "_layouts/default.html",
    "assets/styles.css",
    "LICENSE.md",
]


ARTICLE_REQUIRED_PHRASES = [
    "Decision-PGA and the Need for Decision-State Diagnostics",
    "Zachary D. Michels, PhD",
    "May 18, 2026",
    "personal technical perspective, not an institutional statement",
    "no patient data",
    "not clinical validation",
    "does not describe a medical device or clinical decision support product",
    "Healthcare is not the only place this matters",
    "Decision-PGA should be compared against simpler baselines",
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
    require("Download PDF" in index, "Landing page missing PDF call to action")
    require(
        "assets/decision-pga-decision-state-diagnostics.pdf" in index,
        "Landing page should link to the current PDF asset",
    )

    print("publication site validation passed")


if __name__ == "__main__":
    main()
