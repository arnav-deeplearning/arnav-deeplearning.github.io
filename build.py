#!/usr/bin/env python3
"""
Static site builder.

Renders the Jinja2 templates in templates/ into plain HTML files at the
repo root (index.html, bio.html, ...) so GitHub Pages can serve them
directly with zero server-side Python required at runtime.

Usage:
    python build.py

Add a new page:
    1. Add a template in templates/, extending base.html.
    2. Add its content to data/content.py if needed.
    3. Add an entry to the PAGES list below: (template_name, output_name, extra_context).
"""
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from data import content, flashcards

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT  # GitHub Pages (user site) serves straight from repo root
STATIC_DATA_DIR = ROOT / "static" / "data"

BASE_CONTEXT = {
    "site": content.SITE,
    "nav": content.NAV,
}

FLASHCARDS_DATA = {"categories": flashcards.FLASHCARD_CATEGORIES, "cards": flashcards.FLASHCARDS}

PAGES = [
    ("index.html", "index.html", {
        "apps_preview": content.APPS[:3],
        "status_labels": content.STATUS_LABELS,
        "journey_preview": content.JOURNEY[-3:],
        "profile": content.PROFILE,
    }),
    ("bio.html", "bio.html", {
        "profile": content.PROFILE,
        "paragraphs": content.BIO_PARAGRAPHS,
    }),
    ("journey.html", "journey.html", {
        "journey": content.JOURNEY,
        "profile": content.PROFILE,
    }),
    ("gallery.html", "gallery.html", {
        "gallery": content.GALLERY,
    }),
    ("resources.html", "resources.html", {
        "apps": content.APPS,
        "status_labels": content.STATUS_LABELS,
    }),
    ("flashcards.html", "flashcards.html", {
        "belt_levels": content.BELT_LEVELS,
        "categories": flashcards.FLASHCARD_CATEGORIES,
        "cards_json": json.dumps(FLASHCARDS_DATA),
    }),
]


def build():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    for template_name, output_name, extra_context in PAGES:
        template = env.get_template(template_name)
        context = {**BASE_CONTEXT, **extra_context, "active_page": output_name}
        html = template.render(**context)
        out_path = OUTPUT_DIR / output_name
        out_path.write_text(html, encoding="utf-8")
        print(f"built {out_path.relative_to(ROOT)}")

    STATIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    flashcards_json = STATIC_DATA_DIR / "flashcards.json"
    flashcards_json.write_text(json.dumps(FLASHCARDS_DATA, indent=2), encoding="utf-8")
    print(f"built {flashcards_json.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
