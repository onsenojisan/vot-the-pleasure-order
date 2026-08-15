# Amendment 2 — Dataset Search Log (2026-08-15)

Status: **completed bounded search; no eligible target identified**

Protocol: [Dataset Eligibility And Search Protocol](AMENDMENT2_DATA_ELIGIBILITY_PROTOCOL.md)

Registry: [`amendment2_dataset_screening.v0.json`](simulations/amendment2_dataset_screening.v0.json)

## Declared Scope

### openESM catalogue census

- Source: <https://github.com/openesm-project/openesm>
- Public catalogue: <https://openesmdata.org/datasets/>
- Snapshot commit: `4dcff8ec5598e7a5828efe971122050f451443d1`
- Enumeration rule: every `datasets/**/*_metadata.json` file at that commit
- Enumerated records: 62
- Fields screened: `additional_comments`, `topics`, `participants`, and every
  feature's `name`, `description`, `construct`, `coding`, and `comments`
- Case-insensitive shortlist expression:
  `\b(treat(?:ment|ed|ing)?|therap(?:y|ies|eutic)?|intervention|baseline|post[- _]?baseline|taper(?:ing)?|medicat(?:ion|ed)?|recover(?:y|ing)?|randomi(?:s|z)(?:ed|ation)|trial)\b`

The expression shortlisted 11 of 62 records. The other 51 are recorded by ID
in the registry as `NOT_SHORTLISTED_METADATA`; this means only that their
catalogue metadata did not declare a phase/intervention term.

Reproduction command (from this repository):

```powershell
python simulations/reproduce_openesm_screen.py path/to/openesm simulations/amendment2_dataset_screening.v0.json
```

### Zenodo targeted query set

- API: <https://zenodo.org/api/records>
- API documentation: <https://developers.zenodo.org/>
- Search syntax guide: <https://help.zenodo.org/guides/search/>
- Search date: 2026-08-15
- Fixed request parameters: `size=25`, `sort=bestmatch`

The following queries were run exactly as recorded. The union contained five
Zenodo records representing four study concepts.

| ID | Exact `q` value | Total | Record IDs |
|---|---|---:|---|
| Z1 | `resource_type.type:dataset AND ("experience sampling" OR "ecological momentary assessment") AND (recovery OR tapering OR transition)` | 1 | `6640290` |
| Z2 | `resource_type.type:dataset AND ("experience sampling" OR "ecological momentary assessment") AND (relapse OR remission OR deterioration OR improvement OR "critical transition")` | 1 | `6640290` |
| Z3 | `resource_type.type:dataset AND ("experience sampling" OR "ecological momentary assessment") AND (intervention OR treatment) AND (longitudinal OR daily OR intensive)` | 4 | `6640290`, `8186103`, `17243648`, `17249917` |
| Z4 | `resource_type.type:dataset AND ("experience sampling" OR "ecological momentary assessment") AND ("pre post" OR "pre-post" OR "before and after")` | 1 | `14999348` |

Reproduction command:

```powershell
python simulations/reproduce_zenodo_screen.py simulations/amendment2_dataset_screening.v0.json
```

The command compares the live totals and record-ID sets with the dated result
and fails on drift. This is a targeted query set, not a complete Zenodo census;
the frozen IDs preserve what was reviewed even if the live index changes.

### Known transition-enriched routes

- TRANS-ID Tapering and TRANS-ID Recovery:
  <https://www.transid.nl/?lang=en>
- Bipolar early-warning study and its linked public supplement:
  <https://research.rug.nl/en/publications/anticipating-manic-and-depressive-transitions-in-patients-with-bi>

The public TRANS-ID description treats tapering and recovery as separate
subprojects and populations. A target-blind Methods review also closes the
bipolar lead before access: its protocol labels abrupt increases on manic or
depressive symptom scales, not a recovery arm. The paper says participant data
may be available on reasonable request, but access cannot repair this D4 design
mismatch. The linked public supplement is analysis R code, not participant-level
time-series data.

Future request-only candidates must use the
[Metadata-Only Controlled-Access Gate](AMENDMENT2_METADATA_ONLY_ACCESS_GATE.md)
before any participant-data request.

## Manual Review Of The openESM Shortlist

| ID | Why shortlisted | Disposition from metadata |
|---|---|---|
| `0010_geschwind` | baseline/post-baseline mindfulness periods | two periods, but not labelled decline and recovery; no separate action and bidirectional forcing mapping |
| `0014_habets` | medication plus Parkinson ON/OFF state | target-blind methods review closes the lead: 98 planned beeps total, no labelled decline/recovery arms and no separate exogenous forcing |
| `0022_menghini` | `survey_type` baseline/work | 21 total time points; cannot supply >=50 observations in each of two arms |
| `0024_hasselhorn` | two phases and `treatment` field | phases manipulate beep frequency (3 then 9 or 9 then 3), not decline/recovery dynamics; 84 total time points |
| `0033_fisher` | “randomized” | refers to randomized item order; no decline/recovery design |
| `0036_bosley` | “randomized” | refers to randomized item order; 45 total time points |
| `0058_gainey` | baseline/treatment terms | metadata says some participants completed baseline but not ESM; 42 total time points and no paired arms |
| `0060_beck` | larger intervention project | target-blind paper/codebook review closes the lead: the analysed target is naturalistic trait-plus-state ESM with no treatment, condition, phase or arm variable |
| `0061_merolla` | intervention project | 60 total time points, so two >=50-observation arms are impossible |
| `0062_neubauer` | randomized | refers to quasi-randomized prompts; 84 total time points and no paired arms |
| `0075_ballou` | baseline-day variables | 30 daily time points and no paired arms |

## Target-Blind Design Follow-Up

The two closest open leads were reviewed on 2026-08-15 without inspecting
participant-level outcome values. Public paper pages contain aggregate results,
but those results were not used for these dispositions; only methods,
questionnaire definitions and codebook structure were used.

### `0014_habets`

- Sources: <https://openesmdata.org/datasets/0014_habets/> and the paper's
  Methods/Questionnaire sections at <https://mhealth.jmir.org/2020/5/e15628>
- Design: seven semi-random prompts per day for 14 days, for 98 planned prompts
  total; ordinary free-living medication intake and self-reported ON/OFF state
- Disposition: `BLOCKED_D4`. Two arms of at least 50 observations are impossible
  under the planned schedule, no decline/recovery arms are assigned, and no
  separate exogenous bidirectional forcing variable is declared.

### `0060_beck`

- Sources: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9793429/> and the official
  codebooks at
  <https://github.com/emoriebeck/behavior-prediction/tree/main/01-codebooks>
- Codebook snapshot:
  `emoriebeck/behavior-prediction@24ab1c080faa691fccf9192b7dd87e6b8fdda7f6`
- Design: naturalistic trait and state ESM for idiographic prediction. The
  codebooks group psychological, situational and time variables and contain no
  treatment, condition, phase or arm variable.
- Disposition: `BLOCKED_D4`. The note that this dataset came from a larger
  intervention project does not create decline/recovery arms in the analysed
  target. No separate exogenous forcing or independent non-self-report endpoint
  is declared.

### `bipolar_early_warning`

- Sources: the paper's Methods and data-availability statement at
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8994809/> and the official
  supplementary-record page at
  <https://research.rug.nl/en/datasets/additional-file-2-of-anticipating-manic-and-depressive-transition/>
- Design: five EMA questionnaires per day for four months plus weekly manic and
  depressive symptom questionnaires. A transition is an abrupt increase of at
  least six points within one week on either symptom scale.
- Disposition: `BLOCKED_D4`. The public protocol declares no labelled recovery
  arm, agent-action stream, exogenous bidirectional forcing or independent
  non-self-report endpoint. Participant data are request-only, but access is no
  longer the deciding blocker.

No participant-level outcome values or published aggregate results were used
for this disposition.

## Target-Blind Review Of Zenodo Hits

No participant-level outcome values or published aggregate results were used
for these dispositions. Reviews were limited to public record descriptions,
protocol/design materials and schema-level repository descriptions.

| Record | Design-only finding | Disposition |
|---|---|---|
| [ADARP `6640290`](https://zenodo.org/records/6640290) | four EMA prompts/day for up to 14 days (at most 56 total); outpatient recovery is context, not paired decline/recovery arms | `BLOCKED_D4` |
| [DIAPASON `8186103`](https://zenodo.org/records/8186103) | patients versus matched healthy controls; no same-person decline/recovery arms; participant files restricted | `BLOCKED_D4` plus access blocker |
| [Soundscape pilot `14999348`](https://zenodo.org/records/14999348) and [protocol `14946672`](https://zenodo.org/records/14946672) | baseline/endline surveys and participatory activities are not intensive decline/recovery arms | `BLOCKED_D4` |
| LIFETRACE [`17243648`](https://zenodo.org/records/17243648), [`17249917`](https://zenodo.org/records/17249917), and [analysis repository](https://github.com/USI-PCC/LIFETRACE) | 59 adults in a daily walking protocol versus 29 controls; one-direction intervention exposure, not same-person decline/recovery or bidirectional forcing | `BLOCKED_D4` plus access blocker |

The LIFETRACE records have separate Zenodo concept identifiers, so no formal
version relationship is asserted. They have the same title and describe the
same 14-week study; both search records are retained while the study is counted
once for eligibility review.

## Result

No dataset eligible for the blinded Amendment 2 preflight was identified in
the declared 2026-08-15 openESM census, Zenodo query set and known external
routes. This is a snapshot-bounded search result, not an established absence
from the wider data landscape.

The next legitimate empirical move is one of:

1. identify a new request-only route and clear the metadata-only access gate
   before seeking participant data;
2. extend the same recorded screening procedure to another declared catalogue
   or registry, with exact queries and immutable result identifiers;
3. prospectively collect the decline/recovery, action, forcing and endpoint
   measurements together.

Until one route clears the protocol, Amendment 2B remains a template and the
only permitted outcome is `NO AMENDMENT 2 VERDICT`.
