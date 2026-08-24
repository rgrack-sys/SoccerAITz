# Unified Soccer Simulator v4.3

## Live Soccer Total-Goals Betting Skill

### Core philosophy

> We are not trying to predict the next goal. We are trying to determine whether the market has correctly priced the probability of the remaining goals.

Analyze both UNDER and OVER markets.

Allowed final decisions:

- BET
- LEAN
- HOLD
- PASS
- CASH OUT
- HEDGE

Default when uncertain, stale, or contradictory:

> PASS

Required hierarchy:

> **Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision**

The skill does not place wagers.

---

# STEP 1 — Goal Math — Mandatory

Always calculate first:

- current score
- current total goals
- selected line
- bet side
- exact additional goals relevant to the wager
- current wager status

A recommendation is invalid if Goal Math is wrong.

## UNDER

Ask:

> How many additional goals cause this Under to lose?

```text
additional_goals_to_lose = floor(total_line - current_goals) + 1
```

If current goals exceed the line, the Under is LOST.

Examples:

- 0-0 Under 2.5 → 3 more goals to lose
- 1-0 Under 2.5 → 2 more goals to lose
- 2-0 Under 2.5 → 1 more goal to lose
- 3-0 Under 4.5 → 2 more goals to lose
- 3-1 Under 4.5 → 1 more goal to lose
- 3-2 Under 4.5 → LOST

## OVER

Ask:

> How many additional goals are required for this Over to win?

```text
additional_goals_to_win = floor(total_line - current_goals) + 1
```

If current goals exceed the line, the Over is WON.

Examples:

- 0-0 Over 2.5 → 3 goals to win
- 1-0 Over 2.5 → 2 more goals to win
- 2-0 Over 2.5 → 1 more goal to win
- 2-1 Over 3.5 → 1 more goal to win
- 3-2 Over 4.5 → WON

## UNDER quick reference

| Current goals | U 0.5 | U 1.5 | U 2.5 | U 3.5 | U 4.5 | U 5.5 | U 6.5 | U 7.5 | U 8.5 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| 1 | LOST | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| 2 | LOST | LOST | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 3 | LOST | LOST | LOST | 1 | 2 | 3 | 4 | 5 | 6 |
| 4 | LOST | LOST | LOST | LOST | 1 | 2 | 3 | 4 | 5 |
| 5 | LOST | LOST | LOST | LOST | LOST | 1 | 2 | 3 | 4 |
| 6 | LOST | LOST | LOST | LOST | LOST | LOST | 1 | 2 | 3 |
| 7 | LOST | LOST | LOST | LOST | LOST | LOST | LOST | 1 | 2 |
| 8 | LOST | LOST | LOST | LOST | LOST | LOST | LOST | LOST | 1 |
| 9 | LOST | LOST | LOST | LOST | LOST | LOST | LOST | LOST | LOST |

## OVER quick reference

| Current goals | O 0.5 | O 1.5 | O 2.5 | O 3.5 | O 4.5 | O 5.5 | O 6.5 | O 7.5 | O 8.5 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| 1 | WON | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| 2 | WON | WON | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 3 | WON | WON | WON | 1 | 2 | 3 | 4 | 5 | 6 |
| 4 | WON | WON | WON | WON | 1 | 2 | 3 | 4 | 5 |
| 5 | WON | WON | WON | WON | WON | 1 | 2 | 3 | 4 |
| 6 | WON | WON | WON | WON | WON | WON | 1 | 2 | 3 |
| 7 | WON | WON | WON | WON | WON | WON | WON | 1 | 2 |
| 8 | WON | WON | WON | WON | WON | WON | WON | WON | 1 |
| 9 | WON | WON | WON | WON | WON | WON | WON | WON | WON |

---

# STEP 2 — Effective Time Remaining

Consider:

- current minute
- match phase
- expected stoppage
- VAR delays
- injuries
- substitutions
- extra time
- whether the market includes extra time

Weighting:

- 0–45 Low
- 46–60 Moderate
- 61–70 Increasing
- 71–80 High
- 81–90 Very high
- 90+ Extreme

For Unders, time decay usually helps.
For Overs, time decay usually hurts unless pressure acceleration compensates.

---

# STEP 3 — Current Attack Quality

Evaluate:

- combined xG
- team xG split
- big chances
- shots
- shots on target
- corners
- keeper saves
- dangerous attacks if available
- box entries if available
- possession only as context

Possession without chance quality is not pressure.

---

# STEP 4 — Pressure Score and Pressure Momentum

## Pressure Score

- 0–2 Dormant
- 3–4 Low
- 5–6 Moderate
- 7–8 High
- 9–10 Extreme / chaos

## Pressure Momentum

Use the latest 5–10 minutes:

- 🟢 Cooling
- 🟡 Stable
- 🟠 Heating
- 🔴 Explosion

Track:

- xG added
- shots added
- shots on target added
- big chances added
- corners added
- saves forced
- dangerous attacks
- possession shift
- tactical territory

Sequential change matters more than static totals.

---

# STEP 5 — Momentum Reset After Every Goal

After every goal:

1. record the goal
2. recalculate Goal Math
3. recalculate time
4. reset Pressure Momentum
5. reset recent-pressure baseline
6. ignore pre-goal momentum in the new state
7. build a fresh post-goal window

> Goals change tactics.

---

# STEP 6 — Post-Goal Vulnerability Rule

When an existing UNDER becomes only one additional goal from losing, force immediate reassessment for roughly 2–5 minutes.

Reassess:

- time
- attack quality
- tactical incentives
- chaos
- trailing-team urgency
- counterattack space

Guidance:

- Cooling → HOLD
- Stable / unresolved → HOLD / LEAN CASH OUT
- Heating → CASH OUT or HEDGE
- Explosion → CASH OUT immediately if available

Earlier low-event evidence does not override the new state.

---

# STEP 7 — Match Archetype

Classify:

- Dead / Low Event
- Controlled Dominance
- One-Sided Assault
- Open / Transitional
- Chaos

Important:

> A harmless opponent does not make an Under safe if the dominant team can score enough by itself.

---

# STEP 8 — Match Context

Evaluate:

- competition
- league / group / knockout / aggregate
- need to win
- goal-difference incentives
- draw acceptability
- qualification / relegation pressure
- red cards
- fatigue
- weather
- injuries
- substitutions
- tournament incentives
- whether a team has abandoned structure

---

# STEP 9 — Chaos Index

Rate Low / Medium / High.

Use:

- red cards
- penalties
- VAR
- repeated corners
- rapid counters
- keeper under siege
- crowd pressure
- substitutions
- long stoppage
- rapid goal clusters
- defensive disorganization

---

# STEP 10 — Tournament / Knockout Adjustment

If knockout:

- determine whether extra time is possible
- determine whether market includes extra time
- determine whether current score would produce extra time
- do not apply normal 90-minute decay if another 30 minutes may count

When tied late:

> Survive stoppage and reassess pace in extra time.

---

# STEP 11 — Monte Carlo Probability Layer

Monte Carlo is a formal v4.3 component.

Placement:

> after Match Context / Chaos and before Market Sanity Check

Required hierarchy:

> **Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision**

Preferred inputs:

- current score
- effective time remaining
- stoppage expectation
- team and combined xG
- xG velocity
- shot velocity
- big-chance velocity
- Pressure Score
- Pressure Momentum
- match archetype
- red cards
- tactical incentives
- lead / trail state
- goal-reset state
- Chaos Index
- competition context
- extra-time treatment

Preferred outputs:

- P(1+ additional goals)
- P(2+ additional goals)
- P(3+ additional goals)
- P(4+ additional goals)
- selected Under probability
- selected Over probability
- final-total distribution
- probabilities across 0.5–8.5

Recommended simulations:

- 25,000 minimum
- 50,000 standard
- 100,000 when useful

Monte Carlo informs probability. It does not override:

- Goal Math
- kill switches
- post-goal reset
- context changes
- chaos escalation
- bad inputs
- market-value requirements

If inputs are poor:

> Reduce confidence or PASS.

---

# STEP 12 — Tail Risk

Every recommendation must explain the concrete sequence that defeats the wager.

UNDER example:

3-0 Under 4.5:
- needs 2 more goals to lose
- tail: trailing team scores → match opens → leader counters → long stoppage produces fifth goal

OVER example:

1-0 Over 2.5:
- needs 2 more goals to win
- failure tail: leader slows tempo → opponent creates sterile possession → xG stalls → clock runs out

---

# STEP 13 — Panic Override / Data-First Rule

> Panic is not evidence.

After a goal, penalty, VAR, red card, big chance, near miss, or cash-out collapse:

1. recalculate Goal Math
2. recalculate time
3. reassess Pressure Score
4. reassess Pressure Momentum
5. compare with pre-event pressure
6. reassess Chaos
7. rebuild Tail Risk
8. reassess market value

---

# STEP 14 — Goal Burst / Cluster Risk

Increase caution after:

- two goals within ~10 minutes
- tactical collapse
- red card
- aggressive chase state
- keeper injury
- repeated high-quality chances
- late end-to-end play

For Unders: dangerous.
For Overs: potential opportunity if the book has not fully repriced.

---

# STEP 15 — Score-State Effects

## Leading by 1
Trailing team generally continues attacking.

## Leading by 2
May stabilize or open. Use pressure data.

## Leading by 3+
Trailing team may collapse; leader may reduce intensity.

## Level late
Evaluate incentives and extra-time rules.

---

# STEP 16 — Market Sanity Check

American odds implied probability:

Negative:
```text
p = abs(odds) / (abs(odds) + 100)
```

Positive:
```text
p = 100 / (odds + 100)
```

Compare:

- sportsbook implied probability
- Monte Carlo / model probability
- estimated edge

If little edge remains:

> PASS

---

# STEP 17 — Value Score

Separate probability from price.

Likely winner ≠ good bet.

---

# STEP 18 — Goal-Line Selection Across the Ladder

Compare all available lines from 0.5 through 8.5.

For each:

1. Goal Math
2. Monte Carlo / model probability
3. book implied probability
4. edge
5. Tail Risk
6. risk-adjusted value

Return:

- best_market
- alternate_market
- no_play

The safest line is not automatically the best line.

---

# STEP 19 — Existing Position Management

## HOLD
Use when Goal Math remains favorable, time helps, pressure is favorable or declining, and cash-out discount is excessive.

## CASH OUT
Use when match structure deteriorates, goal cushion becomes fragile, pressure accelerates against the ticket, or cash-out fairly compensates for risk.

## HEDGE
Use when a liquid opposite market exists, exposure can be reduced efficiently, and hedge is better than cash-out without destroying expected value.

Do not hedge merely because the ticket feels uncomfortable.

---

# STEP 20 — Kill Switch

Force recomputation after:

- goal
- red card
- penalty
- VAR penalty review
- goalkeeper injury
- two goals in a short interval
- sharp xG jump
- multiple big chances
- obvious end-to-end chaos
- extra time becoming likely
- stale or contradictory data

> Stop, recompute, then decide.

---

# STEP 21 — Line Movement Rule

Line movement alone does not cause:

- add
- cash out
- reverse
- hedge

Unexpected movement triggers a fresh match-data check.

---

# STEP 22 — Live Visual Information

Visual observation does not create the wager.

It may accelerate execution only when:

1. statistical support already exists
2. price remains acceptable
3. feed is genuinely low latency
4. defense visibly loses structure

Examples:

- confused marking
- failed clearances
- repeated free runners
- inability to reset
- repeated dangerous possessions
- defensive scrambling

> Stats establish edge → market determines value → live observation may improve execution timing.

---

# STEP 23 — Confidence

- 10/10 Exceptional
- 9/10 Very strong
- 8/10 Good wager
- 7/10 Playable
- 6/10 Lean only
- 5/10 Coin flip / no useful edge
- Below 5/10 PASS

Confidence is confidence in the value decision.

---

# STEP 24 — Final Recommendation

Exactly one:

- BET
- LEAN
- HOLD
- PASS
- CASH OUT
- HEDGE

Default:

> PASS

---

# Bankroll Guidance — Provisional

Inherited v4.2 sizing remains provisional:

- 10/10 → up to 2.0%
- 9/10 → up to 1.5%
- 8/10 → up to 1.0%
- 7/10 → up to 0.5%
- 6/10 or lower → small action or PASS

Do not mechanically equate confidence with stake size.

Future sizing should consider:

- edge
- confidence
- price
- variance
- goal cushion
- time remaining
- bankroll
- correlated exposure
- open positions

No Martingale.
No chasing losses.

---

# Missing Data Rules

A new BET requires:

- current score
- current minute
- line or full ladder
- side
- current odds

If recent pressure data is unavailable:

- reduce confidence
- never invent momentum

If market data is stale:

> PASS

If sources conflict:

> PASS until resolved

---

# Core Behavioral Rules

1. Goal Math before narrative.
2. Analyze UNDER and OVER symmetrically.
3. Time decay matters increasingly after 70'.
4. Pressure trend matters more than raw possession.
5. xG velocity matters more than cumulative xG alone.
6. Keep Pressure Score and Momentum separate.
7. Reset momentum after every goal.
8. One-goal vulnerability requires forced reassessment.
9. A harmless opponent does not make an Under safe if one team can score enough alone.
10. Panic is not evidence.
11. Recent goals do not guarantee another goal.
12. Monte Carlo informs probability; it does not override live-state logic.
13. Required hierarchy: Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision.
14. Compare nearby goal lines rather than defaulting to the safest one.
15. Market movement triggers analysis; it does not replace analysis.
16. Live visual information may improve timing only after the statistical case exists.
17. Tournament format can change time-decay logic.
18. Tail Risk must describe the failure path.
19. Likely winner does not equal good price.
20. Protect bankroll before chasing action.
21. When uncertain, PASS.
