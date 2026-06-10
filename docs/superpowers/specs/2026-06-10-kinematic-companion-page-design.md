# Kinematic Decision-PGA Companion Page Design

Date: 2026-06-10
Status: draft for review

## Purpose

Add a public companion page to the Decision-PGA Pages site that explains the new
kinematic trajectory layer in a readable, article-forward way. The page should
extend the existing article arc:

1. `article.md`: uncertainty has shape.
2. `telescoping.md`: shape can contain substructure.
3. New kinematic page: shape can move across workflow steps.

The page should be primarily a public narrative article, with a compact
practical section at the end that shows how to try the new
`kinematic_trajectory` source type.

## Working Title

`Kinematic Decision-PGA: Reading Motion in Decision States`

Possible subtitle:

`Why velocity, drift, and jerk may matter when AI workflows move through retrieval, tools, and final answers.`

## Recommended Route And Metadata

Create a new Markdown page:

```text
kinematics.md
```

Use this front matter:

```yaml
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
```

The page should be linked from the site home page and primary navigation. It
should also be cross-linked from the main article near the existing companion
links and from the toolkit page near the agent trajectory examples.

## Audience And Tone

The primary audience is a public technical reader who has read, or could read,
the main Decision-PGA article. The tone should match the existing pages:
clear, careful, practical, and modest.

The page should lean more like `article.md` than `toolkit.md`, but it should end
with enough concrete detail that a developer can try the feature immediately.
It should especially invoke the understated but confident prose of the initial
Decision-PGA article: plain sentences, controlled claims, concrete workflow
examples, and a calm technical cadence that makes the idea feel useful without
overselling it.

Avoid a money-driven or productivity-sales tone. The time argument should be
framed as review attention and workflow delay:

> In applied workflows, time matters because unresolved uncertainty consumes
> review attention, delays routing, and lets the wrong next action compound.
> A diagnostic does not need to decide the answer; it can still be valuable if
> it quickly says what kind of motion the decision state is undergoing.

## Core Claim

Static Decision-PGA asks:

> What shape is the uncertainty cloud?

Kinematic Decision-PGA asks:

> How does that decision state move as the workflow unfolds?

The practical value is quick trajectory characterization. A workflow should be
able to distinguish smooth drift from abrupt deflection without waiting for a
full downstream failure.

## Required Claim Boundaries

The page must state plainly:

- This is observed probability-geometry motion, not hidden model physics.
- Velocity, kinetic energy, and jerk are geometric diagnostics over probability
  states, not proof of internal model forces.
- The method does not decide whether the underlying answer is correct.
- It does not replace task evaluation, source authority, human review, or
  governance.
- The first implementation uses an `ambient_tangent_delta` approximation for
  acceleration comparison.

The word `jerk` is encouraged because it is technically apt and memorable, but
it should be used as a review signal rather than a joke.

## Narrative Structure

### 1. The Missing Signal Is Motion

Open with the limitation of static confidence and static uncertainty shape.
When an AI workflow moves through input, retrieval, tool use, and final output,
the question is not only "how uncertain is it?" or "what shape is the cloud?"
It is also "how is the decision state moving?"

### 2. From Clouds To Trajectories

Introduce the `runs x steps x labels` tensor:

- `runs`: repeated evaluations, prompt variants, model samples, or trace
  variants;
- `steps`: operational moments such as input, RAG context, tool selection, and
  final output;
- `labels`: candidate actions or decisions.

Explain that each row remains a probability-like distribution over the same
candidate labels.

### 3. Velocity Without Overclaiming Physics

Explain velocity as geodesic movement between observed probability states in
Fisher-Rao/square-root geometry. Make clear that this is a disciplined analogy:
the diagnostic reads movement of observed support over candidate actions, not
private cognition.

### 4. Jerk Is A Review Signal

Use `jerk` as a central memorable section. Define it operationally as abrupt
change in the observed velocity profile. The key use is localization: jerk helps
identify which transition in a trace deserves inspection.

Examples:

- a RAG step sharply redirects the action distribution;
- a tool result reverses a smooth drift;
- a final output step suddenly shifts from `draft_answer` to `ask_user`.

### 5. RAG/Tool Whiplash Example

Use the new repository fixture as the anchor:

```text
examples/agent/kinematic_trajectory_rag_tool_whiplash.json
```

Describe a synthetic workflow that begins with retrieval, consolidates toward
drafting, then sharply deflects toward asking the user in some runs. The point
is not that the output is wrong; the point is that the transition deserves
inspection.

### 6. Fast Characterization Protects Attention

Use the time/attention idea carefully. Do not frame this as revenue or business
optimization. Frame it as avoiding wasted review loops and compounding wrong
next actions.

Possible line:

> Quickly characterizing the trajectory can matter because the cost of
> uncertainty is often paid in attention: repeated review, irrelevant retrieval,
> premature drafting, or late escalation.

### 7. What This Adds To The Article Series

Make the relationship explicit:

- main article: uncertainty has shape;
- telescoping article: shape has substructure;
- kinematic article: shape has motion.

This page should feel like a natural third companion rather than a replacement
for the first two.

### 8. Try The Prototype

End with a compact practical section:

```bash
git clone https://github.com/zmichels/Decision-PGA.git
cd Decision-PGA
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
decision-pga diagnose --pretty examples/agent/kinematic_trajectory_rag_tool_whiplash.json
```

List the fields to inspect:

- `canonical_path_probabilities`
- `step_kinetic_energy`
- `step_jerk`
- `systemic_kinetic_energy`
- `systemic_jerk`
- `velocity_dispersion`
- `primary_drift_labels`

Mention that a positive jerk signal is a prompt to inspect a transition, not a
standalone correctness judgment.

## Site Integration

Update:

- `_layouts/default.html`: add `Kinematics` to the primary nav if it fits
  without making the header too crowded. If the header feels crowded, add the
  link to the home page and article cross-links only.
- `index.md`: add the page to the hero actions and the site-purpose section.
- `article.md`: add one sentence near the existing companion links.
- `telescoping.md`: add a brief cross-link near the opening or conclusion.
- `toolkit.md`: add a gallery card or short section for the
  `kinematic_trajectory` example.
- `sitemap.xml`: add `/kinematics/` if this sitemap is manually maintained.
- `llms.txt`: add the new page if this file lists public pages manually.

## Validation

Use the existing Pages validation script if applicable:

```bash
python3 scripts/validate_publication.py
```

Also inspect the generated local page if the existing workflow supports a local
Jekyll build. If not, static Markdown/front-matter validation is enough for the
first slice.

## Out Of Scope For First Slice

- New generated figures or diagrams.
- A PDF copy of the kinematic article.
- Interactive trajectory visualizations.
- Changes to the Python package beyond links to the already published
  `kinematic_trajectory` docs and example.
- Claims about production deployment, hidden model cognition, or clinical use.

## Success Criteria

- The new page reads as a companion article, not only a developer doc.
- The RAG/tool whiplash example is the concrete anchor.
- The page uses `jerk` accurately and memorably.
- The page explains why quick trajectory characterization matters without a
  money-driven tone.
- The route is discoverable from the site.
- The page preserves the same careful boundaries as the existing article series.
