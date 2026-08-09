# arnav-deeplearning.github.io

Arnav's Taekwondo x AI site — a 3rd Dan black belt's passion project
combining Taekwondo with AI/software, building toward adaptive training
apps for special needs children in the TKD community.

## How this site is built

The site is a **Python-generated static site**: content lives in plain
Python data structures, gets rendered through Jinja2 templates, and the
output is plain HTML/CSS/JS that GitHub Pages serves with no server-side
code required at runtime.

```
data/content.py      -> all editable content (bio, journey, apps, gallery)
templates/            -> Jinja2 templates (base.html + one per page)
static/               -> CSS, JS, images
build.py              -> renders templates -> data into HTML files at repo root
index.html, bio.html, journey.html, gallery.html, resources.html
                      -> generated output (committed, served by GitHub Pages)
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Editing content

Almost everything on the site (bio text, journey milestones, app cards,
gallery captions) lives in [`data/content.py`](data/content.py). Edit
that file, then rebuild:

```bash
python build.py
```

This regenerates `index.html`, `bio.html`, `journey.html`,
`gallery.html`, and `resources.html` at the repo root. Commit the
regenerated HTML along with your `data/content.py` change.

## Adding a new app card

Open `data/content.py` and add an entry to the `APPS` list:

```python
{
    "title": "My New App",
    "icon": "🧠",
    "status": "planned",  # live | coming-soon | in-development | planned
    "description": "One or two sentences about what it does.",
    "tags": ["Some tag", "Another tag"],
},
```

Run `python build.py` and the card appears on both the homepage preview
and the full `resources.html` page — no template edits needed.

## Adding real photos

Drop images into `static/images/gallery/`, then set the matching
`"src"` filename on an entry in the `GALLERY` list in
`data/content.py`, and rebuild.

## Roadmap for the apps themselves

The "Apps & Resources" page currently shows placeholder cards for:

1. **TKD Flashcards** — Korean terminology, poomsae names, belt vocab
2. **TKD Quiz** — leveled by belt rank (see `BELT_LEVELS` in `content.py`)
3. **Form Correction AI** — computer-vision feedback, built accessibility-first
4. **Adaptive Coaching Tips** — sensory-friendly guidance for special needs students

Each of these will likely become its own small Python/JS app (or a
Flask/FastAPI backend + simple frontend) added as its own subfolder or
subdomain, with a live link swapped into its `APPS` entry once ready.
