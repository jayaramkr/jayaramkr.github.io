# jayaramkr.github.io

Personal site for K. R. Jayaram, built with Jekyll and served by GitHub Pages
from the `main` branch. No build step, no GitHub Actions — push to `main` and
GitHub rebuilds the site in about a minute.

## Editing

Everything you'd normally want to change is in one of four places:

| What | Where |
| --- | --- |
| Bio, research narrative, "Elsewhere" links | `index.md` |
| Site title, tagline, nav, footer links | `_config.yml` |
| CV: positions, education, recognition | `cv.md` |
| Program committees, chairing, journal reviewing | `_data/service.yml` |
| News on the home page, and Writing on the publications page | `_data/news.yml` |
| Research themes: prose | `research.md` |
| Research themes: which papers/patents belong to each | `_data/themes.yml` |
| Publications | `_data/publications.yml` |
| Patents | `_data/patents.yml` |

Prose is plain Markdown — edit it in the GitHub web editor (press `.` in the repo
to get a full editor in the browser) or locally, and commit.

### Removing the "under construction" banner

Set `under_construction: false` in `_config.yml`.

### Adding a publication

Append to `_data/publications.yml`, newest anywhere — the page sorts by year:

```yaml
- key: "conf/venue/YourKey26"
  title: "Title of the Paper"
  authors:
    - "First Author"
    - "K. R. Jayaram"
  year: 2026
  venue: "NeurIPS"
  type: inproceedings
  arxiv: "2601.01234"   # optional
  doi: "10.1145/..."    # optional
  selected: true        # optional: also show it on the home page
```

Your own name is matched against `publishing_name:` in `_config.yml` (`K. R.
Jayaram`) and bolded automatically — that's deliberately separate from `title:`
(`Jayaram K Radhakrishnan`), which is the name in the site header.
`selected: true` controls the home-page list — there's no cap, but six or so
reads best.

### Adding a patent

Append to `_data/patents.yml`:

```yaml
- ref: "P202600123"
  title: "Title of the Invention"
  year: 2026
  status: granted        # granted | pending | filed | defensive
  grants:                # only for status: granted
    - country: US
      number: "12345678"
      pdf: "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12345678"
  # pending: [US]        # use instead of `grants` for status: pending
```

A grant can carry two optional link fields:

- `pdf:` renders a separate "PDF" label. Use for direct PDF documents.
  `patents_to_yaml.py` fills this in for US grants from the USPTO document
  endpoint.
- `url:` turns the grant number itself into a link. Use for patent *pages*
  (Google Patents, Espacenet) that aren't a direct PDF.

CN, JP, and GB grant numbers have no equivalent stable public URL, so those
render as plain numbers. Add either field by hand if you find a link — or, so a
re-run of the script keeps it, add it to `GRANT_URL` at the top of
`scripts/patents_to_yaml.py`.

### Editing the research page

`research.md` holds one `##` section of prose per theme. The paper and patent list
under each theme is not written there — it comes from `_data/themes.yml`, which
maps a theme id to DBLP keys and patent refs:

```yaml
- id: agentic-memory
  title: "Agentic memory and self-improving agents"
  span: "2025–2026"
  papers:
    - "journals/corr/abs-2603-10600"
  patents:
    - "P202600929"
```

To move a paper between themes, move its key. To add a theme, add an entry here,
then add a matching `##` section in `research.md` with an `{% raw %}{% assign %}{% endraw %}`
lookup at the top of the file and an `{% raw %}{% include theme_items.html %}{% endraw %}`
at the end of the section — copy an existing one. Keep the Liquid `assign` tags at
the top of the file: a whitespace-trimming tag placed directly under a Markdown
heading swallows the blank line and pulls the next paragraph into the heading.

### Adding a news item

`_data/news.yml` drives both the News section on the home page and the Writing
section on the publications page. Newest goes at the top — the file order is the
display order, it is not sorted by date.

```yaml
- kind: writing          # writing | talk | other
  title: "Post or talk title"
  url: https://example.com/post
  outlet: Where it appeared
  date: September 2026   # optional, free text; omitted renders without a date
  note: >-
    One line of context. Optional.
```

Only `kind: writing` entries appear on the publications page; the home page
shows the most recent four of everything. Change `limit=4` in `index.md` to show
more.

### Adding service entries

`_data/service.yml` has three lists — `organizing`, `program_committee` and
`journals`. Append to whichever fits:

```yaml
program_committee:
  - venue: Conference Name (ACRONYM)
    years: "2019, 2021, 2024"
    note: Young Researchers' Symposium   # optional
```

`years` is a free-text string, so `"2020, 2021"` and `"2014–2016"` both work.
Leave it out entirely and the entry renders without years — useful when you know
you served but not which year. `note` is optional and renders after the years;
use it only where the plain venue name would overstate the role, such as serving
on a satellite symposium rather than the main conference.

The PC list is ordered by most recent year of service, newest first. Journal
reviewing currently stops at 2015 — that is a gap in the source CV, not a
rendering issue, and the page says so.

### Regenerating from source exports

The two YAML files were generated from a DBLP BibTeX export and the IBM
invention-details CSV. To refresh them wholesale:

```sh
python3 scripts/bib_to_yaml.py ~/Downloads/dblp.bib
python3 scripts/patents_to_yaml.py ~/Downloads/Invention_Details.csv
```

Both overwrite their YAML file completely, so hand-edits are lost. The
publications script keeps a `SELECTED` list at the top — update it there rather
than in the YAML if you plan to re-run the script. For one-off additions, just
edit the YAML.

## Previewing locally

Optional; GitHub Pages builds without it.

```sh
bundle install
bundle exec jekyll serve   # http://localhost:4000
```

## Layout

```
_config.yml                site settings, nav, footer links
_data/                     publications.yml, patents.yml
_includes/                 head.html, publication.html
_layouts/default.html      the only layout
assets/css/main.css        all the styling; tokens at the top
index.md                   home
publications.md            full list, grouped by year
patents.md                 granted / pending / other
404.html
scripts/                   regenerate the YAML from source exports
```
