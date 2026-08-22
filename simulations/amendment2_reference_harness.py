#!/usr/bin/env python3
"""Run the Amendment 2 synthetic method-development reference harness.

This module is deliberately narrower than an operative Amendment 2B fitting
engine.  It provides a dependency-free, scalar observed-state reference
implementation for the VOT and R0-R6/S0 scenario families, common chronological
data splits, a shared fitting budget, and held-out observation/action scoring.

It implements the author-selected shared-fold VOT estimator only in its current
observed-state reference form. It does *not* implement latent-state inference or
the full multi-step EFE rival policy model. Every result is therefore labelled
METHOD_DEVELOPMENT_ONLY and cannot authorize an Amendment 2 verdict.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    from simulations.validate_scenario_registry import load_registry, validate_registry
except ModuleNotFoundError:  # Direct `python simulations/...py` execution.
    from validate_scenario_registry import load_registry, validate_registry


HARNESS_VERSION = "0.2-reference"
HARNESS_STATUS = "METHOD_DEVELOPMENT_ONLY"
MODEL_IDS = (
    "R0_MEAN",
    "R0_AR",
    "R0_GENERIC",
    "R1",
    "R2",
    "S0",
    "R3",
    "R4",
    "R5",
    "VOT",
    "R6",
)
REQUIRED_RIVAL_IDS = {"R1", "R2", "S0", "R3", "R4", "R5", "R6"}
NON_FOLD_IDS = ("R0_MEAN", "R0_AR", "R0_GENERIC", "R1", "R2", "S0", "R3", "R4", "R5")
FOLD_IDS = ("VOT", "R6")
RIDGE_GRID = (1e-6, 0.01, 0.1)
PREFERENCE_GRID = (-1.0, 0.0, 1.0)
PRECISION_GRID = (0.5, 1.0, 2.0)
MIN_VARIANCE = 1e-4


@dataclass(frozen=True)
class Transition:
    case_id: int
    arm: str
    t: int
    time_fraction: float
    y: float
    action: int
    forcing: float
    y_next: float

    @property
    def unit_key(self) -> str:
        return f"{self.case_id}:{self.arm}"

    @property
    def case_key(self) -> str:
        return str(self.case_id)


@dataclass
class FittedDynamics:
    model_id: str
    coefficients: dict[str, list[float]]
    residual_sd: float
    parameter_count: int
    ridge: float
    threshold: float = 0.0
    preference: float = 0.0
    policy_precision: float = 1.0
    identified: bool = True
    failure_reason: str = ""

    def predict(self, row: Transition, action: int | None = None) -> float:
        selected_action = row.action if action is None else action
        key = _group_key(self.model_id, row)
        coefficients = self.coefficients.get(key) or self.coefficients.get("GLOBAL")
        if coefficients is None:
            raise KeyError(f"{self.model_id} has no coefficients for {key}")
        features = _features(self.model_id, row, selected_action, self.threshold)
        return sum(value * coefficient for value, coefficient in zip(features, coefficients))


@dataclass(frozen=True)
class Score:
    observation: float
    action: float
    joint: float
    occasions: int


def _sigmoid(value: float) -> float:
    if value >= 0:
        exponent = math.exp(-min(value, 700.0))
        return 1.0 / (1.0 + exponent)
    exponent = math.exp(max(value, -700.0))
    return exponent / (1.0 + exponent)


def _normal(rng: random.Random, sd: float) -> float:
    return rng.gauss(0.0, sd)


def _bounded(value: float, lower: float = -4.0, upper: float = 4.0) -> float:
    return min(upper, max(lower, value))


def _forcing(arm: str, t: int, observations: int, coverage: str) -> float:
    fraction = t / max(1, observations - 1)
    amplitude = 1.35 if "barely" in coverage.lower() else 2.0
    if arm == "decline":
        return amplitude * (1.0 - 2.0 * fraction)
    return amplitude * (-1.0 + 2.0 * fraction)


def _linear_parameters(generator: str, rng: random.Random, case_id: int, arm: str) -> tuple[float, ...]:
    arm_offset = -0.03 if arm == "decline" else 0.03
    if generator == "R3":
        return (
            rng.uniform(-0.25, 0.25),
            rng.uniform(0.58, 0.92),
            rng.uniform(0.05, 0.28),
            rng.uniform(0.12, 0.38),
        )
    if generator == "R4":
        return (
            rng.gauss(arm_offset, 0.06),
            rng.gauss(0.78, 0.05),
            rng.gauss(0.16, 0.03),
            rng.gauss(0.25, 0.04),
        )
    if generator == "R5":
        local = random.Random(700_001 + case_id * 37)
        return (
            local.gauss(0.0, 0.05),
            local.gauss(0.80, 0.04),
            local.gauss(0.17, 0.03),
            local.gauss(0.24, 0.03),
        )
    return (0.0, 0.80, 0.16, 0.25)


def generate_scenario(scenario: dict[str, Any], seed: int) -> list[Transition]:
    """Generate scalar synthetic decline/recovery transitions for one registry scenario."""
    rng = random.Random(seed)
    generator = str(scenario["generator"])
    cases = int(scenario["cases"])
    observations = int(scenario["observations_per_arm"])
    process_sd = float(scenario["process_noise_sd"])
    measurement_sd = float(scenario["measurement_noise_sd"])
    missingness = float(scenario["missingness_rate"])
    coverage = str(scenario["control_coverage"])
    parameters = scenario.get("parameters", {})
    generated: list[Transition] = []

    for case_id in range(cases):
        fold_parameters: tuple[float, float, float, float] | None = None
        if generator in {"VOT", "R6"}:
            alpha = float(parameters.get("alpha", 1.0))
            beta = float(parameters.get("beta", 1.0))
            zeta = float(parameters.get("zeta", 0.4))
            delta = float(parameters.get("delta", 0.05))
            if generator == "R6":
                heterogeneity = float(parameters.get("hierogeneity_sd", 0.1))
                alpha = max(0.05, rng.gauss(alpha, heterogeneity))
                beta = rng.gauss(beta, heterogeneity)
                zeta = rng.gauss(zeta, heterogeneity)
                delta = max(0.01, rng.gauss(delta, heterogeneity * 0.05))
            fold_parameters = (alpha, beta, zeta, delta)

        for arm in ("decline", "recovery"):
            if fold_parameters is not None:
                alpha = fold_parameters[0]
                x = math.sqrt(max(alpha, 0.05)) * (1.0 if arm == "decline" else -1.0)
            else:
                x = 1.0 if arm == "decline" else -1.0

            latent = [x]
            actions: list[int] = []
            forcings: list[float] = []
            switching_state = 1 if arm == "decline" else -1
            linear_parameters = _linear_parameters(generator, rng, case_id, arm)

            for t in range(observations):
                forcing = _forcing(arm, t, observations, coverage)
                action_probability = _sigmoid(0.25 - 0.85 * x - 0.20 * forcing)
                action = 1 if rng.random() < action_probability else -1
                progress = t / max(1, observations - 1)

                if generator == "R1":
                    b, coefficient_y, coefficient_a, coefficient_u = linear_parameters
                    next_x = (
                        b
                        + coefficient_y * x
                        + coefficient_a * action
                        + coefficient_u * forcing
                        + (0.08 if arm == "recovery" else -0.08) * progress
                    )
                elif generator == "R2":
                    b, coefficient_y, coefficient_a, coefficient_u = linear_parameters
                    jump = (0.80 if arm == "recovery" else -0.80) if t >= observations // 2 else 0.0
                    next_x = b + 0.74 * x + coefficient_a * action + coefficient_u * forcing + jump
                elif generator == "S0":
                    if rng.random() < 0.05:
                        switching_state *= -1
                    next_x = 0.68 * x + 0.36 * switching_state + 0.12 * action + 0.18 * forcing
                elif generator in {"R3", "R4", "R5"}:
                    b, coefficient_y, coefficient_a, coefficient_u = linear_parameters
                    next_x = b + coefficient_y * x + coefficient_a * action + coefficient_u * forcing
                elif generator in {"VOT", "R6"}:
                    assert fold_parameters is not None
                    alpha, beta, zeta, delta = fold_parameters
                    next_x = x + delta * (alpha * x - x**3 + beta * forcing + zeta * action)
                else:
                    raise ValueError(f"unsupported generator: {generator}")

                x = _bounded(next_x + _normal(rng, process_sd))
                actions.append(action)
                forcings.append(forcing)
                latent.append(x)

            measured: list[float | None] = []
            for value in latent:
                if rng.random() < missingness:
                    measured.append(None)
                else:
                    measured.append(value + _normal(rng, measurement_sd))

            for t, (action, forcing) in enumerate(zip(actions, forcings)):
                current = measured[t]
                following = measured[t + 1]
                if current is None or following is None:
                    continue
                generated.append(
                    Transition(
                        case_id=case_id,
                        arm=arm,
                        t=t,
                        time_fraction=t / max(1, observations - 1),
                        y=float(current),
                        action=action,
                        forcing=forcing,
                        y_next=float(following),
                    )
                )
    return generated


def split_transitions(
    rows: Iterable[Transition], train_fraction: float = 0.60, validation_fraction: float = 0.20
) -> tuple[list[Transition], list[Transition], list[Transition]]:
    """Create identical chronological within-unit train/validation/test splits."""
    grouped: dict[str, list[Transition]] = {}
    for row in rows:
        grouped.setdefault(row.unit_key, []).append(row)
    train: list[Transition] = []
    validation: list[Transition] = []
    test: list[Transition] = []
    for unit_rows in grouped.values():
        ordered = sorted(unit_rows, key=lambda item: item.t)
        if len(ordered) < 10:
            continue
        train_end = max(4, int(len(ordered) * train_fraction))
        validation_end = max(train_end + 2, int(len(ordered) * (train_fraction + validation_fraction)))
        validation_end = min(validation_end, len(ordered) - 2)
        train.extend(ordered[:train_end])
        validation.extend(ordered[train_end:validation_end])
        test.extend(ordered[validation_end:])
    return train, validation, test


def _solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda index: abs(augmented[index][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("singular normal equations")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row_index in range(size):
            if row_index == column:
                continue
            factor = augmented[row_index][column]
            if factor == 0.0:
                continue
            augmented[row_index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(augmented[row_index], augmented[column])
            ]
    return [augmented[index][-1] for index in range(size)]


def _ridge_fit(
    features: Sequence[Sequence[float]],
    outcomes: Sequence[float],
    ridge: float,
    prior: Sequence[float] | None = None,
) -> list[float]:
    if not features or len(features) != len(outcomes):
        raise ValueError("features and outcomes must be non-empty and aligned")
    width = len(features[0])
    if any(len(row) != width for row in features):
        raise ValueError("feature rows have inconsistent width")
    gram = [[0.0 for _ in range(width)] for _ in range(width)]
    rhs = [0.0 for _ in range(width)]
    for row, outcome in zip(features, outcomes):
        for left in range(width):
            rhs[left] += row[left] * outcome
            for right in range(width):
                gram[left][right] += row[left] * row[right]
    prior_values = list(prior) if prior is not None else [0.0] * width
    for index in range(width):
        penalty = ridge if index else ridge * 0.05
        gram[index][index] += penalty
        rhs[index] += penalty * prior_values[index]
    return _solve(gram, rhs)


def _group_key(model_id: str, row: Transition) -> str:
    if model_id in {"R3", "R4"}:
        return row.unit_key
    if model_id in {"R5", "R6"}:
        return row.case_key
    return "GLOBAL"


def _features(model_id: str, row: Transition, action: int, threshold: float) -> list[float]:
    if model_id == "R0_MEAN":
        return [1.0]
    if model_id == "R0_AR":
        return [1.0, row.y]
    if model_id in {"R0_GENERIC", "R3", "R4", "R5"}:
        return [1.0, row.y, float(action), row.forcing]
    if model_id == "R1":
        return [
            1.0,
            row.y,
            float(action),
            row.forcing,
            row.time_fraction,
            1.0 if row.arm == "recovery" else 0.0,
        ]
    if model_id == "R2":
        post_jump = 1.0 if row.time_fraction >= 0.5 else 0.0
        arm_sign = 1.0 if row.arm == "recovery" else -1.0
        return [
            1.0,
            row.y,
            float(action),
            row.forcing,
            row.time_fraction,
            1.0 if row.arm == "recovery" else 0.0,
            post_jump,
            post_jump * arm_sign,
        ]
    if model_id == "S0":
        state = 1.0 if row.y > threshold else 0.0
        return [
            1.0,
            row.y,
            float(action),
            row.forcing,
            state,
            state * row.y,
            state * float(action),
            state * row.forcing,
        ]
    if model_id in {"VOT", "R6"}:
        return [1.0, row.y, -(row.y**3), float(action), row.forcing]
    raise ValueError(f"unsupported model: {model_id}")


def _median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return 0.5 * (ordered[midpoint - 1] + ordered[midpoint])


def fit_dynamics(model_id: str, rows: Sequence[Transition], ridge: float) -> FittedDynamics:
    threshold = _median([row.y for row in rows]) if model_id == "S0" else 0.0
    grouped: dict[str, list[Transition]] = {}
    for row in rows:
        grouped.setdefault(_group_key(model_id, row), []).append(row)

    coefficients: dict[str, list[float]] = {}
    pooled_prior: list[float] | None = None
    if model_id in {"R4", "R6"}:
        pooled_features = [_features(model_id, row, row.action, threshold) for row in rows]
        pooled_prior = _ridge_fit(pooled_features, [row.y_next for row in rows], ridge)

    parameter_count = len(pooled_prior) if pooled_prior is not None else 0
    try:
        for key, group_rows in grouped.items():
            design = [_features(model_id, row, row.action, threshold) for row in group_rows]
            width = len(design[0])
            if len(group_rows) < width + 2:
                return FittedDynamics(
                    model_id,
                    {},
                    1.0,
                    0,
                    ridge,
                    threshold=threshold,
                    identified=False,
                    failure_reason=f"group {key} has {len(group_rows)} rows for {width} coefficients",
                )
            coefficients[key] = _ridge_fit(
                design,
                [row.y_next for row in group_rows],
                ridge,
                prior=pooled_prior if model_id in {"R4", "R6"} else None,
            )
            parameter_count += width
    except ValueError as exc:
        return FittedDynamics(
            model_id,
            {},
            1.0,
            0,
            ridge,
            threshold=threshold,
            identified=False,
            failure_reason=str(exc),
        )

    provisional = FittedDynamics(model_id, coefficients, 1.0, parameter_count, ridge, threshold=threshold)
    residuals = [row.y_next - provisional.predict(row) for row in rows]
    residual_variance = sum(value * value for value in residuals) / max(1, len(residuals))
    provisional.residual_sd = math.sqrt(max(MIN_VARIANCE, residual_variance))
    return provisional


def _log_normal(value: float, mean: float, sd: float) -> float:
    variance = max(MIN_VARIANCE, sd * sd)
    return -0.5 * (math.log(2.0 * math.pi * variance) + (value - mean) ** 2 / variance)


def _action_log_probability(model: FittedDynamics, row: Transition) -> float:
    positive = model.predict(row, action=1)
    negative = model.predict(row, action=-1)
    variance = max(1.0, model.residual_sd**2)
    positive_logit = -model.policy_precision * (positive - model.preference) ** 2 / (2.0 * variance)
    negative_logit = -model.policy_precision * (negative - model.preference) ** 2 / (2.0 * variance)
    probability_positive = _sigmoid(positive_logit - negative_logit)
    probability = probability_positive if row.action == 1 else 1.0 - probability_positive
    return math.log(min(1.0 - 1e-12, max(1e-12, probability)))


def score_model(model: FittedDynamics, rows: Sequence[Transition]) -> Score:
    if not model.identified or not rows:
        return Score(float("-inf"), float("-inf"), float("-inf"), len(rows))
    observation = 0.0
    action = 0.0
    try:
        for row in rows:
            observation += _log_normal(row.y_next, model.predict(row), model.residual_sd)
            action += _action_log_probability(model, row)
    except (KeyError, OverflowError, ValueError):
        return Score(float("-inf"), float("-inf"), float("-inf"), len(rows))
    occasions = len(rows)
    return Score(observation / occasions, action / occasions, (observation + action) / occasions, occasions)


def _select_policy(model: FittedDynamics, validation: Sequence[Transition]) -> None:
    best = (float("-inf"), 0.0, 1.0)
    for preference in PREFERENCE_GRID:
        for precision in PRECISION_GRID:
            model.preference = preference
            model.policy_precision = precision
            action_score = score_model(model, validation).action
            if action_score > best[0]:
                best = (action_score, preference, precision)
    model.preference = best[1]
    model.policy_precision = best[2]


def fit_with_common_budget(
    model_id: str,
    train: Sequence[Transition],
    validation: Sequence[Transition],
) -> FittedDynamics:
    """Select one of the same ridge/policy grid cells for every model."""
    best_model: FittedDynamics | None = None
    best_score = float("-inf")
    failures: list[str] = []
    for ridge in RIDGE_GRID:
        model = fit_dynamics(model_id, train, ridge)
        if not model.identified:
            failures.append(model.failure_reason)
            continue
        _select_policy(model, validation)
        validation_score = score_model(model, validation).joint
        if validation_score > best_score:
            best_score = validation_score
            best_model = model
    if best_model is not None:
        return best_model
    return FittedDynamics(
        model_id,
        {},
        1.0,
        0,
        RIDGE_GRID[0],
        identified=False,
        failure_reason="; ".join(sorted(set(failures))) or "no finite validation score",
    )


def _fold_admissible(model: FittedDynamics) -> bool:
    if model.model_id not in FOLD_IDS or not model.coefficients:
        return False
    if model.model_id == "VOT":
        coefficients = model.coefficients.get("GLOBAL")
        return bool(coefficients and len(coefficients) >= 3 and coefficients[1] > 1.0 and coefficients[2] > 0.0)
    groups = [
        coefficients
        for coefficients in model.coefficients.values()
        if len(coefficients) >= 3
    ]
    if not groups:
        return False
    admissible = sum(coefficients[1] > 1.0 and coefficients[2] > 0.0 for coefficients in groups)
    mean_linear = sum(coefficients[1] for coefficients in groups) / len(groups)
    mean_cubic = sum(coefficients[2] for coefficients in groups) / len(groups)
    return admissible / len(groups) >= 0.75 and mean_linear > 1.0 and mean_cubic > 0.0


def _finite_or_none(value: float) -> float | None:
    return value if math.isfinite(value) else None


def run_replicate(scenario: dict[str, Any], replicate: int, margin: float = 0.0) -> dict[str, Any]:
    seed = int(scenario["seed"]) + replicate * 1_000_003
    transitions = generate_scenario(scenario, seed)
    train, validation, test = split_transitions(transitions)
    if not train or not validation or not test:
        return {
            "scenario_id": scenario["id"],
            "truth": scenario["truth"],
            "replicate": replicate,
            "generator": scenario["generator"],
            "disposition": "UNDERPOWERED",
            "score_gap": "",
            "winning_model": "",
            "best_fold_model": "",
            "best_non_fold_model": "",
            "best_rival_model": "",
            "vot_vs_best_rival_gap": "",
            "d5_reference_disposition": "UNDERPOWERED",
            "harness_status": HARNESS_STATUS,
            "verdict_authorized": False,
            "failure_reason": "chronological split produced an empty partition",
            "train_rows": len(train),
            "validation_rows": len(validation),
            "test_rows": len(test),
            "models": [],
        }

    fitted = {model_id: fit_with_common_budget(model_id, train, validation) for model_id in MODEL_IDS}
    scores = {model_id: score_model(model, test) for model_id, model in fitted.items()}
    unidentified = sorted(model_id for model_id in REQUIRED_RIVAL_IDS if not fitted[model_id].identified)
    model_audit = []
    for model_id in MODEL_IDS:
        model = fitted[model_id]
        score = scores[model_id]
        model_audit.append(
            {
                "model_id": model_id,
                "identified": model.identified,
                "failure_reason": model.failure_reason,
                "ridge": model.ridge,
                "parameter_count": model.parameter_count,
                "preference": model.preference,
                "policy_precision": model.policy_precision,
                "observation_elpd": _finite_or_none(score.observation),
                "action_elpd": _finite_or_none(score.action),
                "joint_elpd": _finite_or_none(score.joint),
                "test_occasions": score.occasions,
                "fold_admissible": _fold_admissible(model),
            }
        )

    if unidentified:
        disposition = "UNIDENTIFIED"
        score_gap: float | str = ""
        winning_model = ""
        best_fold = ""
        best_non_fold = ""
        best_rival = ""
        vot_gap: float | str = ""
        d5_disposition = "UNIDENTIFIED"
        failure_reason = f"required rivals unidentified: {', '.join(unidentified)}"
    else:
        best_non_fold = max(NON_FOLD_IDS, key=lambda model_id: scores[model_id].joint)
        admissible_folds = [model_id for model_id in FOLD_IDS if _fold_admissible(fitted[model_id])]
        fold_pool = admissible_folds or list(FOLD_IDS)
        best_fold = max(fold_pool, key=lambda model_id: scores[model_id].joint)
        fold_score = scores[best_fold]
        non_fold_score = scores[best_non_fold]
        score_gap = fold_score.joint - non_fold_score.joint
        winning_model = max(MODEL_IDS, key=lambda model_id: scores[model_id].joint)
        if score_gap > margin and best_fold in admissible_folds:
            disposition = "FOLD"
        elif score_gap < -margin:
            disposition = "NO_FOLD"
        else:
            disposition = "TIE"

        best_rival = max(
            (model_id for model_id in MODEL_IDS if model_id != "VOT"),
            key=lambda model_id: scores[model_id].joint,
        )
        vot_gap = scores["VOT"].joint - scores[best_rival].joint
        if not fitted["VOT"].identified:
            d5_disposition = "UNIDENTIFIED"
        elif disposition != "FOLD" or not _fold_admissible(fitted["VOT"]):
            d5_disposition = "NO_VOT_STRUCTURE_PASS"
        elif vot_gap > margin:
            d5_disposition = "VOT_PREFERRED_REFERENCE"
        elif vot_gap < -margin:
            d5_disposition = "ABSORBED_BY_RIVAL"
        else:
            d5_disposition = "ABSORBED_TIE"
        failure_reason = ""

    return {
        "scenario_id": scenario["id"],
        "truth": scenario["truth"],
        "generator": scenario["generator"],
        "replicate": replicate,
        "disposition": disposition,
        "score_gap": score_gap,
        "winning_model": winning_model,
        "best_fold_model": best_fold,
        "best_non_fold_model": best_non_fold,
        "best_rival_model": best_rival,
        "vot_vs_best_rival_gap": vot_gap,
        "d5_reference_disposition": d5_disposition,
        "harness_status": HARNESS_STATUS,
        "verdict_authorized": False,
        "failure_reason": failure_reason,
        "train_rows": len(train),
        "validation_rows": len(validation),
        "test_rows": len(test),
        "models": model_audit,
    }


def run_registry(
    registry: dict[str, Any],
    replicates: int,
    margin: float = 0.0,
    scenario_ids: set[str] | None = None,
    cases_cap: int | None = None,
    observations_cap: int | None = None,
) -> list[dict[str, Any]]:
    validate_registry(registry)
    selected = []
    for registered in registry["calibration_scenarios"]:
        if scenario_ids and registered["id"] not in scenario_ids:
            continue
        scenario = dict(registered)
        if cases_cap is not None:
            scenario["cases"] = min(int(scenario["cases"]), cases_cap)
        if observations_cap is not None:
            scenario["observations_per_arm"] = min(int(scenario["observations_per_arm"]), observations_cap)
        selected.append(scenario)
    if not selected:
        raise ValueError("no calibration scenarios selected")
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    results = []
    for scenario in selected:
        for replicate in range(1, replicates + 1):
            results.append(run_replicate(scenario, replicate, margin=margin))
    return results


def write_results(path: Path, results: Sequence[dict[str, Any]]) -> None:
    fields = [
        "scenario_id",
        "truth",
        "replicate",
        "disposition",
        "score_gap",
        "winning_model",
        "best_fold_model",
        "best_non_fold_model",
        "best_rival_model",
        "vot_vs_best_rival_gap",
        "d5_reference_disposition",
        "generator",
        "harness_status",
        "verdict_authorized",
        "failure_reason",
        "train_rows",
        "validation_rows",
        "test_rows",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)


def build_audit(results: Sequence[dict[str, Any]], margin: float) -> dict[str, Any]:
    return {
        "harness_version": HARNESS_VERSION,
        "status": HARNESS_STATUS,
        "amendment2_verdict_authorized": False,
        "provisional_margin": margin,
        "shared_budget": {
            "ridge_grid": list(RIDGE_GRID),
            "preference_grid": list(PREFERENCE_GRID),
            "policy_precision_grid": list(PRECISION_GRID),
            "partition": "chronological within-case/arm 60/20/20",
            "selection_score": "validation joint observation/action log score",
            "test_score": "held-out joint log predictive density per occasion",
        },
        "decision_contract": {
            "structure": "best admissible VOT/R6 fold model versus best non-fold model",
            "vot": "VOT versus best rival, conditional on a VOT-admissible structure pass",
            "vot_sharing": "one global cubic transition across cases and arms",
            "r6_sharing": "case-level cubic transitions around a pooled ridge prior, shared across arms",
            "r6_fold_admissibility": "at least 75% case fits plus mean linear/cubic signs",
        },
        "limitations": [
            "scalar identity observation model; latent-state VFE is not implemented",
            "one-step risk-only action policy; ambiguity, habits and multi-step EFE are not implemented",
            "selected VOT reference estimator uses observed y in place of latent-state inference",
            "R6 partial pooling is a ridge approximation, not a fitted hierarchical Bayesian model",
            "candidate margin and registry are not author-ratified or locked",
            "results are calibration diagnostics and cannot support or downgrade VOT",
        ],
        "results": list(results),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="write result-contract CSV")
    parser.add_argument("--audit-output", type=Path, help="write full per-model JSON audit")
    parser.add_argument("--replicates", type=int, default=1)
    parser.add_argument("--margin", type=float, default=0.0, help="provisional score margin; not ratified")
    parser.add_argument("--scenario", action="append", dest="scenarios", help="run only this scenario ID")
    parser.add_argument("--cases-cap", type=int, help="explicit method-development size cap")
    parser.add_argument("--observations-cap", type=int, help="explicit method-development size cap")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.margin < 0:
        raise SystemExit("harness error: margin must be non-negative")
    try:
        registry = load_registry(args.registry)
        results = run_registry(
            registry,
            replicates=args.replicates,
            margin=args.margin,
            scenario_ids=set(args.scenarios) if args.scenarios else None,
            cases_cap=args.cases_cap,
            observations_cap=args.observations_cap,
        )
        write_results(args.output, results)
        if args.audit_output:
            args.audit_output.parent.mkdir(parents=True, exist_ok=True)
            args.audit_output.write_text(
                json.dumps(
                    build_audit(results, args.margin),
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                )
                + "\n",
                encoding="utf-8",
            )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"harness error: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
