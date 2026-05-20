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

Imagine a small work queue. One document arrives, the AI reads it, and the
workflow has five possible buttons it could press next: accept the extracted
value, ask a person to clarify the meaning, retrieve another source, flag the
case for review, or defer because the packet is changing underneath the system.

The point is not that Decision-PGA extracts the field. The point is that a
Decision-PGA-style diagnostic can describe the *shape* of uncertainty around
which button should be pressed next.

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

The open-source prototype repository is available at
[github.com/zmichels/Decision-PGA](https://github.com/zmichels/Decision-PGA).

## What the numbers stand for

The numbers are not document text. They are the workflow's repeated estimates
of what should happen next after looking at a document situation. In a real
system, those estimates might come from repeated model samples, model logprobs,
rule checks, OCR perturbations, reviewer votes, or an agent trace. In this demo,
they are clean synthetic values so the patterns are easy to see.

You can read each row as one pass through the same case. A row like
`[0.92, 0.03, 0.02, 0.02, 0.01]` says: on this pass, the workflow strongly
leans toward `accept_extraction`. A row like
`[0.42, 0.45, 0.05, 0.05, 0.03]` says: on this pass, the workflow is split
between accepting and asking for clarification.

Decision-PGA does not judge the document itself. It reads the group of rows as
a cloud of next-action evidence, then asks what shape that cloud has.

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

1. Pick a scenario and read the short document story.
2. Look across the rows, not just at one row. Ask whether the same action keeps
   winning, whether two actions trade places, or whether the evidence is
   scattered.
3. Compare that human reading with the generated diagnostic state.
4. Use the mapped workflow action as the practical interpretation.

The useful experience is the contrast between cases. A stable invoice due date
and a missing attachment can both involve uncertainty, but they should lead to
different next actions. The demo is designed to make that difference visible.

## Live Diagnostic Workspace

Choose a case, inspect or edit the probability rows, then run the same kind of
diagnostic that a CLI, notebook, MCP tool, or agent wrapper would pass to the
prototype. The live runner stays entirely in your browser. It does not call a
model, upload data, or contact a server beyond loading this page's synthetic
fixture.

The easiest way to use it is human-first: read the document situation, look at
which action columns are winning across rows, then click **Run diagnostic** and
compare your intuition with the generated state.

You do not need to type numbers to use the demo. Start with the prebuilt
synthetic cases below. The table is editable only so you can poke at the
boundary cases after you have a feel for the workflow.

<section
  class="live-demo"
  data-dpga-demo-runner
  data-fixture-url="{{ '/examples/document-triage/demo_cases.json' | relative_url }}"
>
  <div class="live-demo-header">
    <div>
      <h3>Interactive document-triage diagnostic</h3>
      <p>
        Pick a synthetic case, edit the action probabilities if you want, and
        watch the diagnostic state update from the probability cloud.
      </p>
      <ol class="live-demo-steps">
        <li>Choose a familiar document situation.</li>
        <li>Notice whether rows agree, split, scatter, or drift.</li>
        <li>Run the diagnostic and compare the suggested action.</li>
      </ol>
    </div>
    <div class="live-demo-controls">
      <label for="dpga-scenario-select">Document case</label>
      <select id="dpga-scenario-select" data-scenario-select></select>
    </div>
  </div>

  <div class="live-demo-case-strip" data-scenario-buttons aria-label="Synthetic document case shortcuts"></div>

  <div class="live-demo-context" data-scenario-context>
    Loading synthetic document cases...
  </div>

  <div class="live-demo-grid">
    <div class="live-demo-editor">
      <div class="live-demo-section-title">
        <h4>Probability rows</h4>
        <p>
          Each row is one synthetic pass through the same document situation,
          such as a model sample, page window, prompt variant, or repeated
          extraction pass. The columns are possible next actions, and each row
          should sum to 1.
        </p>
      </div>
      <div class="table-wrap live-table-wrap" data-matrix-editor></div>
      <div class="live-demo-buttons">
        <button type="button" class="button" data-run-diagnostic>Run diagnostic</button>
        <button type="button" class="button secondary" data-reset-scenario>Reset case</button>
        <button type="button" class="button secondary" data-normalize-rows>Normalize rows</button>
        <button type="button" class="button secondary" data-generate-variation>Generate variation</button>
      </div>
      <p class="microcopy">
        The prebuilt cases are the intended path. Editing is optional: make two
        columns alternate as winners to create ambiguity; spread mass across many
        columns to create missing-context uncertainty; make early and late rows
        disagree to create drift. Use <strong>Generate variation</strong> to
        explore another synthetic cloud without typing values.
      </p>
    </div>

    <aside class="live-demo-output" data-diagnostic-output aria-live="polite">
      <h4>Generated diagnostic readout</h4>
      <p>Run a case to see the state, action, and metric summary.</p>
    </aside>
  </div>

  <section class="manifold-map-panel" data-manifold-map aria-live="polite">
    <h4>Decision-state shape atlas</h4>
    <p>Run a case to see separate schematic projections of common decision-cloud shapes.</p>
  </section>

  <div class="live-demo-explain" data-human-explanation></div>

  <details class="payload-panel">
    <summary>Show the current diagnostic payload</summary>
    <pre><code data-payload-output>{}</code></pre>
  </details>
</section>

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
Read the cases from top to bottom: they move from a clean extraction, to a
two-choice ambiguity, to missing evidence, to threshold sensitivity, to a
sequence that changes over time.

| Case | State | Action | Cue |
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
      If this were in a work queue, most reviewers would expect it to move on.
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
        <p class="microcopy">Across the full eight-row fixture, accept remains the clear winner.</p>
      </div>
      <div class="diagnostic-readout">
        <h3>Generated diagnostic readout</h3>
        <dl>
          <dt>Decision-PGA state</dt><dd>stable</dd>
          <dt>Workflow action</dt><dd><code>accept_extraction</code></dd>
          <dt>Mean margin</dt><dd>0.90</dd>
          <dt>Dispersion</dt><dd>0.002</dd>
        </dl>
        <p>A tight cloud with a large margin means the workflow is not just confident once; it is repeatedly stable.</p>
      </div>
    </div>
  </article>

  <article class="scenario-card">
    <div class="state-label">binary ambiguous -> ask_for_clarification</div>
    <h2>Two plausible contract dates</h2>
    <p>
      A contract amendment includes both an effective date and a signature date.
      A person can understand the confusion immediately: both dates are real,
      but they answer different questions. The cloud mostly varies along one
      axis: accept the extraction, or ask which date definition the user
      intended.
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
        <p class="microcopy">This is not broad confusion; it is a focused two-action dispute.</p>
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
      several actions because the workflow lacks the source it needs.
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
        <p class="microcopy">The pattern reads like missing context, not a clean two-option choice.</p>
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
      rejection; it is targeted review of a boundary case.
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
        <p class="microcopy">The value itself may be readable, but the action depends on a threshold.</p>
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
        <p class="microcopy">The rows tell a time story: early evidence and late evidence disagree.</p>
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

<script src="{{ '/assets/decision-pga-demo-runner.js?v=20260519-atlas-regions' | relative_url }}" defer></script>
