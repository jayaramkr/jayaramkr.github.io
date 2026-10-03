---
layout: default
permalink: /writing/
title: Writing
subtitle: Posts here, and pieces published elsewhere — shorter and less formal than the papers.
description: Writing by Jayaram K Radhakrishnan on agentic memory, self-improving agents, and the systems underneath them.
---
{%- assign elsewhere = site.data.news | where: "kind", "writing" -%}

## Posts

<ul class="news-list">
{%- for post in site.posts %}
  <li>
    <span class="news-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></span>
    <span class="news-meta">
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
    </span>
    {%- if post.subtitle %}<span class="news-note">{{ post.subtitle }}</span>{% endif -%}
  </li>
{%- endfor %}
</ul>

## Elsewhere

Written for IBM Research's blog on Hugging Face.

{% include news_list.html items=elsewhere %}
