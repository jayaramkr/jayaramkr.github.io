#!/usr/bin/env python3
"""Regenerate _data/patents.yml from the IBM invention-details CSV export.

    python3 scripts/patents_to_yaml.py path/to/Invention_Details.csv

The export has one row per filing, so a single invention shows up several times
(once for the disclosure, once per jurisdiction). This groups rows by invention
reference, picks the best status across the family, and lists the jurisdictions
where it issued. Inventions that are only CLOSED or ABANDONED are dropped.
"""
import csv
import os
import re
import sys
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_data", "patents.yml")

COUNTRIES = {"US", "CN", "JP", "GB", "DE", "EP", "IN"}

# Best-to-worst; an invention takes the best status any of its filings reached.
RANK = ["GRANTED", "APPLICATION", "PUBLISHED", "FILED", "DEFENSIVE PUBLICATION",
        "AWAITING PRE-RANKING", "AWAITING SEARCH", "ABANDONED", "CLOSED"]

ACRONYMS = {"AI", "API", "GPU", "LLM", "LLMS", "IBM", "ML", "VOILA"}
SMALL_WORDS = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of",
               "on", "or", "the", "to", "via", "with", "through", "using"}


def titlecase(t):
    """The export is ALL CAPS; convert to title case, keeping acronyms upright."""
    words = re.sub(r"\s+", " ", t).strip().split(" ")
    out = []
    for i, w in enumerate(words):
        lower = w.lower()
        if i not in (0, len(words) - 1) and lower.strip("():,.") in SMALL_WORDS:
            out.append(lower)
            continue
        parts = []
        for p in re.split(r"(-)", w):
            if p.strip("():,.").upper() in ACRONYMS:
                parts.append(p.upper().replace("LLMS", "LLMs"))
            else:
                parts.append(p.lower()[:1].upper() + p.lower()[1:])
        out.append("".join(parts))
    return " ".join(out)


def jurisdiction(patent_ref, invention_ref):
    """P202009267JP01 -> JP. Legacy YOR... references are all US."""
    tail = patent_ref[len(invention_ref):] if patent_ref.startswith(invention_ref) else patent_ref
    m = re.match(r"([A-Z]{2})\d*$", tail)
    if m and m.group(1) in COUNTRIES:
        return m.group(1)
    return "US" if patent_ref.startswith("YOR") else None


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def read_rows(path):
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    header_i = next(i for i, r in enumerate(rows) if r and r[0] == "Inventor Name")
    header = rows[header_i]
    return [dict(zip(header, r)) for r in rows[header_i + 1:]
            if len(r) >= len(header) and r[1].strip()]


def build(rows):
    families = OrderedDict()
    for r in rows:
        families.setdefault(r["Invention Reference"].strip(), []).append(r)

    entries = []
    for ref, group in families.items():
        statuses = {r["Last Status"].strip() for r in group}
        best = min(statuses, key=lambda s: RANK.index(s) if s in RANK else len(RANK))

        grants = []
        for r in group:
            if r["Last Status"].strip() == "GRANTED" and r["Patent Number"].strip():
                grants.append({
                    "country": jurisdiction(r["Patent Reference"].strip(), ref) or "",
                    "number": r["Patent Number"].strip(),
                })
        grants.sort(key=lambda g: (g["country"] != "US", g["country"]))

        # Formal filing titles read better than the raw disclosure titles.
        granted_rows = [r for r in group if r["Last Status"].strip() == "GRANTED"]
        filed_rows = [r for r in group if r["Patent Reference"].strip()]
        title = titlecase((granted_rows or filed_rows or group)[0]["Invention Title"])

        dates = sorted(r["Invention Submitted Date"] for r in group if r["Invention Submitted Date"])

        pending = sorted({jurisdiction(r["Patent Reference"].strip(), ref) or "US"
                          for r in group
                          if r["Last Status"].strip() in ("APPLICATION", "PUBLISHED")})

        if grants:
            status = "granted"
        elif best in ("APPLICATION", "PUBLISHED"):
            status = "pending"
        elif best in ("FILED", "AWAITING PRE-RANKING", "AWAITING SEARCH"):
            status = "filed"
        elif best == "DEFENSIVE PUBLICATION":
            status = "defensive"
        else:
            status = "inactive"

        entries.append({"ref": ref, "title": title, "status": status, "grants": grants,
                        "pending": pending, "year": int(dates[0][:4]) if dates else 0})

    # A continuation is filed under its own reference but carries the same title;
    # show it as one invention with both numbers.
    folded = OrderedDict()
    for e in entries:
        k = re.sub(r"[^a-z0-9]+", "", e["title"].lower())
        if k not in folded:
            folded[k] = e
            continue
        f = folded[k]
        seen = {(g["country"], g["number"]) for g in f["grants"]}
        f["grants"] += [g for g in e["grants"] if (g["country"], g["number"]) not in seen]
        f["pending"] = sorted(set(f["pending"]) | set(e["pending"]))
        f["year"] = min(f["year"], e["year"])
        if e["status"] == "granted":
            f["status"] = "granted"

    entries = sorted(folded.values(), key=lambda e: (-e["year"], e["title"]))
    return entries


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    entries = build(read_rows(sys.argv[1]))
    kept = [e for e in entries if e["status"] != "inactive"]

    lines = [
        "# Patents, generated by scripts/patents_to_yaml.py from the IBM invention export.",
        "# One entry per invention; `grants` lists the jurisdictions where it issued.",
        "# status: granted | pending | filed | defensive",
        "",
    ]
    for e in kept:
        lines.append("- ref: %s" % yaml_str(e["ref"]))
        lines.append("  title: %s" % yaml_str(e["title"]))
        lines.append("  year: %d" % e["year"])
        lines.append("  status: %s" % e["status"])
        if e["grants"]:
            lines.append("  grants:")
            for g in e["grants"]:
                lines.append("    - country: %s" % g["country"])
                lines.append("      number: %s" % yaml_str(g["number"]))
        elif e["pending"]:
            lines.append("  pending: [%s]" % ", ".join(e["pending"]))
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    counts = Counter(e["status"] for e in entries)
    print("wrote %d inventions to %s (%d dropped as closed/abandoned)"
          % (len(kept), os.path.relpath(OUT, ROOT), counts["inactive"]))
    print("  granted %d (%d issued patents), pending %d, filed %d, defensive %d"
          % (counts["granted"], sum(len(e["grants"]) for e in kept),
             counts["pending"], counts["filed"], counts["defensive"]))


if __name__ == "__main__":
    main()
