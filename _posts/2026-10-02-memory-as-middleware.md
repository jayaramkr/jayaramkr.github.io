---
title: "Memory as Middleware for Self-Improving AI Agents"
subtitle: Agent memory today is trapped inside the agent that produced it. Our Middleware 2026 paper argues it should be a layer instead.
description: >-
  On agent memory as a middleware layer — one memory layer running under six
  independently developed agents, and the six systems challenges that come with it.
---

Your agent learned something the hard way yesterday. Today it has forgotten, and your other
agents never knew.

That is the normal state of agent memory right now. Whatever an agent learns lives inside that
agent. It rarely survives the end of the session, and it never leaves the runtime that produced
it, because it is tied to one storage engine and one user. So every team that wants durable
agents builds the same plumbing over again, and none of the results work together.

## One layer, six agents

We built a memory layer that addresses both halves of that. Lessons last across sessions, and
they carry over between agents. The same layer runs under six independently developed agents —
Claude Code, Codex, Claw Code, IBM Bob, Hermes, and CUGA — each one connecting through its own
native extension mechanism.

That is the core idea of our new paper, *Memory as Middleware for Self-Improving AI Agents*, now
on arXiv and appearing at Middleware 2026.

## Systems people have seen this shape before

Data access, messaging, transactions, caching: each of these was once hand-wired into individual
applications, and each eventually became a layer that applications could simply assume was
there. The hand-wiring did not disappear because developers got better at it. It disappeared
because the concern got factored out and given to someone else to maintain.

Agent memory is the next layer to go that way.

## What is in the paper

We describe six systems challenges a memory layer has to answer: two-sided pluggability,
host-native interposition, multi-tenant isolation, write-path consistency, federated sharing
with provenance, and lifecycle governance.

We present **ALTK-Evolve**, an open-source reference implementation. It records what agents do,
turns those records into reusable guidelines, and serves them through pluggable storage and a
standard tool protocol.

And we lay out a research agenda for the systems community, because most of these problems are
not solved — they are just newly visible once you stop treating memory as a feature of a single
agent.

## Read it

- Paper: [arXiv:2609.32091](https://arxiv.org/abs/2609.32091)
- Code: [github.com/AgentToolkit/altk-evolve](https://github.com/AgentToolkit/altk-evolve)

Joint work with Vatche Isahagian, Vinod Muthusamy, Gegi Thomas, Punleuk Oum, Gaodan Fang, and
Ashwath Vaithinathan Aravindan.
