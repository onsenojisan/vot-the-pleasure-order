# Candidate 2 — Freeze Decision Sheet v0.1

Status: decision sheet; no option selected; Candidate 2 remains design-incomplete and un-runnable
Date: 2026-08-14

This sheet turns the blocking decisions in [BRIDGE_SPEC.md](BRIDGE_SPEC.md) into a single pre-collection record. It is not a preregistration and does not itself select an input, endpoint, threshold, or score.

## 1. Decision order

The outcome is selected **before** the bridge score or inputs are finalized. If no independent external outcome is available, stop: Candidate 2 is UN-TESTED / UN-RUNNABLE and no self-report substitute may be installed.

1. Select an external outcome type and identify the endpoint data source.
2. Allocate endpoint items/features first; verify construct separation.
3. Select exactly one lagged input flux and its estimator.
4. Allocate remaining predictor, gate, and baseline features.
5. Freeze windows, score rule, thresholds, rivals, and null/fail conditions.

## 2. External outcome decision

| Choice | Required external observations | Claim after a pass | Author selection |
|---|---|---|---|
| **A. Level** `Y_Omega = OmegaHat(T3)` | one independent external endpoint | predicts an Ω-related level; may **not** be called `dOmega/dt` | [ ] |
| **B. Change** `Y_Omega = OmegaHat(T3) - OmegaHat(T2*)` | two independent external endpoints at frozen occasions | predicts an Ω-related change | [ ] |
| **C. Rate** `Y_Omega = d OmegaHat / d tau` | sufficient independent endpoint observations, fixed time unit and slope estimator | predicts an Ω-related rate; only choice compatible with `dOmega/dt` wording | [ ] |

Selected external endpoint name/source: ________________________________

Declared `(L,H,P)`, units, aggregation, missing-data rule: ________________________________

Why its construct is not defined as option preservation, reversibility, anti-rigidity, harmful order, or a self-report aggregate: ________________________________

If the selected source cannot be obtained, record **UN-TESTED / UN-RUNNABLE** here: ________________________________

## 3. Input-flux decision

Exactly one input becomes `selected_input_lag`. The other two are not silently substituted or combined.

| Choice | What is measured | Minimum freeze record | Author selection |
|---|---|---|---|
| **A. Felt-consonance** `Δp_loc` | change in the felt/reported appearance channel | item/feature source, estimator, scale, sign, `T0/T1` window, missing-data rule | [ ] |
| **B. Structural coherence** `ΔC_struct` | change in the structural C coordinate | operational definition of C, estimator, scale, sign, `T0/T1` window, missing-data rule | [ ] |
| **C. Named C subcomponent** `ΔC_component` | one declared subcomponent of C | component definition/composition, estimator, scale, sign, `T0/T1` window, missing-data rule | [ ] |

Selected input and estimator: ________________________________

Why it is disjoint from `Y_Omega`, Future Option Preservation, harmful-order gate, and every baseline: ________________________________

## 4. Predictor and gate allocation

`BridgeScore_C2` is a predictor / decision statistic only. It is never renamed `dOmega/dt`.

| Role | Feature(s) / items | Owner | Disjointness checked | Frozen? |
|---|---|---|---|---|
| external `Y_Omega` endpoint |  |  | [ ] | [ ] |
| selected input |  |  | [ ] | [ ] |
| persistence |  |  | [ ] | [ ] |
| corrective update |  |  | [ ] | [ ] |
| continuity |  |  | [ ] | [ ] |
| Future Option Preservation |  |  | [ ] | [ ] |
| harmful-order gate |  |  | [ ] | [ ] |
| `selected_input_lag` alone baseline |  |  | [ ] | [ ] |
| Future Option Preservation alone baseline |  |  | [ ] | [ ] |
| C-level / trend / volatility / mean-reversion baselines |  |  | [ ] | [ ] |
| psychological-flexibility and domain/rival baselines |  |  | [ ] | [ ] |

Item-disjointness alone is necessary but insufficient: Future Option Preservation and the harmful-order gate are Ω-aligned by construction. The selected endpoint must state a distal functional consequence not defined by either construct, and the bridge must beat Future Option Preservation alone.

## 5. Freeze record

- [ ] endpoint type and external data source selected
- [ ] endpoint level / change / rate estimator and time units selected
- [ ] one input flux selected; other candidates recorded as not selected
- [ ] all role ownership fields above complete
- [ ] `T0`–`T3` (and `T2*` if needed) non-overlap / timing rule frozen
- [ ] `BridgeScore_C2` vector/scalar form, gate handling, weights, and thresholds frozen
- [ ] baselines, negative controls, performance metric, holdout rule, and pass margin frozen
- [ ] failure statement and no-reinterpretation rule accepted

Only when all boxes are checked may a separate Candidate 2 preregistration be created. If any box is empty, the correct public status remains: **design-incomplete; not preregisterable; not a validated bridge**.
