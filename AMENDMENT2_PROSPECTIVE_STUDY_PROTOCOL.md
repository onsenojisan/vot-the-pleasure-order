# Amendment 2 — Prospective Study Protocol

Status: **design draft; not an operative 2B, ethics submission or recruitment authorization**

Date: 2026-08-15

Governed by: [Amendment 2A](AMENDMENT_2A_GOVERNANCE_RULES.md)

## Purpose And Scope

This protocol defines how a future dataset could be collected with the paired
arms and distinct variables required by D4, D5 and P3. It does not freeze
target-specific numbers and cannot substitute for a completed
[Amendment 2B](AMENDMENT_2B_EXECUTION_ANNEX.md).

Two routes must remain separate:

- **Route L — bounded reversible nonclinical task:** feasible method-development
  route with controlled bidirectional forcing. Any inference is limited to the
  task domain.
- **Route C — naturalistic clinical collaboration:** potentially more relevant
  to mental-health claims, but research must not cause deterioration or direct
  treatment decisions.

Success on Route L does not establish clinical generality. Route C may not
borrow Route L's safety, power or construct-validity conclusions without a new
target-specific 2B.

## Non-Negotiable Human-Research Boundary

No study under this protocol may intentionally induce psychiatric deterioration,
withdraw or delay indicated treatment, direct medication changes, or override
clinical decisions. Participation, withdrawal and stopping rules must remain
independent of the theory's evidential interests.

Before recruitment, the responsible institution must determine the applicable
law and regulation, complete independent ethics review where required, obtain
valid informed consent, and approve privacy, security, adverse-event and data
management procedures. The current repository and its author are not a research
sponsor or ethics committee.

Relevant general sources include Japan's official
[human life-science and medical-research ethics guidance](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/hokabunya/kenkyujigyou/i-kenkyu/index.html)
and the World Medical Association's
[2024 Declaration of Helsinki](https://www.wma.net/what-we-do/medical-ethics/declaration-of-helsinki/).
The governing institution must verify the version and jurisdiction that apply
at submission time.

## Route L — Bounded Reversible Task

### Scientific role

Route L tests whether the proposed model comparison can recover hysteretic and
non-hysteretic dynamics when state, action and external forcing are deliberately
co-measured. It is primarily an S1/S3 methods test. An external endpoint may
provide task-domain S2 evidence, but no result directly establishes clinical
well-being, value or Ω outside the declared task and horizon.

### Candidate design, not frozen numbers

Each participant completes repeated decision occasions under a bounded external
load that follows predeclared upward and downward schedules. The same person
contributes both arms.

| Element | Prospective mapping |
|---|---|
| decline arm | externally scheduled increase in bounded task demand or constraint |
| recovery arm | matched externally scheduled decrease after the high-load region |
| `y_t` observed state | preregistered task-state vector, scored identically in both arms |
| `a_t` agent action | an explicit participant choice such as strategy, effort allocation or optional resource use |
| `u_t` external forcing | computer-assigned task demand; randomized or schedule-assigned independently of the participant's current action |
| action/forcing separation | `a_t` and `u_t` are distinct logged fields and cannot be relabelled after collection |
| P3 candidate | separately scored non-self-report transfer probe or physiological measure not used to construct `y_t`, `a_t` or `u_t` |
| time unit | one decision occasion, with elapsed time also logged |

The starting simulation design uses 32 cases and 100 observations per arm, but
those values are not approved sample-size commitments. The minimum D4 screen is
50 usable observations per person in each arm. Simulation, burden assessment,
attrition allowances and ethics review must determine the final numbers before
2B approval.

### Design protections

- arm labels and the `u_t` schedule are fixed from the protocol, never inferred
  from outcome trajectories;
- order, session and carry-over effects are handled by a prospectively frozen
  randomized crossover or counterbalanced schedule;
- external forcing spans both directions and the same declared domain;
- actions remain voluntary and observable; unavailable options are logged;
- rest periods prevent observation count from becoming an excuse for excessive
  burden;
- stopping thresholds, withdrawal, adverse-event handling and exclusion rules
  are fixed before recruitment;
- the independent endpoint is not used to tune the structural classifier;
- no task score is described as direct measurement of Ω or clinical health.

## Route C — Naturalistic Clinical Collaboration

Route C observes clinically occurring worsening and recovery while ordinary
care proceeds independently. Treatment initiation, tapering, dose changes and
other care decisions are made by participants and qualified clinicians, never
assigned to manufacture both arms for this research.

A Route C candidate may advance only if its prospective protocol establishes:

1. the same people can contribute independently defined worsening and recovery
   periods;
2. both arm labels come from clinical or protocol events fixed without reading
   the target trajectories;
3. the planned measurement schedule can plausibly yield at least 50 usable
   observations per person in each arm;
4. agent action and external forcing are separately measured rather than
   reconstructed from the same symptom item;
5. treatment and external events are timestamped, with exogeneity and
   bidirectionality assessed prospectively;
6. an independent non-self-report endpoint and its horizon are declared if P3
   is to be tested;
7. the institution can run the frozen package locally when participant data
   cannot leave its environment.

If natural recovery does not occur, the study remains incomplete. It may not
induce deterioration, change care or redefine ordinary fluctuation as a
recovery arm to satisfy D4.

## Blindness And Role Separation

Before a target-specific 2B is frozen:

- the methods team may inspect protocols, schemas, codebooks and simulated data;
- a data custodian may compute counts needed for eligibility without disclosing
  outcome values;
- the VOT analysis team must not inspect participant-level target outcomes or
  use published aggregate results to choose mappings or margins;
- the locked-validation seed custodian must be separate from calibration work;
- clinical staff retain sole authority over care and safety decisions.

Any breach is recorded. It does not become harmless because the design later
passes simulation.

## Development Gates

| Gate | Required evidence | Failure result |
|---|---|---|
| P0 model implementation | runnable VOT, R0–R6 and S0 fitting code with common inputs and budgets | method development only |
| P1 synthetic recovery | known fold and non-fold generators recovered across declared nuisance conditions | redesign before human study |
| P2 burden and safety | institutional feasibility review and, where required, ethics approval | no recruitment |
| P3 pilot | blinded data-quality and adherence criteria met without changing target mappings | revise under a new version or stop |
| P4 calibration | proper score and meaningful margin selected on calibration seeds | no locked validation |
| P5 locked validation | all required scenarios meet ratified two-sided targets | no operative 2B |
| P6 target annex | exact study 2B approved and committed before target outcomes are visible | `NO AMENDMENT 2 VERDICT` |

## What May Be Approved Now

The author may approve continued development under this draft's safety boundary.
That is not approval to recruit, access data, lock target-specific numbers or
activate Amendment 2B. Those decisions require the responsible institution and
a later exact annex.

## Current Next Step

Implement the synthetic R0–R6/S0 fitting harness. Until it exists and survives
calibration, a human collection design has no demonstrated ability to answer the
question whose burden it would impose.
