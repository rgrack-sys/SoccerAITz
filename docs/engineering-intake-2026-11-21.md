# SoccerAITz — evidence-first engineering intake (2026-11-21)

## Sources and scope

- Existing repository `rgrack-sys/SoccerAITz`, `main` at `427adea53cd3ab5a71586dad26fad3fa5ab5f612` (inspected 2026-11-21).
- Preserved v4.2 Under/Over simulator and legacy Under skill; v4.3 canonical state, simulator skill, agent specification, input JSON Schema and shared Git workflow.
- Issue #1, *Engineering checkpoint: provisional Rule 29 psychological context backtest*, inspected as open with no comments on 2026-11-21.
- Project Bootstrap `standards/project-standard-v0.4.md` and `docs/project-onboarding-protocol.md` inspected.
- Only supplied file mounted for this intake: `Unified Soccer Simulator v4.2.txt` (580 bytes), containing a v4.3 Monte Carlo note. The **full Engineering Handoff** named by the owner was absent. No claim of full rule-by-rule handoff reconciliation is justified.

## Evidence classification

| Topic | Existing specification | Verified implementation on discovery `main` | M0 change / status |
|---|---|---|---|
| Goal Math for Over and Under 0.5–8.5 | Explicit v4.2/v4.3 formulas and reference tables | None | Pure Python candidate + offline tests |
| Time remaining / stoppage / extra time | Specified | None | Not included |
| xG quality and 5–10 minute trend | Specified | None | Not included |
| Goal-triggered momentum reset and Under vulnerability window | Specified | None | Not included |
| Archetypes, context, chaos, kill switches | Specified | None | Not included |
| 25k/50k/100k Monte Carlo and full ladder | Required layer, calibration ongoing | None | No simulation or claimed calibration |
| American-odds conversion, edge, tail risk, recommendation | Specified | None | No pricing or recommendations |
| Positions, cash-out, hedges, bankroll discipline | Specified; stake sizing provisional | None | No stake or execution code |
| Live feed, sequential store, event notifications | Agent specification only | None | No runtime or external action |
| Rule 29 inherited psychology | Issue #1 provisional hypothesis | None | Disabled; no multiplier |
| Independent Critic / owner acceptance / CI / Hugo-1 | Required by governance | No proof in inspected repo | Pending; isolated test is not qualification |

## Conflicts, ambiguities, and unresolved canon

1. **Rule number collision**: numbered v4.3 Rule 29 = “When uncertain, PASS”; Issue #1 Rule 29 = “Collective Psychological Context.” Neither is deleted or relabeled unilaterally. Stable rule identifiers are a proposed owner decision.
2. **Confidence scale**: legacy `live_soccer_under_skill.md` uses 0–100; v4.2/v4.3 use 1–10. M0 does not emit confidence. New implementation should follow the current v4.3 specification subject to owner confirmation of any historical exceptions.
3. **Stake sizing**: v4.3 records inherited percentages as provisional and warns not to equate confidence with stake. M0 does not size wagers.
4. **Probability quality**: the simulation count is a design recommendation, not evidence of statistical validity. No calibrated event rate, backtest, out-of-sample score, or Rule 29 effect exists in inspected implementation.
5. **Input schema vs decision sufficiency**: v4.3 JSON Schema requires a nonempty `markets` array but allows a line with missing odds and null timestamps. Thus schema-valid input can still be unusable for BET. A future evidence gate must separately enforce minimum recent match/market data and fail closed.
6. **Full owner handoff missing**: cannot assert all historical accepted rules are captured. Existing versions remain untouched, and new work is limited to the uncontested deterministic threshold.

## Accepted rule preservation

Existing v4.2, v4.3, agent and legacy skill files are deliberately not modified by M0. Explicitly retained principles include Goal Math first; Over/Under symmetry; conservative PASS; 70'+ time decay; attack quality vs possession; recent pressure trend and score separate; goal-reset; post-goal one-goal Under reassessment; one-sided scoring capability; panic not evidence; clustered tail risk; contextual incentives and extra-time market scope; Monte Carlo after match context/chaos but before book sanity; implied odds versus model edge; full line ladder; kill-switch recompute rather than automatic exit; cash-out/hedge based on evidence; line movements as triggers; restricted low-latency observation; no Martingale, loss chasing or unapproved stake sizing.

## Smallest verifiable implementation milestone — M0

Build a pure deterministic function with explicit scores, side, and half-goal market line. It must reject malformed inputs and state whether the threshold is still live or already crossed; if live, return only the side-specific additional-goal threshold. It makes **no** future probability, advice, or market execution claim.

Offline qualification: six `unittest` methods including all 216 combinations of 9 goal lines × 12 goals × 2 sides, plus examples and malformed inputs. These tests were run in an isolated Python 3.13.5 environment, not on Hugo-1. See PR receipt; no cross-platform CI or independent Critic has been completed.

## Explicit gates before subsequent milestones

1. Obtain exact full Engineering Handoff; compare source-by-source and record missing/approved semantics.
2. Resolve rule IDs and historical confidence-scale policy with owner approval without erasing legacy versions.
3. Build freshness/conflict semantics and replayable event state before any agentic recommendation.
4. Establish verifiable seed/model version, datasets, calibration, chronologically held-out evaluation and independent review before claiming simulated probabilities support betting edge.
5. Keep Rule 29 numerical effects **disabled** until Issue #1 acceptance criteria and owner approval.
6. Prove Hugo-1 identity, repository SHA and round-trip execution before calling it deployed or integrated.
7. Enforce separate owner authorization for merges, financial external actions and any production betting capability.
