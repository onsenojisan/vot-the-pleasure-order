# Status and known issues (added 2026-07-15)

**This package:** concept DOI <https://doi.org/10.5281/zenodo.21366131> — always resolves to the current
version, **21694817** (2026-07-30, *v0.2 + Amendment 1*). The first deposit was
<https://doi.org/10.5281/zenodo.21366132> (2026-07-04), and the frozen `PREREGISTRATION.md` is
byte-identical in both; what the later version adds is §4 below. **Cite the concept DOI**, because
`21366132` predates the amendment and still routes a critical-slowing failure to *collapse-gate
unsupported* rather than `INCONCLUSIVE`.

⚠️ **This file is dated and grows; the deposited copies do not.** Deposited files are not retroactively
edited, so a copy read inside a Zenodo record stops where it stopped: the copy in `21366132` predates §4
entirely, and the copy in `21694817` ends at §4. **§5, §5b and §5c below are in neither deposit**, and
§5c concerns two figures quoted inside §4 that this project has since retired.

This note travels with the package. It records what happened **after** the
preregistration was frozen, plus one known blemish in it.

`PREREGISTRATION.md` is deliberately left exactly as frozen. A preregistration's
value comes from being a pre-commitment, so it is not edited with hindsight.
Everything learned later is recorded here instead, dated.

## 1. Execution status: the test is UN-RUN (as of 2026-07-14)

`PREREGISTRATION.md` §0.1 says the data request was "out and unanswered". That
was true at freeze time and is now out of date:

- The **on-request routes** to the identified recovery-arm datasets (a TRANS-ID
  recovery arm; a bipolar early-warning dataset) **did not yield access** — the
  data holders could not share within available capacity and governance, and this
  project has no institutional home to provide the required ethical oversight.
- An exhaustive scan of the open ESM landscape found **no dataset that meets D4**
  (within-person decline *and* recovery, intensive, >= 50 beeps per arm).
- Therefore, on the preregistration's own terms, the make-or-break test is
  **un-run**.

**Un-run is not falsified, and not withdrawn.** No outcome data ever touched the
frozen spec; the wager stands undecided. The program is **dormant on this test**.
It becomes runnable again if either (a) an intensive dataset with a within-person
decline -> recovery arm becomes accessible, or (b) the project gains an
institutional home able to run this package under proper governance. This package
is built to run entirely on the data holder's machine; no participant-level data
leaves it.

Current public status (direct link):
<https://github.com/onsenojisan/vot-the-pleasure-order/blob/main/CURRENT_STATUS.md>
Repository: <https://github.com/onsenojisan/vot-the-pleasure-order>

## 2. Known issue: §4.2 leaves `min_shift` as a band, not a single frozen value

§4.2 specifies `min_shift in [1.0, 1.5] z` — a **range**, not a single frozen
value. That is inconsistent with the document's own standard: §4.3 deliberately
freezes the EWS window as a *formula* "so the choice cannot drift per-dataset",
while §4.2 does not get the same treatment. It is disclosed here rather than
quietly patched.

**Why it does not reach the verdict.** §4.1 confines the data-driven magnitude
detector to a **fallback sanity check only**; the primary transition anchoring is
the study design label. In the preregistration's own words: "D4 keys off arm
labels anyway, so the decisive discriminator is unaffected." The residual freedom
therefore cannot move the load-bearing adjudication.

**Commitment.** If the test is ever reopened, a v0.3 will freeze `min_shift` to a
single value **before any data is received**, recorded in a changelog. It is not
being changed now: amending a published, frozen preregistration for a parameter
that cannot reach the verdict would cost more in freeze credibility than it gains
in tidiness.

## 3. Note on `--M` (code aligned to the recipe on 2026-07-15)

The ratified recipe is **M = 2000** (§0.1 and §5 STEP 2).

`calibrate_null.py` originally shipped with an `--M` default of 500, because the
2026-07-14 ratification was documentation-only and did not require touching code
(§0.1: M "lives ONLY in this frozen recipe (no code change: §5 is run at data
arrival, blinded)"). That left a hazard for a package meant to be run by a data
holder: anyone omitting `--M` would silently calibrate at M = 500 — the exact
condition §0.1 rejected ("M=500 estimates that tail from ~25 draws (non-trivial
Monte-Carlo error in the cut)").

The default is therefore now **2000**, matching the ratified recipe. This changes
**no preregistered commitment**: M = 2000 was already ratified data-blind on
2026-07-14, so the code now agrees with the frozen recipe instead of
contradicting it. No new choice was made, and `PREREGISTRATION.md` is untouched.

## 4. AMENDMENT 1 (2026-07-27): disposition row 3 — "unsupported" → "inconclusive"

**This is an amendment to a pre-committed disposition, not a note about one.**
It is made **before any outcome data has touched the frozen spec** — the test is
still un-run (§1) — and it is recorded here rather than in `PREREGISTRATION.md`,
which stays exactly as frozen.

### What changes

§3's disposition table, third row, as frozen:

> | Decline smooth / CSD fails OOS / no scaling signatures | collapse-gate **unsupported** → the anti-rigidity + asymmetry claims lose their empirical basis |

**As amended:**

> | Decline smooth / no scaling signatures | collapse-gate **unsupported** → the anti-rigidity + asymmetry claims lose their empirical basis |
> | **CSD fails out-of-sample** | **INCONCLUSIVE — measurement-limited.** Not evidence against the collapse gate. The theory is neither upgraded nor downgraded on this result alone. |

The other two rows are unchanged. D1–D5, §4's operating points and §5's
recalibration recipe are unchanged.

### Why

The row as frozen treats **not detected** as **not there**. Those are different
claims, and the difference is not incidental in this domain:

- **Helmich MA, Schreuder MJ, Bringmann LF, Riese H, Snippe E, Smit AC (2024),
  *Nature Reviews Psychology*, doi:10.1038/s44159-024-00369-y** argues that early
  warning signals based on critical slowing down are *"not generic indicators of
  upcoming transitions in any and every system"*, and that critical slowing may be
  absent or undetectable for reasons independent of whether a fold exists — the
  wrong bifurcation type, a transition faster than CSD manifests, variables not
  aligned with the direction of resilience loss, or larger processes obscuring it.
  A meta-analysis of 126 ecosystems detected EWS before **13%** of transitions.
- **Measurement, 2026-07-27** (four acquired ESM datasets, 225 persons,
  descriptive): median within-person state separation **1.92 SD**, median **93**
  observations per person. At that separation, distributional methods for
  establishing two-state structure have no power at any sample size; a
  persistence-based method reaches usable power only near ~1,500 observations per
  person.

So a CSD failure on data of this kind is at least as consistent with the
instrument not working as with the structure not existing. The frozen row would
have converted the first into evidence for the second.

### What this does NOT do

- It does **not** weaken the downgrade. Row 2 — *tipping present but D1–D4 fail →
  synthesis / redescription* — is untouched, and remains the pre-declared downgrade.
- It does **not** create an escape. "Inconclusive" is not a safe harbour: a test
  that can confirm but cannot cleanly disconfirm is a worse position for a theory
  than a clean negative, because it approaches unfalsifiability. That cost is
  accepted here rather than hidden.
- It does **not** repair the underlying defect, which is that **D4 estimates
  critical-slowing parameters on the decline arm** in order to predict the
  recovery threshold, and no instrument for the fold that bypasses CSD is in hand.
  A CSD-free pre-gate was built (`structure_gate.py`, `hmm_gate.py`) and
  establishes only that two states exist — not that CSD is measurable. That half
  remains open.

### Provenance

Amendment written 2026-07-27, blind to any outcome data, in `vot-empirical-workbench`.
The frozen `PREREGISTRATION.md` is byte-unchanged.

---

## 5. Known issue in Amendment 1's own wording (2026-07-30)

**This section postdates the deposit.** Amendment 1 was published on 2026-07-30 as Zenodo
`21694817` (version string `v0.2 + Amendment 1`). The copy of this file *inside that record*
ends at §4 and does not contain this section. Files on a published Zenodo record are
immutable, so this is disclosed here rather than patched there — the same reason §2 exists.

**The issue.** Amendment 1 labels the CSD-failure row
`INCONCLUSIVE — measurement-limited`. The verdict is right; **the label is not established.**

On a full re-reading of Helmich et al. 2024 on 2026-07-30, its *Grounding the theory*
section gives four ways a transition can lack critical slowing down, and they are not the
same kind of thing:

1. the wrong bifurcation type, or a transition faster than CSD can manifest;
2. an abrupt change in a control parameter;
3. **external forcing** — a strong perturbation, with **no bifurcation involved**;
4. the attractor **evolving gradually from healthy to disordered without destabilising** —
   again **no bifurcation**.

Items 3 and 4 are not measurement limitations. They are **rival structural hypotheses to
the collapse gate.** Moreover the fold sits in the class of transitions for which CSD *is*
theoretically expected, so under a fold-specific hypothesis a CSD failure carries some
evidential weight against the fold rather than none.

`MEASUREMENT-LIMITED` therefore names one cause out of a set the review itself shows is not
identifiable — and it is the cause favourable to the theory. §4's body text is careful on
this point ("at least as consistent with the instrument not working as with the structure
not existing"); only the two-word label overreaches.

**Not corrected, disclosed.** Candidate wording if a later version is ever cut:
`INCONCLUSIVE — cause not identifiable (measurement failure, or no fold)`. **The disposition
itself does not change**: the outcome was already non-evidential in both directions, so
nothing downstream of §4 moves.

**A second, larger point from the same reading, recorded here because it bears on §4's
closing claim.** §4 says the CSD-free pre-gate "establishes only that two states exist — not
that CSD is measurable", and treats that as half a repair. Helmich et al.'s *Moving forward*
section argues the opposite ordering: establish the structure by CSD-free means **first**,
because otherwise absent EWS can always be attributed to system misspecification — which is
exactly what §4's own routing does. On that reading the pre-gate is not half a repair; it is
the whole prescribed route, and this preregistration has it as a corroborator. Full argument in
`outputs/ews_critique_helmich_2024_assessment.md`, second reading.

> 🛑 **CORRECTED 2026-08-10.** This paragraph originally priced the cost as *"the pre-gate is blind
> below ~6 SD separation; measured separation is 1.92 SD median, so promotion is not currently
> affordable."* **The 1.92 SD figure was retired on 2026-07-30** — in both units it was computed in —
> and must not be quoted. The blindness figure survives, on a benchmark matched to the data's own
> autocorrelation: **power stays under 11% below 6 SD.**
>
> **What replaced the retired number is worse for the argument, not better.** A run on 2026-08-09
> (`outputs/separation_estimability_result_2026-08-09.md`, 100 reps/cell, rules frozen before
> execution) found that at the dwell the observed autocorrelation implies, **separation is not
> estimable at all** — the estimator is bimodal, collapsing below 1 SD in 24–39% of replications even
> at a true 5–6 SD separation, and length does not help. So the honest statement is no longer *"our
> separation is too low to afford promotion."* It is **"we cannot say what our separation is."**

### 5b. §4 overstates the absence of an instrument (found 2026-07-30)

> 🛑 **READ THIS BEFORE THE SECTION — corrected 2026-08-10.** The core finding below stands: a
> CSD-free hysteresis instrument exists, so §4's stated reason the defect *"cannot be repaired"* is
> wrong. **Three of the section's supporting points do not stand**, and each is marked in place:
>
> 1. **The separation figure (item 1) is retired.** `1.92 SD` must not be quoted, and as of
>    2026-08-09 the project cannot state its separation at all.
> 2. **Item 2's arrow is invalid.** *"No multilevel form, therefore D1 has no vehicle"* — **D1 as
>    frozen is a procedure, not an instrument**, and needs no multilevel model.
> 3. **The sibling question at the foot is dissolved, and the reason is larger than the question.**
>    HysTAR **cannot carry the distinctive claim at all** — not a fit preference, a scope boundary.
>
> Nothing is deleted. Corrections sit at each point, because a correction collected at the end of a
> document is a correction most readers never reach.

§4 says, as the reason the underlying defect cannot be repaired:

> "no instrument for the fold that bypasses critical slowing is in hand"

**That is not accurate.** A CSD-free hysteresis detector with a published R package has existed
since 2023: the **hysteretic threshold autoregressive (HysTAR) model** (de Jong, Ryan, van der
Maas & Hamaker, doi:10.31234/osf.io/zrcft; package `hystar`). It is the hysteresis reference
Helmich et al. 2024 themselves cite. It estimates two direction-dependent thresholds and
decides hysteresis by information-criterion comparison. **Critical slowing plays no part in it.**

**What is genuinely absent is narrower, and is what §4 should have said:**

1. HysTAR is **not validated at this project's state separation.** Its simulations use regime
   separations of 3.75 and 5 SD (plus an equal-means edge case the authors call atypical). At the
   equal-means condition the authors' preferred criterion selects correctly only ~10% of the time;
   at 3.75 SD, ~93%. ~~The measured within-person separation here is **1.92 SD** median — between
   the edge case and the lowest working condition.~~
   🛑 **CORRECTED 2026-08-10: `1.92 SD` is retired and must not be quoted** (2026-07-30, in both
   units it was computed in). **And it cannot simply be replaced with a better number** — the
   2026-08-09 estimability run found separation **not estimable** in this regime. So the feasibility
   check against HysTAR's validated range is not *"we fall short of it"* but
   **`NOT CHECKABLE — the quantity is not identified here`**.
2. ~~It has **no multilevel form** (one exists for the non-hysteretic TAR), so it cannot carry
   D1's frozen-parameter cross-case transfer.~~ **The absence is real; the consequence drawn from
   it was not.** 🛑 **CORRECTED 2026-08-08: D1 as frozen is a procedure, not an instrument** — a
   cross-validation harness wrapped around per-case estimators, which needs no multilevel model and
   runs on exactly the N=1 estimators HysTAR provides. Its deciding `n` was computed on 2026-08-08
   and is **4 cases**; the real blocker is cross-case decline↔recovery data, the same wall as D4.
   **What survives is the narrow version:** the genericness test and the hysteresis test cannot
   presently be run **inside one model**.
3. It tests **whether hysteresis exists** — not D4's actual stake, which is that the
   recovery-side threshold is predicted *from* decline-side dynamics under one shared parameter
   set against a parsimony penalty. **HysTAR is not D4**, and D4's specific claim survives.

**Why the overstatement matters.** §4 used "no instrument is in hand" to justify why the CSD
dependency cannot be repaired. The repair path exists; it is **priced, not absent.**
~~The honest blocker is the 1.92 SD separation and the missing multilevel form — the same wall the
pre-gate hit, which is now independently corroborated by a published method's own validation
range.~~

🛑 **CORRECTED 2026-08-10. Both named blockers were wrong, and the corrected version is harder, not
softer.** The multilevel gap does not block D1 (item 2). The separation figure is retired, and the
quantity turned out **not to be estimable** in this regime (item 1) — so the blocker is not a
number the project falls short of but **a number it cannot obtain**. The corroboration claim goes
with it: a retired figure cannot be corroborated by anything.

**What is left standing is narrower and still fatal to "cannot be repaired":** an instrument exists,
this project has not run it, and three commitments are owed before it could be
(`outputs/hystar_aiccp_freeze_v0_1_2026-08-08.md`) — what the control variable `z` is for ESM affect
data, how a single-outcome model carries a cross-channel operator, and a feasibility check that
cannot currently be performed. **"Not repaired" is true. "Cannot be repaired" is not.**

**Two operational consequences, recorded before any run:**

- **If HysTAR is ever used, the model-selection criterion must be frozen in advance to AICcp.**
  In the authors' no-hysteresis cells, BIC selects the *hysteretic* model roughly half to
  three-quarters of the time. Choosing the criterion after seeing data would let a null be
  converted into a fold. ✅ **DONE 2026-08-08** — frozen before any run and before any separation
  estimate existed to check feasibility against: `outputs/hystar_aiccp_freeze_v0_1_2026-08-08.md`.
  **A run using BIC or a post-hoc criterion has a void verdict**, and a negative result is
  `INCONCLUSIVE`, not `NO HYSTERESIS`.
- **A threshold-coverage requirement is needed, not only observations per arm.** One simulation
  cell returns 0% correct selection because the observed control values never came near the true
  threshold. D4's "≥50 beeps/arm" gate does not encode this.

~~**Also unresolved, and a theory question rather than a defect:** the authors note that a
hysteretic HMM with autoregression and the HysTAR model differ *only* in their switching
mechanism — probabilistic versus **deterministic** — and that theory should decide. This project
built the probabilistic one (`hmm_gate.py`) while positing a fold, which is deterministic. On the
authors' own criterion the fold selects HysTAR. **Not corrected here; flagged as owed.**~~

🛑 **WITHDRAWN 2026-08-08/09, and what replaced it is bigger than the question.**

**The inference was invalid.** *"Posits a fold, folds are deterministic, therefore deterministic
switching"* conflates the **geometry** of the state space with the **mechanism of transition**. The
standard bistable formulation — the one this project's entire EWS apparatus assumes — is a
deterministic fold **plus noise**: structure deterministic, switching stochastic, both at once.
Positing a fold commits the theory to the geometry and says **nothing** about the switching
mechanism. **So no sibling is selected, and the "decision owed" was not the decision owed.**

**The larger consequence, from the commitment written on 2026-08-09**
(`vot-theory-stack/docs/TRANSITION_MECHANISM_COMMITMENT_V0_1.md`): this theory commits to
**`B`-tipping in a stochastically perturbed system** — bifurcation-induced, with stability changing
before the transition, and noise required as the **probe** rather than the cause, because variance
and AR(1) are fluctuation statistics and there is nothing to compute them from otherwise.

⚠️ **In HysTAR, critical slowing plays no part — because critical slowing exists only in a
stochastically perturbed system.** So adopting HysTAR as *the* instrument would not swap an
implementation. It would **discard the mechanism the one surviving distinctive claim runs on.**

**Where that leaves the two, and this is a scope boundary rather than a preference:**
**HysTAR can never carry the distinctive claim.** It is a CSD-free **structure** test, and belongs
**first**, which is the ordering Helmich et al. prescribe (§5 above). `hmm_gate` is the
**prediction** test, and comes after. They are not competitors, and neither replaces the other.

🔻 **Direction: this runs against the theory on net.** It withdraws an argument that pointed at a
cleaner instrument, and it removes the hoped-for rescue of the `0/100` persistence result — HysTAR
is not a persistence-route implementation, so that route is not waiting behind a sibling choice.

---

### 5c. Amendment 1's own rationale rests on two retired numbers (found 2026-08-10)

**§4 above is deposited** as part of `10.5281/zenodo.21694817`. **It is not edited here**, and it
should not be: a frozen record's value comes from not being rewritten. What follows is the
disclosure instead.

§4's *Why* section supports the amendment with two measurements, and **both have since been
retired by this project's own later work**:

- **"median within-person state separation `1.92 SD`"** — retired **2026-07-30**, in both units it
  had been computed in, and **must not be quoted**. Worse, as of **2026-08-09** the quantity is not
  merely unmeasured but **not estimable** in this regime.
- **"a persistence-based method reaches usable power only near `~1,500` observations per person"** —
  retired **2026-08-08** (`10.5281/zenodo.21845739`). Within the model class the gate assumes, the
  persistence route returns **0/100 at the observed autocorrelation**, so `~1,500` is not its price
  and **no `N` is**.

⚠️ **The amendment's disposition survives, and the corrected numbers make its case stronger rather
than weaker.** The claim §4 needed was that a CSD failure on data of this kind is at least as
consistent with the instrument not working as with the structure not existing. That still holds, on
better-derived figures: distributional detection is under **11% powered below 6 SD** on a benchmark
matched to the data's own autocorrelation, and the persistence alternative is unusable rather than
expensive. **Nothing downstream of §4 moves.**

**What is owed is a metadata addendum on `21694817`, not a new version** — the precedent used for
`20689077`, `21599880`, `21205718`, `21589463` and `21767213`. The frozen files stay frozen; what
changes is the record's `notes`, so that a reader who never opens this file still learns that two
quoted figures are withdrawn. **Author's browser task; not done at the time of writing.**

🔻 **The pattern, stated because it is the third instance in this corpus:** the numbers were retired
in the working repository and the *deposit that cites them* was not revisited. A retraction reaches
the place the work happened and stops there.

Full survey, including the wider catastrophe-flag reading list, in
`outputs/hysteresis_prior_art_survey_2026-07-30.md`.

---

### 5d. "Priced, not absent" is withdrawn — the repair path has no price (found 2026-08-13)

🛑 **Read this before §5b. §5b's conclusion is the one being corrected, and the correction runs
against the theory even though it partly vindicates the frozen §4 it was written to criticise.**

§5b closes with *"The repair path exists; it is **priced, not absent.**"* The same sentence is in the
`notes` field of the deposit `10.5281/zenodo.21694817` (published 2026-08-11) and in this
repository's `ZENODO_RECORDS.md`. §5b also states that *"three commitments are owed before it could
be [run]."*

**All three commitments have now been discharged, and the test still cannot be run.**

| | Resolution |
|---|---|
| **B-1** — what the control variable `z` is for ESM affect data | **`NO CANDIDATE IN THE ACQUIRED DATA`** (2026-08-13) |
| **B-2** — how a single-outcome model carries a cross-channel operator | **Resolved: the cross-channel instrument exists** (2026-08-13) |
| **B-3** — the feasibility check | `NOT CHECKABLE — the quantity is not identified in this regime` (2026-08-09) |

#### What was found

Every column of all four acquired ESM datasets — **165 columns** — was screened against a rule
frozen and committed before execution, each column carrying its exogeneity judgement and the reason
for it.

- 🔴 **Three of the four datasets contain no exogenous per-beep variable at all.** In two of them
  *every* substantive column is an affect, symptom or appraisal item; the third has one two-level
  design flag. **For three of the four there was never a candidate to fail.** This is a property of
  the instrument class: an ESM protocol of this design **measures the state, not the driver.**
- 🔴 **The one designed control parameter fails on bidirectionality.** The best-behaved variable in
  the entire screen — ten levels, 1,476 observations, no missing — is a monotone taper: **nine
  decreases, zero increases.** One sustained descent identifies **one** threshold, which is TAR and
  not HysTAR. That is **the recovery arm**, the same blocker as D1, D4 and the animal track, arriving
  for the fourth time from the instrument side.
- **B-2 resolved *positively* and moved nothing.** A hysteretic model with a vector outcome driven by
  a single hysteresis variable has existed since 2019 (Chen, Than-Thi & So, *J. Stat. Comput. Simul.*
  **89**(2), 191–210). It still needs the `z` that B-1 has just shown is absent. **A model taking `k`
  channels and one `z` is blocked by a missing `z` exactly as hard as one taking a single channel.**

#### What is withdrawn, and what survives

- 🛑 **WITHDRAWN: *"priced, not absent"*, and *"three commitments are owed"*.** There is **no price**.
  The blocker is a **variable that was never collected**, in datasets whose design does not collect
  one. *"Acquire a longer or larger ESM dataset"* is not a route to it.
- ✅ **SURVIVES, and is stronger than when §5b was written: an instrument exists.** §4's stated reason
  — that no CSD-free instrument for the fold is in hand — is still **factually wrong**, and B-2 makes
  it more wrong, since even the cross-channel version exists.
- ⚠️ **The direction is uncomfortable and is stated rather than left implicit.** §5b was written to
  show that §4's *"cannot be repaired"* overstates the case. On today's evidence **§4's conclusion is
  closer to right than §5b allowed — for a reason §4 did not give.** Not *no instrument*: **no
  control variable.** §5b overcorrected in the theory's favour, and this is the second time a
  correction notice in this corpus has done that.
- 🛑 **Do not read "all three discharged" as `SPECIFIABLE`.** Nothing is owed, and the test is now
  **specified enough to see that it has no data** — a different and worse position than being
  un-specified.
- **Unchanged:** AICcp stays frozen for any future run; a negative result stays `INCONCLUSIVE`, not
  `NO HYSTERESIS`; **HysTAR is still not D4**; and the 2026-08-09 scope boundary — that this model
  class can never carry the distinctive claim, because critical slowing plays no part in it — binds
  the 2019/2021 successors exactly as it binds HysTAR.

#### A second public surface, stale for longer, found in the same pass

⚠️ **The note.com article of 2026-07-31 — the public downgrade — states the price as `~1,500`
observations per person.** That figure was **retired on 2026-08-08** by this project's own
re-derivation, and the retirement reached the deposit `10.5281/zenodo.21845739` and the `notes` of
`21767213` **on the same day**. It never reached the article.

🔻 **So a public article has been carrying a withdrawn specification for five days, and today's
finding adds a second withdrawn claim to the same article** (*"the repair path is not absent, it has
a price"*). **Both run in the theory's favour**, because a route with a price reads as reachable.
**This is the documented failure mode reaching a public surface rather than an internal one.**

#### What is owed

1. ✅ **DONE AND VERIFIED 2026-08-13 — a metadata addendum on `21694817`.** `notes` **2,933 → 6,470
   chars**, the pre-existing 2,933 preserved byte-for-byte and the new `SECOND CORRECTION NOTICE`
   appended. **DOI, version (`v0.2 + Amendment 1`), publication date (2026-07-30), title, the
   5,653-char description and all three file md5s verified unchanged** — snapshotted before the write
   and **re-read from the API after publication rather than trusting the publish response**, with the
   edit gated to abort if anything but `notes` had moved. **No leftover draft and no unpublished edit
   state.** No new version was cut. Precedent: `20689077`, `21599880`, `21205718`, `21589463`,
   `21767213`, and this record on 2026-08-11.
   - ⚠️ **The old closing pointer (*"section 5, 5b and 5c"*) was deliberately NOT rewritten.** Every
     correction in this corpus preserves the existing characters and appends — and a correction record
     that can be edited is one a reader cannot trust, which is why the 2026-08-03 defect in an errata
     field was fixed by publishing a further paragraph rather than by rewriting it. **The cost is one
     incomplete enumeration; the URL it carries is this same file**, which now contains §5d.
2. ✅ **DONE AND VERIFIED 2026-08-13 — the note.com article carries both withdrawals.** A dated block
   at the head plus **ten in-place corrections collected as an erratum list at the foot**, verified
   against the live page: the two headline retractions, the `~1,500` sites, and the closing sentence
   (which changes the article's landing point — *"what was learned is that it cannot be run on data of
   this shape"*, not *"the price is now known"*). **The original 22,565-character body is untouched**,
   confirmed by the absence of any paste damage in it.
   - ⚠️ **One defect was introduced and repaired the same hour, and it is worth keeping because it is
     this corpus's recurring shape: the correction block asserted a property of itself that was false.**
     It read *"I have put the corrections at the relevant places"* while all ten sat at the foot. **A
     document claiming a property it does not have** — the same defect as a frozen rule asserting it had
     been committed while untracked, twice in one day. Repaired by correcting the sentence rather than
     by moving ten blocks, because moving them would have risked the paste damage the body had escaped.
   - **Known and accepted, not a defect to re-open:** markdown emphasis in the added text renders as
     literal `**`, since note does not parse markdown on paste. **Author's call, cosmetic, and confined
     to the added text.**
3. This section. **§5b is not edited**, per disclose-don't-patch.
