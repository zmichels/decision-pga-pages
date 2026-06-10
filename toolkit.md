---
layout: default
title: Agent Toolkit
description: A practical Decision-PGA quickstart and diagnostic payload gallery for agent builders.
permalink: /toolkit/
schema_type: TechArticle
author: Zachary D. Michels, PhD
date_published: "2026-05-20"
date_modified: "2026-05-20"
---

# Decision-PGA Agent Toolkit

This page is the practical companion to the article and demo. It is for
developers asking: "How would I actually try this in an agent workflow?"

Imagine an agent that can answer, ask a clarifying question, retrieve more
evidence, route to review, abstain, or replan. A confidence score can say that
the situation is uncertain. Decision-PGA asks a more workflow-shaped question:
what kind of uncertainty is it?

The prototype accepts repeated probability-like observations over a fixed set
of candidate actions, then returns a compact decision-state readout. It is
local, deterministic, and model-neutral. It is not a production safety layer or
a claim that an answer is correct.

For trajectory-specific reading, see
[Kinematic Decision-PGA]({{ '/kinematics/' | relative_url }}), which explains
how velocity, drift, and jerk can characterize observed motion across RAG,
tool-use, and final-output steps.

<div class="actions">
  <a class="button" href="https://github.com/zmichels/Decision-PGA/blob/main/docs/agent-toolkit.md">Open full toolkit docs</a>
  <a class="button secondary" href="https://github.com/zmichels/Decision-PGA">View code</a>
  <a class="button secondary" href="{{ '/demo/' | relative_url }}">Try visual demo</a>
</div>

## Use Decision-PGA in five minutes

```bash
git clone https://github.com/zmichels/Decision-PGA.git
cd Decision-PGA
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[mcp]"
decision-pga diagnose --pretty examples/agent/tool_action_ambiguity.json
```

Launch the local MCP server:

```bash
decision-pga-mcp
```

Inspect it with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector decision-pga-mcp
```

## Diagnostic Payload Gallery

Each gallery item below mirrors a copy-paste JSON payload in the public repo.
The examples are synthetic, but the situations are meant to feel familiar to
agent builders. The point is to see how similar-looking uncertainty can call for
different next actions.

<div class="grid toolkit-gallery">
  <section class="panel">
    <h3>Tool/action ambiguity</h3>
    <p>
      A support agent is split between searching documentation and querying an
      internal database before answering. The useful move is to resolve that
      tool path, not treat the case as generic low confidence.
    </p>
    <p>
      Expected state: <code>binary_ambiguity</code><br>
      Example:
      <a class="example-link" href="https://github.com/zmichels/Decision-PGA/blob/main/examples/agent/tool_action_ambiguity.json">tool_action_ambiguity.json</a>
    </p>
  </section>
  <section class="panel">
    <h3>RAG evidence conflict</h3>
    <p>
      Two retrieved snippets support incompatible answer paths. Decision-PGA can
      preserve the fact that uncertainty is concentrated between two evidence
      routes, which is different from missing all evidence.
    </p>
    <p>
      Expected state: <code>binary_ambiguity</code><br>
      Example:
      <a class="example-link" href="https://github.com/zmichels/Decision-PGA/blob/main/examples/agent/rag_evidence_conflict.json">rag_evidence_conflict.json</a>
    </p>
  </section>
  <section class="panel">
    <h3>Document extraction routing</h3>
    <p>
      The workflow sees weak support for several routes because a referenced
      attachment or source page is missing. The practical next action is to
      retrieve more context, not ask a narrow two-choice question.
    </p>
    <p>
      Expected state: <code>diffuse_uncertainty</code><br>
      Example:
      <a class="example-link" href="https://github.com/zmichels/Decision-PGA/blob/main/examples/agent/document_extraction_routing.json">document_extraction_routing.json</a>
    </p>
  </section>
  <section class="panel">
    <h3>Multi-step agent drift</h3>
    <p>
      Early trajectory windows prefer retrieval, while later windows prefer
      drafting. The trace should be segmented or replanned instead of averaged
      into one static decision state.
    </p>
    <p>
      Expected state: <code>regime_shift</code><br>
      Example:
      <a class="example-link" href="https://github.com/zmichels/Decision-PGA/blob/main/examples/agent/multi_step_agent_drift.json">multi_step_agent_drift.json</a>
    </p>
  </section>
  <section class="panel">
    <h3>Kinematic trajectory whiplash</h3>
    <p>
      A RAG/tool whiplash trace can consolidate toward drafting after retrieval,
      then sharply deflect after a tool result. The useful signal is not only
      the final action, but the transition that produced the jerk.
    </p>
    <p>
      Source type: <code>kinematic_trajectory</code><br>
      Inspect: <code>step_jerk</code><br>
      Example:
      <a class="example-link" href="https://github.com/zmichels/Decision-PGA/blob/main/examples/agent/kinematic_trajectory_rag_tool_whiplash.json">kinematic_trajectory_rag_tool_whiplash.json</a>
    </p>
  </section>
  <section class="panel">
    <h3>Stable abstain decision</h3>
    <p>
      Abstention can be the stable top action. In that case,
      <code>proceed</code> means proceed with the abstain route, not answer
      anyway.
    </p>
    <p>
      Expected state: <code>stable</code><br>
      Example:
      <a class="example-link" href="https://github.com/zmichels/Decision-PGA/blob/main/examples/agent/abstain_defer_decision.json">abstain_defer_decision.json</a>
    </p>
  </section>
</div>

## What to look for

The key comparison is not "certain versus uncertain." It is the shape of the
uncertainty:

- tight clouds suggest the workflow can continue with the top action;
- line-shaped clouds suggest a focused two-choice ambiguity;
- broad clouds suggest missing or inadequate context;
- boundary-sensitive clouds deserve threshold or policy review;
- drifting clouds suggest segmentation or replanning.

For implementation details, see the full
[agent toolkit docs](https://github.com/zmichels/Decision-PGA/blob/main/docs/agent-toolkit.md)
and the
[MCP quickstart](https://github.com/zmichels/Decision-PGA/blob/main/docs/mcp-server.md).
