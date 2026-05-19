# Guided Demo Kit Design

Date: May 19, 2026

## Decision

Build a local-first, Colab-ready guided demo kit for the Decision-PGA document
extraction triage example.

The goal is to let readers run the public demo while reading the article,
inspect the synthetic probability clouds, reproduce the diagnostic outputs, and
try their own probability-like data with clear guardrails. This should deepen
intuition without turning the publication site into a full interactive
application.

## Scope

The first implementation should add:

- one runnable notebook that mirrors the public document-triage demo;
- one user-data template file with explicit action labels and probability rows;
- one validation helper that checks common data-shape mistakes;
- comparison plots that make Decision-PGA outputs easier to interpret;
- article/site links pointing readers to the notebook and template;
- documentation explaining what user-defined rows and columns are allowed to
  mean.

This pass should not add a hosted web app, require model API keys, ingest
private data, or claim validation on real clinical, financial, or production
workflows.

## Reader Experience

The intended path is:

1. Read the article and static demo page.
2. Open the guided notebook locally.
3. Run the built-in fixture cells to regenerate the demo diagnostics.
4. Inspect plots comparing probability mass, entropy, margin, PGA dispersion
   shape, PC1 fraction, and workflow-action mapping.
5. Copy the user-data template, replace labels and rows, run validation, then
   diagnose the custom cloud.
6. Read warnings and interpretation notes that distinguish descriptive
   diagnostic behavior from proof of correctness.

The notebook should be friendly to a reader who understands tables and
probabilities but has not read the package internals.

## Notebook Structure

The notebook should use sections in this order:

1. **What The Matrix Means**
   - Rows are repeated observations of one decision point.
   - Columns are candidate actions, labels, values, or choices.
   - Each row should be nonnegative and normalized or normalizable to 1.0.

2. **Load The Demo Fixture**
   - Load `examples/document-triage/demo_cases.json`.
   - Show labels and one scenario matrix as a table.

3. **Run Diagnostics**
   - Compute or load the same diagnostic contract used by the static demo.
   - Show state, recommended workflow action, top labels, and metrics.

4. **Compare Baselines**
   - Show entropy, top-label margin, switch rate, and drift-style measures next
     to PGA dispersion metrics.
   - Keep claims conservative: plots should show possible added signal, not
     proof of general advantage.

5. **Plot The Demo**
   - Mean action probability bars.
   - Observation-level top-action sequences.
   - PC1/PC2 projection or tangent-cloud plot when supported by available data.
   - Metric comparison grid across the five synthetic states.

6. **Try User Data**
   - Load a template JSON file.
   - Validate shape, labels, row sums, row count, and negative values.
   - Normalize only after warning the reader what changed.
   - Run diagnostics and plots on the user cloud.

7. **Interpretation Notes**
   - Explain what a stable, ambiguous, diffuse, sensitive, or drifting state
     suggests.
   - Explain what the diagnostic does not know: ground truth, task stakes,
     clinical validity, policy thresholds, or whether the candidate actions are
     well chosen.

## User Data Contract

The template should use a JSON shape similar to:

```json
{
  "label": "my_decision_case",
  "labels": [
    "accept_extraction",
    "ask_for_clarification",
    "retrieve_more_context",
    "flag_for_review",
    "defer"
  ],
  "probabilities": [
    [0.80, 0.08, 0.04, 0.06, 0.02],
    [0.76, 0.10, 0.05, 0.07, 0.02]
  ]
}
```

Required meaning:

- `labels` are candidate decisions, actions, classes, values, or workflow states.
- each probability row is one repeated observation of the same decision point;
- rows may come from repeated samples, scoring passes, human votes, rule checks,
  perturbation runs, or trajectory steps, as long as that source is described;
- all rows must have the same label order;
- rows should contain finite nonnegative values;
- normalized rows should sum to 1.0;
- fewer than five rows should be allowed but warned as a fragile intuition
  exercise.

## Plots

The first plot set should prioritize interpretability:

- **mean probability bars** for each scenario;
- **top-action sequence strips** showing whether the preferred action is stable
  or shifting;
- **metric comparison table or heatmap** with entropy, margin, dispersion,
  PC1 fraction, anisotropy ratio, and drift;
- **simple PCA/PGA projection** if the existing package can expose tangent
  vectors cleanly enough for the notebook.

Avoid ornate visualizations in this pass. The reader should understand what
changed after one glance and a short caption.

## Site Integration

The public site should remain the canonical article companion, not the runtime.
Add:

- a demo-page section named "Run This Demo";
- links to the notebook, fixture, result JSON, and user-data template;
- a short setup command for local use;
- a note that a Colab route is planned once the notebook stabilizes.

The main Decision-PGA code repo can remain private until it is ready. If the
public site needs runnable notebook content before the main package is public,
the notebook should include a small local diagnostic implementation or read
precomputed outputs, with clear labels about what is prototype material.

## Testing And Acceptance

Acceptance checks:

- notebook runs top-to-bottom locally from a clean checkout;
- notebook regenerates or matches the checked-in demo result states/actions;
- template validation catches mismatched row width, negative values, nonfinite
  values, and row sums that are not close to 1.0;
- plots render without external services or model API credentials;
- publication-site validation still passes;
- no wording implies clinical validation, production safety, or correctness of
  any extraction.

## Future Follow-On

After the notebook is stable, the next useful extension is a hosted/click-to-run
path:

- Colab badge or Colab copy instructions first;
- Binder only if dependency friction is low;
- JupyterLite only if the package and dependencies can run comfortably in the
  browser;
- full browser playground only after the data contract and notebook interaction
  have proven useful.
