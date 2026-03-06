# Email Draft to Professor Kilic

---

**To:** Professor Kilic  
**From:** Zuhtu Hilmi  
**Subject:** QC results from the barcode77 long-read run  
**Date:** March 2026

---

Dear Professor Kilic,

I hope you're doing well. I've finished running the quality check on the sequencing data from the barcode77 sample you sent over (the one related to the spoiled product investigation). Here's a quick rundown of what I found.

I set up an automated pipeline that goes through all 81,011 reads in the FASTQ file and calculates three things for each one: read length, GC content, and average quality score. I also ran NanoPlot, which is the go-to tool for nanopore QC -- it generates an interactive HTML report you can open in your browser.

Here are the main takeaways:

Regarding read lengths -- the median is around 547 bp, with a mean of about 1,038 bp. There's a wide spread though, with some very long reads going up to ~686 kb. The N50 is 1,761 bp. A lot of reads are on the shorter side, which might partly be due to the nature of the sample (degraded DNA from a spoiled product can fragment more than usual). That said, there's still a good chunk of longer reads, and the total throughput is ~84 million bases, which should give us decent coverage.

For GC content, the distribution is centered around 53%, which is consistent with what we'd expect from common foodborne bacterial species. The distribution looks clean and fairly symmetrical, so I don't see obvious signs of contamination from unrelated organisms.

Quality-wise, the data looks really solid. The mean quality is Q17.9, and 91% of reads are above Q7 (the standard nanopore threshold). About 78% are above Q10. These are strong numbers -- way above what's needed for reliable downstream analysis.

My recommendation: the data quality is good, and I'd say we should go ahead with alignment. Given the food safety context, we could align these against databases of known foodborne pathogens (Salmonella, Listeria, E. coli, etc.) to try to identify the organism responsible for spoilage. If you already have a suspect species in mind, let me know and I can align directly against that reference genome.

A couple of things I'd like to confirm before moving forward:
- Do you have a specific pathogen or organism you suspect?
- Should we run a broader metagenomic classification first (using something like Kraken2) before doing a targeted alignment?

I've attached the plots and the detailed stats below. The NanoPlot report is also included -- you can just double-click the HTML file to open it.

Best regards,
Zuhtu Hilmi

---

*Attachments:*
- gc_content_distribution.png
- read_length_distribution.png
- mean_quality_distribution.png
- summary_statistics.txt
- NanoPlot-report.html
