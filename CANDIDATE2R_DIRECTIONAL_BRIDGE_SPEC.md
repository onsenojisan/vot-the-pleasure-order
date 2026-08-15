# Candidate 2R — Directional Change / Rate Bridge Specification

Status: **design contract; not preregistered and not yet runnable**
Date: 2026-08-15
Claim level: prospective change/rate hypothesis only

## Purpose

Candidate 2L predicts an adjusted future external Omega-related level. It is a
useful auxiliary prediction study, but it does not estimate `dOmega/dtau` and
cannot validate a directional bridge. Candidate 2R is the separate route for
that claim.

Candidate 2R asks:

> Does a predeclared local `DeltaC1` input, together with independently measured
> bridge-support variables, predict later change or rate in an external
> Omega-related endpoint beyond its baseline, simple dynamics and explicit rival
> models?

No causal verb is licensed by this observational question.

## Primary Estimand

The study must choose one primary estimand before collection.

### Change form

```text
Y_Omega_change = Y_Omega(T3) - Y_Omega(T0)
```

The model predicts `Y_Omega(T3)` with `Y_Omega(T0)` included as a mandatory
baseline. Reporting the raw change score is permitted, but baseline-adjusted
future level is the primary analysis unless a different estimator is frozen with
a measurement-error justification.

### Rate form

```text
Y_Omega_rate = slope_tau(Y_Omega(T2a), ..., Y_Omega(T3))
```

The time unit, minimum number of external observations, slope model and handling
of nonlinear trajectories must be frozen. A two-time-point difference is change,
not a rate.

Only the selected form is confirmatory. The other is secondary.

## Causal Extension

Causal wording requires a separate intervention estimand:

```text
DeltaOmega(a, a0)
  = E[Y_Omega(T3) | do(a)] - E[Y_Omega(T3) | do(a0)]
```

`a0`, population, assignment mechanism, horizon, missing-data rule and analysis
must be frozen before data. A population arm contrast does not license an
individual claim that the outcome would not have occurred without treatment.
Without randomization or a defensible identification strategy, Candidate 2R
remains predictive.

## Required Windows And Measures

| Window | Required role |
|---|---|
| `T0` | external `Y_Omega` baseline and pre-input state |
| `T1` | frozen `DeltaC1` input |
| `T2` | persistence, corrective update, continuity, future-option preservation and harmful-order gate |
| `T3` | independent external endpoint observations for change or rate |

Rules:

- endpoint and predictor streams are item/feature-disjoint;
- `T1/T2` do not overlap the `T3` outcome window;
- endpoint observations cannot define inclusion, thresholds or predictors;
- `DeltaC1`, support variables and the harmful-order gate are frozen before
  collection;
- baseline endpoint, missingness and informative-dropout handling are mandatory;
- measurement invariance across `T0–T3` is tested or its failure makes the result
  inconclusive.

## Required Baselines And Rivals

Candidate 2R must beat:

- `Y_Omega(T0)` alone;
- `DeltaC1` alone;
- Future Option Preservation alone;
- mean, trend, variance, autoregression and generic recovery;
- domain-standard prognostic variables;
- ESM-derived and static psychological-flexibility baselines under the disjoint
  allocation already required by the Bridge Specification;
- the explicit FEP / active-inference rival family applicable to the selected
  endpoint;
- a model without the bridge interaction / gate.

All margins and scoring rules are frozen before outcome inspection.

## Pass, Fail And Inconclusive

### Bounded pass

The preregistered bridge predicts external change or rate beyond every required
baseline by the frozen margin, behaves correctly in harmful-order cases, and
reproduces in holdout or preregistered replication.

Allowed wording:

> In domain D, the frozen Candidate 2R predictor added prospective information
> about the independent external Omega-related change/rate endpoint beyond its
> baseline and the predeclared rival family.

### Fail

The baseline outcome, Future Option Preservation, simple dynamics or a rival
model matches or beats Candidate 2R; the sign is wrong; harmful-order cases are
misclassified; or the increment fails to reproduce.

Required wording:

> This operational directional bridge was not supported in the tested domain.
> VOT remains a two-layer framework for this bridge.

### Inconclusive

Endpoint independence, temporal separation, measurement invariance,
identifiability, power or missing-data assumptions fail. Inconclusive is not a
bridge pass.

## Relation To The Core Claim

Candidate 2R tests the directional bridge unit `S4` in the
[Core Claim Test Contract](CORE_CLAIM_TEST_CONTRACT.md). It does not replace the
joint `S1 + S2 + S3` collapse-gate distinctiveness test.
