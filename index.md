---
layout: default
title: Decision-PGA
description: Article series, demo, and open-source code for decision-state diagnostics in applied AI workflows.
---

<section class="hero">
  <div class="kicker">Open-source diagnostic prototype</div>
  <h1>Decision-state diagnostics for applied AI workflows</h1>
  <p class="lede">
    Decision-PGA is a prototype framework for describing the shape of
    uncertainty around AI decisions before a workflow acts. This site gathers
    the article series, a synthetic demo, the agent toolkit, the public code
    repository, and PDF copies.
  </p>
  <div class="actions">
    <a class="button" href="{{ '/article/' | relative_url }}">Read the article</a>
    <a class="button secondary" href="{{ '/telescoping/' | relative_url }}">Read the follow-up</a>
    <a class="button secondary" href="{{ '/demo/' | relative_url }}">Try the demo</a>
    <a class="button secondary" href="{{ '/toolkit/' | relative_url }}">Use the toolkit</a>
    <a class="button secondary" href="https://github.com/zmichels/Decision-PGA">View code</a>
    <a class="button secondary" href="{{ '/assets/decision-pga-decision-state-diagnostics.pdf' | relative_url }}">Download PDF</a>
  </div>
</section>

<section class="notice">
  This is a personal technical perspective, not an institutional statement.
  The article uses no patient data, is not clinical validation, and is not a
  medical device or clinical decision support product.
</section>

## What This Site Is For

This site is a compact public entry point for Decision-PGA: the framing article,
the Telescoping Decision-PGA companion perspective, the synthetic
document-triage demo, the agent toolkit, the open-source prototype repository,
and PDF versions of the articles.

<div class="grid">
  <section class="panel">
    <h3>Article</h3>
    <p>
      The article explains why workflow-oriented AI systems need diagnostics
      for the shape of decision uncertainty.
    </p>
  </section>
  <section class="panel">
    <h3><a href="{{ '/telescoping/' | relative_url }}">Telescoping Decision-PGA</a></h3>
    <p>
      The follow-up perspective shows how broad uncertainty clouds can contain
      smaller local substructures and cross-document evidence bridges.
    </p>
  </section>
  <section class="panel">
    <h3>Synthetic demo</h3>
    <p>
      A document extraction triage fixture shows how probability clouds can map
      to workflow actions.
    </p>
  </section>
  <section class="panel">
    <h3>Agent toolkit</h3>
    <p>
      A five-minute path shows CLI, Python API, MCP launch, and synthetic
      agent payloads for developers who want to try the diagnostic contract in
      their own workflow vocabulary.
    </p>
  </section>
  <section class="panel">
    <h3>Public code</h3>
    <p>
      The initial Decision-PGA prototype is available at
      <a href="https://github.com/zmichels/Decision-PGA">github.com/zmichels/Decision-PGA</a>.
    </p>
  </section>
  <section class="panel">
    <h3>PDF</h3>
    <p>
      A browser-rendered PDF is included for readers who prefer a document-style
      copy of the article.
    </p>
  </section>
</div>

## Current Status

- Article series and PDFs: available for public reading and critique.
- Demo: synthetic, non-clinical, and designed to build intuition.
- Toolkit: copy-paste agent examples and a local MCP quickstart.
- Code: public initial research release at
  <https://github.com/zmichels/Decision-PGA>.
