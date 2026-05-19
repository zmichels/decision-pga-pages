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

## How To Use The Demo

1. Pick a document extraction scenario.
2. Read the candidate value and the five-action probability cloud.
3. Ask what a simpler confidence score would tell you.
4. Compare that with the expected Decision-PGA state.
5. Route the workflow using the mapped action.

In a future code-backed demo, the probability cloud would come from repeated
model samples, model-score adapters, reviewer votes, rule checks, or an agent
trace. For this public article companion, the values are intentionally clean so
the states are easy to see.

## Scenario Summary

| Scenario | Expected decision state | Suggested workflow action | Demo intuition |
|---|---|---|---|
| Clean invoice due date | stable | `accept_extraction` | Repeated observations point to the same action. |
| Two plausible contract dates | binary ambiguous | `ask_for_clarification` | The workflow is mostly split between two choices. |
| Missing attachment reference | diffuse | `retrieve_more_context` | Uncertainty is scattered because the evidence is incomplete. |
| Near-threshold total | boundary-sensitive | `flag_for_review` | Small perturbations alter whether to accept or review. |
| Contradictory revision packet | drifting | `defer` | The preferred action changes over the read sequence. |

<section class="scenario-list">
  <article class="scenario-card">
    <div class="state-label">stable -> accept_extraction</div>
    <h2>Clean invoice due date</h2>
    <p>
      A vendor invoice shows a clearly labeled due date near the payment total.
      The synthetic observations form a tight cloud around
      <code>accept_extraction</code>.
    </p>
    <pre><code>[0.92, 0.03, 0.02, 0.02, 0.01]
[0.91, 0.04, 0.02, 0.02, 0.01]
[0.94, 0.02, 0.01, 0.02, 0.01]</code></pre>
  </article>

  <article class="scenario-card">
    <div class="state-label">binary ambiguous -> ask_for_clarification</div>
    <h2>Two plausible contract dates</h2>
    <p>
      A contract amendment includes both an effective date and a signature date.
      The cloud mostly varies along one axis: accept the extraction, or ask which
      date definition the user intended.
    </p>
    <pre><code>[0.42, 0.45, 0.05, 0.05, 0.03]
[0.48, 0.39, 0.05, 0.05, 0.03]
[0.38, 0.50, 0.04, 0.05, 0.03]</code></pre>
  </article>

  <article class="scenario-card">
    <div class="state-label">diffuse -> retrieve_more_context</div>
    <h2>Missing attachment reference</h2>
    <p>
      A purchase request says the approved amount is in an attached quote, but
      only the cover page is available. The probability mass spreads across
      several actions because the workflow lacks evidence.
    </p>
    <pre><code>[0.18, 0.20, 0.30, 0.18, 0.14]
[0.22, 0.17, 0.27, 0.19, 0.15]
[0.16, 0.22, 0.29, 0.17, 0.16]</code></pre>
  </article>

  <article class="scenario-card">
    <div class="state-label">boundary-sensitive -> flag_for_review</div>
    <h2>Near-threshold total</h2>
    <p>
      A reimbursement form total is legible, but the extracted value is close to
      an internal manual-review threshold. The safest route is not automatic
      rejection; it is targeted review.
    </p>
    <pre><code>[0.47, 0.05, 0.06, 0.39, 0.03]
[0.41, 0.05, 0.07, 0.43, 0.04]
[0.49, 0.04, 0.06, 0.38, 0.03]</code></pre>
  </article>

  <article class="scenario-card">
    <div class="state-label">drifting -> defer</div>
    <h2>Contradictory revision packet</h2>
    <p>
      A multi-page packet starts clean, then later pages introduce a revision
      note and a conflicting total. The sequence matters, so the workflow should
      pause and re-evaluate before acting.
    </p>
    <pre><code>[0.86, 0.05, 0.03, 0.04, 0.02]
[0.50, 0.11, 0.12, 0.20, 0.07]
[0.08, 0.07, 0.18, 0.25, 0.42]</code></pre>
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
