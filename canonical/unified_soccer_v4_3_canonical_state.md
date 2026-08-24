# Unified Soccer Simulator v4.3 — Current Canonical State

## Purpose

Portable source-of-truth summary for continuing development of the Unified Soccer Simulator v4.3 across chats, devices, or agents.

The full v4.3 skill remains the detailed specification. This file records the current model state, the most important rules, and open design decisions that still need work.

---

# Core Philosophy

> We are not trying to predict the next goal. We are trying to determine whether the market has correctly priced the probability of the remaining goals.

The model analyzes both:

- UNDER
- OVER

Allowed final decisions:

- BET
- LEAN
- HOLD
- PASS
- CASH OUT
- HEDGE

Default when uncertain:

> PASS

---

# Mandatory Analysis Order

## 1. Goal Math

Always calculate first.

For an UNDER:

> How many additional goals cause the bet to lose?

For an OVER:

> How many additional goals are required for the bet to win?

Supported standard half-goal lines:

- 0.5
- 1.5
- 2.5
- 3.5
- 4.5
- 5.5
- 6.5
- 7.5
- 8.5

Never confuse goals already scored with goals still required.

---

## 2. Effective Time Remaining

Include:

- Current minute
- Expected stoppage
- Match phase
- Extra time if relevant
- Whether the sportsbook market includes extra time

Time decay becomes increasingly important after 70'.

Same score, different minute = different wager.

---

## 3. Current Attack Quality

Evaluate:

- Combined xG
- Team xG split
- Big chances
- Shots
- Shots on target
- Corners
- Keeper saves
- Dangerous attacks if available
- Box entries if available

Possession is contextual only.

High possession with low xG may be sterile control rather than pressure.

---

## 4. Pressure

Keep BOTH:

### Pressure Score
0–10 current danger level.

- 0–2 dormant
- 3–4 low
- 5–6 moderate
- 7–8 high
- 9–10 extreme / chaos

### Pressure Momentum
Direction of recent 5–10 minute change.

- 🟢 Cooling
- 🟡 Stable
- 🟠 Heating
- 🔴 Explosion

Sequential change matters more than cumulative totals.

Prefer:

- xG velocity
- shot velocity
- big-chance velocity
- corner velocity
- save velocity
- tactical territory change

---

# Momentum Reset

After EVERY goal:

1. Recalculate Goal Math.
2. Recalculate time remaining.
3. Reset Pressure Momentum.
4. Do not carry pre-goal momentum into the new state.
5. Build a fresh post-goal pressure profile.

Reason:

> Goals change tactics.

---

# Post-Goal Vulnerability Rule

When an existing UNDER is now only ONE additional goal from losing:

Trigger a forced reassessment.

During the next approximately 2–5 minutes:

- Reset momentum.
- Ignore pre-goal momentum.
- Recalculate time.
- Reassess attack quality.
- Reassess tactical incentives.
- Reassess chaos.
- Watch the trailing team's urgency.
- Watch counterattack space for the leading team.

Decision guidance:

- One goal from failure + clear Cooling → HOLD
- One goal from failure + Stable / unresolved → HOLD / LEAN CASH OUT
- One goal from failure + Heating → CASH OUT or HEDGE
- One goal from failure + Explosion → CASH OUT immediately if available

This rule overrides confidence created by the earlier low-event state.

---

# Match Archetypes

Classify the current game as one of:

## Dead / Low Event
Low xG, few shots, few big chances, slow accumulation.

## Controlled Dominance
One side controls the match without repeated high-quality chances.

## One-Sided Assault
One side repeatedly creates dangerous chances.

Important lesson:
A harmless opponent does NOT make an Under safe if the dominant team can score enough by itself.

## Open / Transitional
Both sides generate attacks and transitions.

## Chaos
Red cards, penalties, repeated VAR, tactical collapse, multiple rapid goals, defensive disorganization, long stoppage, or end-to-end late play.

---

# Panic Override / Data-First Rule

> Panic is not evidence.

After a goal, penalty, VAR event, near miss, red card, or cash-out collapse:

Recalculate:

1. Goal Math
2. Time Remaining
3. Pressure Score
4. Pressure Momentum
5. Chaos
6. Tail Risk
7. Market value

Do not extrapolate one scary event into another goal unless the underlying pressure supports it.

---

# Goal Burst / Cluster Risk

Increase caution after:

- two goals within about 10 minutes
- red card
- tactical collapse
- repeated big chances
- goalkeeper injury
- trailing team abandoning structure
- late end-to-end play

For UNDERS:
cluster risk is dangerous.

For OVERS:
cluster conditions can create opportunity, but only if the market has not already repriced.

---

# Match Context

Always consider:

- Competition
- League / group / knockout
- Must-win state
- Goal differential incentives
- Whether a draw is acceptable
- Red cards
- Fatigue
- Weather
- Substitutions
- Qualification / relegation pressure
- Aggregate score
- Third-place / friendly / low-stakes incentives

Tournament context can invalidate normal league assumptions.

---

# Knockout / Extra-Time Rule

If tied late in knockout play:

- Determine whether extra time is possible.
- Determine whether the sportsbook total includes extra time.
- Do not apply normal 90-minute decay if another 30 minutes may count.

When appropriate:

> Survive stoppage and reassess pace in extra time.

---

# Tail Risk

Every recommendation must explain:

> What exact sequence defeats this wager?

UNDER example:

3-0 Under 4.5:
- Need 2 more goals to lose.
- Tail: trailing team scores → game opens → counterattack / long stoppage produces fifth goal.

OVER example:

1-0 Over 2.5:
- Need 2 more goals to win.
- Failure tail: leader slows tempo → opponent produces sterile possession → xG stalls → clock runs out.

---

# Monte Carlo Probability Layer

Monte Carlo simulation is a formal component of v4.3.

It sits **after Match Context / Chaos** and **before Market Sanity Check**.

It informs the probability estimate but does **not** override the rest of the model.

## Required hierarchy

> Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision

The simulation should estimate the distribution of remaining goals using the current live state, but it must **not discard the pre-match scoring prior** simply because the first half or recent window has been quiet.

## Score-State Calibration Rule

When the live Monte Carlo estimate differs materially from the sportsbook, first test whether the simulation is underweighting a structural variable before concluding that the market is wrong.

In particular, the probability engine should blend:

> pre-match scoring prior + live-state update + score-state tactical adjustment + recent pressure

Important score-state effects include:

- trailing-team urgency, especially after halftime
- stronger teams increasing attacking intensity when behind
- leading teams creating additional counterattack space as the opponent commits numbers
- substitutions made specifically to change attacking posture
- historical second-half scoring behavior for the competition and teams
- tactical asymmetry caused by a one-goal margin
- game-state transitions after an equalizer or go-ahead goal

A quiet first half does **not** automatically imply a quiet second half.

Example lesson:

A 1-0 halftime score with modest combined xG may still carry a high probability of additional goals when a strong trailing side is expected to chase aggressively and the leading side gains counterattacking opportunities.

Therefore:

- Do not extrapolate first-half xG linearly into the second half.
- Do not let recent low xG erase the pre-match prior.
- Apply a score-state adjustment before producing remaining-goal probabilities.
- If the model and market diverge sharply, identify the variable that would need to be true for the market price to make sense.

## Required Monte Carlo Sanity Outputs

For the selected total, include when possible:

- model probability
- sportsbook raw implied probability
- sportsbook no-vig probability
- estimated edge
- expected remaining goals (lambda)
- **market-required remaining-goals lambda**: the remaining-goal expectation that would make the sportsbook price approximately fair

The market-required lambda is a diagnostic, not a reason to trust the sportsbook automatically.

Its purpose is to ask:

> What scoring environment must be true for this price to be reasonable, and does the live match state support that environment?

Preferred live inputs:

- current score
- effective time remaining
- expected stoppage time
- combined and team xG
- recent xG velocity
- shot velocity
- big-chance velocity
- Pressure Score
- Pressure Momentum
- match archetype
- red cards
- tactical incentives
- leading/trailing state
- recent goal reset
- chaos level
- competition / knockout context
- whether extra time counts for the market

The simulation should return probabilities for the relevant goal thresholds, including when useful:

- probability of 1+ additional goals
- probability of 2+ additional goals
- probability of 3+ additional goals
- probability of 4+ additional goals
- probability of the selected UNDER winning
- probability of the selected OVER winning
- distribution of likely final goal totals

For a goal ladder, the engine should be able to estimate probabilities across 0.5 through 8.5.

Example output:

- P(final total ≥ 3)
- P(final total ≥ 4)
- P(final total ≥ 5)

Monte Carlo is a **probability engine**, not a standalone betting signal.

A strong simulation probability is not sufficient for BET unless the sportsbook price creates measurable edge.

If live inputs are stale, contradictory, incomplete, or structurally unreliable:

> Reduce confidence or PASS rather than trusting a precise simulation output.

Do not allow Monte Carlo to override:

- Goal Math
- kill-switch events
- post-goal reset logic
- match-context changes
- chaos escalation
- poor or stale input quality
- market value requirements

---

# Market Sanity Check

Separate:

- Probability of winning
- Value at the offered price

A likely winner is not automatically a good bet.

Compare:

- Sportsbook implied probability
- Model probability
- Estimated edge

If the book already prices near-perfection:

> PASS

---

# Goal-Line Selection Across the Ladder

Do not anchor on the first visible line.

Compare available totals from 0.5 through 8.5.

For each candidate:

1. Goal Math
2. Model probability
3. Book implied probability
4. Edge
5. Tail risk
6. Risk-adjusted value

The safest line is not automatically the best line.

---

# Existing Position Management

## HOLD
Use when:

- Goal Math remains favorable
- Time progression favors the position
- Pressure is favorable or declining
- No structural risk has appeared
- Cash-out discount is excessive

## CASH OUT
Use when:

- Match structure materially deteriorates
- Goal cushion becomes fragile
- Pressure accelerates against the position
- Red card / tactical change worsens tail risk
- Cash-out reasonably compensates for remaining risk

## HEDGE
Use when:

- A liquid opposite market exists
- Exposure can be reduced efficiently
- Hedge is superior to cash-out
- Expected value is not destroyed unnecessarily

Do not hedge merely because the ticket feels uncomfortable.

---

# Kill Switch

Force recomputation after:

- Goal
- Red card
- Penalty
- VAR penalty review
- Goalkeeper injury
- Two goals in a short interval
- Sharp xG jump
- Multiple big chances in a short interval
- Obvious end-to-end chaos
- Extra time becoming likely
- Stale / contradictory data

Kill switch means:

> Stop, recompute, then decide.

It does NOT automatically mean exit.

---

# Live Visual Information

Live visual observation is NOT a model rule and does NOT create a bet by itself.

It may accelerate execution ONLY when:

1. The statistical model already supports the wager.
2. The market price is still acceptable.
3. The viewer has a genuinely low-latency / near-live feed.
4. The live picture suddenly confirms structural breakdown, such as:
   - confused marking
   - failed clearances
   - repeated free runners
   - inability to reset shape
   - consecutive dangerous possessions
   - defensive scrambling

Hierarchy:

> Stats establish the edge → market determines value → live observation may improve execution timing.

Broadcast delay can eliminate this execution advantage.

This is a rare bonus edge, not something to hunt for.

---

# Line Movement Rule

Line movement alone is not a reason to:

- add
- cash out
- reverse
- hedge

Unexpected line movement triggers a re-check of the underlying match data.

The sportsbook price is a signal, not the model.

---

# Confidence

Human scale:

- 10/10 Exceptional
- 9/10 Very strong
- 8/10 Good wager
- 7/10 Playable
- 6/10 Lean only
- 5/10 Coin flip / no useful edge
- Below 5/10 PASS

Confidence means confidence in the VALUE decision, not merely probability that the bet wins.

---

# Current Bankroll Rule — OPEN DESIGN ISSUE

The inherited v4.2 rule is:

- 10/10 → up to 2.0%
- 9/10 → up to 1.5%
- 8/10 → up to 1.0%
- 7/10 → up to 0.5%
- 6/10 or lower → small action or PASS

However, live testing showed this may be too conservative and does not match actual practical use.

DO NOT silently replace it yet.

Open design task:

> Separate model confidence from stake sizing and build a better bankroll / unit-sizing method.

Until redesigned, bankroll guidance should be treated as provisional.

No Martingale.
No chasing losses.
No increasing stake because the previous wager lost.

---

# Open Design Decisions

## 1. Stake Sizing
Need a separate risk model that considers:

- confidence
- estimated edge
- price
- variance
- goal cushion
- time remaining
- bankroll
- correlated exposure
- current open positions

## 2. Quantitative Probability Engine
Monte Carlo is now restored as a required probability layer.

Current calibration may still be heuristic until enough live-match data is collected.

The next design step is to improve calibration of the simulation inputs and transition rates using:

- current score
- remaining time
- xG velocity
- pressure state
- match archetype
- red cards
- tactical incentives
- goal-reset state
- chaos level
- competition context

## 3. Visual Input
Keep visual observation as discretionary execution context, not a formal trigger.

## 4. Agent Automation
Agent should:

- collect data
- maintain snapshots
- compare recent windows
- call v4.3
- notify on material changes

Do not automatically place wagers without a separate explicit execution policy.

---

# Agent Inputs — Current Required Shape

Minimum for a new BET:

- score
- minute
- market side or full ladder
- total line
- current odds

Preferred:

- full 0.5–8.5 ladder
- cumulative stats
- recent 5–10 minute deltas
- previous snapshots
- competition context
- red cards
- penalties / VAR
- substitutions
- extra-time rules
- open position / cash-out data

If recent pressure is missing:

> Reduce confidence.

If sportsbook data is stale:

> PASS.

If sources conflict:

> PASS until resolved.

---

# Current Agent Behavior

The Soccer Sentinel should re-run v4.3 after:

- Goal
- Red card
- Penalty
- VAR
- Halftime
- 60' if position open
- 70'
- 80'
- 85'
- Stoppage begins
- Extra time begins
- Large odds move
- Sharp xG acceleration
- Multiple big chances
- Large total-ladder change

It should notify only when:

- recommendation changes
- confidence changes materially
- pressure changes materially
- kill switch fires
- better line appears
- open-position risk changes materially

---

# Current Canonical Principles

1. Goal Math first.
2. Time matters increasingly late.
3. Pressure trend > raw possession.
4. xG velocity > cumulative xG alone.
5. Pressure Score and Pressure Momentum are separate.
6. Reset momentum after every goal.
7. Post-goal one-goal vulnerability requires forced reassessment.
8. Panic is not evidence.
9. A harmless opponent does not make an Under safe if one team can score enough alone.
10. Recent goals do not guarantee another goal.
11. Compare goal lines instead of defaulting to the safest one.
12. Market movement triggers analysis; it does not replace analysis.
13. Live visual information can improve timing only after the statistical case already exists.
14. Tournament format can change time-decay logic.
15. Tail Risk must describe the actual failure path.
16. Likely winner ≠ good price.
17. Protect bankroll before chasing action.
18. When uncertain, PASS.
19. Monte Carlo informs probability; it does not override live-state logic or market value.
20. Required decision hierarchy: Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision.
21. Monte Carlo must blend the pre-match scoring prior with the live-state update; do not linearly extrapolate a quiet first half.
22. When model and market diverge sharply, test score-state and structural variables before declaring the sportsbook wrong.
23. Use market-required remaining-goals lambda as a sanity diagnostic against the current book price.
24. Wager sizing is mechanical and separate from emotional conviction.
25. Every BET must include a recommended stake derived from bankroll, confidence, odds, chaos, failure cushion, and active exposure.
26. The user may always wager less than the model stake, but stake increases require a fresh model evaluation.
27. Total active soccer exposure should normally remain below 3–4% of bankroll.
28. If calculated sizing and emotional impulse disagree, follow the calculated sizing.
29. Announced stoppage time is a minimum, not a guaranteed endpoint.
30. In single-event-failure UNDER positions at or beyond announced stoppage, trigger an immediate Late-Clock Cashout Reassessment.
31. Recalculate effective remaining time using dynamic extension risk rather than assuming the posted stoppage number is terminal.
32. Never ignore a meaningful late cashout offer merely because the match feels finished.

---

# Current Version

**Unified Soccer Simulator v4.3**

Canonical companion files:

- `unified_soccer_simulator_v4_3_skill.md`
- `unified_soccer_simulator_v4_3_input_schema.json`
- `soccer_sentinel_agent_v4_3.md`

This file should be updated whenever a new rule is accepted into the canonical model.


# Late-Clock Cashout Reassessment

This is a mandatory v4.3 rule for existing live UNDER positions.

When an UNDER wager is in a **single-event failure state** and the match reaches or exceeds announced stoppage time, do **not** mentally treat the wager as finished.

Announced stoppage time is a **minimum**, not a guaranteed endpoint.

## Trigger Conditions

Immediately reassess the position when all or most of the following are true:

- one additional goal loses the wager
- the match has reached or exceeded the announced stoppage threshold
- the sportsbook is still offering a meaningful cashout
- the trailing team is still actively attacking
- substitutions, injuries, VAR, cards, celebrations, time-wasting, or other stoppages have occurred during added time
- the posted stoppage amount has increased or effective play has materially exceeded the original expectation

## Required Recalculation

Recalculate:

> effective remaining time = announced remaining time + dynamic extension risk

Dynamic extension risk should increase with:

- substitutions during stoppage
- injuries
- VAR reviews
- penalties
- cards / confrontations
- goal celebrations
- time-wasting
- repeated fouls
- set-piece delays
- stoppages occurring inside stoppage time

Do not assume that reaching 90+N means the game is functionally over.

## Cashout Value Check

For an existing ticket, compare:

> cashout value / full potential payout

against:

> model probability of the wager surviving from the current state

Also compare the remaining upside:

> full payout - cashout offer

against the residual single-event tail risk.

A late cashout can become rational even when an earlier cashout was poor value.

Example:

- Early in the second half, cashing out at a severe discount may be irrational because substantial survival probability remains.
- At or beyond announced stoppage, if only one event loses and the cashout has recovered to a high percentage of full payout, the risk/reward may have changed enough to justify exiting.

## Decision Rule

This is **not** an automatic CASH OUT rule.

It is an automatic **REASSESS NOW** rule.

The decision should consider:

- effective remaining time
- dynamic extension risk
- current field-state pressure
- set-piece / box-entry frequency
- trailing-team urgency
- cashout percentage of full payout
- remaining upside
- single-event tail risk

If the match has reached or exceeded announced stoppage, one goal loses, and the remaining upside is small relative to the live tail risk:

> CASH OUT should be strongly considered.

## Late-Clock Complacency Rule

> Never ignore a meaningful cashout offer merely because the match feels finished.

A wager is not finished until the referee ends the match.

