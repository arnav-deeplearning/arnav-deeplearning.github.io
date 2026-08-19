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

from data import attendance, coaching_tips, content, flashcards, form_correction, quiz, sparring

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT  # GitHub Pages (user site) serves straight from repo root
STATIC_DATA_DIR = ROOT / "static" / "data"

BASE_CONTEXT = {
    "site": content.SITE,
    "nav": content.NAV,
}

FLASHCARDS_DATA = {"categories": flashcards.FLASHCARD_CATEGORIES, "cards": flashcards.FLASHCARDS}
QUIZ_DATA = {"levels": quiz.QUIZ_LEVELS, "categories": quiz.QUIZ_CATEGORIES, "questions": quiz.QUESTIONS}
COACHING_TIPS_DATA = {
    "categories": coaching_tips.SPECIAL_NEEDS_CATEGORIES,
    "tips": coaching_tips.TIPS,
    "sources": coaching_tips.SOURCES,
}
SPARRING_DATA = {
    "levels": sparring.SPARRING_LEVELS,
    "categories": sparring.SCENARIO_CATEGORIES,
    "scenarios": sparring.SCENARIOS,
    "sources": sparring.SOURCES,
}
ATTENDANCE_DATA = {"classes": attendance.CLASSES, "students": attendance.STUDENTS}
FORM_CORRECTION_DATA = {"stances": form_correction.STANCES}

# Each entry here gets written to static/data/<name>.json AND is available
# to any page's template context as `<name>_json` (a JSON string) so pages
# can embed their data inline instead of fetching it -- fetch() is blocked
# by browsers for local file:// pages, but an inline <script> tag isn't.
STATIC_DATASETS = {
    "flashcards": FLASHCARDS_DATA,
    "quiz": QUIZ_DATA,
    "coaching-tips": COACHING_TIPS_DATA,
    "sparring": SPARRING_DATA,
    "attendance": ATTENDANCE_DATA,
    "form-correction": FORM_CORRECTION_DATA,
}

PAGES = [
    ("index.html", "index.html", {
        "apps_preview": content.APPS[:3],
        "total_apps": len(content.APPS),
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
    ("quiz.html", "quiz.html", {
        "levels": quiz.QUIZ_LEVELS,
        "categories": quiz.QUIZ_CATEGORIES,
        "quiz_json": json.dumps(QUIZ_DATA),
    }),
    ("coaching-tips.html", "coaching-tips.html", {
        "categories": coaching_tips.SPECIAL_NEEDS_CATEGORIES,
        "sources": coaching_tips.SOURCES,
        "coaching_tips_json": json.dumps(COACHING_TIPS_DATA),
    }),
    ("sparring.html", "sparring.html", {
        "levels": sparring.SPARRING_LEVELS,
        "categories": sparring.SCENARIO_CATEGORIES,
        "sources": sparring.SOURCES,
        "sparring_json": json.dumps(SPARRING_DATA),
    }),
    ("attendance.html", "attendance.html", {
        "attendance_json": json.dumps(ATTENDANCE_DATA),
    }),
    ("form-correction.html", "form-correction.html", {
        "stances": form_correction.STANCES,
        "form_correction_json": json.dumps(FORM_CORRECTION_DATA),
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
    for name, dataset in STATIC_DATASETS.items():
        out_path = STATIC_DATA_DIR / f"{name}.json"
        out_path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
        print(f"built {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
