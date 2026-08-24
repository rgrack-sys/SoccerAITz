# Unified Soccer Simulator v4.3 — Canonical State

## Status

Portable source of truth for accepted v4.3 rules.

Detailed files:

- `skills/unified_soccer_simulator_v4_3_skill.md`
- `schemas/unified_soccer_simulator_v4_3_input_schema.json`
- `agents/socceraitz_agent_v4_3.md`

## Core philosophy

> We are not trying to predict the next goal. We are trying to determine whether the market has correctly priced the probability of the remaining goals.

Required hierarchy:

> **Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision**

Allowed decisions:

- BET
- LEAN
- HOLD
- PASS
- CASH OUT
- HEDGE

Default: PASS.

## Canonical rules

1. Goal Math is always first.
2. Support UNDER and OVER from 0.5 through 8.5.
3. Never confuse goals scored with goals still required.
4. Time decay matters increasingly after 70'.
5. Pressure Score and Pressure Momentum are separate.
6. Pressure trend matters more than raw possession.
7. xG velocity matters more than cumulative xG alone.
8. Reset Pressure Momentum after every goal.
9. One-goal Under vulnerability forces a 2–5 minute post-goal reassessment.
10. A harmless opponent does not make an Under safe if one team can score enough alone.
11. Panic is not evidence.
12. Goal clusters and tactical collapse increase Tail Risk.
13. Match context modifies scoring expectations.
14. Knockout / extra-time rules can invalidate normal 90-minute decay.
15. Monte Carlo is a required probability layer.
16. Monte Carlo does not override Goal Math, live-state logic, kill switches, or bad inputs.
17. Tail Risk must state the exact failure path.
18. Compare sportsbook probability with model probability to estimate edge.
19. Likely winner does not automatically mean good value.
20. Compare the full goal-line ladder when available.
21. The safest line is not automatically the best line.
22. Line movement triggers analysis; it does not replace analysis.
23. Kill-switch events force recomputation, not automatic exit.
24. Live visual information may improve execution timing only after the statistical case exists.
25. Low-latency viewing is a rare execution advantage, not a primary signal.
26. Stake sizing remains an open design issue.
27. No Martingale.
28. No chasing losses.
29. When uncertain, PASS.

## Pressure

Pressure Score:
- 0–2 Dormant
- 3–4 Low
- 5–6 Moderate
- 7–8 High
- 9–10 Extreme / chaos

Pressure Momentum:
- Cooling
- Stable
- Heating
- Explosion

## Post-Goal Vulnerability Rule

When an existing Under becomes one goal from losing:

- reset momentum
- ignore pre-goal momentum
- recompute time
- recompute attack quality
- recompute context and chaos
- observe first 2–5 post-goal minutes

Guidance:

- Cooling → HOLD
- Stable / unresolved → HOLD / LEAN CASH OUT
- Heating → CASH OUT or HEDGE
- Explosion → CASH OUT immediately if available

## Match archetypes

- Dead / Low Event
- Controlled Dominance
- One-Sided Assault
- Open / Transitional
- Chaos

## Monte Carlo

Placement:

> after Match Context / Chaos and before Market Sanity Check

Preferred outputs:

- P(1+ additional goals)
- P(2+ additional goals)
- P(3+ additional goals)
- P(4+ additional goals)
- selected-side probability
- final-total distribution
- probabilities across 0.5–8.5

Recommended simulations:

- 25,000 minimum
- 50,000 standard
- 100,000 when useful

## Kill switch

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

## Live visual execution note

Visual observation does not create a wager.

It may accelerate an already-supported wager if:

- statistical thesis exists
- price remains acceptable
- feed is genuinely low latency
- defense visibly loses structure

> Stats establish edge → market determines value → live observation may improve timing.

## Open design issue — stake sizing

Inherited v4.2 confidence sizing remains provisional.

Future sizing should consider:

- estimated edge
- confidence
- price
- variance
- goal cushion
- time remaining
- bankroll
- correlated exposure
- current open positions

Do not silently equate confidence with stake size.

## Version

**Unified Soccer Simulator v4.3**
