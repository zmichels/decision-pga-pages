---
layout: default
title: Decision-PGA and the Need for Decision-State Diagnostics
description: A prototype vocabulary for uncertainty shape in agentic AI workflows.
permalink: /article/
---

# Decision-PGA and the Need for Decision-State Diagnostics

## A Prototype Vocabulary for Uncertainty Shape in Agentic AI Workflows

AI systems are moving from one-shot answer generation toward workflow
participation. They retrieve evidence, extract data, route tasks, call tools,
compare options, and recommend next actions. That shift changes the uncertainty
problem. It is no longer enough to ask whether a model is confident in a final
answer. A workflow often needs to know what kind of decision state the system is
in before it acts.

Is the next action stable enough to proceed? Is the uncertainty concentrated
between two plausible choices? Is it scattered across many alternatives? Is the
system sensitive to a small boundary change? Has the decision state drifted over
a multi-step trajectory?

Decision-PGA is a prototype method for studying those questions. It analyzes
clouds of categorical probability vectors on the probability simplex using
Fisher-Rao/square-root geometry, then describes the shape of the resulting
uncertainty. The aim is not to replace task evaluation or human review. The aim
is to make a decision state easier to inspect, compare, and route.

This article is a personal technical perspective, not an institutional
statement. It uses no patient data, is not clinical validation, and does not
describe a medical device or clinical decision support product.

<figure class="diagram-figure">
  <img src="{{ '/assets/decision-pga-diagnostic-loop.svg' | relative_url }}" alt="Decision-PGA diagnostic loop from probability observations to geometry metrics, decision state, and workflow action.">
  <figcaption>
    Decision-PGA treats repeated probability-like observations as a cloud, maps
    that cloud through probability-simplex geometry, and returns a diagnostic
    state that can inform the next workflow action.
  </figcaption>
</figure>

## The gap between confidence and action

Many AI tools already expose useful signals: confidence scores, token
probabilities, calibrated probabilities, retrieval scores, agreement rates,
human review flags, and task-specific benchmarks. Those signals matter. The gap
appears when a system must decide what to do next.

Consider a workflow that can answer, ask a clarifying question, retrieve more
evidence, route to a reviewer, abstain, or replan. Two cases can have similar
entropy but require different responses. In one case, almost all uncertainty may
lie between two options. In another, the probability mass may be scattered
across many actions. A scalar score may say "uncertain" in both cases. A
decision-state diagnostic tries to preserve more of the shape:

- a tight cloud suggests the candidate decision is stable within the tested
  context;
- an elongated two-choice cloud suggests targeted clarification or comparison;
- a diffuse cloud suggests missing context or insufficient evidence;
- a boundary-sensitive cloud suggests assumptions or thresholds should be
  inspected;
- a drifting cloud suggests segmentation, replanning, or escalation.

The practical question is modest but important: can we build diagnostic tools
that help AI workflows choose safer and more useful next actions under
uncertainty?

## Why healthcare is a useful application lens

Healthcare is not the only place this matters, but it is a useful lens because
the workflows are high-accountability, document-heavy, and full of decisions
where "low confidence" is too vague to be operationally helpful.

Examples worth studying include:

- message or request triage, where candidate actions might include answer,
  clarify, route, schedule, retrieve context, or escalate;
- policy and guideline retrieval, where sources may be relevant but incomplete,
  outdated, or in tension;
- medical document extraction, where uncertainty may reflect two plausible
  values, source-span ambiguity, table-row confusion, or OCR sensitivity;
- trial matching and eligibility review, where some criteria are clearly met,
  some are missing, and some conflict across sources;
- operational agents that coordinate multi-step work and may drift as they
  gather context.

These examples should be treated as research and evaluation targets, not as
claims of deployment readiness. A diagnostic can describe the shape of a
decision state; it does not determine clinical truth, prove safety, or replace
domain review.

The broader public context supports caution. The FDA maintains information on
AI-enabled medical devices and clinical decision support software:
https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices
and
https://www.fda.gov/medical-devices/software-medical-device-samd/clinical-decision-support-software-frequently-asked-questions-faqs.
The ONC HTI-1 rule addresses transparency for predictive decision support
interventions in certified health IT:
https://healthit.gov/regulations/hti-rules/hti-1-final-rule/. The WHO has
published guidance on ethics and governance of AI for health:
https://www.who.int/publications/i/item/9789240029200.

The point is not that Decision-PGA solves these governance questions. It does
not. The point is that governance and evaluation need inspectable technical
signals, and decision-state diagnostics may become one useful category of such
signals.

## What Decision-PGA does

Decision-PGA starts with repeated probability-like observations over candidate
labels. The labels might be actions, extracted field values, evidence clusters,
routing choices, or review outcomes. The current prototype then:

1. Normalizes probability vectors.
2. Maps them to the positive unit sphere with the square-root transform.
3. Computes an intrinsic mean.
4. Log-maps samples into a tangent space.
5. Computes a dispersion tensor and eigensystem.
6. Reports shape metrics such as total dispersion, PC1 fraction, anisotropy
   ratio, margin, label switching, and half-window geodesic drift.

That produces a compact diagnostic contract:

| State | Possible workflow interpretation |
| --- | --- |
| Stable | Proceed if the task is in scope and other checks pass. |
| Binary ambiguity | Ask a targeted question or compare top candidates. |
| Diffuse uncertainty | Gather evidence or broaden context. |
| Boundary sensitive | Inspect assumptions, thresholds, or constraints. |
| Regime shift | Segment the task, replan, or escalate. |

This contract is intentionally small. It is meant to be usable by software
systems, not just by notebooks. A local command-line tool, report generator, or
agent tool can call the diagnostic and receive a structured result.

## Why geometry?

Probability vectors live on a simplex, not in ordinary unconstrained Euclidean
space. Decision-PGA uses the square-root transform to place probability vectors
on the positive unit sphere, where Fisher-Rao geometry becomes easier to work
with. The result is a way to analyze dispersion directions, not only dispersion
amount.

That matters because uncertainty can have shape. A cloud stretched along one
direction is different from a cloud spread broadly across many choices. Two
states may have similar entropy while suggesting different next actions. PGA
metrics such as the first principal geodesic fraction and anisotropy ratio are
attempts to capture that distinction.

This is a hypothesis to test, not a settled claim. Decision-PGA should be
compared against simpler baselines such as entropy, margin, switch rate,
agreement, calibration, and task-specific accuracy.

## Application patterns worth testing

### Tool and action selection

Agentic systems frequently choose among tools, routes, or next actions. A
diagnostic could distinguish stable tool choice from two-tool ambiguity or
diffuse uncertainty across the action set.

### Retrieval and evidence conflict

Retrieval systems can surface sources that are relevant but not mutually
consistent. A diagnostic over candidate evidence clusters or answer decisions
could help decide whether to answer, retrieve more, cite uncertainty, or route
to review.

### Document extraction

Extraction systems often face ambiguous spans, conflicting values, incomplete
tables, or uncertain entity associations. A decision-state diagnostic could
separate a stable extracted value from a two-value dispute or a diffuse
source-association problem.

### Multi-step workflow monitoring

An agent may begin with one plan, gather new evidence, and gradually move into a
different decision regime. Sliding-window diagnostics could help identify when a
trajectory should be segmented, replanned, or escalated.

## What must be proven next

The next step is not a bigger claim. It is better evidence. Decision-PGA needs
tests that ask where it adds value over simpler metrics and where it is
redundant.

Useful near-term tests include:

- entropy-matched examples where binary ambiguity and diffuse uncertainty should
  lead to different actions;
- fixture suites for tool selection, retrieval conflict, and document
  extraction;
- held-out synthetic scenarios with known decision states;
- comparisons against entropy, margin, agreement, drift, and switch-rate
  baselines;
- readable reports that state when PGA does not add value.

For healthcare-adjacent examples, the first benchmark should use synthetic or
public, non-patient fixtures. No clinical or operational claim should depend on
private data, anecdote, or unreviewed workflow assumptions.

## A practical open-source path

The healthiest way to publish this idea is to separate the concept from claims
of maturity:

- publish the article and invite critique;
- keep examples synthetic or public;
- release the prototype only when its docs, license, tests, and limitations are
  clear;
- report negative or redundant findings alongside promising ones;
- treat healthcare examples as evaluation targets that require separate
  governance before real-world use.

Decision-PGA may turn out to be most useful as a small observability layer: a
local diagnostic that helps an AI workflow decide whether to proceed, clarify,
gather evidence, inspect sensitivity, segment, replan, or escalate.

## Conclusion

As AI systems become more active participants in workflows, they will need ways
to expose not only what they chose, but what kind of uncertainty surrounded the
choice. Confidence scores are part of that story, but they are not the whole
story.

Decision-PGA proposes a compact way to describe uncertainty shape over candidate
decisions. It is early, model-neutral, and intentionally modest. The important
claim is not that the method is ready for high-stakes deployment. The important
claim is that decision-state diagnostics deserve to be made visible, tested, and
improved before agentic AI systems become routine infrastructure.
