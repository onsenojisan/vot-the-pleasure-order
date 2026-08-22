# Amendment 2 simulation tools

Status: **method development only; no Amendment 2 verdict authorized**

This directory contains four different layers. They must not be treated as one
completed fitting engine:

1. registry, access and data-preflight validators;
2. the two-sided calibration-result summarizer;
3. a scalar synthetic VOT + R0–R6/S0 reference harness;
4. exact target-specific latent-state VFE/EFE and locked-validation code —
   **not yet implemented**.

## Reference harness

`amendment2_reference_harness.py` now supplies the first executable comparison
loop. It:

- generates every registered VOT, R1, R2, S0 and R3–R6 scenario;
- keeps observed agent action `a_t` separate from external forcing `u_t`;
- applies one chronological 60/20/20 split within every person/arm;
- fits R0 baseline variants, R1–R6/S0 and the selected shared-fold VOT under
  the same ridge and policy-grid budget;
- reports held-out observation, action and joint log scores;
- reports fold-family separation independently from the D5 VOT-versus-best-
  rival absorption disposition;
- emits the CSV contract consumed by `calibrate_amendment2.py`;
- writes a full per-model audit when `--audit-output` is supplied.

Run a bounded smoke test:

```powershell
python simulations/amendment2_reference_harness.py `
  simulations/amendment2_scenarios.v0.json `
  --scenario r1_smooth_moderate_noise `
  --scenario vot_shared_fold_strong `
  --cases-cap 4 `
  --observations-cap 50 `
  --replicates 1 `
  --output reference_results.csv `
  --audit-output reference_audit.json
```

Summarize the provisional result contract:

```powershell
python simulations/calibrate_amendment2.py reference_results.csv `
  --output reference_summary.json
```

Do not use `--require-pass` to imply a ratified result. The current registry,
margin and acceptance targets are not locked.

## Scientific boundary

The reference harness is intentionally insufficient for P0. It uses:

- a scalar observed-state identity approximation rather than latent-state VFE;
- a one-step risk-only policy approximation rather than the full ambiguity,
  habit and multi-step EFE contract;
- the selected [shared-fold VOT development estimator](../VOT_SHARED_FOLD_ESTIMATOR_SPEC.md)
  with observed `y` substituted for latent-state inference;
- a ridge partial-pooling approximation for hierarchical R6 rather than a
  fitted hierarchical Bayesian model;
- a provisional zero score margin unless another calibration-only value is
  supplied explicitly.

Every CSV row therefore carries:

```text
harness_status=METHOD_DEVELOPMENT_ONLY
verdict_authorized=False
```

The next implementation step is to replace the reference approximations with
the exact frozen observation/state-inference and multi-step EFE models, then
calibrate the structure and D5 absorption rules before any independent locked
validation registry is opened.

## Tests

```powershell
python -m unittest discover -s simulations -p 'test_*.py'
```
