#!/usr/bin/env python3
"""Run a small, observable Palmer Penguins model-training job."""

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def bounded_integer(value: str) -> int:
    parsed = int(value)
    if not 1 <= parsed <= 1000:
        raise argparse.ArgumentTypeError("must be between 1 and 1000")
    return parsed


def bounded_delay(value: str) -> float:
    parsed = float(value)
    if not 0 <= parsed <= 60:
        raise argparse.ArgumentTypeError("must be between 0 and 60 seconds")
    return parsed


def cancelled(signum: int, _frame: object) -> None:
    print(
        f"cancelled by signal {signum} on {socket.gethostname()} (pid {os.getpid()})",
        file=sys.stderr,
        flush=True,
    )
    raise SystemExit(128 + signum)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--steps", type=bounded_integer, default=8)
    parser.add_argument("--delay", type=bounded_delay, default=1.0)
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, cancelled)
    signal.signal(signal.SIGINT, cancelled)

    penguins = pd.read_csv(args.dataset)
    features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm"]
    complete = penguins.dropna(subset=[*features, "body_mass_g"])
    random = np.random.default_rng(20260904)
    scores: list[float] = []

    for step in range(1, args.steps + 1):
        sample = complete.iloc[random.integers(0, len(complete), len(complete))]
        model = LinearRegression().fit(sample[features], sample["body_mass_g"])
        score = float(model.score(complete[features], complete["body_mass_g"]))
        scores.append(score)
        print(
            f"progress={step}/{args.steps} validation_r2={score:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if step != args.steps:
            time.sleep(args.delay)

    print(
        json.dumps(
            {
                "dataset_rows": len(penguins),
                "host": socket.gethostname(),
                "mean_validation_r2": round(float(np.mean(scores)), 4),
                "pid": os.getpid(),
                "steps": args.steps,
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
