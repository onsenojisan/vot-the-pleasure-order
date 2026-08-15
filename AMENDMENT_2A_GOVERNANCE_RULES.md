# Amendment 2A — Prospective Governance Rules For D5 And Structure Adjudication

Status: **author-approved prospective governance; operative only with the public ratification record described below**
Author approval date: 2026-08-15
Scope: future studies not already governed by the frozen v0.2 preregistration

## What 2A Does

Amendment 2A adopts rules that prevent an under-specified rival, an
unidentifiable model, or a one-sided instrument from being counted as evidence
for VOT. These are research-governance and interpretation rules. They are not a
claim that any model has been fitted, any design has adequate power, or any
target dataset is eligible.

The target-specific numerical and computational commitments are separated into
[Amendment 2B](AMENDMENT_2B_EXECUTION_ANNEX.md). No empirical verdict may be
issued under Amendment 2A unless a complete, prospectively frozen 2B annex was
already in force for that study.

## Non-Retrospective Scope

Amendment 2A does **not** edit, supersede or reinterpret:

- the frozen Generic-Tipping Discriminator v0.2;
- Amendment 1 as the operative disposition record for that frozen test;
- any result already inspected or published;
- any archived Zenodo file or historical status statement.

The asymmetric Amendment 1 disposition therefore remains attached to the
pre-existing frozen test. Amendment 2A governs only a new prospective study
whose own 2B annex satisfies every activation condition below.

## G1. Explicit Rival Rule

A comparator may be described as free-energy / active inference only when its
prospective 2B annex publishes:

1. its generative model with latent states, observations and transitions;
2. the variational-free-energy and/or expected-free-energy objective actually
   used for inference, learning or policy selection;
3. its priors, preferences, process noise and observation noise;
4. the parameters shared across people and arms and those fitted separately;
5. fitting, posterior-prediction and comparison code;
6. the mapping from every empirical variable to the model.

Flexibility, prediction-error terms or independent fitting alone do not satisfy
this rule.

## G2. Minimum Rival Family And Identifiability

A future D5 study must include, at minimum:

| ID | Rival role |
|---|---|
| `R0` | mean, trend, variance, autoregressive and generic state-space baselines |
| `R1` | smooth drift / changing-equilibrium dynamics |
| `R2` | externally forced jump / intervention-response dynamics |
| `S0` | state switching without bifurcation |
| `R3` | per-person, per-arm active inference |
| `R4` | hierarchical active inference with partial pooling across people |
| `R5` | active inference sharing dynamics across decline and recovery |
| `R6` | shared nonlinear / hysteretic active inference |

The current candidate equations for `R3–R6` are in the
[D5 Rival Specification](D5_ACTIVE_INFERENCE_RIVAL_SPEC.md). Amendment 2A does
not freeze those candidate equations; the study's 2B annex must freeze their
exact implementation.

If a required strong rival is absent or unidentified, the D5 result is
`INCONCLUSIVE`. Its absence is never a VOT win. A stronger computable rival
proposed before target-outcome unblinding must be added or its omission must be
published as a scope limit before the run.

## G3. Equal Comparison And Tie Rule

All candidates receive the same observations, arm labels, endpoint variables,
training partitions and compute policy. The 2B annex must freeze a proper
out-of-sample score, complexity treatment, prior-sensitivity set, transfer split
and meaningful win/tie margin.

VOT clears D5 only if it beats every estimable required rival by that frozen
margin and reproduces under the declared rule. A tie is absorption, not weak
support. A win over `R3` with a tie or loss against `R4–R6` is not VOT
distinctiveness.

## G4. Separate Action From External Forcing

The agent-selected action or prospectively justified proxy (`a_t`) and the
exogenous perturbation or control variable (`u_t`) have different causal roles
and must be separately observed and mapped.

- If `a_t` is absent, the expected-free-energy policy mechanism and D5 verdict
  are `INCONCLUSIVE`.
- If bidirectional `u_t` coverage is absent, two-sided fold/non-fold structure
  adjudication is `INCONCLUSIVE`.
- One recorded variable may not be assigned both roles.

The [Data Preflight](AMENDMENT2_DATA_PREFLIGHT.md) records these necessary
conditions. Passing it never proves power, identifiability or runnability.

## G5. Two-Sided Structure Rule

Before target-outcome inspection, the study must demonstrate on independently
seeded simulations matched to its declared design that it can distinguish fold
and non-fold families in both directions. Inconclusive replicates stay in the
denominator. No pooled average may rescue a failing required scenario.

When, and only when, the study's 2B annex and locked validation are complete,
the following disposition meanings apply:

| Result | Permitted disposition |
|---|---|
| Data adequacy or required-model identification fails | `INCONCLUSIVE — UNDERPOWERED / UNIDENTIFIED` |
| Fold family wins by the frozen margin and required flags pass | `STRUCTURE SUPPORTED`; no VOT upgrade yet |
| Non-fold family wins by the frozen margin after the two-sided gate passes | `NO FOLD IN TESTED DOMAIN`; downgrade the collapse-gate claim in that domain |
| Neither family clears the frozen margin | `INCONCLUSIVE — MODEL TIE` |
| Fold structure passes but D1–D4 or D5 rivals absorb it | `STRUCTURE REAL, VOT NOT DISTINCT` |

Critical slowing may be one declared flag, but it is not the sole structure
gatekeeper. The structure comparison is computed without `Y_Omega` and cannot
by itself support VOT.

## G6. Evidence-Scope Rule

A structure result supplies at most `S1`. A core-claim upgrade requires all of:

- `S1`: two-sided structural evidence;
- `S2`: an independent, non-circular external Ω-related endpoint (`P3`);
- `S3`: separation from every estimable declared strong rival.

These units must occur in one preregistered design or an explicitly and
prospectively linked design under the [Core Claim Test Contract](CORE_CLAIM_TEST_CONTRACT.md).
No single unit is sufficient.

## G7. Execution Gate

Amendment 2A alone authorizes no empirical verdict. A study may use the
dispositions above only after its public 2B annex contains all required fields,
its target-data blindness statement, exact code and model identifiers, chosen
margin, committed locked seeds and locked-validation report.

Missing or late 2B commitments route the study to `NO AMENDMENT 2 VERDICT`, not
to a favourable default.

## Ratification Condition

The author approved this staged governance architecture on 2026-08-15. No
target dataset is designated by 2A, so 2A makes no target-outcome blindness
claim. Blindness is a per-study requirement that must be affirmed in 2B.

This document becomes operative only when a public ratification record names an
exact immutable Git commit containing this approved text. A later edit creates a
new version and does not silently alter the adopted text.
