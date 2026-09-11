#!/usr/bin/env python3
"""Build the matched paper-breadth table for all Issue #49 routes."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.g1_kinematics import forward_g1_kinematics
from eval.g1_metrics import load_g1_motion
from eval.g1_paper_metrics import (
    diversity,
    frechet_distance,
    geometric_features_g1,
    kinetic_features_g1,
)
from scripts.run_issue49_evaluation import (
    EVAL,
    EXP_ID,
    ROUTES,
    SAMPLING_SEEDS,
    TRAINING_SEEDS,
    leaf,
)


OUTPUT = EVAL / "paper_breadth/score"
REPRESENTATION = "yaw-anchor absolute 38D + B71"
ROUTE_CONTRASTS = (
    ("AJ-FHC_minus_AJ-HCLEAN", "FD-DF-L-AJ-FHC", "FD-DF-L-AJ-HCLEAN"),
    ("AM-FHC_minus_AM-HCLEAN", "FD-DF-L-AM-FHC", "FD-DF-L-AM-HCLEAN"),
    ("AM-FHC_minus_AM-HDROP", "FD-DF-L-AM-FHC", "FD-DF-L-AM-HDROP"),
    ("AM-HCLEAN_minus_AM-HDROP", "FD-DF-L-AM-HCLEAN", "FD-DF-L-AM-HDROP"),
)
DISTRIBUTION_METRICS = ("FIDk-G1", "FIDg-G1", "Divk-G1", "Divg-G1")
SCALAR_METRICS = (
    "MMR-MS",
    "T-MMR-G1",
    "T-MMR-G1-global",
    "T-MMR-G1-local",
    "G1BAS",
    "G1FKBAS",
    "G1FKRoboPerformBAS",
    "PFC-G1",
)
LOWER_IS_BETTER = {"FIDk-G1", "FIDg-G1", "MMR-MS", "PFC-G1"}


def write_json(payload, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def correct_task(route, training_seed, sampling_seed, scale):
    return {
        "population": "official_final",
        "route": route,
        "training_seed": int(training_seed),
        "sampling_seed": int(sampling_seed),
        "variant": "correct",
        "scale": float(scale),
    }


def source_identity():
    completion = json.loads((EVAL / "completion.json").read_text(encoding="utf-8"))
    if completion.get("status") != "complete_unreviewed":
        raise ValueError("Issue #49 downstream evaluation is not complete")
    if completion.get("representation") != REPRESENTATION:
        raise ValueError("Issue #49 representation identity mismatch")
    freeze = json.loads((EVAL / "cfg/freeze.json").read_text(encoding="utf-8"))
    return completion["evaluation_contract_sha256"], float(freeze["selected_scale"])


def read_leaf(route, training_seed, sampling_seed, scale, source_contract):
    task = correct_task(route, training_seed, sampling_seed, scale)
    root = leaf(task)
    receipt = json.loads((root / "task_receipt.json").read_text(encoding="utf-8"))
    if receipt.get("status") != "passed":
        raise ValueError(f"failed source leaf: {root}")
    if receipt.get("representation") != REPRESENTATION:
        raise ValueError(f"source representation mismatch: {root}")
    if receipt.get("evaluation_contract_sha256") != source_contract:
        raise ValueError(f"source evaluation contract mismatch: {root}")
    if receipt.get("task") != task:
        raise ValueError(f"source task identity mismatch: {root}")
    mmr = json.loads((root / "score/mmr_g1_r.json").read_text(encoding="utf-8"))
    tmmr = json.loads((root / "score/tmmr_g1.json").read_text(encoding="utf-8"))
    if mmr.get("selected_evaluator") != "MMR-G1-FD":
        raise ValueError(f"paper breadth requires frozen MMR-G1-FD: {root}")
    if tmmr.get("role") != "diagnostic_only_gt_calibration_failed":
        raise ValueError(f"unexpected T-MMR-G1 role: {root}")
    standard = {str(row["sequence_id"]): row for row in mmr["standard_metrics"]}
    learned = {str(row["sequence_id"]): row for row in tmmr["ensemble_per_track"]}
    rows = []
    for row in mmr["per_track"]:
        sequence = str(row["sequence_id"])
        if sequence not in standard or sequence not in learned:
            raise ValueError(f"paper metric populations disagree at {root}: {sequence}")
        physical = standard[sequence]
        temporal = learned[sequence]
        rows.append(
            {
                "sequence_id": sequence,
                "kinetic_feature": physical["kinetic_feature"],
                "geometric_feature": physical["geometric_feature"],
                "MMR-MS": float(row["mmr_ms"]),
                "T-MMR-G1": float(temporal["tmmr"]),
                "T-MMR-G1-global": float(temporal["global"]),
                "T-MMR-G1-local": float(temporal["local"]),
                **{name: float(physical[name]) for name in SCALAR_METRICS[4:]},
            }
        )
    if len(rows) != 18 or len({row["sequence_id"] for row in rows}) != 18:
        raise ValueError(f"paper breadth requires 18 unique tracks: {root}")
    return root, sorted(rows, key=lambda row: row["sequence_id"])


def target_features(canonical_root, expected_sequences):
    manifest = json.loads((canonical_root / "motion_manifest.json").read_text(encoding="utf-8"))
    records = sorted(manifest["records"], key=lambda row: str(row["sequence_id"]))
    if [str(row["sequence_id"]) for row in records] != list(expected_sequences):
        raise ValueError("target manifest does not match the official paper population")
    kinetic, geometric = [], []
    for record in records:
        motion = load_g1_motion(record["target_path"])
        fk = forward_g1_kinematics(
            motion,
            str(ROOT / "third_party/unitree_g1_description/g1_29dof_rev_1_0.xml"),
            root_quat_order="xyzw",
        )
        kinetic.append(kinetic_features_g1(fk["keypoints"], fps=motion["fps"]))
        geometric.append(geometric_features_g1(fk["keypoints"], motion["root_pos"]))
    return np.asarray(kinetic), np.asarray(geometric)


def distribution_metrics(target_k, target_g, rows, *, diversity_seed):
    generated_k = np.asarray([row["kinetic_feature"] for row in rows], dtype=np.float64)
    generated_g = np.asarray([row["geometric_feature"] for row in rows], dtype=np.float64)
    return {
        "FIDk-G1": frechet_distance(target_k, generated_k),
        "FIDg-G1": frechet_distance(target_g, generated_g),
        "Divk-G1": diversity(generated_k, seed=int(diversity_seed)),
        "Divg-G1": diversity(generated_g, seed=int(diversity_seed)),
    }


def mean_mapping(rows, names):
    return {name: float(np.mean([row[name] for row in rows])) for name in names}


def route_contrast(left, right):
    per_seed = {}
    for training_seed in map(str, TRAINING_SEEDS):
        left_seed = left["by_training_seed"][training_seed]
        right_seed = right["by_training_seed"][training_seed]
        values = {}
        for metric in DISTRIBUTION_METRICS + SCALAR_METRICS:
            a, b = float(left_seed["mean"][metric]), float(right_seed["mean"][metric])
            values[metric] = b - a if metric in LOWER_IS_BETTER else a - b
        per_seed[training_seed] = values
    return {
        "point": mean_mapping(list(per_seed.values()), DISTRIBUTION_METRICS + SCALAR_METRICS),
        "per_training_seed": per_seed,
        "direction_policy": {
            "FIDk-G1/FIDg-G1/MMR-MS/PFC-G1": "positive_means_left_better",
            "T-MMR-G1/G1BAS/G1FKBAS/G1FKRoboPerformBAS": "positive_means_left_better",
            "Divk-G1/Divg-G1": "raw_left_minus_right_descriptive_only",
        },
    }


def aggregate(reviewed_contract):
    source_contract, scale = source_identity()
    loaded = {}
    canonical_root = None
    sequences = None
    for route in ROUTES:
        for training_seed in TRAINING_SEEDS:
            for sampling_seed in SAMPLING_SEEDS:
                root, rows = read_leaf(
                    route, training_seed, sampling_seed, scale, source_contract
                )
                current = [row["sequence_id"] for row in rows]
                if sequences is None:
                    sequences, canonical_root = current, root
                elif current != sequences:
                    raise ValueError(f"track population mismatch at {root}")
                loaded[(route, training_seed, sampling_seed)] = rows

    target_k, target_g = target_features(canonical_root, sequences)
    table = {}
    for route in ROUTES:
        by_training_seed = {}
        all_rows = []
        for training_seed in TRAINING_SEEDS:
            by_sampling_seed = {}
            seed_rows = []
            for sampling_seed in SAMPLING_SEEDS:
                rows = loaded[(route, training_seed, sampling_seed)]
                seed_rows.extend(rows)
                all_rows.extend(rows)
                by_sampling_seed[str(sampling_seed)] = distribution_metrics(
                    target_k,
                    target_g,
                    rows,
                    diversity_seed=sampling_seed,
                )
            seed_distribution = mean_mapping(
                list(by_sampling_seed.values()), DISTRIBUTION_METRICS
            )
            by_training_seed[str(training_seed)] = {
                "by_sampling_seed": by_sampling_seed,
                "mean": {
                    **seed_distribution,
                    **mean_mapping(seed_rows, SCALAR_METRICS),
                },
            }
        table[route] = {
            "by_training_seed": by_training_seed,
            "mean": mean_mapping(
                [value["mean"] for value in by_training_seed.values()],
                DISTRIBUTION_METRICS + SCALAR_METRICS,
            ),
            "cells": len(all_rows),
        }

    contrasts = {
        name: route_contrast(table[left], table[right])
        for name, left, right in ROUTE_CONTRASTS
    }
    payload = {
        "schema": "issue49_paper_breadth_v1",
        "status": "complete_unreviewed",
        "experiment_id": EXP_ID,
        "reviewed_contract_sha256": reviewed_contract,
        "source_evaluation_contract_sha256": source_contract,
        "representation": REPRESENTATION,
        "population": {
            "tracks": 18,
            "training_seeds": list(TRAINING_SEEDS),
            "sampling_seeds": list(SAMPLING_SEEDS),
            "sampling_seed_policy": "average within each training seed",
            "condition_variant": "correct",
            "guidance_scale": scale,
        },
        "routes": table,
        "route_contrasts": contrasts,
        "metric_policy": {
            "FIDk-G1/FIDg-G1": "lower_better",
            "Divk-G1/Divg-G1": "descriptive_diversity",
            "MMR-MS": "lower_better_primary_learned_music_metric",
            "T-MMR-G1": "diagnostic_only_gt_calibration_failed",
            "G1BAS/G1FKBAS/G1FKRoboPerformBAS": "higher_better",
            "PFC-G1": "lower_better",
            "distribution_inference": "descriptive means and per-training-seed directions; no new route verdict",
        },
        "scientific_verdict": "not_assigned",
    }
    write_json(payload, OUTPUT / "aggregate.json")
    write_json(
        {
            "status": "passed",
            "experiment_id": EXP_ID,
            "reviewed_contract_sha256": reviewed_contract,
            "source_evaluation_contract_sha256": source_contract,
            "representation": REPRESENTATION,
            "aggregate": str((OUTPUT / "aggregate.json").resolve()),
        },
        OUTPUT / "completion_receipt.json",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(
            json.dumps(
                {
                    "routes": list(ROUTES),
                    "training_seeds": list(TRAINING_SEEDS),
                    "sampling_seeds": list(SAMPLING_SEEDS),
                    "tracks": 18,
                    "source": "existing official_final correct leaves",
                    "gpus": 0,
                },
                indent=2,
            )
        )
        return
    reviewed_contract = os.environ.get("REVIEWED_CONTRACT_SHA256", "")
    if not reviewed_contract:
        raise ValueError("missing REVIEWED_CONTRACT_SHA256")
    aggregate(reviewed_contract)


if __name__ == "__main__":
    main()
