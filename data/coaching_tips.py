"""
Content for the Adaptive Coaching Tips page.

This is guidance for instructors and parents adapting Taekwondo
training for children with special needs -- not medical or
therapeutic advice. Tips are drawn from adapted physical education
practice (organizations like NCHPAD and Autism Speaks) and from
peer-reviewed, open-access research (see SOURCES). Every source in
SOURCES was individually verified -- URL fetched, title/authors/venue
confirmed -- rather than recalled from memory; if a claim couldn't be
verified, it was left out rather than guessed at.

Same philosophy as content.py / flashcards.py / quiz.py: plain Python
data, no HTML/JS edits needed to add a tip or source. build.py exports
this to static/data/coaching-tips.json (and embeds it inline in the
page) for the client-side app.

`applies_to` is a list of category ids from SPECIAL_NEEDS_CATEGORIES --
most tips apply to more than one group, and cross-cutting tips include
"universal" alongside (or instead of) specific categories.
`source_id`, when set, must match an `id` in SOURCES, and should only
be set when a tip is directly grounded in that paper's findings (not
just loosely related).

A note on framing: language preferences differ by community -- autism
self-advocates often prefer identity-first language ("autistic child"),
while Down syndrome and broader intellectual-disability communities
more often prefer person-first ("child with Down syndrome"). Category
labels below stay neutral (naming the need, not the child) for that
reason; defer to how an individual family describes their own child.
The autism category icon is the infinity symbol (neurodiversity
movement's preferred symbol) rather than a puzzle piece, which many
autistic self-advocates reject.
"""

SPECIAL_NEEDS_CATEGORIES = [
    {"id": "autism", "label": "Autism Spectrum", "icon": "♾️", "color": "tip-autism"},
    {"id": "adhd", "label": "ADHD", "icon": "⚡", "color": "tip-adhd"},
    {"id": "sensory", "label": "Sensory Processing", "icon": "🎧", "color": "tip-sensory"},
    {"id": "down-syndrome", "label": "Down Syndrome / IDD", "icon": "🤝", "color": "tip-down-syndrome"},
    {"id": "physical", "label": "Physical & Motor Disabilities", "icon": "💪", "color": "tip-physical"},
    {"id": "anxiety", "label": "Anxiety & Emotional Regulation", "icon": "🌬️", "color": "tip-anxiety"},
    {"id": "universal", "label": "Universal Strategies", "icon": "🔑", "color": "tip-universal"},
]

TIPS = [
    # --- Universal / cross-cutting ---
    {
        "id": "tip-01", "applies_to": ["autism", "anxiety", "universal"],
        "title": "Use a visual class schedule",
        "tip": "Post or hand out a simple picture/word sequence of the class order (warm-up, drills, forms, break, sparring) so students know what's coming next.",
        "why": "Predictability reduces anxiety around transitions and helps students self-monitor where they are in class.",
        "source_id": None,
    },
    {
        "id": "tip-08", "applies_to": ["universal"],
        "title": "Use consistent command language",
        "tip": 'Pick one phrase per instruction (always "Joonbi" for ready, never swap in "get set") and stick with it class to class.',
        "why": "Consistent language lets students build reliable associations instead of relearning synonyms.",
        "source_id": None,
    },
    {
        "id": "tip-09", "applies_to": ["universal", "adhd", "down-syndrome"],
        "title": "Make positive reinforcement specific and immediate",
        "tip": 'Praise the exact thing done well ("great job keeping your guard up") right after it happens, not a generic "good job" later.',
        "why": "Specific, immediate feedback helps students connect the praise to the exact behavior to repeat.",
        "source_id": None,
    },
    {
        "id": "tip-12", "applies_to": ["autism", "down-syndrome", "universal"],
        "title": "Break a new technique into small pieces first",
        "tip": "Teach and celebrate each component of a technique on its own before chaining them into the full movement.",
        "why": "Small, masterable steps build confidence and reduce the chance of practicing a mistake repeatedly.",
        "source_id": None,
    },
    {
        "id": "tip-27", "applies_to": ["physical", "universal"],
        "title": "Start with an open conversation about goals",
        "tip": "Before adapting a curriculum, talk directly with the student and family about their goals, physical limitations, and what's worked (or not) elsewhere.",
        "why": "Adaptations built around what a specific student actually needs work better than generic modifications.",
        "source_id": None,
    },
    {
        "id": "tip-30", "applies_to": ["physical", "universal"],
        "title": "Favor engaging drills over isolated repetition",
        "tip": "Use partner drills and light games to practice balance and strength, rather than repetitive solo exercises alone.",
        "why": "Task-oriented, socially engaging drills sustain motivation and consistent participation better than isolated repetition.",
        "source_id": None,
    },
    {
        "id": "tip-36", "applies_to": ["universal"],
        "title": "Set goals collaboratively, and expect pacing to vary",
        "tip": "Build goals together with the student and family, and treat a slower or non-linear pace as normal, not a problem to fix.",
        "why": "Progress isn't uniform across students — patience with individual pacing keeps training sustainable and positive.",
        "source_id": None,
    },
    {
        "id": "tip-37", "applies_to": ["universal", "anxiety", "autism"],
        "title": "End every class with a calm-down segment",
        "tip": "Close class the same way each time: slow movement, stretching, and a breath or two, regardless of how the session went.",
        "why": "A structured 3-phase session (warm-up, skill work, calm-down) was used in a 2025 randomized controlled trial of martial-arts games for children with autism, which found gains in motor function and social communication.",
        "source_id": "fu-shi-2025-asd",
    },

    # --- Autism Spectrum ---
    {
        "id": "tip-02", "applies_to": ["autism", "sensory", "universal"],
        "title": "Give a heads-up before loud moments",
        "tip": 'Before group Kihaps (shouts) or board breaking, give a short verbal or visual warning ("loud sound in 3, 2, 1").',
        "why": "Sudden loud noises can be genuinely overwhelming or painful for students with sound sensitivity.",
        "source_id": None,
    },
    {
        "id": "tip-10", "applies_to": ["autism", "sensory"],
        "title": "Reduce background stimuli where you can",
        "tip": "Dim harsh lighting if possible, reduce echo/crowd noise near the training area, and keep clear physical boundaries around the workspace.",
        "why": "A calmer sensory environment lowers the odds of overload during a session.",
        "source_id": None,
    },
    {
        "id": "tip-11", "applies_to": ["autism"],
        "title": "Let students arrive a few minutes early",
        "tip": "Where possible, let a student come in a little before the group starts so they can settle into the space before it gets busy.",
        "why": "A few unhurried minutes to acclimate can prevent a rough transition into a full class.",
        "source_id": None,
    },
    {
        "id": "tip-13", "applies_to": ["autism"],
        "title": "Use short imitation games to build focus",
        "tip": "Demonstrate a simple 2-3 move sequence and have the student copy it, gradually increasing the sequence length as they succeed.",
        "why": "A 2025 randomized controlled trial found structured martial-arts imitation games improved motor function and social communication in children with autism over 24 weeks.",
        "source_id": "fu-shi-2025-asd",
    },
    {
        "id": "tip-19", "applies_to": ["autism", "sensory"],
        "title": "Offer a sensory menu before or during class",
        "tip": "Have a short list of regulating options ready — deep pressure, jumping, carrying/pushing a heavy bag — that a student can choose from when they need it.",
        "why": "Proprioceptive input (deep pressure, resistance work) is commonly used to support self-regulation for sensory processing differences.",
        "source_id": None,
    },

    # --- ADHD ---
    {
        "id": "tip-03", "applies_to": ["adhd", "universal"],
        "title": "Keep instructions short and sequenced",
        "tip": 'Break a technique into 2-3 word cues ("chamber, extend, snap") instead of one long explanation.',
        "why": "Short, sequenced cues are easier to hold in working memory and act on immediately.",
        "source_id": None,
    },
    {
        "id": "tip-04", "applies_to": ["adhd", "sensory"],
        "title": "Build in movement breaks",
        "tip": "Alternate structured drills with short bursts of free movement (jumping jacks, stretching) every 8-10 minutes.",
        "why": "Regular movement outlets can help students reset attention and reduce restlessness.",
        "source_id": None,
    },
    {
        "id": "tip-15", "applies_to": ["adhd"],
        "title": "Favor one-technique, one-partner drills",
        "tip": "Lean on Taekwondo's natural structure — one technique, one partner, one focus at a time — rather than fast-moving group games with divided attention.",
        "why": "A narrower, more intense attentional demand can suit ADHD better than sports requiring split attention across a field.",
        "source_id": None,
    },
    {
        "id": "tip-16", "applies_to": ["adhd", "universal"],
        "title": "Break belt goals into small, frequent wins",
        "tip": "Track visible mini-goals between belt tests — a stripe, a checklist, a small milestone — not just the next big test.",
        "why": "Frequent, visible progress markers keep motivation up over the months between belt promotions.",
        "source_id": None,
    },
    {
        "id": "tip-17", "applies_to": ["adhd", "anxiety"],
        "title": "Build a breathing moment into bow-in",
        "tip": "Add a brief, consistent breathing or focus moment to the start of class, and reuse it right before sparring.",
        "why": "Practicing a regulation routine in low-stakes moments makes it easier to use it under real pressure.",
        "source_id": None,
    },
    {
        "id": "tip-18", "applies_to": ["adhd"],
        "title": "Aim for steady, regular sessions",
        "tip": "Encourage roughly twice-weekly attendance over occasional intense sessions.",
        "why": "A 2021 meta-analysis of 21 studies (664 children with ADHD) found the clearest gains in inhibitory control and cognitive flexibility came from sustained, moderate-intensity exercise programs, not one-off sessions.",
        "source_id": "liang-2021-adhd",
    },

    # --- Sensory Processing ---
    {
        "id": "tip-20", "applies_to": ["sensory", "autism"],
        "title": "Allow noise-reduction accommodations",
        "tip": "Let students sensitive to shouted counts or pad-strike noise wear earplugs or earmuffs during class.",
        "why": "Removing one source of sensory overload can make the rest of class much more accessible.",
        "source_id": None,
    },
    {
        "id": "tip-21", "applies_to": ["sensory"],
        "title": "Favor dynamic, reactive pad drills",
        "tip": "Have students track and strike a moving target (focus mitts, a partner's pad) rather than only drilling the same strike in place.",
        "why": "A 2024 study of children with sensory integration challenges found structured sport training engaging multiple senses together (vestibular, tactile, proprioceptive) outperformed static therapy alone — not a Taekwondo study, but directly analogous to reactive pad work.",
        "source_id": "ge-2024-basketball-sensory",
    },
    {
        "id": "tip-07", "applies_to": ["anxiety", "autism", "sensory", "universal"],
        "title": "Offer a quiet corner or break option",
        "tip": "Designate a low-stimulation spot in or near the dojang a student can step to when overwhelmed, with a simple signal (a card, a hand sign) to request it.",
        "why": "Having an agreed-upon way to self-regulate reduces the odds of a small stressor escalating.",
        "source_id": None,
    },

    # --- Down Syndrome / IDD ---
    {
        "id": "tip-22", "applies_to": ["down-syndrome", "universal"],
        "title": "Teach true beginner steps, regardless of age",
        "tip": "Start from the same small, foundational steps you'd use for any beginner, rather than assuming prior exposure or skipping ahead to match age-based peer expectations.",
        "why": "Research on physical education for people with Down syndrome recommends building skills from true fundamentals rather than assuming age-typical starting points.",
        "source_id": "jobling-1994-down-syndrome",
    },
    {
        "id": "tip-23", "applies_to": ["down-syndrome", "physical"],
        "title": "Support the movement so it's right from the start",
        "tip": "Offer enough physical or verbal guidance (hand-over-hand if welcomed) that the student practices the correct pattern, rather than repeating an incorrect one.",
        "why": "Incorrect movement patterns can be hard to \"unlearn\" once practiced — getting it right early matters more than independence in the first attempts.",
        "source_id": "jobling-1994-down-syndrome",
    },
    {
        "id": "tip-24", "applies_to": ["down-syndrome"],
        "title": "Explain the \"why,\" not just the repetition",
        "tip": "Pair physical practice with a simple explanation of why a stance or block works the way it does.",
        "why": "Combining the cognitive explanation with the physical demonstration supports learning better than repetition alone.",
        "source_id": "jobling-1994-down-syndrome",
    },
    {
        "id": "tip-25", "applies_to": ["down-syndrome", "universal"],
        "title": "Praise improvement against their own last attempt",
        "tip": "Frame feedback around a student's own progress (\"that kick was higher than last week\") rather than comparisons to classmates.",
        "why": "A mastery-focused climate — praising improvement, not comparison — supports confidence and continued participation.",
        "source_id": "jobling-1994-down-syndrome",
    },
    {
        "id": "tip-26", "applies_to": ["down-syndrome"],
        "title": "Prioritize pad work and target-striking drills",
        "tip": "Weight class time toward drills that combine aiming and coordination — striking pads, targeting drills — over pure repetition.",
        "why": "A 2022 study found regularly active adults with Down syndrome had significantly better motor coordination and aiming/catching skills than sedentary peers — the sample was adults, not children, so treat this as suggestive rather than child-specific proof.",
        "source_id": "alesi-2022-down-syndrome",
    },

    # --- Physical & Motor Disabilities ---
    {
        "id": "tip-06", "applies_to": ["down-syndrome", "physical"],
        "title": "Modify the stance or range of motion",
        "tip": "Let students perform kicks/blocks at a comfortable height or from a seated/supported position rather than requiring the standard form.",
        "why": "Adapting the technique — not skipping it — keeps the student practicing the same skill within their physical range.",
        "source_id": None,
    },
    {
        "id": "tip-05", "applies_to": ["down-syndrome", "physical", "universal"],
        "title": "Demonstrate, don't just describe",
        "tip": "Pair every verbal instruction with a physical demonstration, and offer hand-over-hand guidance if welcomed by the student.",
        "why": "Modeling a movement is often more accessible than verbal-only instruction, especially for motor planning differences.",
        "source_id": None,
    },
    {
        "id": "tip-28", "applies_to": ["physical"],
        "title": "Combine pad work with balance-focused kicking",
        "tip": "Pair striking/blocking pad drills with kicking drills that emphasize balance and stability, in the same session.",
        "why": "A 12-week randomized controlled trial of adapted Taekwondo for children with developmental coordination disorder used exactly this combination and found significant, lasting gains in eye-hand coordination.",
        "source_id": "ma-2018-dcd",
    },
    {
        "id": "tip-29", "applies_to": ["physical"],
        "title": "Reinforce class with a few simple drills at home",
        "tip": "Send home 1-2 short, safe drills a student can practice a few minutes at a time between classes.",
        "why": "In the same developmental coordination disorder study, weekly class plus simple daily home practice produced better results than class time alone.",
        "source_id": "ma-2018-dcd",
    },

    # --- Anxiety & Emotional Regulation ---
    {
        "id": "tip-31", "applies_to": ["anxiety", "adhd"],
        "title": "Teach a simple stop-breathe-look-go routine",
        "tip": "Practice a short reset sequence in calm moments so it's already familiar when a student needs it under pressure, like right before sparring.",
        "why": "Rehearsing a regulation routine in low-stakes settings makes it far more likely to actually get used in a stressful one.",
        "source_id": None,
    },
    {
        "id": "tip-32", "applies_to": ["anxiety"],
        "title": "Use brief, private check-ins",
        "tip": "Correct or check in with a student quietly, one-on-one, rather than calling out corrections in front of the group.",
        "why": "Public correction can trigger performance anxiety that has nothing to do with whether the student understood the technique.",
        "source_id": None,
    },
    {
        "id": "tip-33", "applies_to": ["anxiety", "universal"],
        "title": "Model calm regulation yourself",
        "tip": "Keep your own tone and body language steady, especially in chaotic moments (a missed break, a messy sparring match).",
        "why": "Kids pick up on and mirror an instructor's visible stress response.",
        "source_id": None,
    },
    {
        "id": "tip-34", "applies_to": ["anxiety", "universal"],
        "title": "Separate effort from outcome in feedback",
        "tip": '"You worked hard on that block" lands very differently than "you lost" — say the first one.',
        "why": "Tying feedback to effort protects a student's sense of worth from being tied to winning or losing.",
        "source_id": None,
    },
    {
        "id": "tip-35", "applies_to": ["anxiety"],
        "title": "Build a reset routine after a mistake",
        "tip": "Teach a small physical reset — step back, one breath, re-set stance — as the standard response to a missed technique, instead of dwelling on it.",
        "why": "A quick, practiced reset keeps one mistake from spiraling into a rough rest of class.",
        "source_id": None,
    },
]

# Citations for research referenced on the page. Every entry here was
# individually verified (URL fetched, citation details confirmed) --
# never fabricated. `note` flags an honest caveat (e.g. sample age,
# study stage) rather than overstating what a paper actually showed.
SOURCES = [
    {
        "id": "ma-2018-dcd",
        "title": "Adapted Taekwondo Training for Prepubertal Children with Developmental Coordination Disorder: A Randomized, Controlled Trial",
        "authors": "Ma AWW, Fong SSM, Guo X, Liu KPY, Fong DYT, Bae YH, Yuen L, Cheng YTY, Tsang WWN",
        "venue": "Scientific Reports",
        "year": 2018,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6037761/",
        "note": None,
    },
    {
        "id": "fu-shi-2025-asd",
        "title": "The intervention effect of structured martial arts games on behavioral impairments and motor functions in children with autism spectrum disorder",
        "authors": "Fu X, Shi P",
        "venue": "Frontiers in Psychology",
        "year": 2025,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12510954/",
        "note": None,
    },
    {
        "id": "liang-2021-adhd",
        "title": "The impact of exercise interventions concerning executive functions of children and adolescents with attention-deficit/hyperactivity disorder: a systematic review and meta-analysis",
        "authors": "Liang X, Li R, Wong SHS, Sum RKW, Sit CHP",
        "venue": "International Journal of Behavioral Nutrition and Physical Activity",
        "year": 2021,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8141166/",
        "note": None,
    },
    {
        "id": "alesi-2022-down-syndrome",
        "title": "Motor Coordination and Global Development in Subjects with Down Syndrome: The Influence of Physical Activity",
        "authors": "Alesi M, Giustino V, Gentile A, Gómez-López M, Battaglia G",
        "venue": "Journal of Clinical Medicine",
        "year": 2022,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9457525/",
        "note": "Studied adults with Down syndrome (mean age ~27), not children — included for its motor-coordination findings, which are suggestive but weren't tested in kids specifically.",
    },
    {
        "id": "ge-2024-basketball-sensory",
        "title": "Improving sensory integration in Chinese children with moderate sensory integration challenges through engaging basketball training",
        "authors": "Ge S, Guo X, Jiang BY, Cordova A, Guan J, Zhang JQ, Yao WX",
        "venue": "Frontiers in Psychology",
        "year": 2024,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11775159/",
        "note": "A basketball-training study, not Taekwondo — included because its sensory-integration rationale applies directly to structured martial arts drilling.",
    },
    {
        "id": "jobling-1994-down-syndrome",
        "title": "Physical education for the person with Down syndrome: more than playing games?",
        "authors": "Jobling A",
        "venue": "Down Syndrome Research and Practice",
        "year": 1994,
        "url": "https://www.down-syndrome.org/en-us/library/research-practice/02/1/physical-education-person-down-syndrome-more-playing-games/",
        "note": None,
    },
    {
        "id": "yu-2025-music-tkd-asd",
        "title": "Protocol for evaluating the effects of integrating music with taekwondo training in children with autism spectrum disorder: A randomized controlled trial",
        "authors": "Yu CCW, Mok KM, Mak E, Au CT, Chan DFY, Wu S, Chung RCK, Ip MCK, Wong SWL",
        "venue": "PLOS ONE",
        "year": 2025,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11785272/",
        "note": "A published study protocol, not results — included to show Taekwondo-specific autism research is an active, credible field. No tip above is based on its findings, since none are published yet.",
    },
]
