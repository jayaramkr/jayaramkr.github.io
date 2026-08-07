---
layout: default
permalink: /publications/
title: Publications
subtitle: Peer-reviewed papers, preprints, and edited proceedings, newest first.
description: Publications by K. R. Jayaram — agents and agentic memory, federated learning, and distributed systems.
---

{%- assign pubs = site.data.publications | sort: "year" | reverse -%}
{%- assign years = pubs | map: "year" | uniq -%}

<p class="summary">
{{ pubs | size }} entries. The full record lives on
<a href="https://dblp.org/pid/21/2983.html">DBLP</a> and
<a href="https://scholar.google.com/citations?user=okMlqaMAAAAJ&hl=en">Google Scholar</a>.
</p>

{% for y in years %}
<section class="year-group">
  <div class="year-label">{{ y }}</div>
  <ul class="pub-list">
    {%- for pub in pubs -%}
      {%- if pub.year == y -%}
        {% include publication.html pub=pub %}
      {%- endif -%}
    {%- endfor -%}
  </ul>
</section>
{% endfor %}
