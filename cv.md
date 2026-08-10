---
layout: default
permalink: /cv/
title: CV
subtitle: Positions, education, and research community service. What I actually work on is described at more length on the research page.
description: CV of Jayaram K Radhakrishnan — positions at IBM Research and HP Labs, education, and research community service.
---
{%- assign svc = site.data.service -%}

## Positions

<ul class="cv-list">
  <li>
    <span class="cv-what">IBM Research</span>
    <span class="cv-where">Yorktown Heights, NY<span class="sep">·</span>2014 – present</span>
    <span class="cv-note">Research Scientist → Staff Research Scientist → Senior Research Scientist.
    Agents and agentic memory, conversational and visual copilots for business automation,
    federated learning, and platforms for large-scale distributed training.</span>
  </li>
  <li>
    <span class="cv-what">HP Labs</span>
    <span class="cv-where">Palo Alto, CA<span class="sep">·</span>2012 – 2014</span>
    <span class="cv-note">Postdoctoral Researcher. Elastic scaling of datacenter infrastructure
    applications, and stateful event correlation across distributed security event streams.</span>
  </li>
</ul>

Earlier: research intern at IBM Research (2011), software engineering intern on Amazon Simple
Workflow (2010) and on Microsoft's Static Driver Verifier (2007), and software engineer at
Alcatel-Lucent (2004–2005).

## Education

<ul class="cv-list">
  <li>
    <span class="cv-what">Ph.D., Computer Science — Purdue University</span>
    <span class="cv-where">2012</span>
    <span class="cv-note">Thesis: <em>Engineering Efficient Event-based Distributed Systems</em>.
    Advisor: Patrick Eugster.</span>
  </li>
  <li>
    <span class="cv-what">M.S., Computer Science — Purdue University</span>
    <span class="cv-where">2008</span>
  </li>
  <li>
    <span class="cv-what">B.E. (Honors), Computer Science — BITS Pilani</span>
    <span class="cv-where">2004</span>
  </li>
</ul>

## What I work on

Agentic memory — extracting reusable knowledge from agent execution traces, and retrieving it
under a cost budget. LLM agents for enterprise automation, grounded in real API catalogs.
Federated learning: private and decentralized aggregation, participant selection, and adaptation
under distribution shift. Platforms and schedulers for large-scale distributed training. Earlier,
cloud elasticity and trust, and event-based and publish/subscribe systems.

Each of these is covered in more depth, with the papers and patents behind it, on the
[research page]({{ '/research/' | relative_url }}).

## Recognition

<ul class="cv-list plain">
  <li><span class="cv-what">Maurice H. Halstead Memorial Award</span>
      <span class="cv-where">Purdue University, 2011</span>
      <span class="cv-note">For outstanding research in software engineering.</span></li>
  <li><span class="cv-what">Best Paper, ACM/IFIP/USENIX Middleware</span>
      <span class="cv-where">2010, 2013</span></li>
  <li><span class="cv-what">IBM Outstanding Technical Achievement Award</span>
      <span class="cv-where">4×</span></li>
  <li><span class="cv-what">IBM Invention Plateau Award</span>
      <span class="cv-where">4×</span></li>
  <li><span class="cv-what">IBM Council on Innovation Leadership</span>
      <span class="cv-where">3×</span></li>
</ul>

## Service

### Standing committees

<ul class="cv-list plain">
{%- for s in svc.steering %}
  <li>
    <span class="cv-what">{{ s.role }}</span>
    <span class="cv-where">{{ s.venue }}{% if s.years %}<span class="sep">·</span>{{ s.years }}{% endif %}</span>
  </li>
{%- endfor %}
</ul>

### Organizing

<ul class="cv-list plain">
{%- for s in svc.organizing %}
  <li>
    <span class="cv-what">
      {%- if s.url -%}<a href="{{ s.url }}">{{ s.role }}</a>{%- else -%}{{ s.role }}{%- endif -%}
    </span>
    <span class="cv-where">
      {{- s.venue }}{% if s.years %}<span class="sep">·</span>{{ s.years }}{% endif %}
      {%- if s.where %}<span class="sep">·</span>{{ s.where }}{% endif -%}
    </span>
  </li>
{%- endfor %}
</ul>

{%- assign edited = site.data.publications | where_exp: "p", "svc.edited contains p.key" %}
{%- if edited.size > 0 %}
Proceedings edited in those roles:

<ul class="pub-list">
{%- for pub in edited %}{% include publication.html pub=pub %}{% endfor -%}
</ul>
{%- endif %}

### Program committees

<ul class="cv-list plain">
{%- for s in svc.program_committee %}
  <li>
    <span class="cv-what">{{ s.venue }}</span>
    {%- if s.years %}<span class="cv-where">{{ s.years }}</span>{% endif %}
  </li>
{%- endfor %}
</ul>

### Journal reviewing

<ul class="cv-list plain">
{%- for s in svc.journals %}
  <li>
    <span class="cv-what">{{ s.venue }}</span>
    {%- if s.years %}<span class="cv-where">{{ s.years }}</span>{% endif %}
  </li>
{%- endfor %}
</ul>

### Within IBM

Chaired the IBM-wide committee that evaluated invention disclosures for strategic patent
filing, for four years.

<p class="summary">
This list runs through 2018 for program committees and journals; more recent years are still
being added. The full publication record is on the
<a href="{{ '/publications/' | relative_url }}">publications page</a>, and inventions on the
<a href="{{ '/patents/' | relative_url }}">patents page</a>.
</p>
