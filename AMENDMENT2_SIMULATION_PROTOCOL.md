# Amendment 2 — Two-Sided Calibration Protocol

Status: **2B simulation-design draft; no target-specific numbers are in force**
Date: 2026-08-15
Governed by: [Amendment 2A](AMENDMENT_2A_GOVERNANCE_RULES.md)
To be completed through: [Amendment 2B](AMENDMENT_2B_EXECUTION_ANNEX.md)

## Purpose

This protocol determines whether a proposed D4/D5 study can distinguish fold
and non-fold processes in both directions. It prevents the ratification block
from being filled with conventional numbers that were never calibrated to the
actual design.

The protocol does not itself supply a fold model, an active-inference model or
a final numeric commitment. Those equations, priors and fitting programs must
be frozen first. Until then, this file is a runnable reporting contract, not a
power result.

Before treating a target dataset as eligible, complete the
[Amendment 2 Data Preflight](AMENDMENT2_DATA_PREFLIGHT.md). Clearing that check
establishes necessary observations only; it is not a power or identifiability
result.

## Quantities To Estimate

For every frozen data-generating scenario, estimate these unconditional rates:

| Truth | Correct disposition | Opposite error | Other dispositions |
|---|---|---|---|
| `FOLD` | `FOLD` | `NO_FOLD` = false-non-fold | `TIE`, `UNDERPOWERED`, `UNIDENTIFIED` |
| `NON_FOLD` | `NO_FOLD` | `FOLD` = false-fold | `TIE`, `UNDERPOWERED`, `UNIDENTIFIED` |

Power is the probability of the correct disposition over **all** simulated
replicates. Underpowered, unidentified and tied replicates stay in the
denominator. Conditioning on adjudicable replicates would make a weak design
look stronger by discarding its failures.

Report per scenario:

- correct-disposition rate and 95% Wilson interval;
- opposite-error rate and 95% Wilson interval;
- inconclusive rate;
- worst-case Monte Carlo standard error `0.5 / sqrt(n)`;
- winning model and score-gap distribution, when supplied by the fitting code.

No pooled average may rescue a failing scenario. Ratification uses the
worst-case result across the declared validation scenarios.

## Scenario Registry

Each scenario receives an immutable ID and freezes. The current candidate
registry and R3–R6 equations are in the
[D5 Active-Inference Rival Specification](D5_ACTIVE_INFERENCE_RIVAL_SPEC.md).

1. truth family and exact data-generating equations;
2. people/cases, observations per decline and recovery arm, and time unit;
3. control-variable range and threshold traversal in both directions;
4. process noise, observation noise, autocorrelation and heterogeneity;
5. missingness, informative dropout and irregular timing;
6. perturbation timing and external forcing;
7. parameter-sharing structure across people and arms;
8. endpoint observation model where P3 is simulated;
9. fitting failures that count as `UNIDENTIFIED`;
10. the random-number seed registry and software commit.

The registry must include, at minimum:

- the fitted `R0` baseline suite, which need not be a separate data-generating
  scenario;
- multiple fold/hysteresis scenarios, including weak and narrow folds;
- smooth changing-equilibrium deterioration and recovery;
- externally forced jumps;
- non-bifurcation state switching;
- every explicit estimable D5 rival `R3–R6` once its generative model exists;
- boundary cases with weak control coverage, noise and missingness.

A label such as “active inference” is inadmissible without the generative
model, objective, priors, variable mapping and fitting code required by
Amendment 2A and frozen in the study's Amendment 2B annex.

## Calibration And Locked Validation

Use two independently seeded scenario sets.

### Calibration set

Sweep candidate scoring rules and meaningful win/tie margins. This set may be
used to choose a margin, but not to report final power.

### Locked validation set

Freeze before running the chosen rule. No threshold, margin, model, prior or
failure disposition may change after these results are visible. Only this set
can populate the ratification block.

If the chosen rule fails validation, the design remains unratified. A revised
rule requires a new locked validation set and a new version; it may not reuse
the failed set as if still blinded.

## Candidate Acceptance Targets — Not Yet Ratified

The following are starting targets for the simulation, not commitments already
in force:

- lower 95% bound for fold power: at least `0.80`;
- lower 95% bound for non-fold power: at least `0.80`;
- upper 95% bound for false-fold: at most `0.05`;
- upper 95% bound for false-non-fold: at most `0.05`;
- worst-case Monte Carlo standard error: at most `0.01`;
- recommended minimum: `5,000` replicates per scenario.

These targets must be author-ratified before the locked validation run. The
meaningful win/tie margin cannot be named until the proper scoring rule and its
units are frozen. It is selected on the calibration set and then tested once on
the locked set.

## Result File Contract

The fitting pipeline writes UTF-8 CSV with one row per replicate:

```text
scenario_id,truth,replicate,disposition,score_gap,winning_model
fold_weak,FOLD,1,FOLD,1.82,VOT_FOLD
smooth_high_noise,NON_FOLD,1,NO_FOLD,-2.14,R1_SMOOTH
```

Required fields are `scenario_id`, `truth`, `replicate` and `disposition`.
Allowed dispositions are `FOLD`, `NO_FOLD`, `TIE`, `UNDERPOWERED` and
`UNIDENTIFIED`. `score_gap` and `winning_model` are optional audit fields.

Summarize a result file with:

```powershell
python simulations/calibrate_amendment2.py results.csv --output calibration_report.json
```

A method-development result file can now be produced with the reference
harness:

```powershell
python simulations/amendment2_reference_harness.py `
  simulations/amendment2_scenarios.v0.json `
  --output reference_results.csv `
  --audit-output reference_audit.json
```

This does not fill the ratification block. The reference harness implements the
author-selected shared-fold VOT only as a scalar observed-state approximation,
uses a one-step risk-only policy approximation, and approximates hierarchical
R6 with ridge partial pooling. Its `disposition` and
`d5_reference_disposition` columns exercise structure and absorption result
contracts for calibration only; every row separately states
`verdict_authorized=False`.

Use `--require-pass` only after the acceptance targets have been ratified. The
command then exits non-zero if any scenario fails.

## Ratification Rule

The ratification block may be filled only when all are public and immutable:

1. scenario registry;
2. simulation and model-fitting code;
3. calibration rule and chosen margin;
4. locked validation seed commitment;
5. locked validation result file and generated summary;
6. code/deposit identifier preceding target-data inspection.

An unidentifiable required strong rival remains `INCONCLUSIVE`. Simulation
cannot convert a missing D5 model into evidence for VOT.
