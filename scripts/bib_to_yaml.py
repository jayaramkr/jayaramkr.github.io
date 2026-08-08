#!/usr/bin/env python3
"""Regenerate _data/publications.yml from a DBLP BibTeX export.

    python3 scripts/bib_to_yaml.py path/to/dblp.bib

Get a fresh export from https://dblp.org/pid/21/2983.html -> "export records" ->
BibTeX. The script shortens venue names and merges each arXiv preprint into its
published version, so a paper appears once.

It overwrites _data/publications.yml wholesale. If you have hand-edited that file
(e.g. changed which papers are `selected: true`), either update SELECTED below
first, or skip this script and edit the YAML directly -- the YAML is what the site
reads, not the .bib.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_data", "publications.yml")

# Papers featured on the home page, by DBLP key (the part after "DBLP:").
SELECTED = [
    "journals/corr/abs-2603-10600",       # Trajectory-Informed Memory Generation
    "journals/corr/abs-2602-03007",       # VOILA
    "conf/emnlp/DuesterwaldHIJK25",       # FLOW-BENCH
    "conf/emnlp/BhopeVJIMV25",            # OptiSeq
    "conf/middleware/BhopeJVVT23",        # FLIPS
    "conf/middleware/JayaramMDIWHBAT19",  # FfDL
]

# DBLP key prefix -> short venue name shown on the site.
SLUG = {
    "journals/corr": "arXiv",
    "journals/tpds": "IEEE TPDS",
    "journals/toit": "ACM TOIT",
    "journals/tocs": "ACM TOCS",
    "journals/taosd": "LNCS TAOSD",
    "journals/ibmrd": "IBM J. Res. Dev.",
    "conf/middleware": "Middleware",
    "conf/emnlp": "EMNLP",
    "conf/eurosys": "EuroSys",
    "conf/icdcs": "ICDCS",
    "conf/icse": "ICSE",
    "conf/issre": "ISSRE",
    "conf/dsn": "DSN",
    "conf/debs": "DEBS",
    "conf/aosd": "AOSD",
    "conf/ecoop": "ECOOP",
    "conf/pppj": "PPPJ",
    "conf/compsac": "COMPSAC",
    "conf/coordination": "COORDINATION",
    "conf/wdag": "DISC",
    "conf/mascots": "MASCOTS",
    "conf/ipps": "IPDPS Workshops",
    "conf/icac": "IEEE ICAC",
    "conf/ic2e": "IEEE IC2E",
    "conf/bigdataconf": "IEEE Big Data",
    "conf/bigdata": "IEEE BigData Congress",
    "conf/IEEEcloud": "IEEE CLOUD",
    "conf/IEEEscc": "IEEE SSE",
    "conf/wosc": "WoSC",
    "conf/sosp": "ResilientFL @ SOSP",
    "books/sp": "Book chapter",
}

# Per-paper overrides, where the track or workshop matters.
OVERRIDE = {
    "conf/emnlp/BhopeVJIMV25": "EMNLP Findings",
    "conf/emnlp/DuesterwaldHIJK25": "EMNLP Industry Track",
    "conf/middleware/BhopeVJIMV25": "Middleware (Demos & Posters)",
    "conf/middleware/DuesterwaldIJKM24": "Middleware Industrial Track",
    "conf/ecoop/JayaramE09": "COP @ ECOOP",
    "conf/middleware/2017": "Middleware 2017 (proceedings)",
    "conf/middleware/2015i": "Middleware 2015 Industrial Track (proceedings)",
}

# arXiv key -> published key, for pairs whose titles differ too much to match.
MANUAL_MERGE = {"journals/corr/abs-2501-15030": "conf/emnlp/BhopeVJIMV25"}

# DBLP writes accents as {\'{a}}, {\"{\i}}, {\c{c}} and so on. Rather than
# enumerate every combination, drop the accent command and keep the base letter.
# ASCII-folding is deliberate: it keeps names stable in URLs and search.
ACCENT_RE = re.compile(r"\{\\[`'\"^~=.buvcHkr]\s*\{\\?([a-zA-Z]+)\}\}")
# Standalone letter commands that have no base letter to keep.
LIGATURES = {r"{\aa}": "a", r"{\AA}": "A", r"{\o}": "o", r"{\O}": "O",
             r"{\l}": "l", r"{\L}": "L", r"{\i}": "i", r"{\j}": "j",
             r"{\ss}": "ss", r"{\ae}": "ae", r"{\AE}": "AE"}

ACRONYM_RE = re.compile(r"\{([A-Z][A-Za-z0-9/&+-]{1,14})\}")
STOP_ACRONYMS = {"USA", "UK", "TN", "CA", "NY", "WA", "TX", "IL", "MA", "DC"}


def clean(s):
    """Strip BibTeX braces, LaTeX accents, and line wrapping."""
    s = re.sub(r"\s+", " ", s).strip()
    s = ACCENT_RE.sub(r"\1", s)
    for pat, rep in LIGATURES.items():
        s = s.replace(pat, rep)
    s = s.replace("{\\&}", "&")
    s = re.sub(r"\\emph\{([^}]*)\}", r"\1", s)
    # LaTeX-escaped punctuation, e.g. the \_ that DBLP puts in Springer DOIs.
    s = re.sub(r"\\([_&%#$])", r"\1", s)
    s = s.replace("{", "").replace("}", "").replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()


def parse_entries(text):
    entries = []
    for m in re.finditer(r"^@(\w+)\{([^,]+),\n(.*?)\n\}\n", text, re.S | re.M):
        fields = {}
        for fm in re.finditer(r"^  (\w+)\s*=\s*\{(.*?)\},?$", m.group(3), re.S | re.M):
            fields[fm.group(1)] = fm.group(2)
        entries.append((m.group(1), m.group(2), fields))
    return entries


def fallback_venue(kind, f):
    """Used when the DBLP key prefix isn't in SLUG: guess from the venue text."""
    if kind == "article":
        journal = clean(f.get("journal", ""))
        return "arXiv" if journal == "CoRR" else journal
    booktitle = f.get("booktitle", "")
    cands = [a for a in ACRONYM_RE.findall(booktitle) if a not in STOP_ACRONYMS]
    for a in cands:
        if re.search(re.escape("{" + a + "}") + r"\s*'?\d{2,4}", booktitle):
            return a
    if cands:
        return cands[-1]
    first = clean(booktitle).split(",")[0]
    return re.sub(r"^Proceedings of (the )?", "", first)


def venue_for(entry, kind, fields):
    if entry["key"] in OVERRIDE:
        return OVERRIDE[entry["key"]]
    slug = "/".join(entry["key"].split("/")[:2])
    return SLUG.get(slug) or fallback_venue(kind, fields)


def norm_title(t):
    t = re.sub(r"\((short|poster) paper\)", "", t.lower())
    return re.sub(r"[^a-z0-9]+", "", t)


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_bib(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.endswith("\n"):
        text += "\n"

    pubs = []
    for kind, key, f in parse_entries(text):
        raw_authors = f.get("author") or f.get("editor", "")
        entry = {
            "key": key.replace("DBLP:", ""),
            "type": kind,
            "title": clean(f.get("title", "")).rstrip("."),
            "authors": [clean(a) for a in raw_authors.split(" and\n")] if raw_authors else [],
            "year": int(clean(f.get("year", "0")) or 0),
        }
        entry["venue"] = venue_for(entry, kind, f)
        if kind == "proceedings":
            entry["role"] = "editor"
        for src, dst in (("eprint", "arxiv"), ("doi", "doi"), ("url", "url")):
            if f.get(src):
                entry[dst] = clean(f[src])
        pubs.append(entry)
    return pubs


def merge_preprints(pubs):
    """Fold an arXiv entry into its published counterpart, keeping the arXiv id."""
    by_key = {e["key"]: e for e in pubs}
    published = {norm_title(e["title"]): e for e in pubs
                 if not e["key"].startswith("journals/corr")}

    kept, dropped = [], 0
    for e in pubs:
        if e["key"].startswith("journals/corr"):
            target = by_key.get(MANUAL_MERGE.get(e["key"])) or published.get(norm_title(e["title"]))
            if target is not None:
                if e.get("arxiv"):
                    target["arxiv"] = e["arxiv"]
                dropped += 1
                continue
            e["preprint"] = True
        kept.append(e)
    return kept, dropped


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    pubs, dropped = merge_preprints(load_bib(sys.argv[1]))
    pubs.sort(key=lambda p: (-p["year"], p["title"]))

    lines = [
        "# Publications, generated by scripts/bib_to_yaml.py from the DBLP BibTeX export.",
        "# Safe to hand-edit: add `selected: true` to feature a paper on the home page,",
        "# or append new entries in the same shape.",
        "",
    ]
    for e in pubs:
        lines.append("- key: %s" % yaml_str(e["key"]))
        lines.append("  title: %s" % yaml_str(e["title"]))
        lines.append("  authors:")
        lines += ["    - %s" % yaml_str(a) for a in e["authors"]]
        lines.append("  year: %d" % e["year"])
        lines.append("  venue: %s" % yaml_str(e["venue"]))
        lines.append("  type: %s" % e["type"])
        if e.get("role"):
            lines.append("  role: %s" % e["role"])
        if e.get("preprint"):
            lines.append("  preprint: true")
        for field in ("arxiv", "doi", "url"):
            if e.get(field):
                lines.append("  %s: %s" % (field, yaml_str(e[field])))
        if e["key"] in SELECTED:
            lines.append("  selected: true")
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    keys = {e["key"] for e in pubs}
    print("wrote %d entries to %s (merged away %d preprints)"
          % (len(pubs), os.path.relpath(OUT, ROOT), dropped))
    for k in SELECTED:
        if k not in keys:
            print("  warning: selected key not present in the export:", k)


if __name__ == "__main__":
    main()
