# Decision-PGA Publication Site

This repository is the public GitHub Pages staging site for the article
**Decision-PGA and the Need for Decision-State Diagnostics**.

It intentionally separates the public publication surface from the private
Decision-PGA prototype repository while the code is still being readied for a
broader release.

## Contents

- `index.md` - landing page for GitHub Pages
- `article.md` - canonical article draft
- `demo.md` - synthetic document extraction triage demo
- `examples/document-triage/demo_cases.json` - demo probability-cloud fixture
- `examples/document-triage/demo_results.json` - generated diagnostic outputs
- `assets/document-triage-demo-overview.svg` - visual demo summary
- `publication-plan.md` - no-cost one-week publication route
- `assets/decision-pga-diagnostic-loop.svg` - explanatory diagram
- `assets/decision-pga-decision-state-diagnostics.pdf` - PDF preview
- `releases/v0.1-publication.md` - release staging notes
- `scripts/build_pdf.py` - Chrome-based publication PDF generator

Local prior drafts are kept under `drafts/`, which is intentionally ignored by
git so removed institutional wording does not re-enter the public repository.

## Guardrails

This is a personal technical perspective, not an institutional statement. It
uses no patient data, is not clinical validation, and is not a medical device or
clinical decision support product.

## Local Validation

```bash
python3 scripts/validate_publication.py
```

## Rebuild Demo Outputs

The demo outputs are generated from `examples/document-triage/demo_cases.json`
with the local Decision-PGA prototype.

```bash
python3 scripts/build_demo_outputs.py
```

## Rebuild PDF

The PDF is generated from `article.md` with a local Chrome/Chromium print
renderer so page breaks and margins are handled by a browser layout engine.

```bash
python3 scripts/build_pdf.py
```

## License

Unless otherwise noted, article text and site content are shared under the
Creative Commons Attribution 4.0 International license. See `LICENSE.md`.
