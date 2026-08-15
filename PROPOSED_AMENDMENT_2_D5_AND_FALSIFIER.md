# Proposed Amendment 2 — Explicit D5 Rivals And A Two-Sided Structure Disposition

Status: **author-ratification draft; not in force and not frozen**
Date: 2026-08-15
Applies prospectively only; no target outcome data have been inspected here

## Why An Amendment Is Required

The frozen preregistration remains immutable. Its D5 clause equates a flexible
case-by-feature model and independent per-arm fits with the degrees of freedom
of a bistable-prior expected-free-energy model. That declaration prices
flexibility, but it does not demonstrate that the fitted comparator is an
active-inference model or that active inference must fit cases and arms
independently.

Amendment 1 also sends an out-of-sample critical-slowing failure to
`INCONCLUSIVE`. That is defensible when the measurement is underpowered, but it
leaves measurement failure and evidence for a non-fold process unidentified.
This draft repairs both problems before any future execution.

Ratification requires an author date, immutable deposit or commit identifier,
and confirmation that no target outcome was inspected before the ratification.

## A. Replacement D5 Rival Contract

### A1. What Counts As A Free-Energy / Active-Inference Rival

A model may carry that label only if the preregistration publishes:

1. a generative model with latent states, observations and transition dynamics;
2. the variational or expected-free-energy objective used for inference,
   learning or policy selection;
3. all priors, preferences, process noise and observation noise;
4. which parameters are shared across people and arms and which are not;
5. the fitting, posterior-prediction and model-comparison code;
6. a mapping from every empirical variable to the generative model.

Flexibility, prediction-error terms or independent fitting alone are not enough
to call a comparator FEP / active inference.

### A2. Required Rival Family

All members receive the same observations, arm labels, endpoint and data budget
as VOT.

| ID | Rival | Purpose |
|---|---|---|
| `R0` | mean, trend, variance, autoregressive and generic state-space baselines | Exclude simple dynamics |
| `R1` | smooth drift / changing-equilibrium model | Represent non-bifurcation deterioration or recovery |
| `R2` | externally forced jump / intervention-response model | Represent transitions without loss of stability |
| `R3` | per-person, per-arm active-inference model | Preserve the flexible comparator anticipated by the frozen D5 |
| `R4` | hierarchical active-inference model with partial pooling across people | Test whether cross-case transfer is available to the rival |
| `R5` | shared-dynamics active-inference model coupling decline and recovery | Test whether arm sharing, rather than VOT, carries D4 |
| `R6` | shared nonlinear / hysteretic active-inference model | Test whether the fold geometry is annexable under equal parsimony |

If `R4–R6` are not identifiable on the data, the distinctiveness verdict is
`INCONCLUSIVE`; their absence is not a VOT win. If an external reviewer proposes
a stronger computable rival before outcome unblinding, it is added before the
run or its omission is declared as a scope limit.

### A3. Comparison Rule

The primary score, complexity penalty and meaningful margin must be frozen
before outcome inspection. The comparison must include:

- held-out predictive density or another proper out-of-sample scoring rule;
- a parameter / effective-complexity penalty;
- calibration and error by person and arm, not only a pooled mean;
- the same frozen cross-case and decline-to-recovery transfer split;
- sensitivity to prior choices declared before unblinding.

VOT passes rival separation only if it beats **every estimable member** of
`R0–R6` by the frozen meaningful margin and reproduces. A tie is absorption, not
weak support. A win over `R3` with a loss or tie against `R4–R6` is evidence that
pooling or shared dynamics mattered; it is not VOT distinctiveness.

## B. Two-Sided Structure Disposition

### B1. Data-Adequacy Gate Comes First

Before inspecting the target outcome, the study must show that it can
distinguish the fold and non-fold families in both directions under simulations
matched to the declared design. The gate covers:

- decline and recovery arm length;
- missingness and measurement error;
- control-variable range and bidirectional threshold coverage;
- timescale alignment;
- state and transition identifiability;
- false-fold and false-non-fold rates;
- power for both a fold and the strongest non-fold rival.

The minimum acceptable two-sided power and error rates are numeric ratification
fields. They must be frozen and published before real-outcome inspection. A gate
that has power only to confirm a fold is not adequate for adjudication.

### B2. Independent Structure Models

The structure stage compares at least:

1. fold / shared-hysteresis model;
2. smooth changing-equilibrium model;
3. externally forced transition model;
4. state-switching model without bifurcation;
5. preregistered catastrophe flags: multistability, hysteresis, threshold
   coverage and critical-slowing signatures where measurable.

Critical slowing is one flag, not the sole gatekeeper. Model comparison and
flags are computed without `Y_Omega` and cannot by themselves support VOT.

### B3. Disposition Table

| Result | Disposition |
|---|---|
| Data-adequacy gate fails in either direction | `INCONCLUSIVE — UNDERPOWERED / UNIDENTIFIED`; no support and no downgrade |
| Fold family beats every non-fold family by the frozen margin and required catastrophe flags pass | `STRUCTURE SUPPORTED`; proceed to D4 and P3; no VOT upgrade yet |
| Non-fold family beats the fold family by the frozen margin after the two-sided gate passes | `NO FOLD IN TESTED DOMAIN`; collapse-gate unsupported and VOT downgraded in that domain |
| Neither family wins by the frozen margin | `INCONCLUSIVE — MODEL TIE` |
| Fold structure passes but D1–D4 or explicit D5 rivals absorb it | `STRUCTURE REAL, VOT NOT DISTINCT`; synthesis / redescription |

The earlier asymmetric pre-gate rule is superseded only after this amendment is
ratified. Until then, Amendment 1 remains the operative public record.

## C. Scope Of A Positive Result

Even a full structure and D5 pass remains `D4-dynamics`. It supports the Omega
core claim only when the independent external endpoint contract (`P3`) also
passes under the [Core Claim Test Contract](CORE_CLAIM_TEST_CONTRACT.md).

## Ratification Block

The following fields are intentionally blank because filling them creates a new
scientific commitment rather than an editorial repair:

```text
author ratification date:
target-data blindness confirmation:
two-sided power floor:
false-fold ceiling:
false-non-fold ceiling:
primary scoring rule:
meaningful win/tie margin:
immutable deposit or commit:
```

Until every field is filled and published, this document is a remediation draft
and must not be described as a preregistration amendment in force.
