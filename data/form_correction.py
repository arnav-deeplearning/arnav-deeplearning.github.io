"""
Content for the Form Correction AI app.

This app is architecturally different from every other app on the
site: it uses a real computer-vision pose-estimation model (MediaPipe
Pose Landmarker, Google's open-source library) running entirely in
the visitor's browser via their webcam. No video or image data is
ever uploaded anywhere -- everything happens client-side.

Angle thresholds below are general coaching guidelines synthesized
from public Taekwondo instructional sources (school stance guides,
Taekwondo reference wikis), NOT a clinical biomechanics standard --
different schools and instructors teach slightly different numbers.
Treat them as a reasonable target range for a computer-vision check,
not an exact rule.

Each stance's `checks` list is evaluated by static/js/form-correction.js
against MediaPipe's 3D world-landmark joint angles. `kind` selects
which check function runs (see form-correction.js CHECK_HANDLERS):

  - min_knee_bend: the MORE-bent of the two knees must fall in [min, max]
  - max_knee_straight: the STRAIGHTER of the two knees must fall in [min, max]
  - both_knees_range: BOTH knees must independently fall in [min, max]
  - knee_symmetry_close: |left knee angle - right knee angle| <= max
  - knee_symmetry_apart: |left knee angle - right knee angle| >= min
  - ankle_shoulder_ratio: (ankle-to-ankle distance / shoulder-to-shoulder
    distance) must fall in [min, max] -- a camera-distance-independent
    proxy for stance width/length
  - guard_up: at least one wrist must be raised above the torso midline

Knee angles are measured at the knee joint (hip-knee-ankle), where
180 degrees is a fully straight leg and smaller values mean more bend.
"""

STANCES = [
    {
        "id": "front-stance",
        "name": "Front Stance",
        "korean": "Ap Seogi (Ap Kubi)",
        "description": "A long stance with one knee bent sharply forward and the other leg straight behind you -- the most common stance in early poomsae.",
        "checks": [
            {
                "id": "bent-leg", "label": "Front leg bent", "kind": "min_knee_bend",
                "min": 80, "max": 120,
                "feedback_ok": "Good bend in your front leg.",
                "feedback_bad": "Bend your front knee more -- aim for roughly a right angle, with your knee tracking over your ankle.",
            },
            {
                "id": "straight-leg", "label": "Back leg straight", "kind": "max_knee_straight",
                "min": 155, "max": 185,
                "feedback_ok": "Back leg nicely straight.",
                "feedback_bad": "Straighten your back leg fully -- it should be locked, not bent.",
            },
            {
                "id": "stance-length", "label": "Stance length", "kind": "ankle_shoulder_ratio",
                "min": 1.3, "max": 2.6,
                "feedback_ok": "Good stance length.",
                "feedback_low": "Step out further -- front stance should be long, roughly 1.5-2x your shoulder width.",
                "feedback_high": "Your stance looks a bit long -- bring your feet slightly closer together.",
            },
        ],
    },
    {
        "id": "horse-stance",
        "name": "Horse Stance",
        "korean": "Juchum Seogi",
        "description": "A wide, symmetrical stance with both knees bent evenly -- builds leg strength and stance stability.",
        "checks": [
            {
                "id": "both-bent", "label": "Both knees bent", "kind": "both_knees_range",
                "min": 80, "max": 130,
                "feedback_ok": "Both knees are well bent.",
                "feedback_bad": "Bend both knees more deeply, keeping your shins close to vertical.",
            },
            {
                "id": "knees-even", "label": "Knees evenly bent", "kind": "knee_symmetry_close",
                "min": 0, "max": 25,
                "feedback_ok": "Your weight looks evenly centered.",
                "feedback_bad": "Even out your weight between both legs -- one knee is bent noticeably more than the other.",
            },
            {
                "id": "stance-width", "label": "Stance width", "kind": "ankle_shoulder_ratio",
                "min": 1.4, "max": 2.8,
                "feedback_ok": "Good wide stance.",
                "feedback_low": "Widen your stance -- horse stance is wider than shoulder width, closer to 1.5-2x.",
                "feedback_high": "Your stance looks very wide -- bring your feet in slightly for better control.",
            },
        ],
    },
    {
        "id": "back-stance",
        "name": "Back Stance",
        "korean": "Dwit Seogi (Dwi Kubi)",
        "description": "A shorter defensive stance with most of the weight on the back leg -- both knees stay bent, unlike front stance.",
        "checks": [
            {
                "id": "both-bent", "label": "Both legs bent", "kind": "both_knees_range",
                "min": 80, "max": 150,
                "feedback_ok": "Both legs have some bend, as they should.",
                "feedback_bad": "Keep both knees bent in back stance -- neither leg should be fully straight.",
            },
            {
                "id": "weight-shift", "label": "Weight shifted back", "kind": "knee_symmetry_apart",
                "min": 15, "max": 999,
                "feedback_ok": "Good weight shift toward your back leg.",
                "feedback_bad": "Shift more weight onto your back leg -- it should be bent more than your front leg.",
            },
            {
                "id": "stance-length", "label": "Stance length", "kind": "ankle_shoulder_ratio",
                "min": 1.0, "max": 1.8,
                "feedback_ok": "Good stance length.",
                "feedback_low": "Widen your stance slightly -- back stance is a bit longer than a natural standing position.",
                "feedback_high": "Your stance looks too long for back stance -- bring your feet a bit closer.",
            },
        ],
    },
    {
        "id": "fighting-stance",
        "name": "Fighting / Ready Stance",
        "korean": "Kyorugi Joonbi",
        "description": "A light, mobile sparring stance -- knees only softly bent, hands up guarding the head and chest.",
        "checks": [
            {
                "id": "soft-knees", "label": "Knees softly bent", "kind": "both_knees_range",
                "min": 140, "max": 178,
                "feedback_ok": "Good athletic knee bend.",
                "feedback_bad": "Adjust your knee bend -- fighting stance is a light, springy bend, not deeply bent like horse stance.",
            },
            {
                "id": "guard-up", "label": "Hands up guarding", "kind": "guard_up",
                "feedback_ok": "Guard is up -- good.",
                "feedback_bad": "Raise your hands to guard your head and chest.",
            },
            {
                "id": "stance-width", "label": "Stance width", "kind": "ankle_shoulder_ratio",
                "min": 1.0, "max": 2.0,
                "feedback_ok": "Good, mobile stance width.",
                "feedback_low": "Widen your stance slightly for better balance and mobility.",
                "feedback_high": "Your stance looks wide for sparring -- narrow it slightly for quicker footwork.",
            },
        ],
    },
]
