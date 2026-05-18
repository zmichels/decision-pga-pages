from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "index.md",
    "article.md",
    "publication-plan.md",
    "releases/v0.1-publication.md",
    "assets/decision-pga-healthcare-decision-state-diagnostics.pdf",
    "_config.yml",
    "_layouts/default.html",
    "assets/styles.css",
    "LICENSE.md",
]


ARTICLE_REQUIRED_PHRASES = [
    "Decision-State Diagnostics for Healthcare AI",
    "personal technical perspective, not an institutional statement",
    "no patient data",
    "not clinical validation",
    "not a medical device or clinical decision support product",
    "Mayo Clinic",
    "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",
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
    for phrase in ARTICLE_REQUIRED_PHRASES:
        require(phrase in article, f"Article missing required phrase/link: {phrase}")

    plan = (ROOT / "publication-plan.md").read_text(encoding="utf-8")
    for phrase in PLAN_REQUIRED_PHRASES:
        require(phrase in plan, f"Publication plan missing required phrase: {phrase}")

    index = (ROOT / "index.md").read_text(encoding="utf-8")
    require("Read the article" in index, "Landing page missing article call to action")
    require("Download PDF" in index, "Landing page missing PDF call to action")

    print("publication site validation passed")


if __name__ == "__main__":
    main()

