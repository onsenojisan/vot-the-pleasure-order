# The Pleasure Order — Generic-Tipping Discriminator Pre-Registration v0.2 (consolidated frozen spec)

Date: 2026-07-04

Status: **consolidation** of prereg v0.1 (2026-07-01) with the operating points
calibrated in the power-check / realism / real-data work (2026-07-02, readout
`the_pleasure_order_make_or_break_power_check_readout_v0.1.md` §3–3c). Written
**before** any make-or-break data (TRANS-ID / dedicated study / any
recovery-arm substitute found in the open landscape). **Supersedes v0.1 as THE
single frozen spec.** No discriminator, no disposition row, and no scope
statement is changed from v0.1; this version only (a) folds the already-recorded
calibration decisions into the frozen document and (b) freezes the matched-null
re-calibration recipe that v0.1 left as "we will re-calibrate". Author: Hiroaki
Aizawa. Not results; assumes no outcome.

Code: `work/make_or_break/` (`mob_core.py`, `run_make_or_break.py`).

---

## 0. Changelog vs v0.1

```text
UNCHANGED (carried over in force, restated below verbatim in substance):
  - D1–D5 discriminators (§1)
  - Ω̂ non-circularity specification (§2)
  - Pre-committed disposition table (§3)
  - Scope: narrow collapse-gate subclaim only; philosophical spine stays descriptive;
    failure -> public "synthesis" disposition.

ADDED:
  - §4 Frozen operating points (window, transition anchoring, min_shift fallback,
    data-quality gates) — decided 2026-07-02 on WJ3CV/Kossakowski calibration,
    previously scattered in the readout.
  - §5 Matched-null verdict re-calibration recipe — procedure and numbers frozen now;
    the cut VALUES are computed on data arrival but BEFORE outcome unblinding.
  - §6 D5 operationalization note (per-case flexible comparator = the bistable-prior
    EFE's degrees of freedom), to close the "that's not really FEP" escape hatch in
    both directions.
  - §7 P3 (external-Ω̂) implementation status: spec frozen (§2), implementation
    explicitly DEFERRED until an external endpoint is confirmed in the incoming data.

Two numeric choices in §4–§5 are NEW freezes (marked [RATIFY]); everything else
traces to decisions already recorded on 2026-07-01/02.
```

## 0.1 Ratification log (2026-07-14, data-blind)

Both `[RATIFY]` items were frozen on **2026-07-14, while still blind to any
make-or-break outcome data** (TRANS-ID recovery arm / Bos bipolar EWS / any
dedicated study — none in hand; the Bos request is out and unanswered). Freezing
them now, before the target data exist, is the point: it keeps the pre-commitment
genuinely prior to seeing outcomes. No outcome trajectory informed either choice.

```text
§4.3 EWS WINDOW  — RATIFIED AS-IS.
   window = round(N_arm / 3) clipped to [10, 50], N_arm = median decline-arm length.
   Rationale unchanged (reproduces the recorded 16–20 @ ~60-beep / 25–50 @ dense
   recommendation); the value of the freeze is that it is a data-ADAPTIVE FORMULA,
   so any Bos arm length is handled without a new choice, and the [10,50] clip floor
   sits BELOW the §4.5 >=50-beep adjudication threshold (a safety rail, not an
   operating point). NOW ENFORCED IN CODE: run_make_or_break.py computes this window
   by default (preregistered_window); --window is override-only. Verified on the
   synthetic ground truths (ROW 1/2/3 unchanged at 200-beep arms -> window 50; the
   sub-50 branch exercised at 67-beep arms -> window 22, generic fold still ROW 1).

§5 STEP 2 MATCHED-NULL PANEL COUNT  — RATIFIED WITH A CHANGE: M = 2000 (was 500).
   Reason: the verdict cuts are calibrated at a 5% false-ROW-1 tail; M=500 estimates
   that tail from ~25 draws (non-trivial Monte-Carlo error in the cut). M=2000 tightens
   the cut for a one-shot adjudication at trivial compute cost (the synthetic panels are
   seconds–minutes). D4's near-perfect separation means the load-bearing verdict is
   insensitive to M; the extra panels mainly stabilise the weaker D1/D2 cuts. M lives
   ONLY in this frozen recipe (no code change: §5 is run at data arrival, blinded).
```

## 1. Discriminators (pre-registered; all declared before data) — unchanged

```text
D1. CROSS-CASE TRANSFER (primary)
    Fit the tipping/EWS->transition mapping on person/domain set A. Predict held-out set B
    with the tipping parameters FROZEN (no refit).
    - VOT-generic prediction: transfer holds (one structure fits all).
    - Per-case FEP: transfer degrades (its bistable priors are case-specific).
    Metric: out-of-sample AUC / R2 on B under frozen-vs-refit; VOT passes only if
    FROZEN-transfer performance is within the pre-set margin of refit performance AND beats
    the frozen-transfer of the FEP comparator.

D2. COMPLEXITY-PENALIZED HEAD-TO-HEAD
    VOT parameter-light tipping model vs the FEP model reproducing the same tipping, with a
    fair parameter penalty (cross-validated predictive density / WAIC / MDL, counting
    effective parameters incl. the FEP bistable-prior parameters).
    VOT passes only if it wins on the PENALIZED score.

D3. UNIVERSAL SCALING SIGNATURES (bifurcation fingerprints)
    Variance and lag-1 autocorrelation diverge toward the threshold; implied recovery
    rate -> 0 (critical slowing). Present -> consistent with a genuine bifurcation;
    absent -> a tuned FEP, not an intrinsic tipping.
    (Power note, frozen 7/2: tau_var does NOT separate the classes — AUC 0.50 vs smooth —
    and is FEP-absorbed on the four real EMA sets; tau_ar1/min_rec are corroborators, and
    tau_ar1 requires missingness <= ~30%. D3 is corroborating, never load-bearing.)

D4. DECLINE->RECOVERY CROSS-CONSTRAINT (hysteresis parsimony) — THE decisive discriminator
    In a real fold the hysteresis width is tied to the SAME parameters governing the
    pre-transition CSD, so the RECOVERY-side threshold is predicted FROM the DECLINE-side
    dynamics (one parameter set, both arms). A fitted FEP fits the arms independently.
    Test: decline-side dynamics predict the recovery-side threshold out of sample with
    parameters shared across arms (leave-one-out shared-hysteresis RMSE). Pass = yes.
    (Power note, frozen 7/2: AUC 1.00 in all 18 realism cells; robust to sigma 0.30 and 30%
    missingness; valid down to ~50 beeps/arm. REQUIRES a recovery arm.)

D5. STRONG-RIVAL GUARD (no strawman)
    The FEP comparator MUST be the strongest honest one: EFE with epistemic value AND
    allowed bistable priors, fit with the SAME data budget and the SAME information VOT
    gets. VOT must beat the BEST FEP, not a naive prediction-error baseline.
```

## 2. Ω̂ non-circularity specification — unchanged

```text
- Ω̂ / CR is built ONLY from EXTERNAL / behavioral endpoints (function, attendance, task
  completion, activity range, relapse/recurrence, dropout, other-rating) at T2/T3.
- Direction coding declared BEFORE seeing the appearance channels (ambiguity rules fixed
  in advance; e.g., "less activity").
- The order operator O* is tested for alignment with THIS external Ω̂ only; never with a
  value-fitted or self-report Ω̂ (regret excluded — re-imports the appearance channel).
- The FEP comparator receives the SAME external endpoint and the SAME predictors. τ/λ are
  frozen from an independent split, never tuned to the value Gap or to O*'s performance.
```

## 3. Pre-committed disposition — unchanged

| Result | Move |
|---|---|
| Tipping present AND D1–D4 pass against the strong FEP (D5) | VOT's collapse-gate is doing **generic/intrinsic** work FEP does not own with equal parsimony — the strongest available upgrade (still narrow: a synthesis with a distinct, parameter-light gate) |
| Tipping present BUT D1–D4 fail (only per-case fits transfer / FEP matches at equal complexity) | the critical-transition structure is real but **not VOT-distinct** → VOT = synthesis / redescription (the pre-declared downgrade) |
| Decline smooth / CSD fails OOS / no scaling signatures | collapse-gate **unsupported** → the anti-rigidity + asymmetry claims lose their empirical basis |

## 4. Frozen operating points (NEW in v0.2; decided 2026-07-02, before target data)

```text
4.1 TRANSITION ANCHORING (from the Kossakowski calibration, readout §3c)
    PRIMARY: the transition point/arm split is taken from the STUDY DESIGN LABEL
    (taper phase / treatment arm / pre-defined decline endpoint). The data-driven
    magnitude detector is a FALLBACK SANITY CHECK only. Basis (recorded 7/2): no single
    magnitude threshold both catches a real gradual clinical onset (fires only at ~0.5z)
    and rejects benign fluctuation (0.5z over-fires 17/36 on WJ3CV). D4 keys off arm
    labels anyway, so the decisive discriminator is unaffected.

4.2 FALLBACK DETECTOR: min_shift in [1.0, 1.5] z, level threshold z=0 (benign-safe
    band from the WJ3CV sweep: 1.0z->4/36, 1.5z->3/36 flags, all large sustained shifts).
    Known and accepted cost: misses gradual onsets — acceptable because anchoring is by
    design label (4.1).

4.3 EWS WINDOW: window = round(N_arm / 3), clipped to [10, 50].   [RATIFIED 2026-07-14, data-blind; see §0.1]
    (Consistent with the recorded recommendation "16–20 for ~60-beep arms; 25–50 for
    denser/longer series"; frozen as a formula so the choice cannot drift per-dataset.)
    Declared per-dataset from design parameters only, before outcome unblinding.
    ENFORCED IN CODE: run_make_or_break.py auto-computes this by default (--window override-only).

4.4 CHANNEL: primary channel = the dataset's mood / negative-affect composite,
    z-scored within person; the exact item list is declared per-dataset from the
    codebook BEFORE outcome unblinding, and is DISJOINT from any endpoint used for
    Ω̂ or for transition labeling.

4.5 DATA-QUALITY GATES (from the realism grid + short-arm check):
    - D4 requires >= 50 beeps per arm; below that the dataset cannot adjudicate ROW 1.
    - tau_ar1 is reported as corroborator only if missingness <= ~30%; NEVER load-bearing.
    - tau_var is reported but pre-declared NON-discriminating (FEP-absorbed).
```

## 5. Matched-null verdict re-calibration (NEW in v0.2; recipe frozen now)

v0.1 said the synthetic-calibrated cuts must be re-calibrated on a matched null
before final adjudication. That is now a frozen procedure:

```text
STEP 1 (on data arrival, BEFORE outcome unblinding): record design parameters only —
   N persons, beeps per arm, missingness pattern, and the per-person noise SD of the
   declared channel. No outcome trajectories are inspected beyond these moments.
STEP 2: simulate M = 2000 panels EACH of smooth_mimic and fitted_jump matched to those
   design parameters (generators: mob_core.py; seed fixed and published).   [RATIFIED 2026-07-14: M = 2000, data-blind; see §0.1]
STEP 3: set every verdict cut used by run_make_or_break.py (D1 transfer margin,
   D2 delta-logloss, D3 tau cuts, D4 loop-width and shared-RMSE cuts) at the values
   that keep the JOINT false-ROW-1 rate <= 5% on EACH rival class separately
   (P(ROW1|smooth_mimic) <= 5% AND P(ROW1|fitted_jump) <= 5%).
STEP 4: publish the calibration artifact (CSV of null distributions + chosen cuts)
   BEFORE running the turnkey on the real outcome channel. Then run the turnkey ONCE.
STEP 5: report the fired disposition row plus ALL D-statistics, including nulls and
   failures, per the repo's null-reporting rule. No re-runs with altered cuts.
```

## 6. Strong-rival operationalization note (NEW in v0.2; closes the D5 escape hatch)

```text
DECLARED: in the implemented pipeline, the FEP comparator's per-case freedom is
operationalized as the per-case flexible model (case x feature interactions) in D2, and
as independent per-arm fitting in D4. This is declared EQUIVALENT, for adjudication
purposes, to the degrees of freedom a bistable-prior EFE spends to match a given tipping:
what is being priced is per-case free parameters, which is exactly the property the
prereg wager turns on. An explicit generative EFE simulation may be added as a
ROBUSTNESS analysis, but it is NOT the criterion — declared now so that neither side can
relitigate the comparator after the verdict (pro-VOT: "the rival was too strong";
pro-FEP: "that's not really FEP").
```

## 7. P3 (external-Ω̂ alignment) implementation status

```text
The Ω̂ non-circularity SPEC is frozen (§2). The TEST is not implemented in the turnkey
(the omega_hat column is wired in the data contract only), because no dataset on disk or
in sight has the external endpoint. IMPLEMENTATION IS DEFERRED until the incoming
dataset's endpoint inventory is known; the implementation must then be written and
frozen BEFORE outcome unblinding, following §2 and the §5 blinding discipline.
H2/D4 adjudication does NOT wait on P3.
```

## 8. Why v0.2 (one paragraph)

The 7/2 calibration produced real, recorded operating decisions that lived only in a
readout, leaving two documents that could drift apart and post-hoc room at data arrival
("which spec was frozen?"). v0.2 makes the frozen surface a single document, converts
"we will re-calibrate" into a blinded, numbered procedure, and closes the comparator
loophole. Nothing about the wager itself moved: the distinctiveness of VOT still rides
entirely on D4's shared decline↔recovery parameter against the strongest FEP, exactly
as staked on 2026-07-01.

## Boundary

This addendum sharpens the make-or-break test; it validates nothing and assumes no
outcome. It concedes that a gate alone is annexable by sophisticated FEP, and stakes
VOT's distinctiveness on generic / parameter-light tipping that transfers across cases
and constrains decline↔recovery jointly, tested against the strongest FEP with a
non-circular external Ω̂. If VOT cannot meet these, the honest disposition is
"synthesis," not "distinct theory."
