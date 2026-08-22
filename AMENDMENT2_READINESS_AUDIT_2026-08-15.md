# Amendment 2 — Readiness Audit (2026-08-15)

Status: **2A operative; no target-specific 2B in force**

## Short Verdict

The Amendment 2 architecture is methodologically reasonable at the governance
level. Amendment 2A is author-approved, publicly ratified and operative for
future studies. Amendment 2B is also a reasonable execution template, but it is
not an amendment that can be approved generically: its scientific content must
be completed and frozen separately for one eligible target before outcome
inspection.

The canonical status is therefore:

> Amendment 2A is ratified and operative. No target-specific Amendment 2B is in
> force. Consequently, the only permitted empirical disposition is
> `NO AMENDMENT 2 VERDICT`.

“Amendment 2 itself is still awaiting author approval” is too broad. The common
rules are already approved; the target-specific execution layer does not yet
exist in an approvable form.

## Verified State

| Component | Verified state | Consequence |
|---|---|---|
| Staged routing | the integrated proposal is retired in favour of 2A + 2B | no single all-purpose Amendment 2 document remains to ratify |
| Amendment 2A text | author-approved prospective governance | fairness and interpretation rules are live for future work |
| 2A ratification | adopted commit `b0dff095919295acbaaf1811a29d63736632d429` is an ancestor of `main`; adopted blob is `b5a574fbce4458422a823c6a715c2b9cbd2e4b16` | 2A's immutable-text condition is satisfied |
| Amendment 2B | complete field structure, but every target-specific field remains unset | valid template; no operative target annex |
| Dataset target | no eligible target identified in the declared search scope | no target identity, variable mapping or blindness statement can be frozen |
| R3–R6 | candidate equations and comparison contract exist | conceptual rival specification only |
| Fitting implementation | no R3–R6 simulation/fitting pipeline is present in `simulations/` | identifiability, convergence and equal-budget comparison are untested |
| Scenario registry | validator returns `VALID_DRAFT`; `locked_validation_ready=false` | useful calibration scaffold; not a locked validation instrument |
| Margin and power | candidate targets exist; meaningful score margin is unset | no numeric acceptance rule is ratified |
| Locked validation | parameter grid and seed commitments are unset; no result exists | 2B activation gate is not met |
| Human-study governance | no sponsoring institution, ethics determination, consent package or data-management approval is attached | no participant recruitment or data access is authorized |

## What Is Already Strong Enough

Amendment 2A contains the right high-level protections:

- explicit and strong free-energy / active-inference rivals rather than a weak
  proxy;
- equal data, tuning and compute budgets;
- ties count as absorption rather than support;
- absent or unidentified rivals yield `INCONCLUSIVE`, never a VOT win;
- agent action and external forcing must be different observed variables;
- fold and non-fold processes must both be recoverable in locked simulation;
- structure, external endpoint and rival separation are separate evidence
  units;
- no verdict without a target-blind, immutable 2B annex.

These are substantive governance commitments, not placeholders. Re-opening 2A
merely because 2B is incomplete would weaken the staged architecture.

## What Must Exist Before A 2B Can Be Approved

1. an eligible target that clears the metadata-only access gate and data
   preflight;
2. a complete prospective mapping of `y_t`, `a_t`, `u_t`, arm labels and P3;
3. implemented VOT, R0–R6 and S0 fitting code under one equal-budget harness;
4. identified priors, action/policy sets, horizons, noise models and failure
   rules;
5. calibration results selecting a proper score and meaningful win/tie margin;
6. an independently seeded locked-validation registry and one permitted run;
7. an institutional, ethics, consent, security and data-management route where
   human participants or identifiable data are involved;
8. author approval of the completed target-specific annex before target-outcome
   inspection.

Author approval should occur at item 8, not now. A generic approval of unset
fields would not make the design more prospective; it would authorize later
choices after the target is known.

## Next Development Route

The [Prospective Study Protocol](AMENDMENT2_PROSPECTIVE_STUDY_PROTOCOL.md)
defines two ethically separated routes: a bounded reversible nonclinical task
for method development and a later naturalistic clinical collaboration in which
care decisions remain independent of the research. Neither route is an
operative 2B, and neither authorizes recruitment.

The implementation priority is now:

1. build and test the R0–R6/S0 fitting harness on synthetic data;
2. calibrate the safe nonclinical design without locked seeds;
3. seek institutional and ethics review only if simulation shows the design can
   adjudicate both fold and non-fold families;
4. create and approve a target-specific 2B immediately before any eligible
   target outcomes become visible.

## Post-Audit Implementation Note (2026-08-22)

The statement above that no R3–R6 pipeline was present was correct on the audit
date. A scalar synthetic reference harness has since been added at
[`simulations/amendment2_reference_harness.py`](simulations/amendment2_reference_harness.py),
with its contract and limitations in [`simulations/README.md`](simulations/README.md).

This is progress on item 1, not completion of the 2B prerequisite. It generates
and fits the selected shared-fold VOT and every R0–R6/S0 reference family under
common splits and budgets, emits separate structure and D5 absorption
dispositions, and preserves the calibration-compatible contract. It does not
implement exact latent-state VFE or the full multi-step EFE policy model, and
its R6 hierarchy is a ridge approximation. P0 therefore remains **not
cleared**, the scenario registry remains unlocked, and the only permitted
empirical disposition remains `NO AMENDMENT 2 VERDICT`.
