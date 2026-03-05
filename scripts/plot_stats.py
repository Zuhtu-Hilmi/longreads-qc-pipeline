#!/usr/bin/env python3
"""
plot_stats.py
=============
Read the per-read statistics CSV and generate distribution plots for:
  1. GC Content (%)
  2. Read Length (bp)
  3. Mean Quality Score (Phred)

Also calculates and prints summary statistics (mean, median, N50, etc.).

Usage:
    python scripts/plot_stats.py <read_statistics.csv> <output_directory>
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for pipeline use
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# Plot styling
# =============================================================================
sns.set_theme(style="whitegrid", context="talk", palette="muted")
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "font.family": "sans-serif",
})

COLORS = {
    "gc":      "#2ecc71",
    "length":  "#3498db",
    "quality": "#e74c3c",
}


def calculate_n50(lengths: np.ndarray) -> int:
    """Calculate the N50 metric for a set of read lengths."""
    sorted_lengths = np.sort(lengths)[::-1]
    cumsum = np.cumsum(sorted_lengths)
    half_total = cumsum[-1] / 2
    n50_idx = np.searchsorted(cumsum, half_total)
    return int(sorted_lengths[n50_idx])


def plot_gc_content(df: pd.DataFrame, output_dir: str) -> None:
    """Plot GC content distribution as a histogram with KDE overlay."""
    fig, ax = plt.subplots()
    sns.histplot(
        data=df, x="gc_content", bins=30, kde=True,
        color=COLORS["gc"], edgecolor="white", alpha=0.8, ax=ax,
    )
    median_gc = df["gc_content"].median()
    ax.axvline(median_gc, color="black", linestyle="--", linewidth=1.5,
               label=f"Median: {median_gc:.1f}%")
    ax.set_xlabel("GC Content (%)")
    ax.set_ylabel("Number of Reads")
    ax.set_title("GC Content Distribution")
    ax.legend()
    filepath = os.path.join(output_dir, "gc_content_distribution.png")
    fig.savefig(filepath)
    plt.close(fig)
    print(f"  -> Saved: {filepath}")


def plot_read_lengths(df: pd.DataFrame, output_dir: str) -> None:
    """Plot read length distribution as a histogram with KDE overlay."""
    fig, ax = plt.subplots()
    sns.histplot(
        data=df, x="read_length", bins=40, kde=True,
        color=COLORS["length"], edgecolor="white", alpha=0.8, ax=ax,
    )
    median_len = df["read_length"].median()
    n50 = calculate_n50(df["read_length"].values)
    ax.axvline(median_len, color="black", linestyle="--", linewidth=1.5,
               label=f"Median: {median_len:,.0f} bp")
    ax.axvline(n50, color="orange", linestyle="--", linewidth=1.5,
               label=f"N50: {n50:,} bp")
    ax.set_xlabel("Read Length (bp)")
    ax.set_ylabel("Number of Reads")
    ax.set_title("Read Length Distribution")
    ax.legend()
    filepath = os.path.join(output_dir, "read_length_distribution.png")
    fig.savefig(filepath)
    plt.close(fig)
    print(f"  -> Saved: {filepath}")


def plot_mean_quality(df: pd.DataFrame, output_dir: str) -> None:
    """Plot mean quality score distribution as a histogram with KDE overlay."""
    fig, ax = plt.subplots()
    sns.histplot(
        data=df, x="mean_quality", bins=30, kde=True,
        color=COLORS["quality"], edgecolor="white", alpha=0.8, ax=ax,
    )
    median_q = df["mean_quality"].median()
    # Add a vertical line at Q7 (common threshold for nanopore)
    ax.axvline(7.0, color="gray", linestyle=":", linewidth=1.2,
               label="Q7 threshold")
    ax.axvline(median_q, color="black", linestyle="--", linewidth=1.5,
               label=f"Median: Q{median_q:.1f}")
    ax.set_xlabel("Mean Quality Score (Phred)")
    ax.set_ylabel("Number of Reads")
    ax.set_title("Mean Read Quality Score Distribution")
    ax.legend()
    filepath = os.path.join(output_dir, "mean_quality_distribution.png")
    fig.savefig(filepath)
    plt.close(fig)
    print(f"  -> Saved: {filepath}")


def print_summary_statistics(df: pd.DataFrame, output_dir: str) -> None:
    """Calculate and display summary statistics for all three metrics."""
    n50 = calculate_n50(df["read_length"].values)

    summary_lines = []
    summary_lines.append("=" * 60)
    summary_lines.append("        SUMMARY STATISTICS -- LONG-READ QC")
    summary_lines.append("=" * 60)
    summary_lines.append(f"  Total Reads:  {len(df):,}")
    summary_lines.append(f"  Total Bases:  {df['read_length'].sum():,} bp")
    summary_lines.append("")

    # Read Length
    summary_lines.append("  -- Read Length (bp) -------------------------")
    summary_lines.append(f"    Mean:      {df['read_length'].mean():>10,.1f}")
    summary_lines.append(f"    Median:    {df['read_length'].median():>10,.1f}")
    summary_lines.append(f"    Std Dev:   {df['read_length'].std():>10,.1f}")
    summary_lines.append(f"    Min:       {df['read_length'].min():>10,}")
    summary_lines.append(f"    Max:       {df['read_length'].max():>10,}")
    summary_lines.append(f"    N50:       {n50:>10,}")
    summary_lines.append("")

    # GC Content
    summary_lines.append("  -- GC Content (%) --------------------------")
    summary_lines.append(f"    Mean:      {df['gc_content'].mean():>10.2f}")
    summary_lines.append(f"    Median:    {df['gc_content'].median():>10.2f}")
    summary_lines.append(f"    Std Dev:   {df['gc_content'].std():>10.2f}")
    summary_lines.append(f"    Min:       {df['gc_content'].min():>10.2f}")
    summary_lines.append(f"    Max:       {df['gc_content'].max():>10.2f}")
    summary_lines.append("")

    # Mean Quality
    summary_lines.append("  -- Mean Quality Score (Phred) --------------")
    summary_lines.append(f"    Mean:      {df['mean_quality'].mean():>10.2f}")
    summary_lines.append(f"    Median:    {df['mean_quality'].median():>10.2f}")
    summary_lines.append(f"    Std Dev:   {df['mean_quality'].std():>10.2f}")
    summary_lines.append(f"    Min:       {df['mean_quality'].min():>10.2f}")
    summary_lines.append(f"    Max:       {df['mean_quality'].max():>10.2f}")
    summary_lines.append(f"    Reads >= Q7:{df[df['mean_quality'] >= 7].shape[0]:>10,}  "
                         f"({df[df['mean_quality'] >= 7].shape[0] / len(df) * 100:.1f}%)")
    summary_lines.append(f"    Reads >= Q10:{df[df['mean_quality'] >= 10].shape[0]:>9,}  "
                         f"({df[df['mean_quality'] >= 10].shape[0] / len(df) * 100:.1f}%)")
    summary_lines.append("=" * 60)

    summary_text = "\n".join(summary_lines)

    # Print to console
    print(summary_text)

    # Save to file
    filepath = os.path.join(output_dir, "summary_statistics.txt")
    with open(filepath, "w") as fh:
        fh.write(summary_text + "\n")
    print(f"\n  -> Summary saved to: {filepath}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python plot_stats.py <read_statistics.csv> <output_directory>")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Reading statistics from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"  Loaded {len(df):,} reads\n")

    print("Generating distribution plots...")
    plot_gc_content(df, output_dir)
    plot_read_lengths(df, output_dir)
    plot_mean_quality(df, output_dir)

    print("\nCalculating summary statistics...")
    print_summary_statistics(df, output_dir)

    print("\n[OK] Visualization complete!")


if __name__ == "__main__":
    main()
