# SoccerAITz — decisions and unresolved canon (2026-11-21)

| ID | Status | Decision / question | Evidence |
|---|---|---|---|
| SA-001 | Accepted in existing repo | v4.3 is the latest canonical version **committed to the inspected repository**, not proof that later accepted handoffs or v4.4 do not exist. Preserve all existing files without overwriting them. | `canonical/unified_soccer_v4_3_canonical_state.md`; `skills/` |
| SA-002 | Accepted in existing repo | Required order: Goal Math → live match state → Monte Carlo probability → sportsbook probability → edge → decision. Default PASS for uncertain, stale, contradictory state. | v4.3 canon and skill |
| SA-003 | Proposed; locally tested; owner acceptance pending | Implement only pure, exact Goal Math for both sides and half-goal totals 0.5–8.5; no recommendation. | v4.3 skill Step 1; this feature change |
| SA-004 | Provisional, disabled | Issue #1 Rule 29 psychological context is an unvalidated hypothesis, not a scoring multiplier. | https://github.com/rgrack-sys/SoccerAITz/issues/1 |
| SA-005 | Naming conflict, unresolved | v4.3 numbered rule 29 means “When uncertain, PASS”; Issue #1 Rule 29 means “Collective Psychological Context.” Preserve both; propose stable IDs only after owner approval. | v4.3 numbered canon; Issue #1 |
| SA-006 | Unresolved | The full engineering handoff named in the request was not present; only a 580-byte v4.3 Monte Carlo note was mounted. Full rule-by-rule reconciliation is incomplete. | Intake attachment, 2026-11-21 |
| SA-007 | Unresolved | Legacy Under skill uses confidence 0–100, while v4.2/v4.3 use 10-point confidence; M0 does not choose a confidence scale; a later full handoff may supersede repository-era guidance. | `skills/live_soccer_under_skill.md`; v4.2/4.3 |
| SA-008 | Provisional | Inherited confidence-to-stake sizing is not validated; no executable stake sizing in M0. | v4.3 canon, bankroll guidance |
| SA-009 | Unimplemented | Monte Carlo is formally required, but rate model, calibration, backtest, randomness control, provider inputs and probability quality remain unverified. | v4.3 skill Step 11 |
| SA-010 | Unimplemented | Event-driven Hugo-1 agent, persistence, CI matrix, independently reviewed behavior and ChatGPT-to-Hugo-1 link are future engineering work. | Current repository tree and Project Bootstrap v0.4 |

**Gate:** This file records preexisting canon and a proposed implementation. No unreviewed rule renumbering, calibration adjustment, deployment, or production betting authority is conferred by this document.
