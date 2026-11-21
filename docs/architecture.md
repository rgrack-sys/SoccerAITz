# SoccerAITz — architecture (proposed target vs verified M0)

## Proposed target (not deployed)

ChatGPT conversation → explicitly structured query → Hugo-1 Python orchestrator → evidence/sufficiency gate → match/market source adapters → append-only, timestamped snapshots → deterministic match state / Goal Math → calibrated Monte Carlo layer → price/vig and risk assessment → reviewable recommendation → ChatGPT response.

Events (goal, red card, VAR/penalty, keeper injury, pressure acceleration, time checkpoints, price discontinuity, data conflict/staleness) should trigger bounded re-evaluation rather than AI polling. Ordinary code should collect, validate, filter, compute, and persist; AI is invoked only when documented reasoning is necessary. Idempotency keys, time ordering, post-goal baseline reset, correction handling, re-entry, and source disagreement policies remain **design work**, not verified features.

## Verified M0 capability

`src/socceraitz/goal_math.py` is a side-effect-free pure calculation accepting explicit scores, bet side, and a validated half-goal line. It produces current total, market threshold, and already-crossed status. It has no network, secrets, time-dependent behavior, model calls, state, Rule 29 factor, market pricing, or betting action.

## Runtime and authority boundaries

- **Application runtime target:** Hugo-1 Linux, not yet connected or verified for SoccerAITz.
- **Model runtime:** external ChatGPT service, acting as conversational interface; no proven interface-to-Hugo-1 path in this milestone.
- **Persistent state target:** undecided, to be verified outside ephemeral chats.
- **Test runtime:** isolated local Python environment and, later, exact-final-SHA CI matrix; not proof of Hugo-1 execution.
- **External actions:** no wager placement; consequential writes require separately authorized human approval.

## Future engineering gates

1. M0 goal-math acceptance and canonical reconciliation (full handoff still missing).
2. Timestamped typed snapshot/market contract and stale/conflicting-data PASS gates.
3. Event journal, idempotent trigger detector, goal reset and replay fixtures.
4. Deterministic baseline and simulation with seed, reproducibility and calibration evidence.
5. Market comparison, position-management candidate logic and independent review.
6. Local Hugo-1 round-trip receipt and guarded ChatGPT interface; no automated wagering.
