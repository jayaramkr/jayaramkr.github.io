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

A grant renders a "PDF" link when it has a `pdf:` field. `patents_to_yaml.py`
fills that in for US grants from the USPTO document endpoint; CN, JP, and GB
grant numbers have no equivalent stable public URL, so those render as plain
numbers. Add a `pdf:` by hand if you find one.

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
