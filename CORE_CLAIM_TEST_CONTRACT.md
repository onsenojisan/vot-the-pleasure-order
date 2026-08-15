# Core Claim Test Contract

Status: **current public interpretation contract**
Date: 2026-08-15
Claim level: specification only; no empirical upgrade

## Purpose

This file fixes the mapping between VOT's one-sentence empirical claim and the
tests that can, and cannot, bear it. It does not alter the frozen Generic-Tipping
Discriminator preregistration and does not report a result.

The core empirical claim is:

> In a predeclared domain, horizon and perturbation regime, an externally
> measured Omega-related capacity has reproducible explanatory or predictive
> content beyond local consonance and an explicit strong free-energy / active-
> inference rival family.

"Beyond" means a predeclared out-of-sample or complexity-penalized increment.
It does not mean conceptual non-identity, compatibility, or a different name for
the same fitted dynamics.

## Claim Units

The program contains four claim units. They must not be substituted for one
another.

| Unit | Question | What a pass permits | What it does not permit |
|---|---|---|---|
| `S1 — structure` | Does a fold / hysteresis account describe decline and recovery under shared parameters? | A bounded claim about generic decline-recovery dynamics | Any Omega, value, pleasure or directionality claim |
| `S2 — external alignment` | Does the structure align with a predeclared, independent external viability / functional endpoint (`P3`)? | A bounded Omega-related alignment claim | Distinctiveness from free-energy or causality |
| `S3 — rival separation` | Does the joint structure + endpoint model beat every predeclared strong rival, including hierarchical and shared-dynamics active-inference models? | A bounded distinctiveness claim in the tested domain | Cross-domain generality or value ranking |
| `S4 — directional bridge` | Does a local input predict later Omega-related change or rate beyond baseline outcome and rivals? | A bounded prospective change/rate bridge claim | Causality unless the design identifies an intervention contrast |

## The Core-Claim Gate

The one-sentence core claim receives bounded support only when `S1 + S2 + S3`
pass in one preregistered design, or in a prospectively declared linked design
whose populations, variables and transport assumptions were frozen before any
outcome was inspected.

In particular:

- `D4-dynamics` alone can pass only `S1`.
- `P3` alone can pass only `S2`.
- Candidate 2L is an adjusted future-level prediction study. It passes none of
  `S1–S3` by itself and is not a test of `dOmega/dt`.
- Candidate 2R is the route for `S4`; it is not a substitute for `S1–S3`.
- Results from different populations may not be assembled after the fact into a
  core-claim pass.

## Required Frozen Fields

Before a core-claim study receives data, it must freeze:

1. domain and target population;
2. state variables and observation model;
3. horizon `H` and perturbation set `P`;
4. the meaning of self-recovery versus externally assisted recovery;
5. decline and recovery arm definitions;
6. the external `Y_Omega` endpoint, its units, direction, baseline and follow-up;
7. the VOT model equations and estimator;
8. the full rival family in the [D5 remediation draft](PROPOSED_AMENDMENT_2_D5_AND_FALSIFIER.md);
9. out-of-sample score, complexity penalty and minimum meaningful margin;
10. data-adequacy, structure, support, downgrade and inconclusive rules.

An unfrozen field makes the study exploratory. It cannot be supplied after
viewing the outcome and still count toward the core claim.

## Dispositions

### Bounded support

All of `S1–S3` pass, the external endpoint is independent at the item/feature
level, the strongest explicit rival is beaten by the frozen margin, and the
result reproduces in a holdout or preregistered replication.

Allowed wording:

> In domain D over horizon H and perturbation regime P, the preregistered VOT
> structure aligned with the independent external endpoint and added frozen
> out-of-sample or penalized performance beyond the predeclared rival family.

### Absorption / downgrade

Any explicit strong rival matches or beats the VOT model on the primary frozen
criterion, or the VOT increment does not reproduce.

Required wording:

> In this domain, the tested VOT formulation did not add distinct explanatory
> or predictive content beyond the rival family and is treated as a synthesis,
> redescription or parameterization.

### Collapse-gate unsupported

A study passes its data-adequacy and two-sided power gates and the predeclared
non-fold family beats the fold family by the frozen margin. This is evidence
against the collapse-gate in the tested domain, not merely a measurement null.

### Inconclusive

The endpoint is not independent, the models are not identifiable, the design is
underpowered in either direction, threshold coverage fails, required arms or a
control variable are absent, or the explicit strong rival cannot be estimated.
Inconclusive results do not support or downgrade the core claim.

## Forbidden Substitutions

The following moves are not permitted:

- `D4 passed` -> `Omega was measured`;
- `a fold was detected` -> `VOT beat free-energy`;
- `P3 aligned` -> `the collapse gate is distinctive`;
- `Candidate 2L predicted T3 level` -> `dC/dt caused dOmega/dt`;
- `a flexible statistical comparator lost` -> `active inference lost`;
- `no EWS was detected` -> either `no fold` or `measurement failure` without
  the two-sided structure disposition;
- population-level intervention contrast -> individual counterfactual claim.

## Current Verdict

No existing record passes `S1 + S2 + S3`. The measurable operator lost to the
existing free-energy comparator, `D4-dynamics` is un-run, `P3` is unimplemented,
and Candidate 2L remains design-incomplete. The core claim is therefore
**undecided and empirically trending negative**, not validated.
