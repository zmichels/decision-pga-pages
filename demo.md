---
layout: default
title: Document Extraction Triage Demo
description: A synthetic Decision-PGA demo for routing document extraction workflows by decision-state shape.
permalink: /demo/
---

# Document Extraction Triage Demo

This demo uses **synthetic demonstration data** to make the Decision-PGA idea
more concrete. The setting is a familiar document extraction workflow: an AI
system proposes or reviews an extracted field, then needs to choose what the
workflow should do next.

The point is not that Decision-PGA extracts the field. The point is that a
Decision-PGA-style diagnostic can describe the *shape* of uncertainty around
the next workflow action.

This page uses no patient data, is not clinical validation, and is not a
clinical decision support demonstration.

## Action Vocabulary

Each synthetic observation is a probability-like vector over five possible next
actions:

| Action | Plain meaning |
|---|---|
| `accept_extraction` | The extracted value appears stable enough for the workflow to continue. |
| `ask_for_clarification` | The workflow is mainly split between a small number of plausible meanings. |
| `retrieve_more_context` | The workflow needs another page, attachment, source, or evidence snippet. |
| `flag_for_review` | The value may be usable, but the risk or threshold context deserves review. |
| `defer` | The workflow state is changing enough that action should pause pending re-evaluation. |

The fixture is available as JSON:
[examples/document-triage/demo_cases.json]({{ '/examples/document-triage/demo_cases.json' | relative_url }}).

Generated diagnostic outputs are also available:
[examples/document-triage/demo_results.json]({{ '/examples/document-triage/demo_results.json' | relative_url }}).

## How to read the matrices

Each row is one synthetic observation: one repeated model sample, score pass,
review vote, perturbation, or agent step. The row values are probabilities over
the possible next workflow actions, and each row sums to 1.00.

The columns always follow this order:

<div class="column-order" aria-label="Probability table columns">
  <span><strong>1</strong> accept_extraction</span>
  <span><strong>2</strong> ask_for_clarification</span>
  <span><strong>3</strong> retrieve_more_context</span>
  <span><strong>4</strong> flag_for_review</span>
  <span><strong>5</strong> defer</span>
</div>

So the row `[0.92, 0.03, 0.02, 0.02, 0.01]` means: this observation puts
0.92 probability on `accept_extraction`, 0.03 on `ask_for_clarification`, and
so on. Decision-PGA reads the full matrix as one probability cloud. It does not
diagnose the rows one at a time.

## How To Use The Demo

1. Pick a document extraction scenario.
2. Read the column-labeled probability table.
3. Treat the table as the input cloud for Decision-PGA.
4. Compare the generated diagnostic readout with the simpler visual intuition.
5. Route the workflow using the mapped action.

In a future code-backed demo, the probability cloud would come from repeated
model samples, model-score adapters, reviewer votes, rule checks, or an agent
trace. For this public article companion, the values are intentionally clean so
the states are easy to see.

## Try one case as a diagnostic payload

This is the shape of the first case as a Decision-PGA diagnostic request. The
demo page is static, but this is the same structure a CLI, notebook, MCP tool,
or agent wrapper would pass to the prototype.

```json
{
  "source": "probability_cloud",
  "label": "clean_invoice_due_date",
  "labels": [
    "accept_extraction",
    "ask_for_clarification",
    "retrieve_more_context",
    "flag_for_review",
    "defer"
  ],
  "probabilities": [
    [0.92, 0.03, 0.02, 0.02, 0.01],
    [0.91, 0.04, 0.02, 0.02, 0.01],
    [0.94, 0.02, 0.01, 0.02, 0.01]
  ]
}
```

The generated readout for the full eight-row fixture is:

```json
{
  "state": "stable",
  "recommended_action": "proceed",
  "demo_workflow_action": "accept_extraction",
  "top_labels": ["accept_extraction", "ask_for_clarification", "flag_for_review"]
}
```

## Scenario Summary

The summary uses short action labels to stay readable. The full action names
are listed above in the Action Vocabulary and repeated in the scenario readouts.

| Scenario | Expected decision state | Workflow action | Demo intuition |
|---|---|---|---|
| Clean invoice due date | stable | accept | Repeated observations point to the same action. |
| Two plausible contract dates | binary ambiguous | clarify | The workflow is mostly split between two choices. |
| Missing attachment reference | diffuse | retrieve | Uncertainty is scattered because the evidence is incomplete. |
| Near-threshold total | boundary-sensitive | review | Small perturbations alter whether to accept or review. |
| Contradictory revision packet | drifting | defer | The preferred action changes over the read sequence. |

## Visual Walkthrough

The overview below connects each synthetic document situation to the mean action
probabilities, the top action sequence across observations, the Decision-PGA
state, and the workflow action.

<figure class="diagram-figure">
  <img src="{{ '/assets/document-triage-demo-overview.svg?v=20260519-demo-output' | relative_url }}" alt="Document extraction triage visual summary showing synthetic probability clouds mapped to decision states and workflow actions.">
  <figcaption>
    Each row uses the same action vocabulary. The colored bar summarizes mean
    action probability, the small squares show which action was top-ranked in
    each observation, and the right side shows the diagnostic state mapped to a
    workflow action.
  </figcaption>
</figure>

<section class="scenario-list">
  <article class="scenario-card">
    <div class="state-label">stable -> accept_extraction</div>
    <h2>Clean invoice due date</h2>
    <p>
      A vendor invoice shows a clearly labeled due date near the payment total.
      The observations form a tight cloud around <code>accept_extraction</code>.
    </p>
    <div class="scenario-detail-grid">
      <div>
        <h3>Input cloud sample</h3>
        <div class="table-wrap">
          <table class="probability-table">
            <thead>
              <tr><th>obs</th><th>accept</th><th>clarify</th><th>retrieve</th><th>review</th><th>defer</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>0.92</td><td>0.03</td><td>0.02</td><td>0.02</td><td>0.01</td></tr>
              <tr><td>2</td><td>0.91</td><td>0.04</td><td>0.02</td><td>0.02</td><td>0.01</td></tr>
              <tr><td>3</td><td>0.94</td><td>0.02</td><td>0.01</td><td>0.02</td><td>0.01</td></tr>
            </tbody>
          </table>
        </div>
        <p class="microcopy">Full fixture: 8 rows x 5 action columns.</p>
      </div>
      <div class="diagnostic-readout">
        <h3>Generated diagnostic readout</h3>
        <dl>
          <dt>Decision-PGA state</dt><dd>stable</dd>
          <dt>Workflow action</dt><dd><code>accept_extraction</code></dd>
          <dt>Mean margin</dt><dd>0.90</dd>
          <dt>Dispersion</dt><dd>0.002</dd>
        </dl>
        <p>A tight cloud with a large margin is stable enough for this synthetic workflow to proceed.</p>
      </div>
    </div>
  </article>

  <article class="scenario-card">
    <div class="state-label">binary ambiguous -> ask_for_clarification</div>
    <h2>Two plausible contract dates</h2>
    <p>
      A contract amendment includes both an effective date and a signature date.
      The cloud mostly varies along one axis: accept the extraction, or ask which
      date definition the user intended.
    </p>
    <div class="scenario-detail-grid">
      <div>
        <h3>Input cloud sample</h3>
        <div class="table-wrap">
          <table class="probability-table">
            <thead>
              <tr><th>obs</th><th>accept</th><th>clarify</th><th>retrieve</th><th>review</th><th>defer</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>0.42</td><td>0.45</td><td>0.05</td><td>0.05</td><td>0.03</td></tr>
              <tr><td>2</td><td>0.48</td><td>0.39</td><td>0.05</td><td>0.05</td><td>0.03</td></tr>
              <tr><td>3</td><td>0.38</td><td>0.50</td><td>0.04</td><td>0.05</td><td>0.03</td></tr>
            </tbody>
          </table>
        </div>
        <p class="microcopy">The top action flips between accept and clarify.</p>
      </div>
      <div class="diagnostic-readout">
        <h3>Generated diagnostic readout</h3>
        <dl>
          <dt>Decision-PGA state</dt><dd>binary_ambiguity</dd>
          <dt>Workflow action</dt><dd><code>ask_for_clarification</code></dd>
          <dt>PC1 fraction</dt><dd>0.98</dd>
          <dt>Mean margin</dt><dd>0.01</dd>
        </dl>
        <p>Most variation lies along one axis and the leading actions are nearly tied, so the useful move is a targeted clarification.</p>
      </div>
    </div>
  </article>

  <article class="scenario-card">
    <div class="state-label">diffuse -> retrieve_more_context</div>
    <h2>Missing attachment reference</h2>
    <p>
      A purchase request says the approved amount is in an attached quote, but
      only the cover page is available. The probability mass spreads across
      several actions because the workflow lacks evidence.
    </p>
    <div class="scenario-detail-grid">
      <div>
        <h3>Input cloud sample</h3>
        <div class="table-wrap">
          <table class="probability-table">
            <thead>
              <tr><th>obs</th><th>accept</th><th>clarify</th><th>retrieve</th><th>review</th><th>defer</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>0.18</td><td>0.20</td><td>0.30</td><td>0.18</td><td>0.14</td></tr>
              <tr><td>2</td><td>0.22</td><td>0.17</td><td>0.27</td><td>0.19</td><td>0.15</td></tr>
              <tr><td>3</td><td>0.16</td><td>0.22</td><td>0.29</td><td>0.17</td><td>0.16</td></tr>
            </tbody>
          </table>
        </div>
        <p class="microcopy">No single action dominates the evidence pattern.</p>
      </div>
      <div class="diagnostic-readout">
        <h3>Generated diagnostic readout</h3>
        <dl>
          <dt>Decision-PGA state</dt><dd>diffuse_uncertainty</dd>
          <dt>Workflow action</dt><dd><code>retrieve_more_context</code></dd>
          <dt>PC1 fraction</dt><dd>0.64</dd>
          <dt>Mean margin</dt><dd>0.08</dd>
        </dl>
        <p>The uncertainty is scattered rather than cleanly two-way, so the demo routes toward more context.</p>
      </div>
    </div>
  </article>

  <article class="scenario-card">
    <div class="state-label">boundary-sensitive -> flag_for_review</div>
    <h2>Near-threshold total</h2>
    <p>
      A reimbursement form total is legible, but the extracted value is close to
      an internal manual-review threshold. The safest route is not automatic
      rejection; it is targeted review.
    </p>
    <div class="scenario-detail-grid">
      <div>
        <h3>Input cloud sample</h3>
        <div class="table-wrap">
          <table class="probability-table">
            <thead>
              <tr><th>obs</th><th>accept</th><th>clarify</th><th>retrieve</th><th>review</th><th>defer</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>0.56</td><td>0.03</td><td>0.04</td><td>0.34</td><td>0.03</td></tr>
              <tr><td>2</td><td>0.58</td><td>0.03</td><td>0.04</td><td>0.32</td><td>0.03</td></tr>
              <tr><td>5</td><td>0.38</td><td>0.03</td><td>0.04</td><td>0.52</td><td>0.03</td></tr>
            </tbody>
          </table>
        </div>
        <p class="microcopy">A small context shift moves the top action from accept to review.</p>
      </div>
      <div class="diagnostic-readout">
        <h3>Generated diagnostic readout</h3>
        <dl>
          <dt>Decision-PGA state</dt><dd>boundary_sensitive</dd>
          <dt>Workflow action</dt><dd><code>flag_for_review</code></dd>
          <dt>PC1 fraction</dt><dd>0.97</dd>
          <dt>Half-cloud distance</dt><dd>0.19</dd>
        </dl>
        <p>The samples move coherently along a low-margin boundary, so the demo chooses targeted review.</p>
      </div>
    </div>
  </article>

  <article class="scenario-card">
    <div class="state-label">drifting -> defer</div>
    <h2>Contradictory revision packet</h2>
    <p>
      A multi-page packet starts clean, then later pages introduce a revision
      note and a conflicting total. The sequence matters, so the workflow should
      pause and re-evaluate before acting.
    </p>
    <div class="scenario-detail-grid">
      <div>
        <h3>Input cloud sample</h3>
        <div class="table-wrap">
          <table class="probability-table">
            <thead>
              <tr><th>obs</th><th>accept</th><th>clarify</th><th>retrieve</th><th>review</th><th>defer</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>0.92</td><td>0.03</td><td>0.02</td><td>0.02</td><td>0.01</td></tr>
              <tr><td>4</td><td>0.78</td><td>0.06</td><td>0.05</td><td>0.08</td><td>0.03</td></tr>
              <tr><td>8</td><td>0.02</td><td>0.02</td><td>0.03</td><td>0.10</td><td>0.83</td></tr>
            </tbody>
          </table>
        </div>
        <p class="microcopy">The early rows favor accept; later rows favor defer.</p>
      </div>
      <div class="diagnostic-readout">
        <h3>Generated diagnostic readout</h3>
        <dl>
          <dt>Decision-PGA state</dt><dd>regime_shift</dd>
          <dt>Workflow action</dt><dd><code>defer</code></dd>
          <dt>Dispersion</dt><dd>0.303</dd>
          <dt>Half-cloud distance</dt><dd>1.09</dd>
        </dl>
        <p>The early and late cloud means are far apart, so the demo pauses instead of treating the packet as one static extraction.</p>
      </div>
    </div>
  </article>
</section>

## What This Demonstrates

These examples are deliberately simple. They show how a workflow can benefit
from distinguishing *why* it is uncertain:

- stable uncertainty can be routed differently from ambiguity;
- ambiguity can be routed differently from missing evidence;
- threshold sensitivity can trigger review without treating the whole task as
  failed;
- drift can tell an agent to pause and re-evaluate the trajectory.

That is the practical idea behind Decision-PGA as an agent-facing diagnostic:
turn a cloud of decision evidence into a state description that helps choose the
next workflow action.
