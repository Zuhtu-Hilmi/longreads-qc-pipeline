#!/usr/bin/env python3
"""
generate_test_data.py
=====================
Generate a synthetic FASTQ file that mimics long-read sequencing output
(e.g., Oxford Nanopore or PacBio).

Reads have:
  - Lengths drawn from a log-normal distribution (median ~5 kb, range ~500 bp – 30 kb)
  - Realistic GC content (~40-60 %)
  - Quality scores drawn from a normal distribution (mean ~Q10, σ ~2)

Usage:
    python scripts/generate_test_data.py [--n_reads 100] [--output data/sample.fastq]
"""

import argparse
import os
import random
import string
import numpy as np


def phred_char(q: int) -> str:
    """Convert a Phred quality score (0-40) to its ASCII character."""
    return chr(max(0, min(q, 40)) + 33)


def generate_read(read_id: int, length: int, gc_frac: float, mean_qual: float) -> str:
    """Generate a single FASTQ record."""
    # Build nucleotide sequence with target GC content
    gc_count = int(length * gc_frac)
    at_count = length - gc_count
    bases = (
        random.choices(["G", "C"], k=gc_count)
        + random.choices(["A", "T"], k=at_count)
    )
    random.shuffle(bases)
    seq = "".join(bases)

    # Generate quality string — per-base quality from normal dist around mean_qual
    quals = []
    for _ in range(length):
        q = int(np.random.normal(mean_qual, 2.0))
        q = max(2, min(q, 35))  # clamp to realistic range
        quals.append(phred_char(q))

    qual_str = "".join(quals)

    # Random hex suffix for read name realism
    suffix = "".join(random.choices(string.hexdigits[:16], k=8))

    header = f"@read_{read_id:05d}_{suffix} runid=synthetic_run ch={random.randint(1,512)}"
    return f"{header}\n{seq}\n+\n{qual_str}"


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic long-read FASTQ")
    parser.add_argument("--n_reads", type=int, default=100, help="Number of reads to generate (default: 100)")
    parser.add_argument("--output", type=str, default="data/sample.fastq", help="Output FASTQ file path")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    records = []
    for i in range(args.n_reads):
        # Log-normal length distribution: median ~5000, range ~500-30000
        length = int(np.random.lognormal(mean=8.5, sigma=0.7))
        length = max(200, min(length, 50000))

        # GC content uniformly between 35% and 65%
        gc_frac = np.random.uniform(0.35, 0.65)

        # Mean quality score per read: normal dist, mean=10, σ=2.5
        mean_qual = np.random.normal(loc=10.0, scale=2.5)
        mean_qual = max(5.0, min(mean_qual, 20.0))

        records.append(generate_read(i, length, gc_frac, mean_qual))

    with open(args.output, "w") as fh:
        fh.write("\n".join(records) + "\n")

    print(f"[OK] Generated {args.n_reads} synthetic long reads -> {args.output}")
    print(f"  File size: {os.path.getsize(args.output) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
