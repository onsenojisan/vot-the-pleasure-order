# Amendment 2 — Data Preflight

Status: **2B necessary-condition check; not a power or identifiability result**
Date: 2026-08-15
Required by: [Amendment 2A](AMENDMENT_2A_GOVERNANCE_RULES.md)
Recorded in: [Amendment 2B](AMENDMENT_2B_EXECUTION_ANNEX.md)

## Purpose

This preflight prevents a simulation-ready model specification from being
mistaken for a runnable empirical study. It checks whether a proposed dataset
declares the observations and prospective commitments that Amendment 2 needs
before fitting begins.

Passing this check never returns `RUNNABLE`. The strongest result is
`NECESSARY_CONDITIONS_MET_NOT_SUFFICIENT`, because sample-size adequacy,
parameter identifiability, calibration power and model convergence still have
to be established by the locked simulation protocol.

## Two Observations That Must Stay Separate

The data manifest gives two variables different causal roles:

- `agent_action` (`a_t`) is an action selected by the observed agent, or a
  prospectively justified action proxy. It is required to adjudicate the
  expected-free-energy policy component of D5.
- `external_forcing` (`u_t`) is an exogenous perturbation or control variable.
  It is required to traverse the structural domain in both directions and test
  fold versus non-fold dynamics.

One recorded variable cannot be assigned both roles. If action is absent, D5 is
`INCONCLUSIVE`; if exogenous bidirectional forcing is absent, the two-sided
structure comparison is `INCONCLUSIVE`. Neither absence is evidence for VOT.

## Manifest And Command

Copy [`simulations/amendment2_data_manifest.template.json`](simulations/amendment2_data_manifest.template.json),
replace every `UNSET` or `null`, and run:

```powershell
python simulations/preflight_amendment2.py path/to/manifest.json
```

Use `--require-necessary-conditions` in automation. It exits with status `2`
unless every hard necessary condition is declared and no required decision is
left unset. Malformed manifests exit with status `1`.

## Result Meanings

| Status | Meaning |
|---|---|
| `HARD_BLOCKED` | An explicit dataset property prevents at least one Amendment 2 comparison. |
| `INCOMPLETE` | No explicit hard blocker was declared, but required mappings or model commitments remain unset. |
| `NECESSARY_CONDITIONS_MET_NOT_SUFFICIENT` | The declared inputs clear this preflight only; simulation and identifiability may still fail. |

The report lists the scope of every blocker (`D5`, `STRUCTURE`, `P3`, `BOTH` or
`RATIFICATION`). An absent endpoint blocks P3, not the D5 or structure comparison
by itself. A target outcome inspected before the prospective freeze blocks
ratification for that target, although the code may still be developed and
tested on synthetic data.
