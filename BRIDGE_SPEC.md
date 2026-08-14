# dC/dt -> dOmega/dt Bridge Specification

Status: public-facing candidate specification  
Date: 2026-06-19  
Claim level: unvalidated bridge hypothesis  

## Purpose

This document states the current public bridge hypothesis for Valence Order Theory / The Pleasure Order.

The bridge is needed because the theory distinguishes:

- `C`: local coherence.
- `dC/dt`: local coherence flux, a qualified local pleasure signal — **read the note below before using this line**; the symbol carries two jobs.
- `Omega`: directionality potential, the capacity to revise, repair, reverse, and reorganize future trajectories.
- `dOmega/dt`: long-term directionality flux.

The theory does not currently identify `dC/dt` with `dOmega/dt`.

Note on `C` vs felt consonance: read as a pleasure signal, `dC/dt` is the felt-consonance proxy `p_loc` (an appearance channel), which is distinct from the structural consonance coordinate `C`. The two can diverge — a state can feel coherent (high `p_loc`) while being poorly integrated with the whole system (low structural `C`) and low on `Omega`, as in addiction. See the [Structural Appendix](STRUCTURAL_APPENDIX_OMEGA_C_ACT.md). This divergence is exactly why a positive local `dC/dt` is not, by itself, evidence of positive `dOmega/dt` (see the Core Guardrail below).

🟡 **Open (recorded 2026-08-14) — the notation, not the distinction.** The distinction above is settled: `p_loc` is the felt channel, `C` the structural coordinate, and the philosophy core holds pleasure to be a **functional correlate** of `dC/dt` rather than an identity (F8; the identity is retracted at S2). What is unresolved is that **one symbol does two jobs** — the time derivative of a structural coordinate, and an appearance channel. On 2026-08-14 two readers flagged this from the definition line above **without reaching this note six lines below it**, which is why the pointer is now on that line. Giving the structural derivative its own symbol is the minimal fix, and it is **an author decision rather than a repair**: `dC/dt` is the form used in the frozen deposits, the canonical spec, and the public articles, so changing it here alone would create exactly the drift this project's version discipline exists to prevent.

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

## Construct Role Allocation (contract; frozen before collection)

The window rules above are necessary and **not sufficient**. The independence requirement stated at *Future Option Preservation* below is not satisfied by the window split alone: while the predictor and the endpoint come off the same self-report stream, the construct overlap survives `T2`/`T3` separation. This section states what would satisfy it.

**Contract — all six clauses, frozen and recorded before any data exists:**

1. **The `Omega` endpoint is an external viability or functional endpoint, independent of the self-report stream.** Not a self-report aggregate under a different name.
2. **An external endpoint does not by itself discharge clause 1.** It must not reuse *Future Option Preservation*'s items, its composite score, or any subjective encoding of future option availability. Independence has to be checkable at the item level, not asserted at the label level.
3. **Each item or feature carries exactly one role** — `p_loc`, structural `C`, bridge predictor, `Omega` endpoint, or rival baseline. No item appears twice, and the allocation records, per item, why it is not the neighbouring role.
4. **Reuse under a different aggregation function is prohibited.** This is the configuration that killed `O/M/A`, where the measures *were* the rival's subscales under another name.
5. **Endpoint items are claimed first**; predictors are built from what remains. In the reverse order the endpoint becomes the leftovers.
6. **If no external endpoint is available, the row stays empty and `Candidate 2` is reported as UN-TESTED and, on currently accessible data, UN-RUNNABLE.** An empty endpoint row is the data wall made visible: it must not be filled with a self-report proxy, and its emptiness must not be recorded as a completed allocation.

⚠️ **This contract makes the problem checkable; it does not solve it.** Satisfying clause 1 requires the configuration that the co-measurement gap note ([21427129](https://doi.org/10.5281/zenodo.21427129), current version `21767213`) records as assembled by no adjacent paradigm. **Two readings must be kept apart: *"solvable given an independent endpoint"* is not *"there is no endpoint."***

🛑 **Corrected 2026-08-14: this said "the same wall that leaves D4 un-run", and that conflates two walls.**
`D4` is un-run because **no accessible dataset carries both a decline and a recovery arm** — a data-shape
problem, and the frozen preregistration's §7 states that *"H2/D4 adjudication does **NOT** wait on P3"*, i.e.
the D4 dynamics comparison does **not** require the external Ω̂ endpoint. **Candidate 2 is blocked by the
endpoint wall; D4 is blocked by the arms wall.** They coincide only in the *upgrade* case (`D4 + P3`, see
[README](README.md)), where an external endpoint is required to move VOT's Ω claims rather than the dynamics
comparison. Writing them as one wall makes the endpoint problem look bigger than it is and the arms problem
look smaller.

**Ordering.** Like the `B-flex` item allocation in *Required Baselines*, this can only be fixed **before** collection is designed. Acquisition is on hold, so there is no deadline — but after the hold lifts is too late, because an allocation made once the data is visible is a forking path.

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

**Prior art (recorded 2026-08-09). This construct is not new, and the space it occupies has a named owner.** Lade, Walker & Haider (2020), *Resilience as pathway diversity: Linking systems, individual and temporal perspectives on resilience*, *Ecology and Society* 25(3):19, doi:`10.5751/ES-11760-250319` (preprint arXiv:1911.02294), state their theory as: *"resilience is greater if more actions are currently available and can be maintained or enhanced into the future."* That is the specific move this element makes — counting options that **persist forward**, not options available now — and it is published, peer-reviewed, and prior.

Consequences, stated so they are not left to be inferred:

- **The environment-side option-preservation route may be used, but it cannot be introduced as new.** Any write-up presenting it as a new direction is making a novelty claim this note already refutes.
- **`Omega` itself is affected, not only this element.** `Omega` is *defined* as trajectory-revision capacity, and the same check found five further published constructs whose stated definitions collide with it — including the **viability kernel** (Aubin's viability theory), which owns the word *viability*, and **psychological flexibility** (Kashdan & Rottenberg 2010), which arrives with validated instruments.
- **This is a collision of definitions, not a demonstration of redundancy.** Whether `Omega` earns anything over these constructs is an incremental-validity question on data, and it sits behind the same data wall as `D1` and `D4`. Nothing here refutes the theory; it removes a claim of priority the theory had not earned.
- ✅ **Decided 2026-08-11.** Of the four constructs that check identified, **only psychological flexibility becomes a required baseline** — it is the one with a validated instrument on this population. Pathway diversity is handled here, at the element it actually collides with, by withdrawing the novelty claim rather than by adding a baseline. The viability kernel and resilience/adaptability are recorded as **definitional collisions, not baselines**, because neither has an instrument that runs on this data and **a baseline nobody can compute is not rigour**. Reasoning in *Required Baselines* below.

Verification level: the Lade et al. title, author list and quoted definition were checked against the primary abstract on 2026-08-09; the full *Ecology and Society* article was not read. Full check, including all six colliding constructs and what the check does **not** establish: `omega_ov_construct_redundancy_check_v0_1.md` (workbench).

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
- rival theory models where available;
- **psychological flexibility** (Kashdan & Rottenberg 2010), ~~measured with a validated instrument~~ — **measured PRIMARILY from the ESM stream under a frozen item allocation, with a static validated instrument as a SECONDARY baseline (decided 2026-08-13; see below).**

Candidate 2 is not supported if it merely detects amplitude, non-collapse, persistence, or recovery.

**Why psychological flexibility is named specifically, and why the other collisions are not baselines
(added 2026-08-11).** A construct check on 2026-08-09 found six published constructs whose stated
definitions collide with `Omega`'s. They do not all get the same treatment, and the dividing line is
whether a baseline can actually be computed on the target data:

- **Psychological flexibility is a required baseline** because it is the one that can be run. It is a
  four-part human construct on the same population, and it **arrives with validated instruments**. If
  `Omega` does not beat it, the vector is a redescription — which is exactly the fate the retracted
  `O/M/A` layer met against Sense of Coherence, one construct over.
  - 🛑 **CAVEAT ADDED 2026-08-13, on reading the primary. The requirement stands; the sentence
    "arrives with validated instruments" does not carry what it was asked to carry.**
    **The four-part definition is verbatim-exact** — checked against the full text, no drift, so *"a
    four-part human construct"* is sourced. **But Kashdan & Rottenberg disown the static instruments
    for this construct.** They *"strongly recommend that assessments of psychological flexibility
    explicitly incorporate temporality and person-situation interactions"*, on the ground that
    *"dynamic constructs require dynamic approaches"*, and prescribe **experience-sampling designs**
    instead of single-occasion self-report.
    - 🟢 **The dividing line used on 2026-08-11 survives**: the instruments *can* be administered, so
      this is not the viability kernel's problem, and *"a baseline nobody can compute is not rigour"*
      still separates the cases.
    - 🔴 **And the collision is deeper than this section records.** What the authors prescribe is
      **experience sampling — the method this project itself uses.** So the overlap is not only
      definitional; it reaches the measurement approach.
    - 🛑 **Consequence, stated so it is not discovered late: measuring `B-flex` from the same ESM
      stream as the `BridgeVector` risks the exact failure that killed `O/M/A`** — there, *"the
      `O/M/A` **are** the SOC-13 subscales … there is nothing disjoint left to separate them."*
      🟢 **Unlike that case, this one is still upstream: Candidate 2's data does not exist yet, so
      disjoint measurement can be designed in — and only before collection.**
    - ✅ **DECIDED 2026-08-13 — `B-flex` is measured in two forms, and the ordering matters more than
      either.** Options and reasoning:
      `vot-empirical-workbench/outputs/bflex_disjoint_measurement_materials_2026-08-13.md`.

      **① PRIMARY — ESM-derived, under an item allocation frozen before collection.** This is the form
      the construct's own authors prescribe, and it puts `B-flex` and the `BridgeVector` at the same
      measurement grain, so a win for `Omega` cannot be a win for having measured itself better.
      🛑 **The allocation of ESM items between `B-flex` and the `BridgeVector` must be frozen and
      recorded BEFORE any data exists.** Allocating after the data is seen is a forking path, and this
      is the only window in which the allocation can be made at all.

      **② SECONDARY — a static validated instrument** (AAQ-family or equivalent), administered off the
      beep schedule. It is **not** the primary because its own authors disown it for this construct;
      it is retained because **a baseline's job is to be the rival a sceptic would demand**, and the
      field-standard instrument is what a sceptic would reach for.

      🟢 **The disagreement rule is declared here, in advance, because it is where the information is.**
      If `Omega` beats **only** the static baseline and not the ESM-derived one, **that is a win on
      measurement grain and not on construct**, and it may not be reported as incremental validity.
      Beating both is the only result that carries the claim.

      🛑 **EXCLUDED IN ADVANCE: both measures computed from the same ESM items with different
      aggregation.** This is the exact configuration that killed `O/M/A` — *"the `O/M/A` **are** the
      SOC-13 subscales … there is nothing disjoint left to separate them"* — and it is named because
      it is the cheapest path at implementation time, not because anyone has proposed it.

      ⚠️ **Nothing here is evidence.** This fixes how a baseline would be measured if the study is ever
      run; the study is on hold, and `Candidate 2` remains **a preregisterable specification, not a
      validated bridge**.
- **Pathway diversity** (Lade, Walker & Haider 2020) collides with the *Future Option Preservation*
  element rather than with `Omega` as a whole, and is disclosed there. **No baseline is added**; what
  was owed was the withdrawal of a novelty claim, and that is recorded at the element.
- **The viability kernel** (Aubin) and **resilience / adaptability** (Walker et al. 2004) are declared
  **definitional collisions, not baselines**. Neither has an instrument that runs on intensive
  longitudinal data for one person, so requiring them would make this specification unrunnable for a
  reason that has nothing to do with the theory. **Adding a baseline nobody can compute is not rigour.**

⚠️ **A definitional collision is not absorbed variance.** None of this shows `Omega` is redundant. It
withdraws a claim of priority, and it says which rival has to be beaten on data — behind the same
access wall as `D1` and `D4`.

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
