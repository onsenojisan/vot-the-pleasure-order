# dC/dt -> dOmega/dt Bridge Specification

Status: public-facing candidate specification  
Date: 2026-06-19  
Claim level: unvalidated bridge hypothesis  

## Purpose

This document states the current public bridge hypothesis for Valence Order Theory / The Pleasure Order.

The bridge is needed because the theory distinguishes:

- `C`: local coherence.
- `dC/dt`: local coherence flux, a qualified local pleasure signal.
- `Omega`: directionality potential, the capacity to revise, repair, reverse, and reorganize future trajectories.
- `dOmega/dt`: long-term directionality flux.

The theory does not currently identify `dC/dt` with `dOmega/dt`.

Note on `C` vs felt consonance: read as a pleasure signal, `dC/dt` is the felt-consonance proxy `p_loc` (an appearance channel), which is distinct from the structural consonance coordinate `C`. The two can diverge — a state can feel coherent (high `p_loc`) while being poorly integrated with the whole system (low structural `C`) and low on `Omega`, as in addiction. See the [Structural Appendix](STRUCTURAL_APPENDIX_OMEGA_C_ACT.md). This divergence is exactly why a positive local `dC/dt` is not, by itself, evidence of positive `dOmega/dt` (see the Core Guardrail below).

The bridge question is therefore:

> When does local coherence or pleasure flux become evidence for later directionality, and when does it fail to do so?

## Core Guardrail

The bridge is not assumed.

Local pleasure or rising coherence may reflect:

- repair;
- adaptive integration;
- learning;
- restored continuity;
- future option preservation.

But it may also reflect:

- addictive reward capture;
- rigid closure;
- coercive order;
- brittle optimization;
- avoidance of corrective update;
- reduced uncertainty by eliminating future options.

Therefore a positive local `dC/dt` is not by itself evidence of positive `dOmega/dt`.

## Candidate 2 Bridge Hypothesis

Candidate 2 states:

> Lagged local coherence flux contributes to later directionality only when it is independently anchored by persistence, corrective update, continuity, and future option preservation, and when harmful rigid order is excluded.

Compact form:

```text
dOmega_dt_C2(t + h)
  = Bridge(
      dC_dt_lag,
      persistence,
      corrective_update,
      continuity,
      future_option_preservation,
      harmful_order_gate
    )
```

This is a testable hypothesis, not a validated result.

## Required Windows

Any empirical bridge test must freeze time windows before testing.

| Window | Role |
|---|---|
| `T0` | baseline state |
| `T1` | local coherence or pleasure flux input |
| `T2` | bridge support window |
| `T3` | independent directionality endpoint |

Rules:

- `T3` must not be used to define predictors, gates, thresholds, or inclusion.
- `T1/T2` and `T3` must not overlap.
- endpoint labels must not leak into predictor construction.
- thresholds must not be adjusted after seeing `T3`.

If these rules fail, the result is exploratory and cannot validate the bridge.

## Bridge Support Variables

### `dC_dt_lag`

Pre-endpoint local coherence flux over the frozen input window.

Allowed examples:

- slope of local coherence across `T1`;
- signed change from `T0` to `T1`;
- windowed positive and negative coherence-change terms.

Forbidden examples:

- same-window outcome proxy;
- post-event improvement;
- hand-selected peak after seeing results.

### Persistence

Whether the locally coherent structure survives beyond a transient spike.

### Corrective Update

Whether the system uses new information or perturbation to revise structure rather than merely repeat or harden it.

### Continuity

Whether the trajectory remains connected enough for later repair, revision, or redirection.

Continuity is not mere stasis. Rigid immobility can score low.

### Future Option Preservation

Whether later trajectories remain open, revisable, and recoverable.

This is the closest bridge-side proxy to `Omega`, but it must be measured independently from the endpoint being predicted.

### Harmful Order Gate

A predeclared exclusion or penalty for coherent states that destroy directionality despite high local order.

The gate is activated by evidence of:

- addictive reward loops;
- coercive or exploitative stabilization;
- brittle over-optimization;
- rigid closure against correction;
- high coherence achieved by eliminating reversibility or future options.

If the harmful-order gate is active, Candidate 2 cannot make a positive `dOmega/dt` claim.

## Default Mapping

Early tests should prefer the vector form because it is less likely to smuggle the theory into a single score:

```text
BridgeVector =
  [
    z(dC_dt_lag),
    z(persistence),
    z(corrective_update),
    z(continuity),
    z(future_option_preservation),
    harmful_order_gate
  ]
```

Evidence is evaluated by whether this vector predicts independent directionality endpoints beyond simpler baselines.

If a scalar score is required, the default is:

```text
support_mean =
  mean_z(
    persistence,
    corrective_update,
    continuity,
    future_option_preservation
  )

if harmful_order_gate == 1:
    dOmega_dt_C2 = 0 or negative-channel-only
else:
    dOmega_dt_C2 = z(dC_dt_lag) * max(0, support_mean)
```

Equal weights are the default. Any unequal weights must be frozen before testing.

## Required Baselines

Candidate 2 must be compared against simpler alternatives:

- `dC_dt_lag` alone;
- `C` level alone;
- generic trend or slope;
- generic volatility or amplitude;
- mean reversion;
- persistence-only or recovery-only models;
- domain-standard predictors;
- rival theory models where available.

Candidate 2 is not supported if it merely detects amplitude, non-collapse, persistence, or recovery.

## Negative Controls

Required negative controls include:

- shuffled endpoint labels;
- time-shifted endpoint labels;
- non-event windows matched for amplitude;
- high-coherence harmful-order cases;
- endpoints that should not be directionality-relevant.

## Pass Conditions

Candidate 2 earns bounded bridge support only if all are true:

1. mapping, windows, variables, thresholds, exclusions, and baselines were frozen before testing;
2. endpoint construction is independent from predictor construction;
3. performance reproduces in holdout or preregistered test data;
4. Candidate 2 beats required baselines by a predeclared margin;
5. harmful-order cases are not falsely scored as positive directionality;
6. null result rules were honored.

Allowed wording after a pass:

> In domain X, under frozen measurement rules, lagged local coherence flux plus directionality-support variables predicted independent directionality-relevant endpoints beyond simpler baselines.

## Fail Conditions

Candidate 2 fails if:

- `dC_dt_lag` alone performs as well as the bridge;
- generic trend, amplitude, persistence, or recovery explains the result;
- endpoint labels leak into predictors;
- thresholds are adjusted after inspection;
- harmful-order cases score positive;
- positive results disappear in holdout;
- null results are reinterpreted by changing the bridge.

Required conclusion after a fail:

> This operational bridge is not supported in the tested domain. VOT must remain a two-layer framework for this bridge unless another preregistered bridge is tested.

## Safe Public Wording

Safe:

> VOT distinguishes local coherence flux (`dC/dt`) from directionality flux (`dOmega/dt`). Candidate 2 specifies an unvalidated, testable bridge in which local coherence contributes to directionality only when independently associated with persistence, corrective update, continuity, and future option preservation, and when harmful rigid order is excluded.

Forbidden:

> Pleasure is `dOmega/dt`.

> Coherence proves `Omega`.

> Positive `dC/dt` validates VOT.

> Existing D2/D2+ or L4 proxy results establish the bridge.

> The theory has already unified pleasure and directionality.

## Current Status

The conservative current status is:

> Candidate 2 is a preregisterable bridge specification, not a validated bridge.

Until a frozen bridge test passes, VOT should be presented as a two-layer framework:

1. local pleasure/coherence dynamics;
2. long-term directionality dynamics.

The theoretical task is to test when those layers connect and when they diverge.
