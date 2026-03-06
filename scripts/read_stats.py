#!/usr/bin/env python3
"""
read_stats.py
=============
Parse a FASTQ file and compute per-read statistics:
  1. GC Content (%)
  2. Read Length (bp)
  3. Mean Read Quality Score (Phred)

Output: CSV file with columns [read_id, gc_content, read_length, mean_quality]

Usage:
    python scripts/read_stats.py <input.fastq> <output.csv>
"""

import sys
import os
import csv
import gzip


def phred_score(char: str) -> int:
    """Convert an ASCII quality character to its Phred score."""
    return ord(char) - 33


def compute_gc_content(sequence: str) -> float:
    """Calculate the GC content percentage of a DNA sequence."""
    if len(sequence) == 0:
        return 0.0
    gc_count = sequence.upper().count("G") + sequence.upper().count("C")
    return (gc_count / len(sequence)) * 100.0


def compute_mean_quality(quality_string: str) -> float:
    """Calculate the mean Phred quality score from a quality string."""
    if len(quality_string) == 0:
        return 0.0
    scores = [phred_score(ch) for ch in quality_string]
    return sum(scores) / len(scores)


def parse_fastq(filepath: str):
    """
    Generator that yields (read_id, sequence, quality_string) tuples
    from a FASTQ file. Supports both plain and gzipped (.gz) files.
    """
    open_func = gzip.open if filepath.endswith(".gz") else open
    with open_func(filepath, "rt") as fh:
        while True:
            header = fh.readline().strip()
            if not header:
                break  # EOF
            if not header.startswith("@"):
                raise ValueError(f"Expected FASTQ header starting with '@', got: {header}")

            sequence = fh.readline().strip()
            plus_line = fh.readline().strip()  # '+' separator
            quality = fh.readline().strip()

            # Extract read ID (first word after '@')
            read_id = header[1:].split()[0]

            yield read_id, sequence, quality


def main():
    if len(sys.argv) != 3:
        print("Usage: python read_stats.py <input.fastq> <output.csv>")
        sys.exit(1)

    input_fastq = sys.argv[1]
    output_csv = sys.argv[2]

    if not os.path.exists(input_fastq):
        print(f"Error: Input file not found: {input_fastq}")
        sys.exit(1)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv) if os.path.dirname(output_csv) else ".", exist_ok=True)

    read_count = 0
    total_bases = 0

    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["read_id", "gc_content", "read_length", "mean_quality"])

        for read_id, sequence, quality in parse_fastq(input_fastq):
            gc = compute_gc_content(sequence)
            length = len(sequence)
            mean_q = compute_mean_quality(quality)

            writer.writerow([
                read_id,
                f"{gc:.2f}",
                length,
                f"{mean_q:.2f}",
            ])

            read_count += 1
            total_bases += length

    print(f"[OK] Processed {read_count:,} reads ({total_bases:,} total bases)")
    print(f"  Output saved to: {output_csv}")


if __name__ == "__main__":
    main()
