# Long-Read Sequencing QC Pipeline

A reproducible **Snakemake** pipeline for Quality Control (QC) of raw long-read sequencing data (Oxford Nanopore). Developed for a food safety investigation to assess the quality of barcode-demultiplexed Nanopore reads before downstream pathogen identification. The pipeline runs NanoPlot for comprehensive QC, computes per-read statistics (GC content, read length, mean quality), and generates distribution plots.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Workflow](#pipeline-workflow)
- [Expected Output](#expected-output)
- [Example Results](#example-results)
- [License](#license)

---

## Overview

This pipeline was developed to provide a quick, reproducible quality assessment of long-read sequencing data. It is designed for researchers who need to evaluate their raw reads before proceeding to downstream analyses (e.g., alignment, assembly).

**What it does:**
1. **NanoPlot QC** — Generates an interactive HTML quality control report specifically designed for long reads.
2. **Per-Read Statistics** — Calculates GC content (%), read length (bp), and mean Phred quality score for every individual read.
3. **Visualization** — Produces histograms with density overlays for all three metrics, plus a detailed summary statistics report.

---

## Project Structure

```
Bioinformatics/
├── Snakefile                        # Pipeline definition (3 rules)
├── config.yaml                      # Pipeline configuration
├── environment.yml                  # Conda environment specification
├── .gitignore
├── README.md                        # This file
├── email_to_professor.md            # Email draft for Prof. Kılıç
├── data/
│   └── barcode77.fastq.gz           # Input FASTQ (not tracked in git)
├── scripts/
│   ├── generate_test_data.py        # Synthetic test data generator
│   ├── read_stats.py                # Per-read statistics calculator
│   └── plot_stats.py                # Distribution plot generator
└── results/                         # Pipeline output (gitignored)
    ├── nanoplot/                     # NanoPlot QC report
    ├── read_statistics.csv           # Per-read statistics
    ├── plots/
    │   ├── gc_content_distribution.png
    │   ├── read_length_distribution.png
    │   ├── mean_quality_distribution.png
    │   └── summary_statistics.txt
    └── logs/                         # Process logs
```

---

## Prerequisites

- **Conda** (Miniconda or Anaconda) — [Install Conda](https://docs.conda.io/en/latest/miniconda.html)
- **Git** — [Install Git](https://git-scm.com/)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Zuhtu-Hilmi/longreads-qc-pipeline.git
cd longreads-qc-pipeline
```

### 2. Create the Conda Environment

```bash
conda env create -f environment.yml
conda activate longreads-qc
```

### 3. Generate Test Data (Optional)

If you don't have your own FASTQ file, generate synthetic long-read data:

```bash
python scripts/generate_test_data.py --n_reads 100 --output data/sample.fastq
```

---

## Usage

### Run the Full Pipeline

```bash
snakemake --configfile config.yaml --cores 1
```

### Use Your Own FASTQ File

Edit `config.yaml` to point to your own FASTQ file:

```yaml
input_fastq: "path/to/your/reads.fastq"
```

Then run the pipeline as shown above.

### Run Individual Steps

You can also run the custom scripts independently:

```bash
# Calculate per-read statistics
python scripts/read_stats.py data/barcode77.fastq.gz results/read_statistics.csv

# Generate plots from the statistics CSV
python scripts/plot_stats.py results/read_statistics.csv results/plots/
```

### Dry Run (Preview What Will Execute)

```bash
snakemake --configfile config.yaml -n
```

---

## Pipeline Workflow

```
                    ┌─────────────────┐
                    │  Input FASTQ    │
                    │  (long reads)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              │
     ┌────────────┐  ┌──────────────┐       │
     │  NanoPlot  │  │  read_stats  │       │
     │    QC      │  │  .py         │       │
     └────────────┘  └──────┬───────┘       │
              │              │              │
              ▼              ▼              │
     ┌────────────┐  ┌──────────────┐       │
     │  HTML QC   │  │  Statistics  │       │
     │  Report    │  │  CSV         │       │
     └────────────┘  └──────┬───────┘       │
                             │              │
                             ▼              │
                     ┌──────────────┐       │
                     │  plot_stats  │       │
                     │  .py         │       │
                     └──────┬───────┘       │
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
           ┌──────────────┐  ┌──────────────┐
           │  PNG Plots   │  │  Summary     │
           │  (3 graphs)  │  │  Statistics  │
           └──────────────┘  └──────────────┘
```

---

## Expected Output

After a successful run, the `results/` directory will contain:

| File | Description |
|------|-------------|
| `nanoplot/NanoPlot-report.html` | Interactive NanoPlot QC report |
| `read_statistics.csv` | Per-read GC%, length, and quality |
| `plots/gc_content_distribution.png` | GC content histogram |
| `plots/read_length_distribution.png` | Read length histogram |
| `plots/mean_quality_distribution.png` | Quality score histogram |
| `plots/summary_statistics.txt` | Mean, median, N50, and more |

---

## Example Results

After running the pipeline, you will see summary statistics similar to:

```
============================================================
        SUMMARY STATISTICS -- LONG-READ QC
============================================================
  Total Reads:  81,011
  Total Bases:  84,108,485 bp

  -- Read Length (bp) -------------------------
    Mean:         1,038.2
    Median:         547.0
    N50:            1,761

  -- GC Content (%) --------------------------
    Mean:           53.00
    Median:         53.53

  -- Mean Quality Score (Phred) --------------
    Mean:           17.90
    Median:         17.31
    Reads >= Q7:    73,993  (91.3%)
============================================================
```

---

## License

This project is open source and available under the [MIT License](LICENSE).
