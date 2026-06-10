# Decision-PGA Site

This repository hosts the public GitHub Pages companion site for
**Decision-PGA and the Need for Decision-State Diagnostics**.

The site links the article, the Telescoping Decision-PGA companion perspective,
synthetic document-triage demo, agent toolkit page, PDF copies, and the public
Decision-PGA prototype repository:
<https://github.com/zmichels/Decision-PGA>.

## Contents

- `index.md` - landing page for GitHub Pages
- `article.md` - canonical article draft
- `telescoping.md` - companion technical perspective on uncertainty substructure
- `demo.md` - synthetic document extraction triage demo
- `toolkit.md` - practical agent-builder quickstart and payload gallery
- `examples/document-triage/demo_cases.json` - demo probability-cloud fixture
- `examples/document-triage/demo_results.json` - generated diagnostic outputs
- `assets/document-triage-demo-overview.svg` - visual demo summary
- `assets/decision-pga-diagnostic-loop.svg` - explanatory diagram
- `assets/decision-pga-decision-state-diagnostics.pdf` - PDF copy
- `assets/telescoping-decision-pga.pdf` - companion PDF copy
- `assets/telescoping-zoom.svg` and `.png` - telescoping uncertainty figure
- `assets/cross-document-bridge.svg` and `.png` - cross-document bridge figure
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

## Rebuild PDFs

The PDFs are generated from site Markdown with a local Chrome/Chromium print
renderer so page breaks, margins, and figures are handled by a browser layout
engine.

```bash
python3 scripts/build_pdf.py
python3 scripts/build_pdf.py telescoping.md assets/telescoping-decision-pga.pdf
```

## License

Unless otherwise noted, article text and site content are shared under the
Creative Commons Attribution 4.0 International license. See `LICENSE.md`.
