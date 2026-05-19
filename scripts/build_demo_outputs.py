from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "document-triage" / "demo_cases.json"
RESULTS = ROOT / "examples" / "document-triage" / "demo_results.json"
SVG = ROOT / "assets" / "document-triage-demo-overview.svg"
PRIVATE_PACKAGE_ROOT = Path("/Users/Z/Documents/Decision-PGA")


STATE_DISPLAY = {
    "stable": "stable",
    "binary_ambiguity": "binary ambiguous",
    "diffuse_uncertainty": "diffuse",
    "boundary_sensitive": "boundary-sensitive",
    "regime_shift": "drifting",
}


ACTION_MAP = {
    "proceed": "accept_extraction",
    "clarify_between_top_labels": "ask_for_clarification",
    "gather_more_evidence": "retrieve_more_context",
    "inspect_sensitivity": "flag_for_review",
    "segment_or_replan": "defer",
}


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


def main() -> int:
    package_path = PRIVATE_PACKAGE_ROOT
    if package_path.exists():
        sys.path.insert(0, str(package_path))
    try:
        from decision_pga.diagnostics import diagnose_probability_cloud
    except ImportError as exc:
        raise SystemExit(
            "Could not import decision_pga. Run this from the local publication "
            "workspace where /Users/Z/Documents/Decision-PGA is available, or "
            "install decision-pga into the active Python environment."
        ) from exc

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    labels = fixture["labels"]
    scenarios = []
    for scenario in fixture["scenarios"]:
        diagnostic = diagnose_probability_cloud(
            scenario["observations"],
            labels=labels,
            label=scenario["id"],
        )
        diag_payload = diagnostic.to_dict()
        metrics = diag_payload["metrics"]
        mean_probability = [
            round(float(value), 6)
            for value in diagnostic.pga_result.mean_probability
        ]
        workflow_action = ACTION_MAP[diag_payload["recommended_action"]]
        scenarios.append(
            {
                "id": scenario["id"],
                "name": scenario["name"],
                "document_context": scenario["document_context"],
                "candidate_value": scenario["candidate_value"],
                "diagnostic_state": diag_payload["state"],
                "display_state": STATE_DISPLAY[diag_payload["state"]],
                "diagnostic_action": diag_payload["recommended_action"],
                "workflow_action": workflow_action,
                "expected_action": scenario["expected_action"],
                "top_labels": diag_payload["top_labels"][:3],
                "mean_probability": mean_probability,
                "top_action_sequence": [
                    labels[max(range(len(row)), key=lambda index: row[index])]
                    for row in scenario["observations"]
                ],
                "metrics": {
                    "total_dispersion": round(float(metrics["total_dispersion"]), 6),
                    "pc1_fraction": round(float(metrics["pc1_fraction"]), 6),
                    "mean_margin": round(float(metrics["mean_margin"]), 6),
                    "half_geodesic_distance": round(float(metrics["half_geodesic_distance"]), 6),
                    "top_label_switch_rate": round(float(metrics["top_label_switch_rate"]), 6),
                },
                "rationale": diag_payload["rationale"],
            }
        )

    result_payload = {
        "schema_version": "decision-pga-document-triage-results-v1",
        "source_fixture": "examples/document-triage/demo_cases.json",
        "method": "Generated with the local Decision-PGA diagnostic prototype.",
        "labels": labels,
        "scenarios": scenarios,
    }
    RESULTS.write_text(json.dumps(result_payload, indent=2) + "\n", encoding="utf-8")
    SVG.write_text(render_svg(labels, scenarios), encoding="utf-8")
    print(RESULTS)
    print(SVG)
    return 0


def render_svg(labels: list[str], scenarios: list[dict[str, object]]) -> str:
    width = 1120
    row_height = 178
    header_height = 122
    footer_height = 86
    height = header_height + row_height * len(scenarios) + footer_height
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">Document extraction triage demo</title>",
        "<desc id=\"desc\">Synthetic Decision-PGA probability-cloud scenarios mapped to diagnostic states and workflow actions.</desc>",
        "<defs><marker id=\"arrowhead\" viewBox=\"0 0 12 12\" refX=\"10\" refY=\"6\" markerWidth=\"9\" markerHeight=\"9\" orient=\"auto\"><path d=\"M 0 0 L 12 6 L 0 12 z\" fill=\"#236a7c\"/></marker></defs>",
        "<rect width=\"1120\" height=\"100%\" fill=\"#f7f8fb\"/>",
        "<style>text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.small{font-size:13px;fill:#5d687a}.label{font-size:12px;font-weight:750;letter-spacing:.03em;text-transform:uppercase}.title{font-size:30px;font-weight:800;fill:#172033}.h{font-size:19px;font-weight:800;fill:#172033}.metric{font-size:13px;fill:#172033}.mono{font-family:'SFMono-Regular',Consolas,monospace;font-size:12px}</style>",
        "<text x=\"40\" y=\"52\" class=\"title\">Document extraction triage demo</text>",
        "<text x=\"40\" y=\"82\" class=\"small\">Synthetic probability clouds over five workflow actions, diagnosed by the local Decision-PGA prototype.</text>",
    ]
    x = 40
    for index, label in enumerate(labels):
        legend_x = x + index * 190
        parts.append(f'<rect x="{legend_x}" y="98" width="14" height="14" rx="3" fill="{ACTION_COLORS[label]}"/>')
        parts.append(f'<text x="{legend_x + 20}" y="110" class="small">{esc(ACTION_SHORT[label])}</text>')

    y = header_height
    for scenario in scenarios:
        parts.extend(render_scenario(labels, scenario, y))
        y += row_height

    parts.append(f'<text x="40" y="{height - 42}" class="small">Read left to right: synthetic document situation -> mean action probabilities -> Decision-PGA state -> workflow action.</text>')
    parts.append(f'<text x="40" y="{height - 20}" class="small">This is an illustrative diagnostic walkthrough, not a document parser, benchmark, or clinical validation.</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_scenario(labels: list[str], scenario: dict[str, object], y: int) -> list[str]:
    card_y = y + 12
    card_h = 154
    name = str(scenario["name"])
    context = str(scenario["document_context"])
    state = str(scenario["display_state"])
    workflow_action = str(scenario["workflow_action"])
    metrics = scenario["metrics"]
    mean_probability = scenario["mean_probability"]
    sequence = scenario["top_action_sequence"]
    row = [
        f'<rect x="28" y="{card_y}" width="1064" height="{card_h}" rx="12" fill="#ffffff" stroke="#dbe1ea"/>',
        f'<text x="52" y="{card_y + 34}" class="h">{esc(name)}</text>',
        f'<text x="52" y="{card_y + 58}" class="small">{esc(shorten(context, 84))}</text>',
    ]

    bar_x = 52
    bar_y = card_y + 82
    bar_w = 410
    bar_h = 24
    offset = 0.0
    for label, probability in zip(labels, mean_probability):
        segment_w = float(probability) * bar_w
        row.append(
            f'<rect x="{bar_x + offset:.2f}" y="{bar_y}" width="{max(segment_w, 1.0):.2f}" height="{bar_h}" fill="{ACTION_COLORS[label]}"/>'
        )
        offset += segment_w
    row.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" fill="none" stroke="#172033" stroke-opacity=".18"/>')
    row.append(f'<text x="{bar_x}" y="{bar_y + 46}" class="small">mean action probabilities</text>')

    seq_x = 52
    seq_y = card_y + 132
    for index, action in enumerate(sequence):
        row.append(f'<rect x="{seq_x + index * 22}" y="{seq_y}" width="16" height="16" rx="3" fill="{ACTION_COLORS[action]}"/>')
    row.append(f'<text x="{seq_x + len(sequence) * 22 + 8}" y="{seq_y + 13}" class="small">top action sequence</text>')

    arrow_x = 506
    row.extend(
        [
            f'<path d="M {arrow_x} {card_y + 76} L {arrow_x + 78} {card_y + 76}" fill="none" stroke="#236a7c" stroke-width="3" marker-end="url(#arrowhead)"/>',
            f'<rect x="610" y="{card_y + 38}" width="190" height="78" rx="10" fill="#eef8fa" stroke="#b7d1d8"/>',
            f'<text x="705" y="{card_y + 68}" text-anchor="middle" class="label" fill="#174a59">state</text>',
            f'<text x="705" y="{card_y + 94}" text-anchor="middle" font-size="18" font-weight="800" fill="#174a59">{esc(state)}</text>',
            f'<rect x="832" y="{card_y + 38}" width="210" height="78" rx="10" fill="#fff8e9" stroke="#e5c878"/>',
            f'<text x="937" y="{card_y + 68}" text-anchor="middle" class="label" fill="#6f4f12">workflow action</text>',
            f'<text x="937" y="{card_y + 94}" text-anchor="middle" font-size="17" font-weight="800" fill="#6f4f12">{esc(ACTION_SHORT[workflow_action])}</text>',
        ]
    )

    metric_text = (
        f"dispersion {float(metrics['total_dispersion']):.3f}  "
        f"PC1 {float(metrics['pc1_fraction']):.2f}  "
        f"margin {float(metrics['mean_margin']):.2f}  "
        f"drift {float(metrics['half_geodesic_distance']):.2f}"
    )
    row.append(f'<text x="610" y="{card_y + 137}" class="metric">{esc(metric_text)}</text>')
    return row


def shorten(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "..."


def esc(value: str) -> str:
    return html.escape(value, quote=True)


if __name__ == "__main__":
    raise SystemExit(main())
