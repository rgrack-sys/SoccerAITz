# SoccerAITz

SoccerAITz is being migrated from a versioned live-soccer analysis **specification** into a governed, event-driven Python decision-support agent. The source specifications are preserved unchanged under `canonical/`, `skills/`, `agents/`, and `schemas/`.

**Milestone M0 is intentionally narrow:** deterministic Goal Math only. It does not estimate goal probabilities, recommend wagers, fetch live feeds, schedule tasks, run Monte Carlo, modify Rule 29, or place bets.

## Test offline (Linux Bash / Windows PowerShell)

From the repository root, with Python 3.10 or later:

Linux Bash:
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Windows PowerShell:
```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
Remove-Item Env:PYTHONPATH
```

## Evidence and governance

- [Engineering intake and reconciliation](docs/engineering-intake-2026-11-21.md)
- [Project charter](docs/project-charter.md)
- [Architecture: target vs as-built](docs/architecture.md)
- [Open decisions and gates](docs/decisions.md)
- [Current verification status](docs/current-status.md)
- [Rule 29 deferred checkpoint](https://github.com/rgrack-sys/SoccerAITz/issues/1)

No automated betting execution is authorized. No numerical Rule 29 adjustment is enabled. The full engineering handoff named in the initiating request was not available in the intake environment; completing its exact reconciliation remains open.
