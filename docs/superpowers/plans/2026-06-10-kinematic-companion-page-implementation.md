# Kinematic Companion Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a public `/kinematics/` companion article to the Decision-PGA Pages site that explains velocity, drift, RAG/tool whiplash, and jerk as observed decision-state trajectory diagnostics.

**Architecture:** Keep the site static and Markdown-first. Add one new article page, extend the existing publication validator in small stages, then wire the page into navigation, cross-links, sitemap, `llms.txt`, and README discovery surfaces. No new generated figures, PDFs, JavaScript, or Python package changes are included in this slice.

**Tech Stack:** GitHub Pages/Jekyll Markdown, Liquid relative links, the existing Python publication validator, and plain HTML snippets already used by the site layout.

---

## Repository Context

Repository root:

```text
/Users/michels.zachary/Documents/Decision-PGA-Publishing/decision-pga-pages
```

Current public pages:

- `article.md`: original Decision-PGA article.
- `telescoping.md`: first companion article.
- `toolkit.md`: practical agent-builder page.
- `index.md`: landing page.
- `_layouts/default.html`: shared layout and primary navigation.
- `scripts/validate_publication.py`: publication validation gate.

The new page should extend the existing article sequence:

1. `article.md`: uncertainty has shape.
2. `telescoping.md`: shape has substructure.
3. `kinematics.md`: shape has motion.

## File Structure

- Create `kinematics.md`
  - Public companion article at `/kinematics/`.
  - Holds the full explanatory prose and compact command-line prototype section.
- Modify `scripts/validate_publication.py`
  - Add staged requirements for the page body, page discoverability, cross-links, and public metadata.
- Modify `_layouts/default.html`
  - Add `Kinematics` to the primary navigation after `Telescoping`.
- Modify `index.md`
  - Add a hero action and site-purpose panel for the kinematic companion.
- Modify `article.md`
  - Cross-link the new companion from the original article near the existing companion links.
- Modify `telescoping.md`
  - Cross-link the new companion from the opening companion paragraph.
- Modify `toolkit.md`
  - Add a trajectory-specific pointer and gallery card for the `kinematic_trajectory` RAG/tool whiplash fixture.
- Modify `sitemap.xml`
  - Add `/kinematics/`.
- Modify `llms.txt`
  - Add the page as a canonical entry point and mention trajectory diagnostics.
- Modify `README.md`
  - Add `kinematics.md` to repository contents and the site summary.

## Task 1: Page Contract And Article Body

**Files:**
- Modify: `scripts/validate_publication.py`
- Create: `kinematics.md`

- [ ] **Step 1: Add the page-level validation contract**

In `scripts/validate_publication.py`, add `kinematics.md` to `REQUIRED_FILES` immediately after `telescoping.md`:

```python
    "article.md",
    "telescoping.md",
    "kinematics.md",
    "demo.md",
```

Add this constant immediately after `TELESCOPING_REQUIRED_PHRASES`:

```python
KINEMATICS_REQUIRED_PHRASES = [
    "Kinematic Decision-PGA: Reading Motion in Decision States",
    "Zachary D. Michels, PhD",
    "June 10, 2026",
    "observed probability-geometry motion",
    "not hidden model physics",
    "does not prove causal internal forces",
    "does not decide whether the underlying answer is correct",
    "ambient_tangent_delta",
    "RAG/tool whiplash",
    "Jerk Is A Review Signal",
    "jerk is a review signal",
    "quickly characterizing the trajectory",
    "review attention",
    "uncertainty has shape",
    "shape has substructure",
    "shape has motion",
    "kinematic_trajectory",
    "decision-pga diagnose --pretty examples/agent/kinematic_trajectory_rag_tool_whiplash.json",
    "canonical_path_probabilities",
    "step_kinetic_energy",
    "step_jerk",
    "systemic_kinetic_energy",
    "systemic_jerk",
    "velocity_dispersion",
    "primary_drift_labels",
]
```

Add this validation block after the article checks and before the `index = ...` line:

```python
    kinematics = (ROOT / "kinematics.md").read_text(encoding="utf-8")
    normalized_kinematics = " ".join(kinematics.split())
    for phrase in KINEMATICS_REQUIRED_PHRASES:
        require(
            phrase in kinematics or phrase in normalized_kinematics,
            f"Kinematic article missing required phrase/link: {phrase}",
        )
    require("schema_type: TechArticle" in kinematics, "Kinematic article should be marked as TechArticle")
    require("permalink: /kinematics/" in kinematics, "Kinematic article should use the public permalink")
    require("{{ '/article/' | relative_url }}" in kinematics, "Kinematic article should link back to the original article")
    require("{{ '/telescoping/' | relative_url }}" in kinematics, "Kinematic article should link to the telescoping companion")
    require("https://github.com/zmichels/Decision-PGA" in kinematics, "Kinematic article should link to the public code repo")
```

- [ ] **Step 2: Run validation and confirm the red state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
Missing required file: kinematics.md
```

- [ ] **Step 3: Create the kinematic companion article**

Create `kinematics.md` with this full content:

```markdown
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
model mechanics. They do not decide whether the underlying answer is correct.
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
wrong next action compound. Quickly characterizing the trajectory can matter
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
```

- [ ] **Step 4: Run validation and confirm the green state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
site validation passed
```

- [ ] **Step 5: Commit the page contract and article**

Run:

```bash
git add scripts/validate_publication.py kinematics.md
git commit -m "Add kinematic companion article"
```

Expected result: one commit containing the new page and page-level validation.

## Task 2: Primary Navigation And Landing Page Discovery

**Files:**
- Modify: `scripts/validate_publication.py`
- Modify: `_layouts/default.html`
- Modify: `index.md`

- [ ] **Step 1: Add validation checks for nav and landing page discovery**

In `scripts/validate_publication.py`, add these checks after the existing index checks for the telescoping companion:

```python
    require("Read kinematics" in index, "Landing page missing kinematic call to action")
    require("Kinematic Decision-PGA" in index, "Landing page should mention the kinematic companion")
    require("{{ '/kinematics/' | relative_url }}" in index, "Landing page should link to the kinematic companion")
```

Add these layout checks after the existing `Telescoping` nav check:

```python
    require("Kinematics" in layout, "Nav should link to the kinematic companion article")
    require("{{ '/kinematics/' | relative_url }}" in layout, "Nav should use the relative kinematic article link")
```

- [ ] **Step 2: Run validation and confirm the red state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
Landing page missing kinematic call to action
```

- [ ] **Step 3: Add the nav link**

In `_layouts/default.html`, replace the current primary nav block:

```html
        <a href="{{ '/article/' | relative_url }}">Article</a>
        <a href="{{ '/telescoping/' | relative_url }}">Telescoping</a>
        <a href="{{ '/demo/' | relative_url }}">Demo</a>
```

with:

```html
        <a href="{{ '/article/' | relative_url }}">Article</a>
        <a href="{{ '/telescoping/' | relative_url }}">Telescoping</a>
        <a href="{{ '/kinematics/' | relative_url }}">Kinematics</a>
        <a href="{{ '/demo/' | relative_url }}">Demo</a>
```

- [ ] **Step 4: Update the landing page hero**

In `index.md`, replace this paragraph:

```markdown
    Decision-PGA is a prototype framework for describing the shape of
    uncertainty around AI decisions before a workflow acts. This site gathers
    the article series, a synthetic demo, the agent toolkit, the public code
    repository, and PDF copies.
```

with:

```markdown
    Decision-PGA is a prototype framework for describing the shape of
    uncertainty around AI decisions before a workflow acts. This site gathers
    the article series, the kinematic trajectory companion, a synthetic demo,
    the agent toolkit, the public code repository, and PDF copies.
```

Replace the hero actions block:

```markdown
    <a class="button" href="{{ '/article/' | relative_url }}">Read the article</a>
    <a class="button secondary" href="{{ '/telescoping/' | relative_url }}">Read the follow-up</a>
    <a class="button secondary" href="{{ '/demo/' | relative_url }}">Try the demo</a>
```

with:

```markdown
    <a class="button" href="{{ '/article/' | relative_url }}">Read the article</a>
    <a class="button secondary" href="{{ '/telescoping/' | relative_url }}">Read the follow-up</a>
    <a class="button secondary" href="{{ '/kinematics/' | relative_url }}">Read kinematics</a>
    <a class="button secondary" href="{{ '/demo/' | relative_url }}">Try the demo</a>
```

- [ ] **Step 5: Update the landing page site-purpose text and grid**

In `index.md`, replace:

```markdown
This site is a compact public entry point for Decision-PGA: the framing article,
the Telescoping Decision-PGA companion perspective, the synthetic
document-triage demo, the agent toolkit, the open-source prototype repository,
and PDF versions of the articles.
```

with:

```markdown
This site is a compact public entry point for Decision-PGA: the framing article,
the Telescoping Decision-PGA companion perspective, the Kinematic Decision-PGA
trajectory companion, the synthetic document-triage demo, the agent toolkit,
the open-source prototype repository, and PDF versions of the articles.
```

Add this panel immediately after the `Telescoping Decision-PGA` panel:

```html
  <section class="panel">
    <h3><a href="{{ '/kinematics/' | relative_url }}">Kinematic Decision-PGA</a></h3>
    <p>
      The kinematic companion explains how observed decision states can move
      across retrieval, tool use, and final output, including RAG/tool whiplash
      and jerk as review signals.
    </p>
  </section>
```

In the `Current Status` list, replace:

```markdown
- Article series and PDFs: available for public reading and critique.
```

with:

```markdown
- Article series and PDFs: available for public reading and critique.
- Kinematic trajectory page: companion perspective on velocity, drift, and jerk.
```

- [ ] **Step 6: Run validation and confirm the green state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
site validation passed
```

- [ ] **Step 7: Commit the navigation and landing page changes**

Run:

```bash
git add scripts/validate_publication.py _layouts/default.html index.md
git commit -m "Surface kinematic companion on site home"
```

Expected result: one commit containing the discovery path from the header and landing page.

## Task 3: Article, Telescoping, And Toolkit Cross-Links

**Files:**
- Modify: `scripts/validate_publication.py`
- Modify: `article.md`
- Modify: `telescoping.md`
- Modify: `toolkit.md`

- [ ] **Step 1: Add validation checks for companion cross-links**

In `scripts/validate_publication.py`, add these checks after the existing article telescoping-link checks:

```python
    require("Kinematic Decision-PGA" in article, "Article should link to the kinematic companion article")
    require("{{ '/kinematics/' | relative_url }}" in article, "Article should use the relative kinematic article link")
```

Add these checks after the existing telescoping article link checks:

```python
    require("{{ '/kinematics/' | relative_url }}" in telescoping, "Telescoping article should link to the kinematic companion")
    require("shape has motion" in telescoping, "Telescoping article should point to the motion companion")
```

Add these toolkit checks after the existing toolkit required phrase loop:

```python
    for phrase in [
        "Kinematic Decision-PGA",
        "{{ '/kinematics/' | relative_url }}",
        "Kinematic trajectory whiplash",
        "kinematic_trajectory",
        "RAG/tool whiplash",
        "step_jerk",
        "kinematic_trajectory_rag_tool_whiplash.json",
    ]:
        require(phrase in toolkit, f"Toolkit page missing kinematic phrase: {phrase}")
```

- [ ] **Step 2: Run validation and confirm the red state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
Article should link to the kinematic companion article
```

- [ ] **Step 3: Cross-link from the original article**

In `article.md`, add this paragraph after the existing `Telescoping Decision-PGA` companion paragraph and before `The public prototype code is available at`:

```markdown
A second companion,
[Kinematic Decision-PGA]({{ '/kinematics/' | relative_url }}), follows the
same line of thought across workflow steps: uncertainty has shape, shape has
substructure, and shape has motion.
```

- [ ] **Step 4: Cross-link from the telescoping article**

In `telescoping.md`, replace this opening paragraph:

```markdown
This companion perspective extends
[Decision-PGA and the Need for Decision-State Diagnostics]({{ '/article/' | relative_url }})
by focusing on how uncertainty clouds can contain smaller local structures and
cross-document bridges. A PDF copy is available at
[assets/telescoping-decision-pga.pdf]({{ '/assets/telescoping-decision-pga.pdf' | relative_url }}).
```

with:

```markdown
This companion perspective extends
[Decision-PGA and the Need for Decision-State Diagnostics]({{ '/article/' | relative_url }})
by focusing on how uncertainty clouds can contain smaller local structures and
cross-document bridges. The next companion,
[Kinematic Decision-PGA]({{ '/kinematics/' | relative_url }}), follows the
same diagnostic line into workflow motion: uncertainty has shape, shape has
substructure, and shape has motion. A PDF copy is available at
[assets/telescoping-decision-pga.pdf]({{ '/assets/telescoping-decision-pga.pdf' | relative_url }}).
```

- [ ] **Step 5: Add a toolkit pointer**

In `toolkit.md`, add this paragraph after the paragraph ending `It is not a production safety layer or a claim that an answer is correct.`:

```markdown
For trajectory-specific reading, see
[Kinematic Decision-PGA]({{ '/kinematics/' | relative_url }}), which explains
how velocity, drift, and jerk can characterize observed motion across RAG,
tool-use, and final-output steps.
```

- [ ] **Step 6: Add the RAG/tool whiplash gallery card**

In `toolkit.md`, add this panel immediately after the `Multi-step agent drift` panel:

```html
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
```

- [ ] **Step 7: Run validation and confirm the green state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
site validation passed
```

- [ ] **Step 8: Commit the cross-link changes**

Run:

```bash
git add scripts/validate_publication.py article.md telescoping.md toolkit.md
git commit -m "Cross-link kinematic companion"
```

Expected result: one commit containing article-series and toolkit cross-links.

## Task 4: Public Discovery Metadata And README

**Files:**
- Modify: `scripts/validate_publication.py`
- Modify: `sitemap.xml`
- Modify: `llms.txt`
- Modify: `README.md`

- [ ] **Step 1: Add validation checks for discovery files**

In the `sitemap` required phrase list in `scripts/validate_publication.py`, add:

```python
        "{{ \"/kinematics/\" | absolute_url }}",
```

In the `llms` required phrase list, add:

```python
        "Kinematic companion",
        "{{ \"/kinematics/\" | absolute_url }}",
        "kinematic_trajectory",
```

After the `llms` validation loop, add this README validation block:

```python
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in [
        "Kinematic Decision-PGA",
        "kinematic trajectory companion",
        "kinematics.md",
    ]:
        require(phrase in readme, f"README missing kinematic phrase: {phrase}")
```

- [ ] **Step 2: Run validation and confirm the red state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
sitemap.xml missing required phrase: {{ "/kinematics/" | absolute_url }}
```

- [ ] **Step 3: Add the sitemap entry**

In `sitemap.xml`, add this block after the `/telescoping/` URL entry:

```xml
  <url>
    <loc>{{ "/kinematics/" | absolute_url }}</loc>
    <lastmod>2026-06-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
```

- [ ] **Step 4: Update `llms.txt` canonical pages and entry points**

In `llms.txt`, add this line after `Telescoping companion` in `Canonical Pages`:

```markdown
- Kinematic companion: {{ "/kinematics/" | absolute_url }}
```

In `Best Entry Points For AI Assistants`, add this bullet after the telescoping bullet:

```markdown
- Use the kinematic companion for observed trajectory diagnostics, RAG/tool
  whiplash, and jerk as a review signal.
```

In `Technical Summary`, add this sentence after the existing paragraph:

```markdown
The `kinematic_trajectory` source type extends the diagnostic from static
probability clouds to observed movement across workflow steps, including
velocity, step kinetic energy, and jerk summaries.
```

- [ ] **Step 5: Update README site summary and contents**

In `README.md`, replace:

```markdown
The site links the article, the Telescoping Decision-PGA companion perspective,
synthetic document-triage demo, agent toolkit page, PDF copies, and the public
Decision-PGA prototype repository:
```

with:

```markdown
The site links the article, the Telescoping Decision-PGA companion perspective,
the Kinematic Decision-PGA trajectory companion, synthetic document-triage
demo, agent toolkit page, PDF copies, and the public Decision-PGA prototype
repository:
```

In the `Contents` list, add this line immediately after `telescoping.md`:

```markdown
- `kinematics.md` - companion article on velocity, drift, RAG/tool whiplash, and jerk
```

- [ ] **Step 6: Run validation and confirm the green state**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
site validation passed
```

- [ ] **Step 7: Commit public discovery changes**

Run:

```bash
git add scripts/validate_publication.py sitemap.xml llms.txt README.md
git commit -m "Add kinematic companion discovery metadata"
```

Expected result: one commit containing sitemap, LLM discovery, README, and their validator checks.

## Task 5: Final Verification

**Files:**
- Inspect: all changed files from Tasks 1-4.

- [ ] **Step 1: Run the publication validator**

Run:

```bash
python3 scripts/validate_publication.py
```

Expected result:

```text
site validation passed
```

- [ ] **Step 2: Check for whitespace or patch formatting issues**

Run:

```bash
git diff --check
```

Expected result: no output and exit code `0`.

- [ ] **Step 3: Check for accidental planning markers in public files**

Run:

```bash
rg -n 'TO''DO|T''BD|fill in de''tails|imple''ment later|sim''ilar to Ta''sk' kinematics.md index.md article.md telescoping.md toolkit.md llms.txt README.md scripts/validate_publication.py
```

Expected result: no matches and exit code `1`.

- [ ] **Step 4: Review the staged public diff**

Run:

```bash
git log --oneline -5
git status --short --branch
```

Expected result:

- The recent commits include the kinematic companion article commits from this plan.
- `git status --short --branch` shows a clean working tree.
- The branch is ahead of `origin/main` by the new local commits until the user chooses to push.

## Self-Review Checklist For The Implementer

- [ ] The new page is article-forward, not only a developer note.
- [ ] The prose stays modest: it describes observed trajectory diagnostics and avoids claims about hidden model cognition.
- [ ] The phrase `jerk is a review signal` appears in a serious diagnostic context.
- [ ] The RAG/tool whiplash fixture is the concrete anchor.
- [ ] Quick trajectory characterization is framed around review attention and workflow delay, not revenue.
- [ ] The page links back to the original article and the telescoping companion.
- [ ] The site exposes `/kinematics/` from navigation, the landing page, sitemap, `llms.txt`, README, article, telescoping page, and toolkit page.
- [ ] `python3 scripts/validate_publication.py` passes at the end.
