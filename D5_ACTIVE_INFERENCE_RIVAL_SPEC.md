# D5 Active-Inference Rival Specification — R3–R6

Status: **author-ratification draft; equations and registry are not frozen**
Date: 2026-08-15
Applies to: [Proposed Amendment 2](PROPOSED_AMENDMENT_2_D5_AND_FALSIFIER.md)

## Purpose

This file turns the labels `R3–R6` into explicit candidate models. It closes the
gap between “a flexible comparator” and an actual active-inference rival without
pretending that one active-inference formulation exhausts the framework.

The selected instantiation is a controlled continuous-Gaussian state-space
model with variational state inference and policy selection by expected free
energy. This is a prospective comparison contract. It is not evidence that the
target data contain an active-inference process.

## Source Basis And Scope

The common factorization follows the POMDP / state-space treatment in:

- Da Costa et al. (2020), *Active inference on discrete state-spaces: A
  synthesis*, doi:`10.1016/j.jmp.2020.102447`;
- Friston et al. (2017), *Active Inference: A Process Theory*,
  doi:`10.1162/NECO_a_00912`;
- Çatal et al. (2020), *Learning Generative State Space Models for Active
  Inference*, doi:`10.3389/fncom.2020.574372`.

Those sources motivate a generative state-space model, variational free-energy
minimization for inference/learning, and expected free energy for policy
selection. The particular linear, hierarchical and cubic dynamics below are
this project's rival-family choices, not formulas attributed to those papers.

## Common Observed And Latent Variables

For person/case `i`, arm `r`, and time `t`:

| Symbol | Role | Required status |
|---|---|---|
| `y_i,r,t` | continuous observed state vector used by both VOT and rivals | observed under one frozen mapping |
| `a_i,r,t` | agent-selected action or defensible action proxy | observed for an active-inference verdict |
| `u_i,r,t` | externally applied perturbation / forcing | observed; never relabelled as agent action |
| `x_i,r,t` | latent state inferred by the rival | latent |
| `c_i,r` | preferred-outcome distribution parameters | estimated or externally anchored under a frozen prior |
| `pi_i,r,t` | candidate policy / action sequence | latent when only the executed first action is observed |

External perturbation `u` and agent action `a` have different causal roles. If
the acquired data contain no action stream and no prospectively justified proxy,
the policy mechanism, preference precision and expected-free-energy term are
not identified. The D5 active-inference verdict is then `INCONCLUSIVE`; fitting
a passive state-space model does not repair the missing action data.

## Common Generative Model

For parameters `theta` and known external forcing `u`:

```text
p_theta(y_1:T, x_1:T, a_1:T | u_1:T)
  = p_theta(x_1)
    product_t p_theta(y_t | x_t)
    product_t p_theta(x_t+1 | x_t, a_t, u_t)
    product_t p_theta(a_t | history_t)
```

Observation model:

```text
y_t | x_t ~ Normal(H x_t + d, Sigma_y)
```

The recognition density `q_phi(x_1:T | y_1:T, a_1:T, u_1:T)` is fitted by
minimizing variational free energy:

```text
F(theta, phi)
  = E_q[log q_phi(x_1:T) - log p_theta(y_1:T, x_1:T | a_1:T, u_1:T)]
```

For a candidate policy `pi`, the frozen expected-free-energy form is the
risk-plus-ambiguity decomposition:

```text
G_t(pi)
  = sum_tau=t+1:t+H {
      KL[Q_theta(y_tau | pi) || P_C(y_tau)]
      + E_Q H[p_theta(y_tau | x_tau)]
    }
```

Executed actions are scored by:

```text
p_theta(a_t = first(pi) | history_t)
  proportional_to sum_{pi:first(pi)=a_t} exp(-gamma * G_t(pi)) P_E(pi)
```

`P_C` is the preferred-outcome distribution, `P_E` a habitual policy prior,
`gamma` policy precision, and `H` the planning horizon. All action sets, policy
sets, preference parameterizations and precision priors are frozen.

The fitted objective is the approximate negative joint evidence:

```text
Loss = F(theta, phi) - sum_t log p_theta(a_t | history_t)
```

The primary comparison score is held-out joint log predictive density per
decision occasion:

```text
elpd_joint = sum_test [log p(y_t | past) + log p(a_t | past)] / N_test
```

Observation and action components are also reported separately. A win carried
only by one component is visible and cannot be redescribed as a general win.

## R3 — Person/Arm-Specific Active Inference

Dynamics:

```text
x_i,r,t+1
  = b_i,r + A_i,r x_i,r,t + B_i,r a_i,r,t + U_i,r u_i,r,t + w_i,r,t
w_i,r,t ~ Normal(0, Sigma_x,i,r)
```

Every person's decline and recovery arm is fitted independently, including
dynamics, preferences and policy precision. R3 receives no cross-case or
cross-arm transfer benefit. It preserves the flexible comparator anticipated by
the frozen D5 clause.

Required minimum: enough action-state transitions in every person/arm to
identify its declared parameter count. Failure in any required held-out unit is
`UNIDENTIFIED`, not a VOT win.

## R4 — Hierarchical Partially Pooled Active Inference

R4 keeps R3's linear dynamics but places person/arm parameters under group
distributions:

```text
vec(A_i,r, B_i,r, U_i,r, H_i,r, c_i,r, log gamma_i,r)
  ~ Normal(mu_group + Z_i,r beta, Sigma_group)
```

Partial pooling is learned only from the training partition. Held-out people do
not contribute posterior information to their group distribution. R4 tests
whether the apparent VOT transfer advantage is ordinary hierarchical shrinkage.

## R5 — Shared Decline/Recovery Active Inference

R5 shares observation, transition, preference and policy parameters across the
two arms:

```text
A_i,decline = A_i,recovery = A_i
B_i,decline = B_i,recovery = B_i
U_i,decline = U_i,recovery = U_i
H_i,decline = H_i,recovery = H_i
c_i,decline = c_i,recovery = c_i
gamma_i,decline = gamma_i,recovery = gamma_i
```

Only the initial-state distribution, observed external forcing sequence and
predeclared arm label may differ. R5 receives the same cross-arm transfer split
as VOT. It tests whether parameter sharing, rather than a VOT-specific gate,
explains D4.

## R6 — Nonlinear/Hysteretic Active Inference

R6 replaces the linear transition with a controlled cubic potential:

```text
V_i(x; a_t, u_t)
  = x^4 / 4 - alpha_i x^2 / 2 - (beta_i u_t + zeta_i a_t) x

x_i,t+1
  = x_i,t - delta * dV_i/dx + w_i,t
  = x_i,t + delta * (alpha_i x_i,t - x_i,t^3
                     + beta_i u_i,t + zeta_i a_i,t) + w_i,t
```

For admissible positive `alpha` and an adequate forcing range this model can
express multistability, path dependence and hysteresis. It keeps the same
observation model, VFE state inference, EFE policy score and held-out partitions
as R3–R5. Parameters are hierarchically pooled across people and shared across
decline/recovery arms unless a field is explicitly listed as arm-specific.

R6 is intentionally strong: if it matches VOT, the fold geometry has been
annexed by an explicit active-inference model and VOT is not distinct on D5.

## Equal-Budget And Complexity Rules

All candidates receive identical training observations, action observations,
external forcing, endpoint variables and held-out partitions. Comparison must
freeze:

- latent-state dimension grid;
- action and policy set;
- planning horizon grid;
- prior families and prior-sensitivity grid;
- optimizer starts, compute budget and convergence criteria;
- effective-complexity estimate;
- failure and divergence rules;
- the meaningful `elpd_joint` win/tie margin.

R6 cannot receive a larger tuning budget because it is the stronger rival. VOT
cannot receive a privileged failure restart. Non-converged required models are
`UNIDENTIFIED` unless the same predeclared retry rule succeeds for every model.

## Identifiability Gates

The active-inference family is not adjudicable if any are true:

1. agent actions/proxies are absent or indistinguishable from external forcing;
2. the action set or policy horizon cannot be reconstructed prospectively;
3. preferred outcomes and policy precision are mutually unidentified under the
   declared data range;
4. observations do not cover the external forcing range needed by R6;
5. per-unit transition counts do not support R3's parameter count;
6. posterior predictive checks fail under the frozen rule;
7. materially different priors reverse the winner inside the frozen sensitivity
   set without one model clearing the win margin.

Any gate failure yields `INCONCLUSIVE` for D5.

## Machine-Readable Registry

The candidate scenario grid is recorded in
[`simulations/amendment2_scenarios.v0.json`](simulations/amendment2_scenarios.v0.json).
It is validated by `simulations/validate_scenario_registry.py`. Locked validation
seeds remain deliberately unset until the equations, priors, grids and candidate
acceptance targets receive author ratification.
