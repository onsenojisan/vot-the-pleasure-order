# VOT Shared-Fold Estimator — P0 Development Specification

Status: **author-selected method-development specification; not an operative 2B freeze**
Date: 2026-08-22
Claim level: implementation contract only; no empirical upgrade

## Decision

For continued P0 development, the VOT candidate is the smallest model that
directly carries the frozen D1/D4 wager:

> one cubic fold/hysteresis transition law is shared across people and across
> decline and recovery arms; only initial state, observed inputs and declared
> nuisance terms may differ.

This choice is intentionally austere. It does not add a second VOT mechanism to
escape a loss, and it exposes the theory to absorption by the stronger R6
active-inference rival. Target-specific priors, dimensions, margins, variables
and seeds remain unset and must later be frozen in an Amendment 2B annex.

## State And Observation Model

For person `i`, arm `r` and time `t`:

```text
y_i,r,t | x_i,r,t ~ Normal(H x_i,r,t + d, Sigma_y)
```

The method-development implementation is scalar. A future target may use a
fixed vector state only if its dimension, observation mapping and identifiability
rules are declared before target outcomes are inspected.

## Shared Fold Transition

```text
x_i,r,t+1
  = x_i,r,t
    + delta * (alpha x_i,r,t - x_i,r,t^3
               + beta u_i,r,t + zeta a_i,r,t)
    + w_i,r,t

w_i,r,t ~ Normal(0, Sigma_x)
```

Required constraints:

```text
delta > 0
alpha > 0
```

The effective control is:

```text
h_t = beta u_t + zeta a_t
```

For the cubic potential used here, both fold thresholds can be traversed only
if the observed control range crosses:

```text
h_fold = +/- 2 alpha^(3/2) / (3 sqrt(3))
```

Insufficient bidirectional coverage is `INCONCLUSIVE`, never evidence for or
against the fold.

## Parameter Sharing — The Load-Bearing Restriction

The following are global and shared across all people and both arms:

- `alpha`, `beta`, `zeta`, `delta`;
- observation mapping `H`, `d`;
- process and observation noise families;
- the declared nuisance action-model form.

The following may vary only as declared nuisance quantities:

- initial latent state by person and arm;
- observed action and forcing sequences;
- missingness already governed by the common rule.

No person-specific or arm-specific refit of the transition parameters is
allowed. Decline-side fitting must predict the recovery path and threshold with
the same parameter set. That cross-constraint is the VOT wager, not merely the
presence of a cubic term.

## Action Score

VOT does not claim a separate expected-free-energy policy mechanism. To make
the joint held-out score defined, its action component uses one frozen nuisance
policy:

```text
p(a_t | history_t)
  proportional_to exp(
    -kappa * (E[y_t+1 | a_t] - c)^2 / (2 sigma_pref^2)
  )
```

The action set, `c`, `kappa`, horizon and estimation grid receive the same
training information and budget as the corresponding rival fields. This
one-step risk form is only the current reference implementation. R3–R6 retain
their stronger ambiguity, habit and multi-step EFE terms in the exact future
implementation. If those terms improve R6 enough to match or beat VOT, the
result is absorption, not an unfair-rival objection.

## Estimation And Score

The target implementation must infer the latent state and parameters from the
training partition only. The primary score remains the D5 contract:

```text
elpd_joint
  = sum_test [log p(y_t | past) + log p(a_t | past)] / N_test
```

Observation and action components are reported separately. The exact latent
inference method, priors, optimization budget, convergence rule and complexity
treatment are target-specific 2B fields and are not fixed by this document.

## Relation To R6

R6 uses the same cubic geometry but may partially pool person parameters and
models action selection through full active inference. It therefore asks the
right hostile question:

> Is VOT's apparent generic fold better explained by a hierarchical
> active-inference model that contains the same geometry?

Reference dispositions:

- VOT beats every required rival by the frozen margin and reproduces: bounded
  D5 separation may be considered, subject to S1–S3 and an operative 2B;
- R6 ties or beats VOT: `STRUCTURE REAL, VOT NOT DISTINCT`;
- a non-fold family beats both after two-sided calibration: evidence against
  the collapse gate in the tested domain;
- missing coverage, power or identification: `INCONCLUSIVE`.

## Current Implementation Boundary

The reference implementation in
[`simulations/amendment2_reference_harness.py`](simulations/amendment2_reference_harness.py)
uses observed `y` as a scalar state approximation and the one-step nuisance
policy above. It is suitable for exercising generators, sharing rules, splits,
scores and dispositions. It does not clear P0 until latent-state VOT inference
and the full R3–R6 VFE/EFE interface are implemented and calibrated.
