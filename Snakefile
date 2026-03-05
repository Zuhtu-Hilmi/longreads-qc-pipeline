# =============================================================================
# Mini-Bioinformatics Pipeline: Long-Read Sequencing QC
# =============================================================================
# A reproducible Snakemake pipeline that performs quality control on raw
# long-read sequencing data, calculates per-read statistics, and generates
# publication-quality visualizations.
#
# Usage:
#   snakemake --configfile config.yaml --cores 1 --use-conda
# =============================================================================

configfile: "config.yaml"

# Input / output paths from config
INPUT_FASTQ = config["input_fastq"]
OUTPUT_DIR  = config["output_dir"]


rule all:
    """Target rule: request all final outputs."""
    input:
        # NanoPlot QC report
        f"{OUTPUT_DIR}/nanoplot/NanoPlot-report.html",
        # Per-read statistics CSV
        f"{OUTPUT_DIR}/read_statistics.csv",
        # Distribution plots
        f"{OUTPUT_DIR}/plots/gc_content_distribution.png",
        f"{OUTPUT_DIR}/plots/read_length_distribution.png",
        f"{OUTPUT_DIR}/plots/mean_quality_distribution.png",
        # Summary statistics text file
        f"{OUTPUT_DIR}/plots/summary_statistics.txt",


# -----------------------------------------------------------------------------
# Rule 1: NanoPlot QC — long-read specific quality control
# -----------------------------------------------------------------------------
rule nanoplot_qc:
    """
    Run NanoPlot on the raw FASTQ file.
    NanoPlot is specifically designed for long-read sequencing QC and produces
    interactive HTML reports with read length distributions, quality plots, etc.
    """
    input:
        fastq = INPUT_FASTQ,
    output:
        report = f"{OUTPUT_DIR}/nanoplot/NanoPlot-report.html",
    params:
        outdir = f"{OUTPUT_DIR}/nanoplot",
    log:
        f"{OUTPUT_DIR}/logs/nanoplot.log",
    shell:
        """
        NanoPlot \
            --fastq {input.fastq} \
            --outdir {params.outdir} \
            --plots dot \
            --loglength \
            2>&1 | tee {log}
        """


# -----------------------------------------------------------------------------
# Rule 2: Custom per-read statistics
# -----------------------------------------------------------------------------
rule read_stats:
    """
    Calculate GC content (%), read length, and mean quality score for each
    individual read in the FASTQ file using a custom Python script.
    Output: a CSV with columns [read_id, gc_content, read_length, mean_quality].
    """
    input:
        fastq = INPUT_FASTQ,
    output:
        csv = f"{OUTPUT_DIR}/read_statistics.csv",
    log:
        f"{OUTPUT_DIR}/logs/read_stats.log",
    shell:
        """
        python scripts/read_stats.py \
            {input.fastq} \
            {output.csv} \
            2>&1 | tee {log}
        """


# -----------------------------------------------------------------------------
# Rule 3: Visualization — distribution plots & summary stats
# -----------------------------------------------------------------------------
rule plot_distributions:
    """
    Generate histograms for GC content, read length, and mean quality score
    distributions. Also compute and save summary statistics (mean, median,
    N50, etc.) to a text file.
    """
    input:
        csv = f"{OUTPUT_DIR}/read_statistics.csv",
    output:
        gc_plot      = f"{OUTPUT_DIR}/plots/gc_content_distribution.png",
        length_plot  = f"{OUTPUT_DIR}/plots/read_length_distribution.png",
        quality_plot = f"{OUTPUT_DIR}/plots/mean_quality_distribution.png",
        summary      = f"{OUTPUT_DIR}/plots/summary_statistics.txt",
    log:
        f"{OUTPUT_DIR}/logs/plot_distributions.log",
    shell:
        """
        python scripts/plot_stats.py \
            {input.csv} \
            {OUTPUT_DIR}/plots \
            2>&1 | tee {log}
        """
