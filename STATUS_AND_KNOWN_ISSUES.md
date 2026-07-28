# Status and known issues (added 2026-07-15)

**This deposit:** <https://doi.org/10.5281/zenodo.21366132>

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
