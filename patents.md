---
layout: default
permalink: /patents/
title: Patents
subtitle: Inventions filed at IBM, grouped by invention rather than by filing — one entry may have issued in several jurisdictions. Filed under my full legal name, Jayaram Kallapalayam Radhakrishnan.
description: Patents and patent applications by Jayaram K Radhakrishnan, covering agentic memory, AI agents, federated learning, and deep learning infrastructure.
---

{%- assign granted = site.data.patents | where: "status", "granted" | sort: "year" | reverse -%}
{%- assign pending = site.data.patents | where: "status", "pending" | sort: "year" | reverse -%}
{%- assign filed = site.data.patents | where: "status", "filed" | sort: "year" | reverse -%}
{%- assign defensive = site.data.patents | where: "status", "defensive" | sort: "year" | reverse -%}

{%- assign grant_count = 0 -%}
{%- for p in granted -%}{%- assign grant_count = grant_count | plus: p.grants.size -%}{%- endfor -%}

<p class="summary">
{{ granted | size }} granted inventions ({{ grant_count }} issued patents across jurisdictions),
{{ pending | size }} pending applications. Years shown are the disclosure year.
US grants link to the full document on USPTO; the CN, JP, and GB counterparts
have no stable public PDF to link to.
</p>

## Granted

<ul class="pub-list">
{%- for p in granted -%}
  <li>
    <span class="pub-title">{{ p.title }}</span>
    <span class="patent-numbers">
      {%- for g in p.grants -%}
        {{ g.country }}&nbsp;<span class="num">{{ g.number }}</span>
        {%- if g.pdf %}&nbsp;<a class="pdf" href="{{ g.pdf }}">PDF</a>{% endif -%}
        {%- unless forloop.last %}<span class="sep">·</span>{% endunless -%}
      {%- endfor -%}
    </span>
    <span class="pub-meta">Disclosed {{ p.year }}</span>
  </li>
{%- endfor -%}
</ul>

## Pending applications

<ul class="pub-list">
{%- for p in pending -%}
  <li>
    <span class="pub-title">{{ p.title }}</span>
    <span class="pub-meta">Disclosed {{ p.year }}{% if p.pending %}<span class="sep">·</span>{{ p.pending | join: ", " }}{% endif %}</span>
  </li>
{%- endfor -%}
</ul>

{% if filed.size > 0 or defensive.size > 0 %}
## Other disclosures

<ul class="pub-list">
{%- for p in filed -%}
  <li>
    <span class="pub-title">{{ p.title }}<span class="tag">filed</span></span>
    <span class="pub-meta">Disclosed {{ p.year }}</span>
  </li>
{%- endfor -%}
{%- for p in defensive -%}
  <li>
    <span class="pub-title">{{ p.title }}<span class="tag">defensive publication</span></span>
    <span class="pub-meta">Disclosed {{ p.year }}</span>
  </li>
{%- endfor -%}
</ul>
{% endif %}
