#!/usr/bin/env python3
"""Print a compact summary of the Palmer Penguins dataset."""

from __future__ import annotations

import csv
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} DATASET.csv")

    dataset = Path(sys.argv[1])
    with dataset.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    counts = Counter(row["species"] for row in rows)
    masses: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row["body_mass_g"] not in {"", "NA"}:
            masses[row["species"]].append(float(row["body_mass_g"]))

    print(f"Palmer Penguins: {len(rows)} observations")
    for species in sorted(counts):
        mean_mass = statistics.fmean(masses[species])
        print(f"{species}: {counts[species]} birds, mean mass {mean_mass:.0f} g")


if __name__ == "__main__":
    main()
