"""
Starter content for the Attendance Tracker app.

This app works differently from flashcards.py / quiz.py / sparring.py:
those are read-only content, but attendance records change constantly,
so they can't live in a file that only updates when someone runs
build.py. Instead:

  - CLASSES and STUDENTS below are a STARTER roster, embedded in the
    page at build time -- think of it as the app's first-run seed data.
  - The live roster (once a visitor starts using the app) and every
    attendance record live in the browser's own localStorage, editable
    entirely from the app UI. Nothing entered in the app is ever sent
    anywhere or committed to this repo.

IMPORTANT -- this file IS committed to a public GitHub repo. Do not
put real students' names here. The names below are placeholders so
the app has something to demonstrate on first load; use the app's own
"Add Student" feature (which saves privately to your browser) for any
real roster.
"""

CLASSES = [
    {"id": "youth", "name": "Youth Class", "description": "Ages 7-12 · White through Green belt"},
    {"id": "teen-adult", "name": "Teen & Adult Class", "description": "Ages 13+ · all belt levels"},
]

STUDENTS = [
    {"id": "st-01", "name": "Alex P. (example)", "class_id": "youth", "belt": "Yellow"},
    {"id": "st-02", "name": "Jordan K. (example)", "class_id": "youth", "belt": "Green"},
    {"id": "st-03", "name": "Sam R. (example)", "class_id": "youth", "belt": "White"},
    {"id": "st-04", "name": "Morgan L. (example)", "class_id": "teen-adult", "belt": "Blue"},
    {"id": "st-05", "name": "Casey T. (example)", "class_id": "teen-adult", "belt": "Red"},
]
