# Articles & Projects database

A small, PR-driven database of articles and projects with a searchable website on GitHub Pages.

- **Data:** one YAML file per entry in `entries/articles/` and `entries/projects/`
- **Rules:** `schema/entry.schema.json` (required fields, allowed values, URL formats)
- **Checks:** every pull request is validated automatically (`.github/workflows/validate.yml`)
- **Website:** on every merge to `main` the index `site/data.json` is rebuilt and the site in `site/` is deployed to GitHub Pages (`.github/workflows/deploy.yml`)

## Adding an entry

**From the website:** click *Add an article* / *Add a project*. GitHub opens a pre-filled file; edit it, choose *Propose changes*, and open the pull request.

**From git:**

```bash
cp entries/articles/example-article.yml entries/articles/my-paper-title.yml
# edit the file
python scripts/build.py --check     # optional local validation
git checkout -b add-my-paper && git add . && git commit -m "Add: my paper" && git push
```

### Fields

| field | required | notes |
|---|---|---|
| `type` | yes | `article` or `project` (must match the folder) |
| `title` | yes | |
| `authors` | articles | list of names |
| `year` | yes | integer |
| `venue` | articles | conference / journal |
| `stage` | no (articles) | `preprint`, `under-review`, `published` (default) |
| `status` | projects | `planned`, `active`, `finished` |
| `summary` | recommended | 20–1500 characters |
| `tags` | yes | `lowercase-with-dashes` |
| `links` | no | `paper`, `preprint`, `pdf`, `code`, `website`, `doi` |
| `contact` | no | |

## Updating an entry (e.g. preprint → published)

Click **✎ edit** on the entry on the website (or edit the file in git) and open a pull request. Typical change:

```yaml
year: 2027                         # publication year
venue: ICLR 2027                   # was: arXiv
stage: published                   # was: preprint
links:
  paper: https://openreview.net/…  # final version
  preprint: https://arxiv.org/abs/…  # keep the arXiv link
```

Keep the file name unchanged so links to the entry keep working. Git history keeps every earlier version.

## One-time setup

1. Create the repository and push these files.
2. In `site/index.html` set `const REPO = "owner/name"`.
3. *Settings → Pages → Source: **GitHub Actions***.
4. (Recommended) *Settings → Branches*: protect `main`, require the **validate** check before merging.

## Local preview

```bash
pip install pyyaml jsonschema
python scripts/build.py
python -m http.server -d site 8000   # open http://localhost:8000
```

## Visual identity

The site follows the CCAI Brand Guidelines (January 2026): horizontal logo in the navbar (≥ 230 px), greyscale palette with PW Prussian `#004A6C` only for small accents (underlines, highlights), Lexend Deca + Roboto Mono (self-hosted in `site/assets/fonts`, SIL OFL), and the marble + pixel-pattern key visual in the hero.
