"""
Content for the Sparring Strategy Trainer app.

Unlike flashcards.py or quiz.py, this isn't about memorizing terms or
facts -- it's about tactical decision-making in Olympic-style (World
Taekwondo) sparring. Each scenario sets up a realistic in-match
situation and asks what the strategically sound choice is. Reasoning
draws on real coaching sources and, where noted, on peer-reviewed
notational-analysis research of elite competition (see SOURCES) --
every source was individually verified (URL fetched, citation details
confirmed) before being cited, never fabricated.

Same philosophy as content.py / flashcards.py / quiz.py: plain Python
data, no HTML/JS edits needed to add a scenario. build.py exports this
to static/data/sparring.json (and embeds it inline in the page) for
the client-side app.

`level` values must match an entry in SPARRING_LEVELS.
`category` values must match an `id` in SCENARIO_CATEGORIES.
`source_id`, when set, must match an `id` in SOURCES, and is only set
when a scenario's reasoning is directly grounded in that source.

Scoring values reflect the official 2026 USA Taekwondo Kyorugi
Competition Rules (which implement World Taekwondo rules, effective
Jan 1, 2026) -- note the turning/spinning kick to the head scores 6
points under this cycle, up from 5 in earlier rule sets some older
articles still cite.
"""

SPARRING_LEVELS = ["Intermediate", "Advanced", "Competition"]

SCENARIO_CATEGORIES = [
    {"id": "distance", "label": "Distance & Footwork"},
    {"id": "counter", "label": "Counter-Fighting"},
    {"id": "feinting", "label": "Feinting & Baiting"},
    {"id": "combinations", "label": "Combinations & Timing"},
    {"id": "game-management", "label": "Scoreboard & Game Management"},
    {"id": "reading-opponents", "label": "Reading Opponents"},
]

SCENARIOS = [
    # --- Distance & Footwork ---
    {
        "id": "sc-dist-01", "category": "distance", "level": "Intermediate",
        "situation": "You're sparring an opponent with noticeably longer legs. Every time you close in straight on, their kicks land first.",
        "prompt": "What's your best strategic adjustment?",
        "choices": [
            "Keep charging straight in and try to out-muscle them",
            "Use angled footwork to close distance off-line instead of straight on",
            "Stay at long range and try to out-kick them at their own distance",
            "Stop attacking and wait for the round to end",
        ],
        "correct": 1,
        "explanation": "Closing at an angle avoids feeding directly into a longer-legged opponent's straight-line kicking range, letting you get inside their reach before they can fire cleanly.",
        "source_id": None,
    },
    {
        "id": "sc-dist-02", "category": "distance", "level": "Intermediate",
        "situation": "You control the center of the mat and your opponent keeps circling to reset distance before you can attack.",
        "prompt": "What should you do?",
        "choices": [
            "Chase them around the mat in the same direction they're circling",
            "Cut off their circling angle by stepping into their path instead of chasing",
            "Back up to give them more room",
            "Ignore footwork and just throw kicks from wherever you are",
        ],
        "correct": 1,
        "explanation": "Cutting the angle — stepping into where they're circling to, not where they currently are — closes distance efficiently instead of endlessly chasing.",
        "source_id": None,
    },
    {
        "id": "sc-dist-03", "category": "distance", "level": "Intermediate",
        "situation": "You're getting pushed toward the boundary line by an opponent who keeps advancing, and you keep retreating straight back.",
        "prompt": "What's the better footwork choice?",
        "choices": [
            "Keep retreating straight back until you reach the line",
            "Circle or step laterally instead of retreating in a straight line",
            "Stop moving entirely and plant your feet",
            "Turn around and run to the other side of the mat",
        ],
        "correct": 1,
        "explanation": "A straight retreat runs out of mat and keeps feeding the opponent's forward line; lateral or angled movement keeps you off the boundary while staying in a position to counter.",
        "source_id": None,
    },
    {
        "id": "sc-dist-04", "category": "distance", "level": "Advanced",
        "situation": "You're just barely out of kicking range of your opponent — not far, just a few inches short.",
        "prompt": "What's the most efficient way to close that small gap?",
        "choices": [
            "A full sliding step, covering much more distance than you need",
            "An incline attack — shifting your body weight forward without moving your feet",
            "A big jump forward",
            "Wait for them to close the gap instead",
        ],
        "correct": 1,
        "explanation": "For a small gap, shifting weight forward without a telegraphing foot-slide (an 'incline attack') closes just enough distance without announcing the attack early.",
        "source_id": None,
    },
    {
        "id": "sc-dist-05", "category": "distance", "level": "Advanced",
        "situation": "Your opponent is already inside your kicking range and squared up in front of you.",
        "prompt": "What should you do?",
        "choices": [
            "Reposition and reset your stance before attacking",
            "Fire immediately — you're already in range, no need to close more distance",
            "Step back to create more space first",
            "Wait for them to move first",
        ],
        "correct": 1,
        "explanation": "When you're already in range, repositioning just wastes the opening — an 'in-place attack' fired immediately capitalizes on distance you already have.",
        "source_id": None,
    },
    {
        "id": "sc-dist-06", "category": "distance", "level": "Competition",
        "situation": "Your opponent is retreating and you need to cover real ground quickly to catch them before the round clock runs out.",
        "prompt": "What kind of entry fits this situation?",
        "choices": [
            "A small weight shift with no footwork",
            "A sliding attack — sliding the front foot to cover real distance quickly",
            "Standing still and waiting",
            "A backward step",
        ],
        "correct": 1,
        "explanation": "Covering real distance quickly calls for a sliding attack; speed in the slide is what makes it work before the opponent resets again.",
        "source_id": None,
    },
    {
        "id": "sc-dist-07", "category": "distance", "level": "Competition",
        "situation": "Every time you retreat straight back, your opponent closes and counters you before you can reset.",
        "prompt": "What footwork adjustment addresses this?",
        "choices": [
            "Retreat straight back, just faster",
            "Pivot off-line to change your angle instead of retreating straight",
            "Stop retreating and stand your ground with no movement",
            "Retreat and then sprint away entirely",
        ],
        "correct": 1,
        "explanation": "Pivoting changes the angle you present, letting you evade or counter from a direction the opponent isn't set up to defend — straight retreat just lets them keep closing.",
        "source_id": None,
    },

    # --- Counter-Fighting ---
    {
        "id": "sc-counter-01", "category": "counter", "level": "Intermediate",
        "situation": "Your opponent throws the same lead-leg roundhouse kick every time they attack, fully committing their weight forward.",
        "prompt": "What's the strategically sound response?",
        "choices": [
            "Back away every time they attack",
            "Time a counter-kick as they commit, exploiting their forward momentum",
            "Match their kick with the identical technique",
            "Grab their leg and hold on",
        ],
        "correct": 1,
        "explanation": "A committed, repeated attack is predictable — timing a counter as they commit exploits the moment they can't easily change direction or defend.",
        "source_id": None,
    },
    {
        "id": "sc-counter-02", "category": "counter", "level": "Intermediate",
        "situation": "Your opponent throws a fast lead kick, then immediately resets to a strong defensive guard before you can respond.",
        "prompt": "What adjustment gives you a better counter opportunity?",
        "choices": [
            "Counter during their reset, when their guard is still forming",
            "Wait until they're fully reset and attack straight into their guard",
            "Only counter after they attack a second time",
            "Give up on countering and only initiate your own attacks",
        ],
        "correct": 0,
        "explanation": "The brief window while an opponent is still resetting — before their guard is fully reformed — is often the highest-percentage moment to counter.",
        "source_id": None,
    },
    {
        "id": "sc-counter-03", "category": "counter", "level": "Intermediate",
        "situation": "An aggressive opponent keeps closing distance and firing kicks on nearly every exchange.",
        "prompt": "What's a reliable counter option here?",
        "choices": [
            "A slide-back roundhouse — retreat slightly, then fire as their attacking leg begins to descend",
            "Full retreat every time with no counter attempt",
            "Match their pace and throw first every time",
            "Turn your back and cover up",
        ],
        "correct": 0,
        "explanation": "Retreating only slightly and firing as their kicking leg descends (their natural recovery moment) turns their own aggression into your scoring window.",
        "source_id": None,
    },
    {
        "id": "sc-counter-04", "category": "counter", "level": "Advanced",
        "situation": "Your opponent uses hit-and-run tactics — landing a strike, then fully retreating out of range every time.",
        "prompt": "How should you adjust your counters?",
        "choices": [
            "Chase them the full distance they retreat",
            "Retreat only about two-thirds of your normal distance, then answer with a double kick as they reset",
            "Stop attacking and only play defense",
            "Retreat further than they do to bait them in",
        ],
        "correct": 1,
        "explanation": "A full retreat surrenders the counter opportunity entirely — cutting your retreat short keeps you close enough to answer the instant they reset.",
        "source_id": None,
    },
    {
        "id": "sc-counter-05", "category": "counter", "level": "Advanced",
        "situation": "You notice your opponent's shoulder turns and their stance sinks slightly deeper right before every kick they throw.",
        "prompt": "What should you do with this information?",
        "choices": [
            "Ignore it — footwork is the only thing that matters",
            "Use these telegraphs to time your counter before they fully commit to the kick",
            "Copy their stance change yourself",
            "Point it out to the referee",
        ],
        "correct": 1,
        "explanation": "Subtle pre-movement tells — shoulder turns, weight shifts, a deeper stance — telegraph an attack before it launches, giving you a timing window to counter early.",
        "source_id": None,
    },
    {
        "id": "sc-counter-06", "category": "counter", "level": "Advanced",
        "situation": "You threw a direct attack and it was blocked. You're deciding what to do immediately after.",
        "prompt": "What's a strategically sound follow-up?",
        "choices": [
            "Reset completely and wait several seconds before doing anything else",
            "Follow up with a circular kick — countering right off a blocked direct attack is a real, common scoring pathway",
            "Repeat the exact same blocked technique immediately",
            "Retreat to the far side of the mat",
        ],
        "correct": 1,
        "explanation": "Analysis of elite Grand Prix finals found lower-scoring competitors' points often came from a circular-kick counter fired right after their own blocked or missed direct attack — a legitimate scoring pattern, not just a fallback.",
        "source_id": "gamero-castillero-2022",
    },
    {
        "id": "sc-counter-07", "category": "counter", "level": "Competition",
        "situation": "You're specifically trying to set up a high-value head-kick score against a live opponent.",
        "prompt": "What kind of setup gives you the best chance?",
        "choices": [
            "A completely static, unmoving stance with no setup",
            "A dodge or indirect entry, followed by a counterattack after the opponent commits",
            "Announcing the kick before throwing it",
            "Only ever attacking with the same kick repeatedly",
        ],
        "correct": 1,
        "explanation": "Analysis of Olympic medalists found 3-point head-kick scores were frequently preceded by dodges, indirect attacks, and counterattacks thrown after the opponent had already committed — not clean, unset entries.",
        "source_id": "menescardi-2019-medalists",
    },

    # --- Feinting & Baiting ---
    {
        "id": "sc-feint-01", "category": "feinting", "level": "Intermediate",
        "situation": "Your opponent reacts by flinching their guard up every time you fake a head-height kick.",
        "prompt": "How can you use this to your advantage?",
        "choices": [
            "Stop faking since it doesn't score points directly",
            "Fake high to draw the guard up, then attack the now-open body/trunk",
            "Always follow the fake with the exact same head kick",
            "Fake low instead since it isn't working",
        ],
        "correct": 1,
        "explanation": "A feint's value is creating an opening elsewhere — drawing the guard up with a high fake, then scoring on the body it just exposed, is a classic bait-and-attack sequence.",
        "source_id": None,
    },
    {
        "id": "sc-feint-02", "category": "feinting", "level": "Intermediate",
        "situation": "You've faked a kick twice and your opponent hasn't reacted to either one.",
        "prompt": "What does this tell you, and what should you do?",
        "choices": [
            "They're not reading your feints yet — try a third identical fake",
            "They may be reading your feints as fakes — vary the setup or commit for real next time",
            "Feinting doesn't work against this opponent, so switch to only defense",
            "Repeat the exact same feint a few more times to be sure",
        ],
        "correct": 1,
        "explanation": "An opponent who stops reacting has likely picked up on the pattern. Feints work best used sparingly and varied — repeating the same one trains the opponent to ignore it.",
        "source_id": None,
    },
    {
        "id": "sc-feint-03", "category": "feinting", "level": "Intermediate",
        "situation": "It's early in the first round against an opponent you've never sparred before.",
        "prompt": "What's a sound early-round approach?",
        "choices": [
            "Commit to your biggest, riskiest attack immediately",
            "Use feints to test how they react before committing to real attacks",
            "Stand completely still and do nothing until round two",
            "Copy whatever the opponent does",
        ],
        "correct": 1,
        "explanation": "Feints are especially useful early against an unfamiliar opponent — they reveal how that specific opponent reacts before you commit to a real attack.",
        "source_id": None,
    },
    {
        "id": "sc-feint-04", "category": "feinting", "level": "Advanced",
        "situation": "You want to fake a front kick specifically to set up a body attack.",
        "prompt": "What matters most for the fake to work?",
        "choices": [
            "It just needs to look vaguely like motion, technique doesn't matter",
            "It should specifically resemble a real front kick, to draw the front-kick-specific guard reaction",
            "It should look nothing like any real technique",
            "It should be thrown as slowly as possible",
        ],
        "correct": 1,
        "explanation": "Baiting is technique-specific — a convincing front-kick fake draws the front-kick-specific defensive reaction you're trying to exploit; a vague motion won't reliably trigger it.",
        "source_id": None,
    },
    {
        "id": "sc-feint-05", "category": "feinting", "level": "Advanced",
        "situation": "You fake an attack, then wait almost two full seconds before throwing your real technique.",
        "prompt": "What's the problem with this timing?",
        "choices": [
            "There's no problem, longer gaps are always safer",
            "The long gap gives the opponent time to recover and block the real attack — it should follow quickly",
            "The fake should have been even slower",
            "You should fake again before attacking",
        ],
        "correct": 1,
        "explanation": "A feint only sets up an opening briefly — too long a gap between the fake and the real attack lets the opponent recover their guard before it lands.",
        "source_id": None,
    },
    {
        "id": "sc-feint-06", "category": "feinting", "level": "Competition",
        "situation": "You're sparring a purely defensive, counter-only opponent who refuses to initiate any attacks of their own.",
        "prompt": "What's the best way to break through?",
        "choices": [
            "Wait them out — eventually they'll have to attack",
            "Use feints and footwork to actively draw them into reacting or committing",
            "Stand still to match their passivity",
            "Only throw single techniques with no setup",
        ],
        "correct": 1,
        "explanation": "A truly defensive opponent won't initiate on their own — feints and footwork are the tools that actively draw a reaction out of them instead of waiting for one that won't come.",
        "source_id": None,
    },

    # --- Combinations & Timing ---
    {
        "id": "sc-combo-01", "category": "combinations", "level": "Intermediate",
        "situation": "You keep landing your first kick in a combination, but your opponent recovers and blocks the follow-up every time.",
        "prompt": "What's the likely fix?",
        "choices": [
            "Throw the same two-kick combo faster with no change in rhythm",
            "Vary the timing or target of the second technique to break the predictable rhythm",
            "Only ever throw single techniques from now on",
            "Throw the combination in the exact reverse order",
        ],
        "correct": 1,
        "explanation": "If a follow-up is consistently blocked, the opponent has adapted to its timing — changing the rhythm or target of the second technique disrupts their read.",
        "source_id": None,
    },
    {
        "id": "sc-combo-02", "category": "combinations", "level": "Intermediate",
        "situation": "Your opponent is strong defensively but has a brief lag right after they finish blocking, before resetting their stance.",
        "prompt": "How should you attack?",
        "choices": [
            "Wait a few seconds after the block before attacking again",
            "Attack immediately into the gap right after their block, before their stance resets",
            "Only attack right as they're mid-block",
            "Stop attacking that side entirely",
        ],
        "correct": 1,
        "explanation": "Attacking into the recovery gap — the moment right after a block, before the stance resets — targets a real timing weakness instead of a fully-set defense.",
        "source_id": None,
    },
    {
        "id": "sc-combo-03", "category": "combinations", "level": "Advanced",
        "situation": "You're choosing between a single clean kick and a two-kick combination, and you assume the combination must be the faster option since it's more techniques.",
        "prompt": "Is that assumption correct?",
        "choices": [
            "Yes — combinations are always faster to throw than a single kick",
            "No — research measured combinations as slower to plan and execute than a single kick; their value is in changing what the opponent must defend, not raw speed",
            "Speed is identical either way",
            "Only true for advanced athletes, not intermediate ones",
        ],
        "correct": 1,
        "explanation": "A 2025 study of elite athletes found multi-kick sequences significantly increased both reaction time and movement time compared to a single kick — combinations work by presenting multiple problems to defend, not because they're quicker.",
        "source_id": "chen-2025-sequential-kicks",
    },
    {
        "id": "sc-combo-04", "category": "combinations", "level": "Advanced",
        "situation": "Your opponent has settled into a steady rhythm and is timing their blocks accurately against your attacks.",
        "prompt": "What can you do to get through?",
        "choices": [
            "Keep the exact same rhythm and hope for a mistake",
            "Deliberately break the rhythm — hesitate, then accelerate — to attack in the gap",
            "Slow down every single technique",
            "Stop attacking until they change something first",
        ],
        "correct": 1,
        "explanation": "Once an opponent is 'entrained' to your tempo, deliberately breaking it — a hesitation followed by a burst — opens a gap their timing isn't prepared for.",
        "source_id": None,
    },
    {
        "id": "sc-combo-05", "category": "combinations", "level": "Competition",
        "situation": "You've thrown two roundhouse kicks in a row and both landed cleanly.",
        "prompt": "What should your third attack look like?",
        "choices": [
            "A third identical roundhouse kick",
            "A different, unexpected technique like a back kick, since the opponent is now anticipating the roundhouse pattern",
            "No attack at all for the rest of the round",
            "Announce the next technique before throwing it",
        ],
        "correct": 1,
        "explanation": "After two of the same technique land, the opponent starts anticipating a repeat — switching to an unexpected technique exploits that expectation.",
        "source_id": None,
    },
    {
        "id": "sc-combo-06", "category": "combinations", "level": "Competition",
        "situation": "It's a close match and you're deciding between playing conservatively for one clean shot, or staying active and initiating combinations frequently.",
        "prompt": "What does match data support?",
        "choices": [
            "Conservative, low-volume play is statistically the better approach",
            "Higher total kick volume across a match is strongly associated with winning — staying active and initiating is the better approach",
            "Volume makes no measurable difference",
            "It's better to stop attacking once you're ahead at all",
        ],
        "correct": 1,
        "explanation": "A decision-tree analysis of match outcomes found competitors who threw significantly more kicks over a match had a much higher win probability than lower-volume competitors — staying active pays off.",
        "source_id": "jeon-lim-2024-decision-tree",
    },

    # --- Scoreboard & Game Management ---
    {
        "id": "sc-game-01", "category": "game-management", "level": "Intermediate",
        "situation": "You're ahead by 3 points with 15 seconds left in the final round.",
        "prompt": "What's the smart strategic approach?",
        "choices": [
            "Retreat and avoid engagement to run out the clock",
            "Stay controlled but active — avoid unnecessary risk while continuing to engage",
            "Attack as recklessly as possible",
            "Stand still without moving at all",
        ],
        "correct": 1,
        "explanation": "Competition rules penalize passivity — retreating purely to run out the clock draws a penalty. Protecting a lead means staying controlled and active, not stalling.",
        "source_id": "usatkd-rules-2026",
    },
    {
        "id": "sc-game-02", "category": "game-management", "level": "Intermediate",
        "situation": "You're down by 4 points with 20 seconds left in the final round.",
        "prompt": "What should your strategy be?",
        "choices": [
            "Play it safe and hope for a mistake from your opponent",
            "Increase aggression and actively look for higher-value scoring opportunities, like head kicks",
            "Focus only on avoiding penalties for the rest of the match",
            "Try to run out the clock yourself",
        ],
        "correct": 1,
        "explanation": "A meaningful deficit late in the match calls for calculated aggression and higher-value scoring attempts — passive play all but guarantees the loss.",
        "source_id": None,
    },
    {
        "id": "sc-game-03", "category": "game-management", "level": "Advanced",
        "situation": "You land a clean turning (spinning) kick to your opponent's head.",
        "prompt": "How many points does that score under current rules?",
        "choices": ["3 points", "4 points", "5 points", "6 points"],
        "correct": 3,
        "explanation": "Under the current rule cycle, a turning/spinning kick to the head is doubled to 6 points — up from 5 points in earlier rule sets some older articles still reference.",
        "source_id": "usatkd-rules-2026",
    },
    {
        "id": "sc-game-04", "category": "game-management", "level": "Advanced",
        "situation": "The score is tied after all 3 regular rounds have finished.",
        "prompt": "What happens next, under current rules?",
        "choices": [
            "The match ends in an official tie",
            "A 1-minute golden round starts with all prior scores voided; the first competitor to reach 2 or more points wins",
            "Whoever scored first in round 1 is declared the winner",
            "The match restarts completely from round 1",
        ],
        "correct": 1,
        "explanation": "The golden round resets scores to zero and requires reaching 2+ points (or 2 opponent penalties) to win — a higher bar than the old 'first point wins' sudden-death format.",
        "source_id": "usatkd-rules-2026",
    },
    {
        "id": "sc-game-05", "category": "game-management", "level": "Advanced",
        "situation": "You've built a 3-point lead going into the final round.",
        "prompt": "How should you treat this lead?",
        "choices": [
            "As essentially a guaranteed win — no further care needed",
            "As a real but not guaranteed advantage worth defending carefully — the data shows a clear edge, but not a certainty",
            "As meaningless since anything can happen",
            "As a reason to stop defending entirely",
        ],
        "correct": 1,
        "explanation": "Match data shows a 3+ point lead corresponds to roughly an 80% win probability — a strong edge, but the other 20% is exactly why careless play late can still lose it.",
        "source_id": "jeon-lim-2024-decision-tree",
    },
    {
        "id": "sc-game-06", "category": "game-management", "level": "Competition",
        "situation": "You're ahead, but only by 1-2 points, heading into the final minute.",
        "prompt": "How safe is this lead, strategically speaking?",
        "choices": [
            "Just as safe as a big lead — no adjustment needed",
            "Meaningfully less safe than a bigger lead — data shows this margin is close to a coin flip, so it should be played as still contested",
            "Guaranteed to hold with any strategy",
            "Impossible to protect under any circumstances",
        ],
        "correct": 1,
        "explanation": "A 1-2 point lead corresponds to only about a 57.5% win probability in match data — much closer than a 3+ point lead, so it calls for continued engagement rather than passive protection.",
        "source_id": "jeon-lim-2024-decision-tree",
    },
    {
        "id": "sc-game-07", "category": "game-management", "level": "Competition",
        "situation": "You're leading 19-0 in the third round.",
        "prompt": "What rule is directly relevant here?",
        "choices": [
            "Nothing changes — the match always runs the full clock",
            "A 20-point gap ends the match immediately, so one more clean score likely finishes it",
            "You automatically lose for being too far ahead",
            "The round restarts once a score gets this lopsided",
        ],
        "correct": 1,
        "explanation": "A 20-point gap at any point in the third round ends the match immediately under the point-gap rule — awareness of this can shape both competitors' urgency.",
        "source_id": "usatkd-rules-2026",
    },
    {
        "id": "sc-game-08", "category": "game-management", "level": "Competition",
        "situation": "The referee calls \"Gong-gyeok\" (engage) and neither competitor moves for 3 full seconds, though you were the one who last stepped backward.",
        "prompt": "What's the likely consequence?",
        "choices": [
            "Nothing — inactivity is never penalized",
            "A Gam-jeom (penalty point) is issued, likely against you as the one who moved backward",
            "The round is immediately replayed",
            "Both competitors are disqualified",
        ],
        "correct": 1,
        "explanation": "Passivity rules penalize inactivity after the engage command — if one competitor moved backward into that inactivity, the penalty is assessed against them specifically.",
        "source_id": "usatkd-rules-2026",
    },

    # --- Reading Opponents ---
    {
        "id": "sc-read-01", "category": "reading-opponents", "level": "Intermediate",
        "situation": "Your opponent is fast and constantly moving, landing quick strikes and immediately retreating out of range.",
        "prompt": "What's an effective way to deal with a hit-and-run style?",
        "choices": [
            "Chase them around the entire mat",
            "Cut off angles and control center position so they run out of space to retreat into",
            "Match their speed by moving even faster with no plan",
            "Stand completely still and wait",
        ],
        "correct": 1,
        "explanation": "Hit-and-run fighters rely on space to retreat into — controlling center position and cutting off angles limits where they can run, forcing more direct engagements.",
        "source_id": None,
    },
    {
        "id": "sc-read-02", "category": "reading-opponents", "level": "Intermediate",
        "situation": "Your opponent is very aggressive, constantly pushing forward and attacking first.",
        "prompt": "What's a sound counter-strategy?",
        "choices": [
            "Match their aggression and attack first every exchange",
            "Use their forward pressure against them with well-timed counters as they advance",
            "Continuously back straight away for the whole match",
            "Stop defending entirely",
        ],
        "correct": 1,
        "explanation": "An opponent who consistently advances is committing to forward momentum you can time counters against, rather than needing to match their pace directly.",
        "source_id": None,
    },
    {
        "id": "sc-read-03", "category": "reading-opponents", "level": "Advanced",
        "situation": "No matter what you do, your opponent refuses to throw the first technique of any exchange.",
        "prompt": "What kind of opponent is this, and how do you handle it?",
        "choices": [
            "An aggressive attacker — pressure them harder",
            "A defensive, counter-heavy style — you have to actively draw them out with feints and footwork",
            "A hit-and-run fighter — chase them down",
            "There's nothing you can do differently",
        ],
        "correct": 1,
        "explanation": "A purely reactive opponent won't initiate on their own — recognizing this style means shifting to feints and footwork to force a reaction, rather than waiting for an attack that won't come.",
        "source_id": None,
    },
    {
        "id": "sc-read-04", "category": "reading-opponents", "level": "Advanced",
        "situation": "You're sparring someone noticeably taller than you with a longer kicking range.",
        "prompt": "What's a sound overall approach?",
        "choices": [
            "Charge straight in as often as possible",
            "Stay patient with a higher guard, minimize retreat, and time counters to the moment their kicking leg is recovering",
            "Retreat continuously for the whole match",
            "Try to match their kicks at their preferred range",
        ],
        "correct": 1,
        "explanation": "A taller opponent's longer leg takes longer to return to the floor after kicking — patience and counters timed to that recovery window exploit the one disadvantage their reach gives them.",
        "source_id": None,
    },
    {
        "id": "sc-read-05", "category": "reading-opponents", "level": "Competition",
        "situation": "You're facing an opponent whose competitive profile leans toward direct attacks and simultaneous counterattacks rather than dodging and repositioning.",
        "prompt": "What should this tell you about how they're likely to try to score?",
        "choices": [
            "Nothing — all competitors score the same way regardless of style",
            "They're more likely to come forward directly or counter simultaneously with your attack, rather than dodge-and-counter from an angle",
            "They will only ever attack with head kicks",
            "They will refuse to engage at all",
        ],
        "correct": 1,
        "explanation": "Notational analysis of Olympic data found scoring-sequence patterns differ meaningfully by competitor profile — some lean on direct-attack and simultaneous-counterattack sequences, others lean on dodge-and-indirect-attack sequences. Recognizing which you're facing helps you anticipate their most likely path to score.",
        "source_id": "menescardi-2021-weight-gender",
    },
    {
        "id": "sc-read-06", "category": "reading-opponents", "level": "Competition",
        "situation": "After a round of sparring, you notice your opponent has scored using the same narrow handful of technique sequences over and over, rather than varying their attacks.",
        "prompt": "How should you use this observation?",
        "choices": [
            "Ignore it — past patterns don't predict future actions",
            "Specifically prepare defenses and counters for that repeated pattern, since they're likely to keep using it",
            "Assume they will never repeat it again",
            "Copy their exact pattern yourself",
        ],
        "correct": 1,
        "explanation": "Research analyzing elite competitors found some rely on a smaller set of scoring patterns used more frequently rather than a wide variety — once you spot the repeated pattern, preparing for it specifically pays off.",
        "source_id": "menescardi-2019-polar-coords",
    },
]

# Citations for research referenced on the page. Every entry here was
# individually verified (URL fetched, citation details confirmed) --
# never fabricated.
SOURCES = [
    {
        "id": "menescardi-2019-medalists",
        "title": "Technical-Tactical Actions Used to Score in Taekwondo: An Analysis of Two Medalists in Two Olympic Championships",
        "authors": "Menescardi C, Falcó C, Ros C, Morales-Sánchez V, Hernández-Mendo A",
        "venue": "Frontiers in Psychology",
        "year": 2019,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6914813/",
        "note": None,
    },
    {
        "id": "menescardi-2019-polar-coords",
        "title": "Is It Possible to Predict an Athlete's Behavior? The Use of Polar Coordinates to Identify Key Patterns in Taekwondo",
        "authors": "Menescardi C, Falcó C, Estevan I, Ros C, Morales-Sánchez V, Hernández-Mendo A",
        "venue": "Frontiers in Psychology",
        "year": 2019,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6548838/",
        "note": None,
    },
    {
        "id": "menescardi-2021-weight-gender",
        "title": "Analysis of Different Key Behavioral Patterns to Score in Elite Taekwondoists According to the Weight Category and Gender",
        "authors": "Menescardi C, Falcó C, Hernández-Mendo A, Morales-Sánchez V",
        "venue": "Frontiers in Psychology",
        "year": 2021,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8326363/",
        "note": None,
    },
    {
        "id": "gamero-castillero-2022",
        "title": "Application of the Polar Coordinate Technique in the Study of Technical-Tactical Scoring Actions in Taekwondo",
        "authors": "Gamero-Castillero JA, Quiñones-Rodríguez Y, Apollaro G, Hernández-Mendo A, Morales-Sánchez V, Falcó C",
        "venue": "Frontiers in Sports and Active Living",
        "year": 2022,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9167957/",
        "note": None,
    },
    {
        "id": "chen-2025-sequential-kicks",
        "title": "Effect of Sequential Kicks on Programming Time and Movement Time in Taekwondo",
        "authors": "Chen CY, Yu CH, Chen TY, Su TY",
        "venue": "Journal of Human Kinetics",
        "year": 2025,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12360942/",
        "note": None,
    },
    {
        "id": "jeon-lim-2024-decision-tree",
        "title": "Taekwondo win-loss determining factors using data mining-based decision tree analysis: focusing on game analysis for evidence-based coaching",
        "authors": "Jeon M, Lim H",
        "venue": "BMC Sports Science, Medicine and Rehabilitation",
        "year": 2024,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11110419/",
        "note": None,
    },
    {
        "id": "usatkd-rules-2026",
        "title": "2026 USA Taekwondo Kyorugi Competition Rules & Interpretation",
        "authors": "USA Taekwondo (implementing World Taekwondo rules)",
        "venue": "Official competition rules, effective Jan 1, 2026",
        "year": 2026,
        "url": "https://assets.contentstack.io/v3/assets/blteb7d012fc7ebef7f/blta5faf747d0f05bc5/695fb747f3d40d4592598474/2026_USATKD_Kyorugi_Rules_010826.pdf",
        "note": "An official rulebook, not a research paper — cited for exact scoring values and match-format facts, which do change between rule cycles.",
    },
]
