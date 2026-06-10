---
layout: default
title: Kinematic Decision-PGA
description: A companion perspective on velocity, drift, and jerk in observed decision-state trajectories.
permalink: /kinematics/
schema_type: TechArticle
author: Zachary D. Michels, PhD
date_published: "2026-06-10"
date_modified: "2026-06-10"
---

# Kinematic Decision-PGA: Reading Motion in Decision States

<p class="article-meta">
  Zachary D. Michels, PhD<br>
  June 10, 2026
</p>

Decision-PGA begins with a static question: what shape does the uncertainty
have?

That question is useful. A tight cloud, a stretched cloud, a diffuse cloud, and
a drifting cloud should not all lead to the same workflow action. But many AI
workflows do not only hold a decision state. They move through one.

A retrieval step changes the evidence. A tool call changes the available
facts. A final answer step may consolidate the prior motion, or reverse it.
When the workflow has several observable moments, the diagnostic question
changes:

How is the decision state moving?

This companion perspective treats that motion as observed probability-geometry
motion, not hidden model physics. It does not claim to read private model
cognition. It does not prove causal internal forces. It asks whether repeated
probability-like observations over the same candidate decisions can reveal a
useful trajectory as a workflow unfolds.

## The Missing Signal Is Motion

Static confidence is often too blunt. Static uncertainty shape is better, but
it can still miss a useful signal.

Suppose an agent moves through four operational moments: input, retrieval,
tool use, and final output. At each moment, it reports support over the same
candidate actions: retrieve more context, call a tool, draft an answer, ask the
user, or defer.

The final state may look acceptable. It may even be confident. But the path
could still matter. A smooth shift from retrieval to drafting says something
different from an abrupt reversal after a tool result. A trace that consolidates
gradually deserves a different kind of inspection than a trace that snaps
across a decision boundary at the last step.

The point is not to make motion sound dramatic. The point is practical. A
workflow often needs to know which transition deserves review.

## From Clouds To Trajectories

The data shape is simple:

```text
runs x steps x labels
```

`runs` are repeated evaluations, prompt variants, model samples, or trace
variants. `steps` are operational moments such as input, RAG context, tool
selection, tool result, and final output. `labels` are the candidate decisions
or actions being tracked.

Each row remains a probability-like distribution over the same labels. That
constraint matters. Without a stable action vocabulary, movement cannot be read
cleanly because the coordinate system is changing underneath the diagnostic.

The original article argued that uncertainty has shape. The telescoping
companion argued that shape has substructure. The kinematic layer adds a third
claim: shape has motion.

## Velocity Without Overclaiming Physics

The square-root/Fisher-Rao embedding maps categorical probability vectors to a
positive unit sphere. On that surface, a change from one observed decision state
to the next can be read as geodesic movement. The logarithmic map turns that
movement into a tangent vector.

That tangent vector is useful because it gives direction and magnitude. It can
say that a workflow is moving toward drafting, away from retrieval, or into a
review state. The norm of that vector can be summarized as speed. Squared speed
can be summarized as kinetic energy.

These are disciplined analogies. Velocity, kinetic energy, and jerk are
geometric diagnostics over probability states. They are not proof of hidden
model mechanics. The method does not decide whether the underlying answer is correct.
They describe how observed support over candidate actions changes across the
workflow.

That boundary is important. The method can make a trace easier to inspect, but
it does not replace task evaluation, source authority, human review, or
governance.

## Jerk Is A Review Signal

Velocity describes change in position. Acceleration describes change in
velocity. Jerk describes abrupt change in the acceleration profile.

In the current prototype, acceleration comparison uses an
`ambient_tangent_delta` approximation. That is intentionally modest. It compares
successive tangent vectors in the ambient coordinate frame rather than
claiming a fully parallel-transported manifold acceleration. For diagnostics,
that first approximation can still be useful if it is treated carefully.

The phrase is memorable, but the use is serious: jerk is a review signal.

A high jerk step says, "inspect this transition." It does not say the answer is
wrong. It does not say the model behaved irrationally. It says the observed
decision trajectory changed direction sharply enough that a person or test
suite may want to know why.

Examples are ordinary:

- a RAG step sharply redirects support from `draft_answer` to `retrieve_more`;
- a tool result reverses a smooth drift toward `answer_now`;
- a final output step suddenly shifts from `draft_answer` to `ask_user`;
- a policy check makes a previously stable route boundary-sensitive.

That localization can be more valuable than a global failure label. It narrows
the review question from "why did this run feel unstable?" to "what happened
between retrieval and tool use?"

## RAG/tool whiplash

The first kinematic fixture in the public prototype is synthetic, but it names
a common pattern: RAG/tool whiplash.

In one kind of trace, retrieval adds context and the decision state moves
smoothly toward drafting an answer. The tool result confirms the route. The
workflow is moving, but it is moving coherently.

In another kind of trace, retrieval appears to consolidate the route, but the
tool result sharply deflects support toward asking the user or deferring. The
point is not that the final action is bad. The point is that the transition is
diagnostically interesting.

A static summary may report only the final action. A kinematic summary can
show that the final action arrived after a sharp deflection. That difference
matters because it changes what to inspect: the retrieval payload, the tool
schema, the tool result, the prompt segment that interpreted the result, or the
candidate action vocabulary itself.

## Fast Characterization Protects Attention

This should not be framed as a money argument. The more immediate cost of
uncertainty is attention.

Unresolved uncertainty consumes review attention, delays routing, and lets the
wrong next action compound. quickly characterizing the trajectory can matter
because a diagnostic does not need to decide the answer to be useful. It can
still say whether the trace is moving smoothly, drifting persistently, or
jerking across a boundary.

That helps a workflow spend review attention where it is most likely to pay
off: at the transition that changed the motion.

## What This Adds To The Series

The relationship to the earlier pages is direct.

The original article asks whether a probability cloud has a useful diagnostic
shape. The telescoping article asks whether a broad cloud contains smaller
local structures. This page asks whether a decision state has a trajectory
across workflow steps.

Those are not competing views. They are different zoom levels on the same
problem: how to make uncertainty inspectable before a workflow acts too
confidently.

For the broader framing, see
[Decision-PGA and the Need for Decision-State Diagnostics]({{ '/article/' | relative_url }}).
For substructure and bridge cases, see
[Telescoping Decision-PGA]({{ '/telescoping/' | relative_url }}).

## Try The Prototype

The current repository includes a `kinematic_trajectory` source type and a
synthetic RAG/tool whiplash fixture.

```bash
git clone https://github.com/zmichels/Decision-PGA.git
cd Decision-PGA
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
decision-pga diagnose --pretty examples/agent/kinematic_trajectory_rag_tool_whiplash.json
```

Useful fields to inspect include:

- `canonical_path_probabilities`
- `step_kinetic_energy`
- `step_jerk`
- `systemic_kinetic_energy`
- `systemic_jerk`
- `velocity_dispersion`
- `primary_drift_labels`

The example is not a benchmark. It is a small diagnostic object that makes the
shape of motion visible.

## Cautions

The candidate labels must stay stable across steps. If the labels change, the
trajectory can become a comparison between vocabularies rather than a movement
through one decision space.

The geometry should also be compared against simpler trajectory summaries:
switch rate, entropy change, margin change, agreement, and ordinary per-step
probability deltas. If those simpler signals explain the useful distinction,
that should be reported.

Finally, a positive jerk signal is not a correctness judgment. It is a prompt
to inspect a transition. The transition may reveal a bug, a missing source, a
good correction, a policy boundary, or a candidate set that needs refinement.

Decision-PGA remains a diagnostic scaffold. The kinematic extension keeps that
same boundary. It helps describe how the observed decision state moved. It does
not decide what the world is.
