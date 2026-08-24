# Live Soccer Under Model Skill

## Purpose

Analyze an in-play soccer match for live total-goals opportunities, with a primary focus on **Under** markets.

This skill does **not** place wagers. It evaluates the match state, current sportsbook prices, risk, and whether the market appears mispriced.

The model's core objective is:

> Detect whether the market is overpricing the probability of future goals.

The default action is **PASS** when the available evidence is incomplete, contradictory, or insufficiently strong.

---

# 1. Required Inputs

The calling agent should provide as much of the following as possible.

## Match state

- Competition / league
- Teams
- Current score
- Current minute
- Stoppage time if known
- First half / second half / extra time
- Whether extra time is possible
- Knockout / group / league context
- Red cards
- Important injuries
- VAR events
- Penalty events

## Match statistics

For each team when available:

- Possession
- xG
- Total shots
- Shots on target
- Big chances
- Corners
- Goalkeeper saves
- Fouls
- Yellow cards

## Market data

For each available total-goals line:

- Goal line
- Over price
- Under price

Example:

```json
{
  "line": 4.5,
  "over": 285,
  "under": -375
}
```

Optional:

- Current cash-out value
- Original wager price
- Original stake
- Current open position

---

# 2. Mandatory Step 1 — Goal Math

Before analyzing momentum, xG, odds, or match narrative, calculate exactly how many **additional goals** are required for the Under to lose.

Examples:

| Score | Current Goals | Bet | Additional Goals Needed to Lose |
|---|---:|---:|---:|
| 0-0 | 0 | Under 2.5 | 3 |
| 1-0 | 1 | Under 2.5 | 2 |
| 2-0 | 2 | Under 3.5 | 2 |
| 2-1 | 3 | Under 4.5 | 2 |
| 3-0 | 3 | Under 4.5 | 2 |
| 3-1 | 4 | Under 4.5 | 1 |

Formula:

```text
additional_goals_to_lose = floor(total_line - current_goals) + 1
```

For standard half-goal lines, this simplifies to:

```text
additional_goals_to_lose = ceil(total_line - current_goals)
```

Never skip this step.

A model recommendation is invalid if the goal math is wrong.

---

# 3. Mandatory Step 2 — Effective Time Remaining

Estimate remaining playable time.

Consider:

- Current minute
- Expected stoppage time
- VAR delays
- Injuries
- Substitutions
- Tournament rules
- Extra time if the selected market includes it

The importance of time decay increases sharply after 70 minutes.

General weighting:

- 0–45: Low
- 46–60: Moderate
- 61–70: Increasing
- 71–80: High
- 81–90: Very high
- 90+: Extreme

Do not treat 3-0 at 55' as equivalent to 3-0 at 81'.

---

# 4. Match Archetype Classification

Classify the match before making a recommendation.

## A. Dead / Low Event

Typical indicators:

- Low xG
- Low shot volume
- Few big chances
- Slow xG accumulation
- Low corner pressure
- Few dangerous transitions

Under-friendly.

## B. Controlled Dominance

One team controls territory and possession but does not generate repeated dangerous chances.

Typical indicators:

- Large possession edge
- Moderate shot edge
- xG not accelerating
- Losing team offers little counter-threat

Often Under-friendly after the leader is established.

## C. One-Sided Assault

One team is producing repeated high-quality chances.

Typical indicators:

- Large xG gap
- Multiple big chances
- High shot rate
- High save count
- Sustained corners / box entries

Dangerous for Unders even if the trailing team is harmless.

## D. Open / Transitional

Both teams are generating attacks.

Typical indicators:

- Both teams accumulating xG
- End-to-end play
- Multiple big chances
- High shot frequency
- Frequent counters

Under-hostile.

## E. Chaos

Any combination of:

- Red cards
- Penalties
- Repeated VAR
- Defensive collapse
- Multiple goals in a short period
- Tactical abandonment
- Late desperation
- Tournament game state forcing attacks

Usually PASS unless the goal cushion is extremely large.

---

# 5. Pressure Momentum

Evaluate whether attacking pressure is **accelerating, stable, or fading**.

Prefer change over static totals.

Useful comparisons:

- xG over the last 5–15 minutes
- Shots added over the last 5–15 minutes
- Big chances added
- Corners added
- Saves forced
- Possession shift
- Tactical state after a goal

## Pressure score concept

Rate 0–10.

Suggested interpretation:

- 0–2: dormant
- 3–4: low
- 5–6: moderate
- 7–8: high
- 9–10: extreme / chaos

Do not infer pressure merely because a goal was just scored.

---

# 6. Panic Override / Data-First Rule

A sudden adverse event does not automatically invalidate an Under.

After:

- a goal
- penalty
- VAR decision
- red card
- big chance
- near miss

immediately perform:

1. Recalculate goal math.
2. Recalculate time remaining.
3. Reassess current pressure.
4. Compare current pressure with pressure before the event.
5. Determine whether the event changed the underlying scoring process or was isolated.

Important principle:

> Panic is not evidence.

Example:

An Under 4.5 position at 3-0 still requires **two additional goals** to lose.

If the score becomes 3-0 at 55', risk may still be significant.

If it remains 3-0 at 81' while xG and shot pressure have flattened, the same scoreboard can represent a much safer position.

---

# 7. Goal Burst / Cluster Risk

Goals are not fully independent.

Increase caution after:

- two goals within ~10 minutes
- a tactical collapse
- a red card
- a team chasing aggressively
- a goalkeeper injury
- repeated high-quality chances
- late game state where both teams benefit from attacking

A recent goal should increase short-term attention, but must not automatically be extrapolated into another goal.

---

# 8. Score-State Effects

## Team leading by 1

Trailing team usually remains aggressive.

Higher late-goal risk.

## Team leading by 2

Game may either:

- stabilize, or
- become open if the trailing team abandons structure.

Require pressure data.

## Team leading by 3+

Trailing team may psychologically or tactically collapse.

But the leading team may also reduce intensity.

Do not assume continued scoring solely from dominance.

---

# 9. Tournament / Knockout Adjustment

If the match is knockout:

- identify whether the market includes extra time
- identify whether the current score would produce extra time
- do not apply normal 90-minute decay if another 30 minutes may be played

When tied late in knockout play:

> Survive stoppage and reassess pace in extra time.

Third-place games, friendlies, and low-stakes matches may behave differently from elimination games.

Treat unusual incentive structures as an archetype modifier.

---

# 10. Market Interpretation

Convert American odds to approximate implied probability when useful.

For negative odds:

```text
p = abs(odds) / (abs(odds) + 100)
```

For positive odds:

```text
p = 100 / (odds + 100)
```

Examples:

- -200 ≈ 66.7%
- -300 = 75.0%
- -400 = 80.0%
- -500 ≈ 83.3%
- -1000 ≈ 90.9%

Do not treat sportsbook implied probability as true probability because of vig.

The question is:

> Is our estimated probability materially higher than the book's price implies?

---

# 11. Price Discipline

A bet can be likely to win and still be a bad wager.

The skill must distinguish:

- probability of winning
- price / value
- bankroll exposure

A heavy favorite Under is acceptable only when the remaining goal burden, time decay, and pressure state justify the price.

Do not recommend a wager merely because it is "almost certain."

---

# 12. Position Management

If an Under is already held, choose among:

- HOLD
- CASH OUT
- HEDGE

## HOLD

Use when:

- goal math remains favorable
- time decay is working
- pressure is flat or falling
- no major structural risk has appeared
- cash-out discount is excessive

## CASH OUT

Use when:

- a red card materially changes the game
- repeated big chances emerge
- xG accelerates rapidly
- tactical structure collapses
- another goal reduces the remaining cushion to one
- the cash-out offer reasonably compensates for the remaining risk

## HEDGE

Use only when:

- a liquid opposite market exists
- risk can be materially reduced without destroying expected value
- the hedge is preferable to the available cash-out

Do not cash out simply because the wager feels uncomfortable.

---

# 13. Kill Switch

Immediately downgrade to PASS / CASH OUT review when any of these occur:

- Red card
- Penalty
- VAR penalty review
- Goalkeeper injury
- Two goals in a short interval
- Sudden jump in combined xG
- Multiple big chances in a short interval
- Match enters obvious end-to-end chaos
- Extra time becomes likely and the market includes extra time
- Input data becomes stale or contradictory

A kill switch does not automatically mean exit.

It means **stop normal reasoning and recompute the match from scratch.**

---

# 14. Confidence

Return confidence from 0–100.

Suggested interpretation:

- 0–49: PASS
- 50–59: weak lean
- 60–69: LEAN
- 70–79: playable
- 80–89: strong
- 90+: exceptional, rare

Confidence should fall when inputs are incomplete.

---

# 15. Allowed Recommendations

The final recommendation must be exactly one of:

- BET
- LEAN
- HOLD
- PASS
- CASH OUT
- HEDGE

Default to PASS.

---

# 16. Output Format

Return a compact structured result.

```json
{
  "recommendation": "HOLD",
  "confidence": 84,
  "match_archetype": "Controlled Dominance",
  "pressure_score": 3,
  "pressure_trend": "falling",
  "current_goals": 3,
  "line": 4.5,
  "additional_goals_to_lose": 2,
  "effective_minutes_remaining": 12,
  "risk_flags": [],
  "market_price": -420,
  "estimated_under_probability": 0.88,
  "value_assessment": "small positive edge",
  "reasoning_summary": "Two additional goals are required to defeat the Under. Time decay is now dominant, Tottenham remains low threat, and recent xG accumulation has slowed. The adverse third goal increased emotional pressure more than statistical risk.",
  "next_trigger": "Recompute immediately after any goal, penalty, red card, VAR penalty review, or major xG acceleration."
}
```

---

# 17. Missing Data Rule

If any of the following are unknown:

- score
- minute
- total line
- current odds

the model cannot issue BET.

If pressure data is missing, confidence must be reduced.

If the data is contradictory or stale:

```text
recommendation = PASS
```

---

# 18. Core Behavioral Rules

1. Goal math before narrative.
2. Time decay matters more as the match gets late.
3. Pressure trend matters more than raw possession.
4. xG accumulation matters more than total xG alone.
5. Recent goals do not guarantee future goals.
6. Panic is not evidence.
7. A likely winner is not automatically a good price.
8. Tournament format can invalidate ordinary late-game assumptions.
9. Protect bankroll before chasing opportunity.
10. When uncertain, PASS.

---

# 19. Agent Calling Guidance

The calling agent should:

1. Gather a fresh match snapshot.
2. Gather fresh sportsbook totals.
3. Normalize the data.
4. Call this skill.
5. Present the recommendation.
6. Re-run the skill after material state changes.

Material state changes include:

- goal
- red card
- penalty
- VAR
- halftime
- 70'
- 80'
- 85'
- start of stoppage
- large odds move
- sharp xG / chance acceleration

The skill should remain deterministic and analytical.

The agent is responsible for:

- data collection
- repeated monitoring
- user notifications
- maintaining match history
- comparing sequential snapshots
