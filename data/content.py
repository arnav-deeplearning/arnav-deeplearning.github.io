"""
Central content store for the site.

Everything the templates render lives here as plain Python data
structures. To add a new page section, a new app card, or a new
journey milestone, edit this file only — templates and build.py
never need to change for routine content updates.
"""

SITE = {
    "name": "Arnav Saravanakumar",
    "short_name": "Arnav",
    "title": "Arnav | Taekwondo x AI",
    "tagline": "3rd Dan Black Belt. Builder of AI-powered Taekwondo tools.",
    "mission": (
        "I'm on a mission to combine everything Taekwondo has taught me "
        "with everything I'm learning about AI and software — starting "
        "with simple training tools for students of every belt level, "
        "and building toward adaptive apps designed specifically for "
        "special needs children in the TKD community."
    ),
}

NAV = [
    {"label": "Home", "href": "index.html"},
    {"label": "Bio", "href": "bio.html"},
    {"label": "My Journey", "href": "journey.html"},
    {"label": "Apps & Resources", "href": "resources.html"},
]

# High-level facts used across the bio / journey pages.
PROFILE = {
    "rank": "3rd Dan WT Certified Black Belt",
    "rank_date": "June 6, 2026",
    "school": "Ji Ho Choi Taekwondo Institute",
    "instructor": "Grand Master Ji Ho Choi",
    "started": "early childhood",
}

BIO_PARAGRAPHS = [
    "I've been training in Taekwondo since I was a young child, and it's "
    "been one of the biggest constants in my life ever since. What started "
    "as a kids' class turned into a genuine passion for the discipline, "
    "the community, and the philosophy behind the art.",

    "In June 2026, I earned my 3rd Dan WT Certified Black Belt from the "
    "Ji Ho Choi Taekwondo Institute, presented by Grand Master Ji Ho Choi. "
    "Every stripe and belt along the way taught me something new about "
    "focus, patience, and pushing past what I thought I could do.",

    "Outside of the dojang, I'm equally passionate about AI and software "
    "engineering. This site is where those two worlds meet: a place to "
    "document my Taekwondo journey and to build real, useful applications "
    "for the TKD community — starting with study tools for students, and "
    "growing toward adaptive, accessible apps for special needs children "
    "who deserve training tools built with them in mind from day one.",
]

# Timeline milestones — add new entries as your journey continues.
# `belt` is used to color-code the timeline marker.
JOURNEY = [
    {
        "period": "Early childhood",
        "title": "First steps on the mat",
        "belt": "white",
        "description": (
            "Started Taekwondo as a young child — first class, first "
            "bow, first taste of a sport that would stick for life."
        ),
    },
    {
        "period": "September 22, 2018",
        "title": "Blue Belt — 4th Gup",
        "belt": "blue",
        "description": (
            "Promoted to Blue Belt, 4th Gup, certified by the Ji Ho Choi "
            "Taekwondo Institute Black Belt Center."
        ),
    },
    {
        "period": "2022",
        "title": "Advancing through the color belts",
        "belt": "green",
        "description": (
            "Continued testing through the Green and Yellow Gup ranks at "
            "the Black Belt Center, building toward black belt eligibility."
        ),
    },
    {
        "period": "2023",
        "title": "Black Belt achieved",
        "belt": "black",
        "description": (
            "Earned 1st Dan Black Belt at the Ji Ho Choi Taekwondo "
            "Institute, capped off by testing up through Blue, 2nd Gup "
            "that April."
        ),
    },
    {
        "period": "July 7, 2023",
        "title": "Special Needs Mentor Training",
        "belt": "black",
        "description": (
            "Completed a 3.0-hour Level I training program for mentors "
            "and instructors of children with special needs, through the "
            "Spectrum Taekwondo Instructor Education and Development "
            "program."
        ),
    },
    {
        "period": "August 9, 2023",
        "title": "Certificate of Recognition — Spectrum Taekwondo",
        "belt": "black",
        "description": (
            "Recognized by Spectrum Taekwondo and the Jiho Choi TKD "
            "Institute for 10 volunteer hours as a mentor during the PEC "
            "(Parents with Exceptional Needs Children) summer program, "
            "demonstrating the Five Tenets of Taekwondo throughout."
        ),
    },
    {
        "period": "February 14, 2026",
        "title": "2nd Dan — Kukkiwon Certified",
        "belt": "black",
        "description": (
            "Officially Kukkiwon-certified 2nd Dan Black Belt (Certificate "
            "No. 09878182). Kukkiwon certificates are typically issued "
            "roughly a year after testing, so this documents a promotion "
            "earned earlier."
        ),
    },
    {
        "period": "June 6, 2026",
        "title": "3rd Dan Black Belt",
        "belt": "black",
        "description": (
            "Certified 3rd Dan WT Black Belt by Grand Master Ji Ho Choi "
            "at the Ji Ho Choi Taekwondo Institute."
        ),
    },
    {
        "period": "Now",
        "title": "Building for the community",
        "belt": "black",
        "description": (
            "Combining TKD experience with AI and coding skills to build "
            "training apps for the community — with a focus on making "
            "them accessible to special needs children."
        ),
    },
]

# Placeholder gallery slots. Drop real photos into
# static/images/gallery/ and update `src` to match the filename.
GALLERY = [
    {"caption": "Training session", "src": None},
    {"caption": "Belt test day", "src": None},
    {"caption": "Tournament / sparring", "src": None},
    {"caption": "Board breaking", "src": None},
    {"caption": "With instructors", "src": None},
    {"caption": "3rd Dan certification", "src": None},
]

# Belt levels — the actual 14-rank ladder used by the Ji Ho Choi Taekwondo
# Institute (per the school's own "Kukkiwon Taekwondo Ranking" and belt
# study guide handouts), not a generic 6-color curriculum. Junior/Medium/
# Senior sub-ranks are the same color belt with 1-3 gold stripes.
# `color` maps to a CSS custom property defined in static/css/style.css.
# Also used by the future quiz app's leveling system.
BELT_LEVELS = [
    {"name": "White", "color": "white-belt"},
    {"name": "Sr. White", "color": "white-belt"},
    {"name": "Yellow", "color": "yellow-belt"},
    {"name": "Sr. Yellow", "color": "yellow-belt"},
    {"name": "Green", "color": "green-belt"},
    {"name": "Sr. Green", "color": "green-belt"},
    {"name": "Blue", "color": "blue-belt"},
    {"name": "Jr. Blue", "color": "blue-belt"},
    {"name": "Sr. Blue", "color": "blue-belt"},
    {"name": "Red", "color": "red-belt"},
    {"name": "Jr. Red", "color": "red-belt"},
    {"name": "Med. Red", "color": "red-belt"},
    {"name": "Sr. Red", "color": "red-belt"},
    {"name": "Black (Dan)", "color": "black-belt"},
]

# Status values: "planned", "in-development", "coming-soon", "live"
APPS = [
    {
        "title": "TKD Flashcards",
        "icon": "🥋",
        "status": "live",
        "href": "flashcards.html",
        "description": (
            "Learn Korean terminology, poomsae names, and belt-level "
            "vocabulary through quick, swipeable flashcards."
        ),
        "tags": ["Beginner-friendly", "Terminology"],
    },
    {
        "title": "TKD Quiz — Belt Levels",
        "icon": "🎯",
        "status": "live",
        "href": "quiz.html",
        "description": (
            "Test your knowledge with quizzes leveled by belt rank, from "
            "white belt basics up to black belt theory."
        ),
        "tags": ["Leveled by belt", "Practice mode"],
    },
    {
        "title": "Adaptive Coaching Tips",
        "icon": "💡",
        "status": "live",
        "href": "coaching-tips.html",
        "description": (
            "Bite-sized, sensory-friendly tips and drills to help "
            "instructors and parents adapt training for special needs "
            "children."
        ),
        "tags": ["Special needs focus", "For instructors & parents"],
    },
    {
        "title": "Sparring Strategy Trainer",
        "icon": "🥊",
        "status": "live",
        "href": "sparring.html",
        "description": (
            "Scenario-based drills that help students think through "
            "sparring strategy, not just memorize combinations."
        ),
        "tags": ["Intermediate+"],
    },
    {
        "title": "Form Correction AI",
        "icon": "🤖",
        "status": "live",
        "href": "form-correction.html",
        "description": (
            "Computer-vision powered feedback on poomsae and stances, "
            "designed with accessibility for special needs students "
            "as a core requirement, not an afterthought."
        ),
        "tags": ["Special needs focus", "Computer vision"],
    },
    {
        "title": "Attendance Tracker",
        "icon": "📋",
        "status": "live",
        "href": "attendance.html",
        "description": (
            "Track class attendance and streaks over time, so instructors "
            "can spot patterns and students can see their own consistency "
            "add up."
        ),
        "tags": ["For instructors", "Progress tracking"],
    },
]

STATUS_LABELS = {
    "live": "Live",
    "coming-soon": "Coming Soon",
    "in-development": "In Development",
    "planned": "Planned",
}
