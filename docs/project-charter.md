# SoccerAITz — project charter (intake, 2026-11-21)

**Project classification:** existing repository, not a new repo.
**Accountable human:** repository owner; individual approvals must be recorded.
**Business outcome:** provide disciplined, evidence-first, reproducible soccer match-state and sportsbook value analysis through ChatGPT, with a governed Python agent intended to run on Hugo-1.

## In scope (target, not implemented)

- Preserve v4.2/v4.3 accepted behavioral canon and its provenance.
- Normalize timestamped match snapshots and full goal-line market ladders from replaceable sources.
- Compute deterministic Goal Math, event-triggered state resets and safeguards; persist match/position state outside model sessions.
- Add a reproducible, calibrated Monte Carlo probability layer, then compare model probability and vig-aware sportsbook price.
- Return traceable recommendations or PASS, with human approval controls and independent Critic review.

## Explicit exclusions

- No live sportsbook execution, auto-betting, Martingale or loss-chasing.
- No unvalidated Rule 29 psychological probability adjustment.
- No invented calibration, dataset, test completion, low-latency feed, or Hugo-1 connectivity.

## M0 success definition

A pure goal-math function preserves Under/Over symmetry and settled thresholds for half-goal lines 0.5–8.5, rejects invalid inputs, and passes offline tests. No scoring probability or recommendation is produced. Owner acceptance and merge are separate future gates.
