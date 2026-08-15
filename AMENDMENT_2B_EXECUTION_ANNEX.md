# Amendment 2B — Target-Specific Execution Annex Template

Status: **template; not in force for any dataset**
Date: 2026-08-15
Governed by: [Amendment 2A](AMENDMENT_2A_GOVERNANCE_RULES.md)

## Purpose

Amendment 2B freezes the target-specific scientific and computational choices
that Amendment 2A deliberately does not choose. Each target study requires its
own completed, versioned annex. A generic template, a partially completed copy,
or a copy published after target-outcome inspection is not operative.

Until every activation field is complete, the only permitted status is
`NO AMENDMENT 2 VERDICT`.

## 1. Study Identity And Prospective Status

```text
2B version: UNSET
target study and dataset ID: UNSET
target dataset access date: UNSET
target-outcome blindness confirmed by: UNSET
blindness confirmation date: UNSET
outcomes already inspected before freeze: UNSET
Amendment 2A immutable commit: UNSET
2B pre-run commitment commit or deposit: UNSET
```

If target outcomes were inspected before the freeze, state that fact and stop.
The annex may document method development but cannot prospectively govern that
target.

## 2. Data Preflight And Variable Mapping

Attach the generated preflight report and freeze:

```text
data-manifest path and SHA-256: UNSET
preflight report path and SHA-256: UNSET
observed state y_t: UNSET
agent action or proxy a_t: UNSET
prospective action/proxy justification: UNSET
external forcing u_t: UNSET
proof that a_t and u_t are distinct: UNSET
decline and recovery arm definitions: UNSET
time unit and irregular-timing rule: UNSET
P3 / external endpoint, or explicit absence: UNSET
missingness and dropout rule: UNSET
```

The preflight must clear its necessary-condition check. That clearance is not a
power or identifiability result.

## 3. Frozen Models

For VOT and every required `R0`, `R1`, `R2`, `S0`, `R3–R6` candidate, record:

```text
generative equations and version: UNSET
observation model: UNSET
inference / learning objective: UNSET
policy objective and preference model where applicable: UNSET
parameter-sharing rule: UNSET
latent-state dimension grid: UNSET
action and policy set: UNSET
planning-horizon grid: UNSET
process and observation noise families: UNSET
prior families and sensitivity grid: UNSET
fitting code commit: UNSET
```

Any required model that cannot be made estimable must be declared before the
run and routes D5 to `INCONCLUSIVE`.

## 4. Equal-Budget Fitting And Holdout Rule

```text
training / validation / locked-test split: UNSET
decline-to-recovery transfer split: UNSET
held-out person rule: UNSET
optimizer and initialization policy: UNSET
per-model compute budget: UNSET
convergence criteria: UNSET
shared retry and divergence rule: UNSET
effective-complexity treatment: UNSET
posterior-predictive failure rule: UNSET
```

No candidate receives privileged restarts, target information or tuning budget.

## 5. Score And Decision Rule

```text
primary proper score and units: UNSET
observation-score component: UNSET
action-score component: UNSET
complexity adjustment: UNSET
meaningful win/tie margin: UNSET
reproduction rule: UNSET
prior-sensitivity reversal rule: UNSET
```

The meaningful margin is selected on calibration data only and then frozen
before locked validation.

## 6. Two-Sided Calibration Targets

The candidate targets currently recorded in the
[Calibration Protocol](AMENDMENT2_SIMULATION_PROTOCOL.md) are not ratified by
this template. The completed annex must state:

```text
fold power lower-95% floor: UNSET
non-fold power lower-95% floor: UNSET
false-fold upper-95% ceiling: UNSET
false-non-fold upper-95% ceiling: UNSET
worst-case Monte Carlo SE ceiling: UNSET
replicates per required scenario: UNSET
scenario-registry path and SHA-256: UNSET
calibration seed registry: UNSET
calibration report and SHA-256: UNSET
chosen rule and margin: UNSET
```

## 7. Locked Validation Commitment

This block is published before the locked seeds are used:

```text
locked scenario-registry version: UNSET
locked seed commitment: UNSET
software environment and code commit: UNSET
failure disposition: UNSET
authorized runner: UNSET
freeze timestamp: UNSET
```

After the one permitted locked run, append without rewriting the commitment:

```text
locked result file and SHA-256: UNSET
locked summary and SHA-256: UNSET
validation outcome: UNSET
publication commit or deposit: UNSET
```

The pre-run commitment and post-validation result record therefore have
different immutable identifiers. The latter may append results but must not
rewrite the former.

Failure does not authorize tuning against the locked set. A revised rule needs
a newly versioned 2B annex and independently seeded locked validation.

## 8. Activation Checklist

- [ ] author approved this exact target-specific annex;
- [ ] target-outcome blindness was affirmatively recorded;
- [ ] data preflight cleared necessary conditions;
- [ ] every required rival is implemented and estimable, or D5 is declared
      `INCONCLUSIVE`;
- [ ] calibration selected the rule without using locked results;
- [ ] locked seeds and code were committed before execution;
- [ ] every required locked scenario passed its declared targets;
- [ ] the annex and results have immutable public identifiers.

Only when all boxes are checked may the study report an Amendment 2 disposition.
Otherwise report `NO AMENDMENT 2 VERDICT` and retain the ordinary evidence
boundary.
