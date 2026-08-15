# Amendment 2 — Metadata-Only Controlled-Access Gate

Status: **prospective intake procedure; no access authorization**

Date: 2026-08-15

Governed by: [Amendment 2A](AMENDMENT_2A_GOVERNANCE_RULES.md)

## Purpose

This gate determines whether a request-only dataset is worth taking into formal
institutional and ethics review. It deliberately precedes any transfer of
participant-level data and any inspection of target outcomes by the VOT team.

Passing the gate means only `ELIGIBLE_FOR_FORMAL_GOVERNANCE_REVIEW`. It does not
authorize access, analysis, an Amendment 2B activation or an empirical verdict.

## Order Of Operations

1. **Public design review.** Use protocols, Methods sections, codebooks and data
   availability statements only. Do not use aggregate results to decide
   eligibility.
2. **Metadata-only intake.** Ask the data custodian to complete the intake or
   provide the same design facts. Explicitly ask them not to send participant
   data.
3. **D4 stop rule.** Stop if the same people do not contribute labelled decline
   and recovery arms, or if either arm has fewer than 50 observations per
   analysed person. Access cannot repair an incompatible design.
4. **Governance review.** Only a surviving candidate may proceed to an
   institutional-sponsor, ethics, data-use-agreement and security review.
5. **Local preflight.** Prefer execution on the data holder's system. A completed
   data manifest may be checked without exporting participant-level data.
6. **Target-specific freeze.** A complete Amendment 2B must be approved and
   committed before the VOT team sees target outcomes or any locked run occurs.

## Machine-Readable Intake

Copy
[`simulations/amendment2_access_intake.template.json`](simulations/amendment2_access_intake.template.json),
complete it from non-outcome design information and run:

```powershell
python simulations/validate_access_intake.py path/to/intake.json
```

Use `--require-formal-review-eligibility` in automation. It exits with status
`2` unless the candidate clears this metadata gate. Even a passing report always
sets `participant_data_access_authorized` to `false` and returns
`NO AMENDMENT 2 VERDICT`.

## Short Custodian Request

The following text may be adapted only after an official contact route has been
verified. It is a draft, not a sent communication.

> We are assessing design compatibility for a prospectively governed,
> participant-level time-series analysis. At this stage, please do not send any
> participant data, row-level summaries or outcome results. Could you confirm
> only whether the same participants contribute protocol-labelled decline and
> recovery periods, the planned or available observations per person in each
> period, the time unit and arm-boundary source, and whether distinct state,
> agent-action, exogenous bidirectional forcing and non-self-report endpoint
> variables were recorded? If the design clears this screen, any further step
> would require a separate institutional, ethics and data-use review.

## Known Routes Reassessed On 2026-08-15

### TRANS-ID

The public project page defines Tapering and Recovery as separate subprojects
and recruitment populations. Neither route therefore supplies the same people
in both arms required by D4. No participant-data request should be made for this
specific D4 purpose unless a different linked study protocol establishes paired
arms.

Source: <https://www.transid.nl/?lang=en>

### Bipolar early-warning study

The public Methods define EMA five times per day for four months and weekly
mania/depression questionnaires. A transition is an abrupt increase of at least
six points within one week on the manic or depressive scale. No labelled
recovery arm, agent-action stream, exogenous bidirectional forcing or
independent non-self-report endpoint is declared. Participant data are described
as available on reasonable request, but obtaining them cannot repair the frozen
D4 design mismatch.

Sources: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8994809/> and
<https://research.rug.nl/en/datasets/additional-file-2-of-anticipating-manic-and-depressive-transition/>

No participant-level outcome values or published aggregate results were used
for either disposition.

## Current Consequence

There is no currently identified request-only route that should advance to a
participant-data request for the frozen D4 purpose. The next empirical route is
therefore either a newly identified study that clears this metadata gate or
prospective collection under the
[Prospective Study Protocol](AMENDMENT2_PROSPECTIVE_STUDY_PROTOCOL.md).
Amendment 2B remains a template, and the only permitted disposition is
`NO AMENDMENT 2 VERDICT`.
