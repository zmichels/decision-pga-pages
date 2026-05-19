# Guided Demo Kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-first, Colab-ready runnable notebook kit for the public Decision-PGA document extraction triage demo.

**Architecture:** Keep the public article site independent from the private Decision-PGA prototype by adding a small transparent demo-support module that can validate probability-cloud inputs, compute baseline metrics, reproduce the checked-in demo diagnostics, and generate plots. The notebook imports this public demo-support module, runs the existing synthetic fixtures, then lets readers swap in a user-defined JSON template.

**Tech Stack:** Python 3.10+, JSON fixtures, NumPy, pandas, matplotlib, nbformat/nbclient for notebook execution checks, GitHub Pages Markdown, existing `scripts/validate_publication.py`.

---

## File Structure

- Create `demo_support/__init__.py`
  - Public import surface for demo-only helpers.
- Create `demo_support/document_triage.py`
  - Load fixtures, validate probability payloads, normalize rows, compute baseline metrics, produce a lightweight local diagnostic, and generate matplotlib plots.
- Create `tests/test_document_triage_support.py`
  - Stdlib `unittest` tests for validation, metrics, state/action matching, and plotting smoke checks.
- Create `requirements-demo.txt`
  - Notebook/runtime dependencies: NumPy, pandas, matplotlib, nbformat, nbclient.
- Create `examples/document-triage/user_cloud_template.json`
  - User-editable data template with clear fields and comments encoded as description strings.
- Create `notebooks/document_extraction_triage_demo.ipynb`
  - Guided notebook that runs the built-in fixture, produces plots, and validates user data.
- Create `scripts/execute_notebook.py`
  - CI-friendly notebook execution helper using nbclient.
- Modify `demo.md`
  - Add a "Run This Demo" section linking to the notebook, fixture, results, and template.
- Modify `README.md`
  - Document local setup and notebook execution.
- Modify `scripts/validate_publication.py`
  - Require new notebook, template, requirements, support module, and demo links.
- Modify `.github/workflows/validate.yml`
  - Add demo dependency install, unit tests, and notebook execution smoke test.
- Modify `releases/v0.1-publication.md`
  - Note that the article companion now includes a runnable guided demo kit.

---

### Task 1: Add Public Demo-Support Module Skeleton And Validation

**Files:**
- Create: `demo_support/__init__.py`
- Create: `demo_support/document_triage.py`
- Create: `tests/test_document_triage_support.py`
- Create: `requirements-demo.txt`

- [ ] **Step 1: Write failing validation tests**

Create `tests/test_document_triage_support.py` with:

```python
from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

from demo_support.document_triage import (
    REQUIRED_KEYS,
    load_probability_payload,
    normalize_probability_rows,
    validate_probability_payload,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "document-triage" / "demo_cases.json"


class ProbabilityPayloadValidationTests(unittest.TestCase):
    def test_demo_fixture_loads_with_expected_labels(self) -> None:
        payload = load_probability_payload(FIXTURE)
        self.assertEqual(
            payload["labels"],
            [
                "accept_extraction",
                "ask_for_clarification",
                "retrieve_more_context",
                "flag_for_review",
                "defer",
            ],
        )
        self.assertEqual(len(payload["scenarios"]), 5)

    def test_user_payload_validation_accepts_probability_rows(self) -> None:
        payload = {
            "label": "example_case",
            "labels": ["accept", "clarify", "defer"],
            "probabilities": [
                [0.80, 0.10, 0.10],
                [0.76, 0.14, 0.10],
                [0.82, 0.08, 0.10],
                [0.78, 0.12, 0.10],
                [0.81, 0.09, 0.10],
            ],
        }
        report = validate_probability_payload(payload)
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["row_count"], 5)
        self.assertEqual(report["column_count"], 3)

    def test_validation_rejects_missing_keys(self) -> None:
        report = validate_probability_payload({"labels": ["a"], "probabilities": [[1.0]]})
        self.assertFalse(report["valid"])
        self.assertIn("Missing required key: label", report["errors"])
        self.assertEqual(set(REQUIRED_KEYS), {"label", "labels", "probabilities"})

    def test_validation_rejects_mismatched_row_width(self) -> None:
        payload = {
            "label": "bad_width",
            "labels": ["a", "b", "c"],
            "probabilities": [[0.5, 0.5], [0.2, 0.3, 0.5]],
        }
        report = validate_probability_payload(payload)
        self.assertFalse(report["valid"])
        self.assertIn("Row 1 has width 2; expected 3.", report["errors"])

    def test_validation_rejects_negative_and_nonfinite_values(self) -> None:
        payload = {
            "label": "bad_values",
            "labels": ["a", "b"],
            "probabilities": [[1.1, -0.1], [math.inf, 0.0]],
        }
        report = validate_probability_payload(payload)
        self.assertFalse(report["valid"])
        self.assertIn("Row 1 contains a negative value.", report["errors"])
        self.assertIn("Row 2 contains a nonfinite value.", report["errors"])

    def test_validation_warns_for_unnormalized_rows_and_small_row_count(self) -> None:
        payload = {
            "label": "warn_case",
            "labels": ["a", "b"],
            "probabilities": [[2.0, 1.0], [3.0, 1.0]],
        }
        report = validate_probability_payload(payload)
        self.assertTrue(report["valid"])
        self.assertIn("Only 2 rows supplied; diagnostic intuition is fragile below 5 rows.", report["warnings"])
        self.assertIn("Row 1 sums to 3.000000 rather than 1.0.", report["warnings"])

    def test_normalize_probability_rows(self) -> None:
        rows = normalize_probability_rows([[2.0, 1.0], [3.0, 1.0]])
        self.assertAlmostEqual(sum(rows[0]), 1.0)
        self.assertAlmostEqual(rows[0][0], 2.0 / 3.0)
        self.assertAlmostEqual(rows[1][1], 0.25)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run validation tests and verify they fail**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: fail with `ModuleNotFoundError: No module named 'demo_support'`.

- [ ] **Step 3: Add demo dependencies**

Create `requirements-demo.txt`:

```text
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
nbformat>=5.9
nbclient>=0.8
```

- [ ] **Step 4: Add public module exports**

Create `demo_support/__init__.py`:

```python
"""Public helpers for the Decision-PGA article companion demo."""

from .document_triage import (
    REQUIRED_KEYS,
    load_probability_payload,
    normalize_probability_rows,
    validate_probability_payload,
)

__all__ = [
    "REQUIRED_KEYS",
    "load_probability_payload",
    "normalize_probability_rows",
    "validate_probability_payload",
]
```

- [ ] **Step 5: Add validation implementation**

Create `demo_support/document_triage.py` with:

```python
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


REQUIRED_KEYS = ("label", "labels", "probabilities")


def load_probability_payload(path: str | Path) -> dict[str, Any]:
    """Load a JSON probability payload or the public multi-scenario demo fixture."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_probability_payload(payload: dict[str, Any], *, atol: float = 1e-6) -> dict[str, Any]:
    """Validate a probability-cloud payload and return machine-readable feedback."""
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in payload:
            errors.append(f"Missing required key: {key}")

    labels = payload.get("labels")
    rows = payload.get("probabilities")
    if not isinstance(labels, list) or not labels or not all(isinstance(label, str) for label in labels):
        errors.append("labels must be a nonempty list of strings.")
        labels = []
    if not isinstance(rows, list) or not rows:
        errors.append("probabilities must be a nonempty list of rows.")
        rows = []

    expected_width = len(labels)
    for row_index, row in enumerate(rows, start=1):
        if not isinstance(row, list):
            errors.append(f"Row {row_index} is not a list.")
            continue
        if expected_width and len(row) != expected_width:
            errors.append(f"Row {row_index} has width {len(row)}; expected {expected_width}.")
        numeric_values: list[float] = []
        for value in row:
            if not isinstance(value, (int, float)):
                errors.append(f"Row {row_index} contains a nonnumeric value.")
                continue
            numeric_values.append(float(value))
        if any(not math.isfinite(value) for value in numeric_values):
            errors.append(f"Row {row_index} contains a nonfinite value.")
        if any(value < 0 for value in numeric_values):
            errors.append(f"Row {row_index} contains a negative value.")
        row_sum = sum(numeric_values)
        if numeric_values and math.isfinite(row_sum) and abs(row_sum - 1.0) > atol:
            warnings.append(f"Row {row_index} sums to {row_sum:.6f} rather than 1.0.")

    if 0 < len(rows) < 5:
        warnings.append(f"Only {len(rows)} rows supplied; diagnostic intuition is fragile below 5 rows.")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "row_count": len(rows),
        "column_count": expected_width,
    }


def normalize_probability_rows(rows: list[list[float]], *, eps: float = 1e-12) -> list[list[float]]:
    """Return normalized, positive probability rows for notebook experimentation."""
    normalized: list[list[float]] = []
    for row_index, row in enumerate(rows, start=1):
        clean = [max(float(value), eps) for value in row]
        total = sum(clean)
        if total <= 0 or not math.isfinite(total):
            raise ValueError(f"Row {row_index} cannot be normalized.")
        normalized.append([value / total for value in clean])
    return normalized
```

- [ ] **Step 6: Run tests and commit**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: all six tests pass.

Commit:

```bash
git add demo_support tests requirements-demo.txt
git commit -m "Add document triage demo support validation"
```

---

### Task 2: Add Baseline Metrics And Lightweight Public Diagnostics

**Files:**
- Modify: `demo_support/__init__.py`
- Modify: `demo_support/document_triage.py`
- Modify: `tests/test_document_triage_support.py`

- [ ] **Step 1: Add failing metric and diagnostic tests**

Append to `tests/test_document_triage_support.py`:

```python
from demo_support.document_triage import (
    ACTION_MAP,
    compute_baseline_metrics,
    diagnose_probability_cloud,
    load_demo_scenarios,
)


class BaselineMetricAndDiagnosticTests(unittest.TestCase):
    def test_compute_baseline_metrics_for_stable_cloud(self) -> None:
        rows = [
            [0.90, 0.05, 0.03, 0.01, 0.01],
            [0.92, 0.04, 0.02, 0.01, 0.01],
            [0.91, 0.05, 0.02, 0.01, 0.01],
        ]
        metrics = compute_baseline_metrics(rows)
        self.assertAlmostEqual(metrics["mean_margin"], 0.8666666667, places=6)
        self.assertEqual(metrics["top_label_switch_rate"], 0.0)
        self.assertGreater(metrics["mean_entropy"], 0.0)

    def test_load_demo_scenarios_returns_user_payloads(self) -> None:
        cases = load_demo_scenarios(FIXTURE)
        self.assertEqual(len(cases), 5)
        self.assertEqual(cases[0]["label"], "clean_invoice_due_date")
        self.assertIn("probabilities", cases[0])

    def test_public_diagnostics_match_expected_demo_actions(self) -> None:
        cases = load_demo_scenarios(FIXTURE)
        states = []
        actions = []
        for case in cases:
            diagnostic = diagnose_probability_cloud(case)
            states.append(diagnostic["state"])
            actions.append(diagnostic["workflow_action"])
        self.assertEqual(
            states,
            ["stable", "binary_ambiguity", "diffuse_uncertainty", "boundary_sensitive", "regime_shift"],
        )
        self.assertEqual(
            actions,
            [
                "accept_extraction",
                "ask_for_clarification",
                "retrieve_more_context",
                "flag_for_review",
                "defer",
            ],
        )

    def test_action_map_is_explicit(self) -> None:
        self.assertEqual(ACTION_MAP["stable"], "accept_extraction")
        self.assertEqual(ACTION_MAP["binary_ambiguity"], "ask_for_clarification")
        self.assertEqual(ACTION_MAP["diffuse_uncertainty"], "retrieve_more_context")
        self.assertEqual(ACTION_MAP["boundary_sensitive"], "flag_for_review")
        self.assertEqual(ACTION_MAP["regime_shift"], "defer")
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: fail with missing imports for `ACTION_MAP`, `compute_baseline_metrics`, `diagnose_probability_cloud`, or `load_demo_scenarios`.

- [ ] **Step 3: Add metric and diagnostic exports**

Modify `demo_support/__init__.py`:

```python
"""Public helpers for the Decision-PGA article companion demo."""

from .document_triage import (
    ACTION_MAP,
    REQUIRED_KEYS,
    compute_baseline_metrics,
    diagnose_probability_cloud,
    load_demo_scenarios,
    load_probability_payload,
    normalize_probability_rows,
    validate_probability_payload,
)

__all__ = [
    "ACTION_MAP",
    "REQUIRED_KEYS",
    "compute_baseline_metrics",
    "diagnose_probability_cloud",
    "load_demo_scenarios",
    "load_probability_payload",
    "normalize_probability_rows",
    "validate_probability_payload",
]
```

- [ ] **Step 4: Add metrics and lightweight diagnostic implementation**

Append to `demo_support/document_triage.py`:

```python
ACTION_MAP = {
    "stable": "accept_extraction",
    "binary_ambiguity": "ask_for_clarification",
    "diffuse_uncertainty": "retrieve_more_context",
    "boundary_sensitive": "flag_for_review",
    "regime_shift": "defer",
}


def load_demo_scenarios(path: str | Path) -> list[dict[str, Any]]:
    """Convert the checked-in multi-scenario fixture into single-case payloads."""
    fixture = load_probability_payload(path)
    labels = fixture["labels"]
    cases: list[dict[str, Any]] = []
    for scenario in fixture["scenarios"]:
        cases.append(
            {
                "label": scenario["id"],
                "name": scenario["name"],
                "labels": labels,
                "probabilities": scenario["observations"],
                "expected_state": scenario["expected_state"],
                "expected_action": scenario["expected_action"],
                "document_context": scenario["document_context"],
                "candidate_value": scenario["candidate_value"],
            }
        )
    return cases


def compute_baseline_metrics(rows: list[list[float]]) -> dict[str, float]:
    """Compute simple entropy, margin, switch-rate, and drift baselines."""
    normalized = normalize_probability_rows(rows)
    entropies: list[float] = []
    margins: list[float] = []
    top_indices: list[int] = []
    for row in normalized:
        sorted_row = sorted(row, reverse=True)
        entropies.append(-sum(value * math.log(value) for value in row if value > 0))
        margins.append(sorted_row[0] - sorted_row[1] if len(sorted_row) > 1 else sorted_row[0])
        top_indices.append(max(range(len(row)), key=row.__getitem__))
    switch_count = sum(1 for left, right in zip(top_indices, top_indices[1:]) if left != right)
    switch_rate = switch_count / max(len(top_indices) - 1, 1)
    midpoint = max(len(normalized) // 2, 1)
    first_mean = _column_means(normalized[:midpoint])
    second_mean = _column_means(normalized[midpoint:])
    half_window_euclidean_drift = math.sqrt(sum((a - b) ** 2 for a, b in zip(first_mean, second_mean)))
    return {
        "mean_entropy": sum(entropies) / len(entropies),
        "entropy_variance": _variance(entropies),
        "mean_margin": sum(margins) / len(margins),
        "min_margin": min(margins),
        "top_label_switch_rate": switch_rate,
        "half_window_euclidean_drift": half_window_euclidean_drift,
    }


def diagnose_probability_cloud(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a transparent public-demo diagnostic for one probability cloud.

    This mirrors the article demo behavior. It is a teaching scaffold, not the
    full private Decision-PGA research package.
    """
    report = validate_probability_payload(payload)
    if not report["valid"]:
        raise ValueError("; ".join(report["errors"]))
    labels = list(payload["labels"])
    rows = normalize_probability_rows(payload["probabilities"])
    baseline = compute_baseline_metrics(rows)
    mean_probability = _column_means(rows)
    top_labels = [
        labels[index]
        for index in sorted(range(len(labels)), key=lambda index: mean_probability[index], reverse=True)
    ]
    first_top = max(range(len(rows[0])), key=rows[0].__getitem__)
    last_top = max(range(len(rows[-1])), key=rows[-1].__getitem__)

    if baseline["half_window_euclidean_drift"] > 0.6:
        state = "regime_shift"
        rationale = "Early and late observations favor different workflow actions."
    elif baseline["half_window_euclidean_drift"] > 0.12 and baseline["mean_margin"] < 0.12:
        state = "boundary_sensitive"
        rationale = "Samples move across a low-margin decision boundary."
    elif baseline["mean_margin"] > 0.60 and baseline["top_label_switch_rate"] == 0.0:
        state = "stable"
        rationale = "Repeated observations favor the same action with a large margin."
    elif baseline["top_label_switch_rate"] >= 0.5 and baseline["mean_margin"] < 0.08:
        state = "binary_ambiguity"
        rationale = "The cloud is mostly split between two leading actions."
    else:
        state = "diffuse_uncertainty"
        rationale = "No stronger stable, binary, sensitive, or drifting pattern dominates."

    return {
        "label": payload["label"],
        "state": state,
        "workflow_action": ACTION_MAP[state],
        "rationale": rationale,
        "labels": labels,
        "top_labels": top_labels[:3],
        "mean_probability": mean_probability,
        "top_action_sequence": [labels[max(range(len(row)), key=row.__getitem__)] for row in rows],
        "metrics": baseline
        | {
            "sample_count": float(len(rows)),
            "first_top_index": float(first_top),
            "last_top_index": float(last_top),
        },
    }


def _column_means(rows: list[list[float]]) -> list[float]:
    width = len(rows[0])
    return [sum(row[index] for row in rows) / len(rows) for index in range(width)]


def _variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / len(values)
```

- [ ] **Step 5: Run tests and tune thresholds only if needed**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: all tests pass. If the expected demo state test fails, inspect the printed metric values and adjust only the explicit thresholds in `diagnose_probability_cloud`; do not change fixture data in this task.

- [ ] **Step 6: Commit**

```bash
git add demo_support tests
git commit -m "Add public demo diagnostics"
```

---

### Task 3: Add Plotting Helpers And Plot Smoke Tests

**Files:**
- Modify: `demo_support/__init__.py`
- Modify: `demo_support/document_triage.py`
- Modify: `tests/test_document_triage_support.py`

- [ ] **Step 1: Add failing plotting tests**

Append to `tests/test_document_triage_support.py`:

```python
from demo_support.document_triage import (
    plot_mean_probability,
    plot_metric_comparison,
    plot_top_action_sequence,
)


class PlottingTests(unittest.TestCase):
    def test_plot_helpers_return_figures(self) -> None:
        cases = load_demo_scenarios(FIXTURE)
        diagnostics = [diagnose_probability_cloud(case) for case in cases]
        figures = [
            plot_mean_probability(diagnostics[0]),
            plot_top_action_sequence(diagnostics[1]),
            plot_metric_comparison(diagnostics),
        ]
        for figure in figures:
            self.assertTrue(hasattr(figure, "savefig"))
            figure.clf()
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: fail with missing plotting imports.

- [ ] **Step 3: Add plotting exports**

Modify `demo_support/__init__.py` to import and export:

```python
    plot_mean_probability,
    plot_metric_comparison,
    plot_top_action_sequence,
```

Ensure `__all__` includes the same names.

- [ ] **Step 4: Add plotting implementation**

Append to `demo_support/document_triage.py`:

```python
ACTION_COLORS = {
    "accept_extraction": "#2f7d73",
    "ask_for_clarification": "#d6a437",
    "retrieve_more_context": "#2f6f9f",
    "flag_for_review": "#c7643a",
    "defer": "#6456a3",
}

ACTION_SHORT = {
    "accept_extraction": "accept",
    "ask_for_clarification": "clarify",
    "retrieve_more_context": "retrieve",
    "flag_for_review": "review",
    "defer": "defer",
}


def plot_mean_probability(diagnostic: dict[str, Any]):
    """Return a horizontal mean-probability bar chart for one diagnostic."""
    import matplotlib.pyplot as plt

    labels = diagnostic["labels"]
    values = diagnostic["mean_probability"]
    colors = [ACTION_COLORS.get(label, "#64748b") for label in labels]
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.barh([ACTION_SHORT.get(label, label) for label in labels], values, color=colors)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Mean probability")
    ax.set_title(str(diagnostic["label"]).replace("_", " "))
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    return fig


def plot_top_action_sequence(diagnostic: dict[str, Any]):
    """Return a strip plot of the top action across observations."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    sequence = diagnostic["top_action_sequence"]
    fig, ax = plt.subplots(figsize=(8, 1.8))
    for index, action in enumerate(sequence):
        ax.add_patch(Rectangle((index, 0), 0.92, 1.0, color=ACTION_COLORS.get(action, "#64748b")))
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Observation")
    ax.set_title("Top action sequence")
    fig.tight_layout()
    return fig


def plot_metric_comparison(diagnostics: list[dict[str, Any]]):
    """Return a compact metric comparison heatmap across scenarios."""
    import matplotlib.pyplot as plt
    import numpy as np

    metric_names = [
        "mean_entropy",
        "mean_margin",
        "top_label_switch_rate",
        "half_window_euclidean_drift",
    ]
    matrix = np.array([[diagnostic["metrics"][name] for name in metric_names] for diagnostic in diagnostics], dtype=float)
    scaled = matrix.copy()
    for column in range(scaled.shape[1]):
        column_min = float(scaled[:, column].min())
        column_max = float(scaled[:, column].max())
        if column_max > column_min:
            scaled[:, column] = (scaled[:, column] - column_min) / (column_max - column_min)
        else:
            scaled[:, column] = 0.0
    fig, ax = plt.subplots(figsize=(9, 3.2))
    image = ax.imshow(scaled, aspect="auto", cmap="viridis")
    ax.set_yticks(range(len(diagnostics)), [str(item["label"]).replace("_", " ") for item in diagnostics])
    ax.set_xticks(range(len(metric_names)), [name.replace("_", " ") for name in metric_names], rotation=30, ha="right")
    ax.set_title("Relative metric comparison")
    fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02, label="Column-scaled value")
    fig.tight_layout()
    return fig
```

- [ ] **Step 5: Install demo dependencies and run tests**

Run:

```bash
python3 -m pip install -r requirements-demo.txt
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: all tests pass and matplotlib figure smoke tests succeed.

- [ ] **Step 6: Commit**

```bash
git add demo_support tests
git commit -m "Add document triage demo plots"
```

---

### Task 4: Add User Data Template

**Files:**
- Create: `examples/document-triage/user_cloud_template.json`
- Modify: `tests/test_document_triage_support.py`

- [ ] **Step 1: Add failing template test**

Append to `tests/test_document_triage_support.py`:

```python
TEMPLATE = ROOT / "examples" / "document-triage" / "user_cloud_template.json"


class UserTemplateTests(unittest.TestCase):
    def test_user_template_is_valid_and_has_guidance_fields(self) -> None:
        payload = load_probability_payload(TEMPLATE)
        report = validate_probability_payload(payload)
        self.assertTrue(report["valid"], report)
        self.assertIn("description", payload)
        self.assertIn("row_meaning", payload)
        self.assertIn("labels_meaning", payload)
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: fail because `examples/document-triage/user_cloud_template.json` does not exist.

- [ ] **Step 3: Create template**

Create `examples/document-triage/user_cloud_template.json`:

```json
{
  "label": "my_document_decision_case",
  "description": "Replace this example with one decision point from your workflow. The rows should all describe repeated observations of the same decision point.",
  "row_meaning": "Each row is one repeated model sample, score pass, reviewer vote, perturbation, rule check, or agent step.",
  "labels_meaning": "Each label is one candidate action, class, extracted value, or workflow state. Keep the label order fixed for every row.",
  "labels": [
    "accept_extraction",
    "ask_for_clarification",
    "retrieve_more_context",
    "flag_for_review",
    "defer"
  ],
  "probabilities": [
    [0.80, 0.08, 0.04, 0.06, 0.02],
    [0.76, 0.10, 0.05, 0.07, 0.02],
    [0.82, 0.07, 0.04, 0.05, 0.02],
    [0.78, 0.09, 0.05, 0.06, 0.02],
    [0.81, 0.08, 0.04, 0.05, 0.02]
  ]
}
```

- [ ] **Step 4: Run tests**

Run:

```bash
python3 -m unittest tests/test_document_triage_support.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add examples/document-triage/user_cloud_template.json tests
git commit -m "Add user probability cloud template"
```

---

### Task 5: Add Notebook Execution Helper

**Files:**
- Create: `scripts/execute_notebook.py`
- Create: `tests/test_execute_notebook_script.py`

- [ ] **Step 1: Add failing script test**

Create `tests/test_execute_notebook_script.py`:

```python
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "execute_notebook.py"


class ExecuteNotebookScriptTests(unittest.TestCase):
    def test_missing_notebook_returns_machine_readable_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing.ipynb"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(missing)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('"ok": false', result.stderr)
        self.assertIn("Notebook not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```bash
python3 -m unittest tests/test_execute_notebook_script.py -v
```

Expected: fail because `scripts/execute_notebook.py` does not exist.

- [ ] **Step 3: Create notebook execution helper**

Create `scripts/execute_notebook.py`:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"ok": False, "error": "Usage: execute_notebook.py NOTEBOOK"}), file=sys.stderr)
        return 2
    notebook_path = Path(argv[1])
    if not notebook_path.exists():
        print(json.dumps({"ok": False, "error": f"Notebook not found: {notebook_path}"}), file=sys.stderr)
        return 2
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(notebook_path.parent)}},
    )
    client.execute()
    print(json.dumps({"ok": True, "notebook": str(notebook_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run script test**

Run:

```bash
python3 -m unittest tests/test_execute_notebook_script.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/execute_notebook.py tests/test_execute_notebook_script.py
git commit -m "Add notebook execution helper"
```

---

### Task 6: Add Guided Notebook

**Files:**
- Create: `notebooks/document_extraction_triage_demo.ipynb`
- Create: `notebooks/README.md`

- [ ] **Step 1: Create notebook README**

Create `notebooks/README.md`:

```markdown
# Decision-PGA Document Extraction Triage Notebook

This folder contains the runnable companion notebook for the public
Decision-PGA article demo.

Run locally from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-demo.txt
python scripts/execute_notebook.py notebooks/document_extraction_triage_demo.ipynb
```

The notebook uses synthetic demonstration data only. It does not call model
APIs, does not use patient data, and is not clinical validation.
```

- [ ] **Step 2: Create notebook with these cells**

Create `notebooks/document_extraction_triage_demo.ipynb` as a valid notebook with this section sequence and code cells:

Markdown cell:

```markdown
# Decision-PGA Document Extraction Triage Demo

This notebook reproduces the public article companion demo with synthetic
probability clouds. It is a teaching scaffold: it helps you inspect decision
state shapes, compare simple baselines, and try a user-defined probability
cloud. It is not a document parser, benchmark, clinical validation, or
production safety layer.
```

Code cell:

```python
from pathlib import Path
import sys

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT))

from demo_support.document_triage import (
    diagnose_probability_cloud,
    load_demo_scenarios,
    load_probability_payload,
    plot_mean_probability,
    plot_metric_comparison,
    plot_top_action_sequence,
    validate_probability_payload,
)

FIXTURE = ROOT / "examples" / "document-triage" / "demo_cases.json"
TEMPLATE = ROOT / "examples" / "document-triage" / "user_cloud_template.json"
```

Markdown cell:

```markdown
## What the matrix means

Rows are repeated observations of one decision point. Columns are candidate
actions, labels, values, or workflow states. Every row should use the same
column order and should contain nonnegative probability-like values.
```

Code cell:

```python
cases = load_demo_scenarios(FIXTURE)
cases[0]["labels"], cases[0]["probabilities"][:3]
```

Markdown cell:

```markdown
## Run the built-in demo cases
```

Code cell:

```python
diagnostics = [diagnose_probability_cloud(case) for case in cases]
[(item["label"], item["state"], item["workflow_action"], item["top_labels"]) for item in diagnostics]
```

Markdown cell:

```markdown
## Plot one case
```

Code cell:

```python
fig = plot_mean_probability(diagnostics[0])
fig
```

Code cell:

```python
fig = plot_top_action_sequence(diagnostics[1])
fig
```

Markdown cell:

```markdown
## Compare metrics across scenarios
```

Code cell:

```python
fig = plot_metric_comparison(diagnostics)
fig
```

Markdown cell:

```markdown
## Try user-defined data

Edit `examples/document-triage/user_cloud_template.json` or copy it to a new
file. The labels should describe the candidate decisions/actions/classes. The
probability rows should be repeated observations of the same decision point.
```

Code cell:

```python
user_payload = load_probability_payload(TEMPLATE)
validation = validate_probability_payload(user_payload)
validation
```

Code cell:

```python
if not validation["valid"]:
    raise ValueError(validation)
user_diagnostic = diagnose_probability_cloud(user_payload)
user_diagnostic
```

Code cell:

```python
fig = plot_mean_probability(user_diagnostic)
fig
```

Markdown cell:

```markdown
## Interpretation limits

The diagnostic describes the shape of a probability cloud. It does not know
ground truth, task stakes, policy thresholds, clinical validity, or whether the
candidate labels were well chosen.
```

Use `nbformat` from a short temporary script if manual JSON editing is
error-prone, but commit only the finished `.ipynb`.

- [ ] **Step 3: Execute notebook**

Run:

```bash
python3 scripts/execute_notebook.py notebooks/document_extraction_triage_demo.ipynb
```

Expected output contains:

```json
{"ok": true, "notebook": "notebooks/document_extraction_triage_demo.ipynb"}
```

- [ ] **Step 4: Commit**

```bash
git add notebooks
git commit -m "Add guided document triage notebook"
```

---

### Task 7: Link Notebook Kit From Public Site

**Files:**
- Modify: `demo.md`
- Modify: `README.md`
- Modify: `releases/v0.1-publication.md`

- [ ] **Step 1: Add demo page "Run This Demo" section**

Insert after the fixture/result links in `demo.md`:

```markdown
## Run This Demo

The demo now has a local-first companion notebook:
[notebooks/document_extraction_triage_demo.ipynb]({{ '/notebooks/document_extraction_triage_demo.ipynb' | relative_url }}).

To run it from a local checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-demo.txt
python scripts/execute_notebook.py notebooks/document_extraction_triage_demo.ipynb
```

To try your own probability cloud, start from:
[examples/document-triage/user_cloud_template.json]({{ '/examples/document-triage/user_cloud_template.json' | relative_url }}).

The notebook is designed to be Colab-ready once the public demo API settles,
but v1 is local-first so the examples remain transparent and reproducible.
```

- [ ] **Step 2: Update README contents list and local commands**

Modify `README.md` so `## Contents` includes:

```markdown
- `notebooks/document_extraction_triage_demo.ipynb` - runnable companion notebook
- `examples/document-triage/user_cloud_template.json` - user-editable probability-cloud template
- `requirements-demo.txt` - notebook dependency set
```

Add a section:

```markdown
## Run The Guided Demo Notebook

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-demo.txt
python scripts/execute_notebook.py notebooks/document_extraction_triage_demo.ipynb
```

The notebook uses synthetic demonstration data only. It does not call model
APIs, does not use patient data, and is not clinical validation.
```

- [ ] **Step 3: Update release notes**

Add to `releases/v0.1-publication.md`:

```markdown
## Runnable Demo Kit

- Added a local-first companion notebook for the document extraction triage demo.
- Added a user-editable probability-cloud template.
- Added public demo-support helpers for validation, baseline metrics, and plots.
- Kept the implementation synthetic and local; no model APIs or private data are used.
```

- [ ] **Step 4: Run publication validation**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected: pass.

- [ ] **Step 5: Commit**

```bash
git add demo.md README.md releases/v0.1-publication.md
git commit -m "Link guided notebook demo kit"
```

---

### Task 8: Extend Publication Validation And CI

**Files:**
- Modify: `scripts/validate_publication.py`
- Modify: `.github/workflows/validate.yml`

- [ ] **Step 1: Extend publication validator required files**

Modify `REQUIRED_FILES` in `scripts/validate_publication.py` to include:

```python
    "demo_support/__init__.py",
    "demo_support/document_triage.py",
    "examples/document-triage/user_cloud_template.json",
    "notebooks/README.md",
    "notebooks/document_extraction_triage_demo.ipynb",
    "requirements-demo.txt",
    "scripts/execute_notebook.py",
```

- [ ] **Step 2: Extend demo required phrases**

Add these phrases to the `demo` phrase loop:

```python
        "Run This Demo",
        "document_extraction_triage_demo.ipynb",
        "user_cloud_template.json",
        "Colab-ready",
```

- [ ] **Step 3: Validate the user template**

Add after fixture validation:

```python
    template = json.loads((ROOT / "examples/document-triage/user_cloud_template.json").read_text(encoding="utf-8"))
    require(template["label"] == "my_document_decision_case", "Unexpected user template label")
    require(template["labels"] == DEMO_REQUIRED_ACTIONS, "User template labels should match demo actions")
    for row in template["probabilities"]:
        require(len(row) == len(DEMO_REQUIRED_ACTIONS), "User template row width mismatch")
        require(abs(sum(row) - 1.0) < 1e-9, "User template probabilities should sum to 1")
        require(all(value > 0 for value in row), "User template should contain positive values")
```

- [ ] **Step 4: Update CI workflow**

Modify `.github/workflows/validate.yml`:

```yaml
name: Validate publication site

on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -r requirements-demo.txt
      - run: python -m unittest discover -s tests -v
      - run: python scripts/execute_notebook.py notebooks/document_extraction_triage_demo.ipynb
      - run: python scripts/validate_publication.py
```

- [ ] **Step 5: Run local CI equivalent**

Run:

```bash
python3 -m pip install -r requirements-demo.txt
python3 -m unittest discover -s tests -v
python3 scripts/execute_notebook.py notebooks/document_extraction_triage_demo.ipynb
python3 scripts/validate_publication.py
git diff --check
```

Expected: all commands pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_publication.py .github/workflows/validate.yml
git commit -m "Validate guided demo notebook kit"
```

---

### Task 9: Final Browser And Release Verification

**Files:**
- No required source edits unless verification finds a defect.

- [ ] **Step 1: Push branch**

Run:

```bash
git push
```

Expected: push succeeds.

- [ ] **Step 2: Watch GitHub Actions**

Run:

```bash
gh run list --repo zmichels/decision-pga-pages --limit 5
gh run watch <latest-validate-run-id> --repo zmichels/decision-pga-pages --exit-status
gh run watch <latest-pages-run-id> --repo zmichels/decision-pga-pages --exit-status
```

Expected: validation and Pages deployment both succeed.

- [ ] **Step 3: Browser QA the public demo page**

Open:

```text
https://zmichels.github.io/decision-pga-pages/demo/?qa=<final-commit-sha>
```

Check:

- page title is `Document Extraction Triage Demo | Decision-PGA Publication`;
- "Run This Demo" section is visible;
- notebook link points to `/notebooks/document_extraction_triage_demo.ipynb`;
- template link points to `/examples/document-triage/user_cloud_template.json`;
- no relevant console errors or warnings;
- desktop and mobile widths have no page-level horizontal overflow.

- [ ] **Step 4: Final repository cleanliness check**

Run:

```bash
git status --short
rg -n "Ma""yo|TO""DO|T""BD" . --glob '!drafts/**' --glob '!.git/**' --glob '!.publication-build/**' --glob '!assets/decision-pga-decision-state-diagnostics.pdf' || true
```

Expected: `git status --short` has no tracked changes and `rg` returns no active-publication matches.

---

## Self-Review

Spec coverage:

- Local-first notebook: Task 6.
- Colab-ready path without overbuilding: Task 7 documentation.
- User-data template and clear data contract: Task 4 and Task 7.
- Validation helper: Task 1 and Task 8.
- Comparative plots: Task 3 and Task 6.
- Site integration: Task 7 and Task 8.
- CI/local acceptance: Task 8 and Task 9.
- No model APIs, no private data, no clinical validation claims: Tasks 6, 7, 8, and 9.

Placeholder scan:

- No unresolved placeholders or unspecified error-handling steps are used.

Type consistency:

- The same public payload fields are used throughout: `label`, `labels`, `probabilities`.
- The same diagnostic fields are used throughout: `state`, `workflow_action`, `top_labels`, `mean_probability`, `top_action_sequence`, `metrics`.
