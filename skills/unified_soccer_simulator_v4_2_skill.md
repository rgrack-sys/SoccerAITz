# UNIFIED SOCCER SIMULATOR v4.2 — Skill Specification

## Live Soccer Betting Engine

### Purpose

Analyze live soccer total-goals markets and determine whether the sportsbook has mispriced the probability of **future goals**.

This is a betting model, not a next-goal prediction model.

The model may analyze either:

- **UNDER**
- **OVER**

The model must return only one of these final actions:

- **BET**
- **LEAN**
- **HOLD**
- **PASS**
- **CASH OUT**
- **HEDGE**

If confidence is insufficient, data is stale, or the evidence is contradictory, the answer is always:

> **PASS**

The skill itself does not place wagers.

---

# STEP 1 — Goal Math — MANDATORY

Goal math is always the first calculation.

Before discussing xG, momentum, odds, match narrative, team quality, or intuition, explicitly calculate:

- Current score
- Current total goals
- Selected market line
- Bet side: UNDER or OVER
- Exact number of additional goals relevant to the wager
- Whether the wager is already won/lost if applicable

A recommendation is invalid if this calculation is wrong.

## UNDER math

For an Under wager, calculate:

> **How many additional goals cause the wager to lose?**

For standard half-goal lines:

```text
additional_goals_to_lose = floor(total_line - current_goals) + 1
```

If:

```text
current_goals > total_line
```

then the Under is already **LOST**.

Examples:

- 0-0, Under 2.5 → 3 additional goals to lose.
- 1-0, Under 2.5 → 2 additional goals to lose.
- 2-0, Under 2.5 → 1 additional goal to lose.
- 3-0, Under 4.5 → 2 additional goals to lose.
- 3-1, Under 4.5 → 1 additional goal to lose.
- 3-2, Under 4.5 → already lost because 5 total goals > 4.5.

## OVER math

For an Over wager, calculate:

> **How many additional goals are required for the wager to win?**

For standard half-goal lines:

```text
additional_goals_to_win = floor(total_line - current_goals) + 1
```

If:

```text
current_goals > total_line
```

then the Over is already **WON**.

Examples:

- 0-0, Over 2.5 → needs 3 goals to win.
- 1-0, Over 2.5 → needs 2 more goals to win.
- 2-0, Over 2.5 → needs 1 more goal to win.
- 2-1, Over 3.5 → needs 1 more goal to win.
- 3-2, Over 4.5 → already won.

## Critical symmetry

For a given score and total line:

> The number of additional goals that makes an **Under lose** is the same number that makes the corresponding **Over win**.

The interpretation is different, so the skill must state the side explicitly.

---

# Goal-Math Quick Reference — UNDER 0.5 through 8.5

Each number below means:

> **additional goals required for the Under to lose**

`LOST` means the current total is already above the line.

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

---

# Goal-Math Quick Reference — OVER 0.5 through 8.5

Each number below means:

> **additional goals required for the Over to win**

`WON` means the current total is already above the line.

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

# STEP 2 — Time Remaining

Calculate:

- Current minute
- Match phase
- Expected stoppage time
- Effective remaining playing time
- Whether extra time is possible
- Whether the selected sportsbook market includes extra time

Time weighting increases rapidly after 70'.

General weighting:

- 0–45: Low
- 46–60: Moderate
- 61–70: Increasing
- 71–80: High
- 81–90: Very high
- 90+: Extreme

Never treat the same score identically at different times.

Example:

- 3-0 at 55' is materially different from 3-0 at 81'.

For Unders, time decay usually helps.

For Overs, time decay usually hurts unless pressure is accelerating strongly enough to compensate.

---

# STEP 3 — Current Attack Quality

Evaluate the current scoring environment.

Use:

- Combined xG
- Team xG split
- Big Chances
- Shots
- Shots on Target
- Corners
- Dangerous Attacks, if available
- Keeper Saves
- Box entries, if available

Do not rely on possession alone.

High possession with low chance creation may indicate control rather than danger.

---

# STEP 4 — Pressure Momentum

Measure the most recent **5–10 minutes**, not merely the cumulative match totals.

Track changes in:

- xG
- Shots
- Shots on target
- Big chances
- Corners
- Keeper saves
- Dangerous attacks
- Possession shift
- Tactical territory

Classify Pressure Momentum as:

## 🟢 Cooling

Little or no increase in attacking indicators.

## 🟡 Stable

Small increases without meaningful acceleration.

## 🟠 Heating

Multiple attacking indicators are increasing.

## 🔴 Explosion

Several high-value indicators are accelerating simultaneously.

Pressure Momentum is independent of total xG.

A match can have high cumulative xG but be cooling.

A match can have modest cumulative xG but be heating rapidly.

---

# STEP 5 — Momentum Reset

Whenever a goal is scored:

1. Record the goal.
2. Recalculate Goal Math.
3. Recalculate effective time remaining.
4. **Reset Pressure Momentum.**
5. Ignore pre-goal pressure when evaluating the immediate post-goal state.
6. Build a fresh pressure profile over approximately the next 5 minutes.

Reason:

> Goals change tactics.

The previous match state may no longer apply.

A team may:

- protect a lead,
- chase the game,
- collapse,
- increase tempo,
- reduce tempo,
- become vulnerable to counters.

---

# STEP 6 — Match Archetype

Classify the match.

## A. Dead / Low Event

Typical:

- Low xG
- Few shots
- Few big chances
- Slow xG accumulation
- Little box pressure

Usually Under-friendly.

## B. Controlled Dominance

One side controls the game without producing repeated high-quality chances.

Often Under-friendly once the leader is established.

## C. One-Sided Assault

One side generates repeated dangerous chances.

Indicators:

- Large xG gap
- Multiple big chances
- High shot rate
- High keeper-save count
- Sustained corners or box entries

Dangerous for Unders even when the opponent offers little.

Can be favorable to Overs when the line still requires achievable scoring.

## D. Open / Transitional

Both sides generate attacking opportunities.

Indicators:

- Both sides accumulating xG
- End-to-end transitions
- Big chances at both ends
- Rapid shot generation

Under-hostile and potentially Over-friendly.

## E. Chaos

Examples:

- Red card
- Penalty
- Repeated VAR
- Defensive collapse
- Multiple goals in a short interval
- Tactical abandonment
- Late desperation
- Goalkeeper injury
- Very long stoppage

High variance.

Usually PASS unless the price and goal math create an unusually large cushion or edge.

---

# STEP 7 — Match Context

Evaluate:

- Competition
- League / group / knockout
- Need for goal differential
- Need to win
- Whether both teams would accept a draw
- Red cards
- Fatigue
- Weather
- Substitutions
- Tournament incentives
- Relegation / qualification pressure
- Whether one side has effectively abandoned the match

Context modifies expected future scoring.

Do not assume a generic league-state model applies to:

- tournament third-place games,
- friendlies,
- knockout extra time,
- aggregate-score situations,
- matches where goal differential matters.

---

# STEP 8 — Chaos Index

Rate:

- **Low**
- **Medium**
- **High**

Factors include:

- Red cards
- Penalties
- VAR
- Repeated corners
- Rapid counters
- Keeper under siege
- Crowd pressure
- Multiple substitutions
- High expected stoppage time
- Multiple goals in a short span
- Defensive disorganization

Higher chaos means higher variance and therefore more tail risk.

---

# STEP 9 — Tail Risk

Every recommendation must explicitly answer:

> **What sequence of events actually beats this wager?**

For an Under, describe the path to enough future goals to cross the line.

Example:

Under 4.5 at 3-0:

- Need 2 more goals to lose.
- Possible tail: Tottenham pulls one back → Brentford counters into an open game → long stoppage time creates another high-quality chance.

For an Over, describe the path by which scoring fails to reach the line.

Example:

Over 2.5 at 1-0:

- Need 2 more goals to win.
- Failure tail: leading team slows tempo → opponent produces sterile possession → xG remains flat through 75' → match closes.

Tail Risk must be concrete, not generic.

---

# STEP 10 — Panic Override / Data-First Rule

An adverse event does not automatically invalidate the position.

After:

- Goal
- Penalty
- VAR
- Red card
- Big chance
- Near miss
- Sudden cash-out deterioration

perform a fresh calculation:

1. Goal Math
2. Time Remaining
3. Pressure Momentum
4. Chaos Index
5. Tail Risk
6. Market value

Core rule:

> **Panic is not evidence.**

For an Under, a new goal matters because it changes the remaining goal cushion, not because the event feels alarming.

For an Over, a missed chance does not automatically invalidate the thesis if pressure remains high and enough time remains.

---

# STEP 11 — Goal Burst / Cluster Risk

Goals are not fully independent events.

Increase caution after:

- Two goals within approximately 10 minutes
- Tactical collapse
- Red card
- A trailing side abandoning structure
- Goalkeeper injury
- Repeated high-quality chances
- End-to-end late play

For Unders, cluster risk is dangerous.

For Overs, cluster conditions may create opportunity — but the sportsbook may reprice faster than the model.

Do not extrapolate a recent goal mechanically into another goal.

---

# STEP 12 — Score-State Effects

## Leading by 1

The trailing team usually continues to attack.

Late scoring risk remains meaningful.

## Leading by 2

The game may:

- stabilize, or
- open dramatically as the trailing team chases.

Pressure data decides which.

## Leading by 3+

The trailing team may collapse psychologically or tactically.

The leader may also reduce intensity.

Do not assume continued scoring solely from domination.

## Level score late

Evaluate incentives carefully.

Some teams accept the draw.

Others must win.

In knockout play, extra time can completely change the time-decay calculation.

---

# STEP 13 — Market Sanity Check

Convert American odds to approximate implied probability.

Negative odds:

```text
p = abs(odds) / (abs(odds) + 100)
```

Positive odds:

```text
p = 100 / (odds + 100)
```

Examples:

- -200 ≈ 66.7%
- -300 = 75.0%
- -400 = 80.0%
- -500 ≈ 83.3%
- -1000 ≈ 90.9%

Because of sportsbook vig, implied probability is not true probability.

Compare:

- Book implied probability
- Model probability
- Estimated edge

If the sportsbook already prices near-perfection and the model has little additional edge:

> **PASS**

Never chase certainty at terrible odds.

---

# STEP 14 — Value Score

Separate:

> **Probability of winning**

from:

> **Value at the offered price**

Examples:

Model says Under wins 94%.

Book implies 93%.

Result:

> Very likely winner, almost no measurable edge → PASS.

Model says Under wins 83%.

Book implies 74%.

Result:

> Material edge → BET candidate.

The same logic applies to Overs.

A low-probability Over can still be a valid BET if the offered price materially understates its true probability.

---

# STEP 15 — Existing Position Management

If a position already exists, choose among:

- HOLD
- CASH OUT
- HEDGE

## HOLD

Use when:

- Goal math remains favorable
- Time progression favors the wager
- Pressure is stable or moving favorably
- No major structural risk has appeared
- Cash-out discount is excessive

## CASH OUT

Use when:

- The underlying scoring environment has materially changed against the bet
- Goal math has become fragile
- Pressure has accelerated against the position
- Red card / tactical shift materially increases tail risk
- Cash-out value reasonably compensates for remaining risk

## HEDGE

Use only when:

- A liquid opposite market exists
- Exposure can be materially reduced
- The hedge is superior to the available cash-out
- The hedge does not destroy expected value unnecessarily

Do not cash out merely because the wager feels uncomfortable.

---

# STEP 16 — Kill Switch

Immediately stop normal reasoning and recompute the match after:

- Goal
- Red card
- Penalty
- VAR penalty review
- Goalkeeper injury
- Two goals in a short interval
- Sudden combined-xG jump
- Multiple big chances in a short interval
- Obvious end-to-end chaos
- Extra time becoming likely when the market includes extra time
- Stale or contradictory data

Kill switch means:

> **Recompute from scratch.**

It does not automatically mean exit.

---

# STEP 17 — Final Recommendation

The final recommendation must be exactly one of:

## BET

Clear measurable edge.

## LEAN

Small edge, not enough for a full wager.

## HOLD

Existing ticket remains favorable.

## CASH OUT

Remaining risk now exceeds expected reward.

## HEDGE

Protect exposure efficiently.

## PASS

No measurable edge or insufficient information.

Default:

> **PASS**

---

# Confidence Scale

Use the permanent 10-point scale.

- **10/10** — Exceptional value
- **9/10** — Very strong
- **8/10** — Good wager
- **7/10** — Playable
- **6/10** — Lean only
- **5/10** — Coin flip / no useful edge
- **Below 5/10** — PASS

Confidence is confidence in the **value decision**, not merely confidence that the wager will win.

---

# Bankroll Rules

Maximum suggested stake as a percentage of bankroll:

- **10/10:** up to **2.0%**
- **9/10:** up to **1.5%**
- **8/10:** up to **1.0%**
- **7/10:** up to **0.5%**
- **6/10 or lower:** small action or PASS

Rules:

- No Martingale
- No chasing losses
- No increasing stake because a previous bet lost
- No forcing action because a match is available
- Price discipline overrides certainty

The edge comes from waiting for mispriced opportunities.

---

# Permanent Output Format

## Match

Teams  
Minute  
Score  
Competition / context

---

## Goal Math

Bet side  
Goal line  
Current total goals  
For UNDER: additional goals before wager loses  
For OVER: additional goals required to win  
Current wager status

---

## Time Pressure

Effective time remaining  
Expected stoppage  
Extra-time treatment if relevant

---

## Attack Quality

Combined xG  
Team xG split  
Big Chances  
Shots  
Shots on Target  
Corners  
Keeper Saves  
Dangerous Attacks if available

---

## Pressure Momentum

One of:

- 🟢 Cooling
- 🟡 Stable
- 🟠 Heating
- 🔴 Explosion

Include the 5–10 minute evidence.

---

## Match Archetype

Dead / Low Event  
Controlled Dominance  
One-Sided Assault  
Open / Transitional  
Chaos

---

## Match Context

Need goal?  
Protecting lead?  
Would draw be acceptable?  
Knockout?  
Goal differential?  
Red cards?  
Substitutions / fatigue?

---

## Chaos Index

Low  
Medium  
High

---

## Tail Risk

Exactly what sequence beats the wager.

---

## Market Check

Sportsbook odds  
Book implied probability  
Model probability  
Estimated edge

---

## Value Assessment

Probability of win  
Quality of price  
Whether the edge is large enough to act

---

## Final Decision

Exactly one:

BET  
LEAN  
HOLD  
PASS  
CASH OUT  
HEDGE

---

## Confidence

__/10

---

## Bankroll Guidance

Only if recommendation is BET or LEAN.

State the maximum suggested percentage according to the bankroll table.

---

# Missing Data Rules

A new **BET** recommendation requires at minimum:

- Current score
- Current minute
- Bet side
- Total line
- Current odds

If recent pressure data is unavailable:

- Reduce confidence.

If market data is stale:

- PASS.

If match-state data conflicts between sources:

- PASS until resolved.

If an existing position is being managed but current odds are unavailable:

- HOLD / CASH OUT analysis may still be possible from match state and cash-out value, but explicitly flag the missing market comparison.

---

# Core Principles

1. Goal math before narrative.
2. Never confuse total goals already scored with goals still required.
3. Analyze both UNDER and OVER symmetrically.
4. Time decay becomes increasingly important after 70'.
5. Pressure trend matters more than raw possession.
6. xG velocity matters more than cumulative xG alone.
7. A goal resets momentum.
8. Recent goals do not guarantee future goals.
9. Panic is not evidence.
10. A likely winner is not automatically good value.
11. A lower-probability bet can still have value at the right price.
12. Tournament format can invalidate ordinary 90-minute assumptions.
13. Tail risk must describe the actual sequence that defeats the wager.
14. Protect bankroll before chasing opportunity.
15. When uncertain, PASS.

---

# Core Philosophy

> **We are not trying to predict the next goal. We are trying to determine whether the market has correctly priced the probability of the remaining goals.**

That is the foundation of the Unified Soccer Simulator v4.2.
