#!/usr/bin/env python3
"""Analyse the Palmer Penguins dataset with pandas and scikit-learn."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} DATASET.csv")

    dataset = Path(sys.argv[1])
    penguins = pd.read_csv(dataset)

    print(f"Palmer Penguins: {len(penguins)} observations")
    summary = penguins.groupby("species")["body_mass_g"].agg(["count", "mean"])
    for species, row in summary.sort_index().iterrows():
        print(f"{species}: {int(row['count'])} birds, mean mass {row['mean']:.0f} g")

    features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm"]
    complete = penguins.dropna(subset=[*features, "body_mass_g"])
    model = LinearRegression().fit(complete[features], complete["body_mass_g"])
    print(
        "Linear mass model: "
        f"{len(complete)} complete rows, R^2={model.score(complete[features], complete['body_mass_g']):.3f}"
    )


if __name__ == "__main__":
    main()
