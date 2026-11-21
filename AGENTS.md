# SoccerAITz engineering instructions

Use the requirements in `rgrack-sys/project-bootstrap/standards/project-standard-v0.4.md` and the existing SoccerAITz versioned canonical documents. Preserve previous canonical versions and never silently renumber accepted rules.

- Python domain calculations must be deterministic and independently testable offline.
- Separate **specified**, **implemented**, **locally tested**, **CI-qualified**, **Hugo-1 verified**, **critic-reviewed**, and **owner-accepted** states.
- Capture provenance, freshness, completeness, and contradictory inputs before any recommendation. Fail closed to PASS in future decision components.
- Use event-driven triggers, persisted state, provider-replaceable adapters, and no invented observations or Monte Carlo calibration.
- Rule 29 in Issue #1 (Collective Psychological Context) is provisional. No goal-rate multiplier, probability adjustment, or production effect until backtest, independent Critic, and human approval.
- No wagering API integration or automatic order placement without a **separate explicit execution policy** and human authorization.
- Reviewable feature-branch / PR only; no force push, main merge, release, deployment, or secret commits without the required gate.
- Do not claim to have executed on Hugo-1 unless a Hugo-1 execution receipt was actually produced.
- Keep a living inventory of autonomous components when such components are introduced; recording absent capability is preferable to inventing implementation.
- Exact-final-SHA cross-platform acceptance matrix follows Project Bootstrap v0.4 cost-aware CI rules, not every draft commit.
