---
layout: default
description: Jayaram K Radhakrishnan — senior technical leader at IBM working on agents and automation, with a focus on agentic memory.
---
{%- comment -%}
Counts used further down. Kept at the top of the file: a Liquid tag that trims
whitespace sitting directly under a Markdown heading swallows the blank line and
pulls the next paragraph into the heading.
{%- endcomment -%}
{%- assign selected = site.data.publications | where: "selected", true | sort: "year" | reverse -%}
{%- assign granted = site.data.patents | where: "status", "granted" -%}
{%- assign pending = site.data.patents | where: "status", "pending" -%}
{%- assign grant_count = 0 -%}
{%- for p in granted %}{% assign grant_count = grant_count | plus: p.grants.size %}{% endfor -%}

# Jayaram K Radhakrishnan

<p class="intro">
I am a senior technical leader at <a href="https://research.ibm.com/people/jayaram-kr-kallapalayam-radhakrishnan">IBM Research</a>,
working on <strong>agents and automation</strong>. My current focus is <strong>agentic memory</strong> —
how autonomous agents form, store, retrieve, and reuse what they learn from experience.
</p>

<p class="namenote">
I publish as <strong>K. R. Jayaram</strong>; my patents are filed under my full legal name,
Jayaram Kallapalayam Radhakrishnan.
</p>

Agents that run real work do not fail because a single model call is weak. They fail because
nothing carries forward: the same subtask gets re-derived, hard-won context is dropped between
runs, and useful trajectories are thrown away instead of becoming reusable knowledge. Memory is
the systems problem underneath that, and it is the one I spend my time on.

## What I work on

**Agentic memory.** Turning agent trajectories into durable, retrievable knowledge — generating
memory from execution traces, generalizing subtask-level knowledge so it transfers beyond the run
that produced it, deciding what is worth keeping at all, and packaging memory so it survives
deployment.

**Agents and automation.** Conversational generation of enterprise workflows, in-context example
selection and ordering for reliable API sequence generation, and cost-aware multimodal agents that
spend inference budget where it actually buys accuracy.

**Federated and distributed learning.** Private and decentralized aggregation, intelligent
participant selection, and the security properties that make cross-silo learning practical.

**Systems for large-scale ML.** Multi-tenant deep learning platforms, elastic scaling of training
workloads, and scheduling that is aware of what the job is actually doing.

The through-line across two decades — from publish/subscribe and event correlation, through cloud
elasticity and deep learning infrastructure, to federated learning and now agents — is the same:
building the distributed systems substrate that makes a new class of computation dependable enough
to run in production.

## Selected publications

<ul class="pub-list">
{%- for pub in selected -%}
  {% include publication.html pub=pub %}
{%- endfor -%}
</ul>

[All publications →]({{ '/publications/' | relative_url }})

## Patents

{{ granted | size }} granted inventions ({{ grant_count }} issued patents worldwide) and
{{ pending | size }} pending applications, spanning agentic memory, AI agents, federated
learning, and deep learning infrastructure.

[All patents →]({{ '/patents/' | relative_url }})

## Elsewhere

My [IBM Research page](https://research.ibm.com/people/jayaram-kr-kallapalayam-radhakrishnan)
is the official one. Find me on [LinkedIn](https://www.linkedin.com/in/jayaramkr/) — that is the
best way to reach me. Publication records:
[Google Scholar](https://scholar.google.com/citations?user=okMlqaMAAAAJ&hl=en) ·
[DBLP](https://dblp.org/pid/21/2983.html).
