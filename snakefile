import os

wd = os.cwd()
directories, subs = glob_wildcards(wd + "/{dir}/{sub}")

rule all:
    input:
        wd + "/experiment_summary.tab"

rule package_fq:
    input:
        "./{dir}/{sub}/fastq_pass/"
    output:
        "{dir}.fastq.tar.gz"
    shell:
        "tar -czvf {output} {input}"

rule delete_fails:
    input:
        ffive = "./{dir}/{sub}/fast5_fail/",
        fq = "./{dir}/{sub}/fastq_fail/"
    output:
        touch("{dir}.{sub}_erased.txt")
    shell:
        """
        rm -r {input.ffive}
        rm -r {input.fq}
        """
rule package_exp:
    input:
        task = "{dir}.{sub}_erased.txt",
        libs = "./{dir}/{sub}/"
    output:
        "{dir}.exp.tar.gz"
    shell:
        "tar -czvf {output} {input.libs}"

rule run_summary_plot:
    input:
        "./{dir}/{sub}/fastq_pass/"
    output:
        "read_plots/{dir}-lrplots.png",
        "read_summaries/{dir}-summary_stats.tab"
    shell:
        """
        python3 scripts/lrplot.py {dir} {input}
        """

#rule delete_everything:
