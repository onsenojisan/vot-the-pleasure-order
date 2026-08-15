# Amendment 2 — Dataset Eligibility And Search Protocol

Status: **prospective screening rule; not an empirical verdict**

Version: 0.1

Date: 2026-08-15

Governed by: [Amendment 2A](AMENDMENT_2A_GOVERNANCE_RULES.md)

## Purpose And Claim Limit

This protocol decides which datasets may advance to the
[Amendment 2 Data Preflight](AMENDMENT2_DATA_PREFLIGHT.md). It also makes a
catalogue search re-runnable. It does not certify power, identifiability,
runnability or the truth of VOT.

A search may conclude only:

> No eligible dataset was identified in the declared sources, snapshot and
> screening procedure.

It must not conclude that no suitable dataset exists. An inaccessible dataset,
an unindexed dataset and a dataset whose public metadata is incomplete remain
different possibilities.

## Two Eligibility Tracks

### Track A — frozen D4-dynamics

The target must declare all of the following without inspecting the target
outcomes:

1. the same persons contribute a labelled decline arm and a labelled recovery
   arm;
2. each arm has at least 50 planned or available observations per analysed
   person;
3. the time unit and arm boundary are recoverable;
4. the data can be accessed and analysed under a stated licence or governance
   route.

Track A does not require P3. It implements the frozen D4 design boundary and
does not amend the preregistration or Amendment 1.

### Track B — Amendment 2 comparisons

Track B starts with Track A and additionally requires metadata sufficient to
map:

- an observed state `y_t`;
- an agent-selected action, or prospectively justified action proxy, `a_t`;
- an exogenous forcing/control variable `u_t` with adequate coverage in both
  directions;
- proof that `a_t` and `u_t` are different recorded variables with different
  causal roles;
- timestamps, missingness and dropout handling.

One variable cannot serve as both `a_t` and `u_t`. Absence of `a_t` blocks D5;
absence of bidirectional exogenous `u_t` blocks the two-sided structural
comparison. Neither absence counts for VOT.

An independent non-self-report P3 endpoint is an additional requirement only
for S2 / an upgrade of the core claim. Its absence does not by itself block
D4-dynamics or D5.

## Screening Stages

| Stage | Question | Permitted result |
|---|---|---|
| S0 record | Is the candidate, date and primary evidence URL recorded? | record or reject as undocumented |
| S1 access | Is participant-level analysis possible under a stated route? | open, controlled/request, unavailable or unknown |
| S2 D4 design | Are same-person decline and recovery arms declared with >=50 observations each? | pass, blocked or unknown |
| S3 action | Is `a_t` observed and prospectively defensible? | pass, blocked or unknown |
| S4 forcing | Is a separate, exogenous, bidirectional `u_t` observed? | pass, blocked or unknown |
| S5 P3 | Is an independent endpoint present? | core-capable, core-blocked or unknown |
| S6 preflight | Has a blinded manifest cleared the necessary-condition checker? | preflight candidate or not advanced |

`unknown` never means `pass`. A metadata-only screen may shortlist a dataset,
but only a target-blind schema/codebook review may advance it to S6.

## Search Procedure

Every search run must freeze:

1. search date;
2. each source URL and, where possible, repository commit;
3. number and identifiers of all enumerated records;
4. exact fields and regular expression used for automated shortlisting;
5. a manual disposition for every shortlisted record;
6. known request-only or restricted routes considered separately;
7. limitations and the bounded conclusion.

The machine-readable record is
[`simulations/amendment2_dataset_screening.v0.json`](simulations/amendment2_dataset_screening.v0.json).
Validate it with:

```powershell
python simulations/validate_dataset_screening.py simulations/amendment2_dataset_screening.v0.json
```

To reproduce the openESM census and shortlist from an exact local checkout:

```powershell
python simulations/reproduce_openesm_screen.py path/to/openesm simulations/amendment2_dataset_screening.v0.json
```

The command refuses a checkout whose `HEAD` differs from the recorded commit.

## Status Vocabulary

- `NOT_SHORTLISTED_METADATA`: no declared phase/intervention term was found;
  this is not proof of ineligibility.
- `BLOCKED_D4`: public metadata establishes that the frozen D4 design cannot be
  met.
- `UNRESOLVED_METADATA`: plausible fields or phases exist, but metadata is not
  sufficient to pass.
- `BLOCKED_ACCESS`: participant-level analysis is not available through the
  recorded route.
- `READY_FOR_BLINDED_PREFLIGHT`: metadata/schema clears screening only; never
  synonymous with runnable.

No dataset may be labelled `RUNNABLE` by this protocol.
