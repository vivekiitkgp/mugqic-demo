# Google Summer of Code 2016

----

## Project Info

Project title: **Implement base modification analysis in the *pacbio_assembly* pipeline**

Project short title (30 characters): Improve *pacbio_assembly* pipeline

URL of project idea page: [Implement base modification analysis in the *pacbio_assembly* pipeline](https://bitbucket.org/mugqic/gsoc2016#markdown-header-implement-base-modification-analysis-in-the-pacbio_assembly-pipeline-from-mugqic-pipelines)

## Biographical Information

I am hooked to open-source software development, an ambitious outgrowth of my
personal interests to create [free](https://www.gnu.org/philosophy/free-sw.html)
(as in [freedom!](http://c2.com/cgi/wiki?FreeAsInBeer)) and
[open-source](http://c2.com/cgi/wiki?OpenSource) content.

I have learned a lot by contributing to these projects:

* [Sequenceserver](https://github.com/wurlmab/sequenceserver)
* [WIGI](https://github.com/notconfusing/WIGI) and [WIGI-website](https://github.com/hargup/WIGI-website)
* [Afra](https://github.com/wurlmab/afra)

I use [GNU/Linux](https://www.debian.org/releases/squeeze/i386/ch01s02.html.en),
keep files under [version control](https://git-scm.com/), and edit using
[Vim](http://vim.org).

Languages I use: Python, Ruby, JavaScript, MATLAB, BASH.

In addition, sequencing data analysis poses a significant challenge

## Contact Information

* Student name: Vivek Rai
* Telephone(s): +91 8013291569
* Email(s): vivekraiiitkgp@gmail.com
* Skype: vivekrai.iitkgp
* Google+ (Hangouts): vivekraiiitkgp@gmail.com
* IRC: vivekrai @ freenode
* GitHub: https://github.com/vivekiitkgp
* BitBucket: https://bitbucket.com/vivekiitkgp
* Twitter: https://twitter.com/vivek_ziel

## Student Affiliation

Institution: **Indian Institute of Technology Kharagpur**

Program: *Integrated Dual Degree (Bachelor’s and Master’s)*

Stage of completion: 8th semester, 2017 (expected graduation)

Contact to verify: Official enrollment certificate


## Schedule Conflicts

A significant portion of the coding period is available as the summer break
during which I have no other commitment. I have, however, applied to other
internships and projects where again I would be working on next-generation
sequencing data analysis.

I believe that the two experiences, if selected, could be complementary.

## Mentors

Mentor names: Mathieu Bourgey, Edouard Henrion, Gary Leveque

Mentor emails:
[mathieu.bourgey@...](mailto:mathieu.bourgey@computationalgenomics.ca),
[edouard.henrion@...](mailto:edouard.henrion@computationalgenomics.ca),
[gary.leveque@...](mailto:gary.leveque@computationalgenomics.ca)

I have been in touch with the mentors since organization announcement through
email.

## Synopsis

 [Single Molecule, Real
 Time](http://www.pacb.com/products-and-services/analytical-software/smrt-analysis/)
 (SMRT) analysis is an exciting technology by Pacific Biosciences for the
 detection of DNA sequences and DNA base modifications. SMRT Sequencing
 identifies bases at each position using kinetic information recorded during
 each nucleotide addition step.[1] The same information can also be used to
 distinguish modified and native bases by compare results of SMRT Sequencing to
 an *in silico* kinetic reference for dynamics without modifications. MUGQIC
 pipelines currently consist of a general basic analysis implementation of
 *pacbio_assembly* pipeline following the [HGAP
 workflow](https://github.com/PacificBiosciences/Bioinformatics-Training/wiki/HGAP-in-SMRT-Analysis).
 In this proposal, we wish to extend the analysis pipeline by adding base
 modification detection and analysis tools. They may be of interest when
 pursuing more in-depth base modification studies or searching for epigenetics
 markers.

##  Benefits to Community

 Advent of next-generation sequencing platforms and their continuous improvement
 has led to a data explosion problem. The corresponding progress in the research
 and analysis of the subsequent data, however, has long been outpaced. These
 reasons combined have greatly pushed for the development of software and
 pipelines for automated analysis in the past decade. Sequence assembly is
 a computationally *hard* problem and it in non-trivial to obtain the optimal
 assembly. However, as the information is being unearthed, it is also being
 applied rapidly across different domains of science, industry and medicine.
 From personalized medicine, disease hall mark detection, genome and metabolome
 engineering. And these examples are only going to increase with the increased
 efficiency of computation from current stage.

 Nevertheless, there are several non-optimal but efficient implementations exist
 that seek to approach the solution in different ways with varying degree of
 accuracy. As a result there is no single tool today that does it all for us. We
 often have to rely on several independent pieces of software, as a pipeline, to
 process the data and generate sensible output. Here comes the contribution of
 C3G group (and MUGQIC pipelines). MUGQIC pipelines consist of interesting and
 user-friendly Python scripts for the analysis of sequencing (NGS) data. The
 automated assembly is currently available for processing DNA-Seq, RNA-Seq, and
 ChiP-Seq data.
 
 The proposal aims to extend the existing ability of MUGQIC *pacbio_assembly*
 pipeline. The changes, when implemented, could be used for downstream analysis
 by hundreds of researchers groups. Additionally, the fact that these pipelines
 are developed in open, allows one to receive critical community feedback,
 adoption, and good-will. It will ultimately promote the culture of a barrier
 free open science and research, an idea that I am increasingly inclined to
 pursue in my career.

 And not to mention, I will be working with an able community of researchers and
 engineers alike, learn about latest developments, work hands-on handling large
 amount of data and processing. Essentially, a lot of tricky details to learn
 that are available only though a practical experience.

## Coding Plan & Methods

The Pacific Biosciences team published their findings of detecting base
modifications using the sensitivity of SMRT analysis.[1] The SMRT analysis can
detect the methylation status at single molecule level via shifts in the
polymerase kinetics observed in the real-time sequencing traces.

The functionality is made available to the users through the
[kineticsTools](https://github.com/PacificBiosciences/kineticsTools) tool.
kineticsTools is written in Python and used to process a reference FASTA plus
the associated aligned reads HDF5 file and output modification and motif
analysis in CSV and GFF (after applying a significance filter). A detailed list
of [inputs](https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst#inputs)
and [outputs](https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst#outputs)
can be found on the [documentation](https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst)
page.

The output of this tool can subsequently be fed to tools like
[MotifMaker](https://github.com/PacificBiosciences/MotifMaker). MotifMaker is
a command-line Java program that identifies motifs associated with DNA
modifications in prokaryotic genomes, specifically the methylome pattern.

> Modified DNA in prokaryotes commonly arises from restriction-modification
> systems that methylate a specific base in a specific sequence motif. The
> canonical example the m6A methylation of adenine in GATC contexts in E.coli.
> Prokaryotes may have a very large number of active restriction-modification
> systems present, leading to a complicated mixture of sequence motifs.
>
> -- (MotifMaker documentation)

The command line API of MotifMaker is shown below.

```bash
$ java -jar target/motif-maker-0.2.one-jar.jar

Usage: MotifMaker [options] [command] [command options]
  Options:
    -h, --help
                 Default: false
  Commands:
    find      Run motif finding
      Usage: find [options]
        Options:
        * -f, --fasta      Reference fasta file
        * -g, --gff        modifications.gff or .gff.gz file
          -m, --minScore   Minimum Qmod score to use in motif finding
                           Default: 40.0
        * -o, --output     Output motifs csv file
          -x, --xml        Output motifs xml file

    reprocess      Reprocess gff file with motif information
      Usage: reprocess [options]
        Options:
          -c, --csv           Raw modifications.csv file
        * -f, --fasta         Reference fasta file
        * -g, --gff           original modifications.gff or .gff.gz file
              --minFraction   Only use motifs above this methylated fraction
                              Default: 0.75
        * -m, --motifs        motifs csv
        * -o, --output        Reprocessed modifications.gff file
```

MotifMaker supports two commands:
* `find` takes as input the reference FASTA file and a `modifications.gff`
    generated by kineticsTools as described before and outputs a motifs CSV
    file. The additional parameter `-m` is used to specific Qmod score. The
    score can be used to regulate motif search based on the modification types
    or genome type. A [detailed
    description](https://github.com/PacificBiosciences/Bioinformatics-Training/wiki/Base-Modification-:--From-Sequencing-Data-to-a-High-Confidence-Motif-List)
    of the score is available.

* `reprocess` will update a `modifications.gff` file with information
    based on new modification QV thresholds.

### Updating Pipeline

The base modification analysis will be added as a analysis step in the existing
`pacbio_assembly.py` file. Since, MotifMaker is a standalone Java tool, the
program can be run independently as a Job and the output generated can be saved
in a separate directory.

> TODO: Probe the Java installation status on the clusters, setting up
> environment if not available.

Since, MotifMaker is dependent on the files generated by kineticsTools, the
dependency will be installed and made available as a command line commands
(kineticsTools packages handy `setup.py`) - `ipdSummary` and
`summarizeModifications`. These scripts require a standard `.cmp.h5` file
containing alignments (which is generated in the `polishing()` step of the
assembly) and a reference FASTA file.

> ### Request comment:
>
> The kineticsTools documentation says the following about reference sequence
> file:
> “Currently this must be supplied via the path to a SMRTportal reference
> repository entry.”[2]
>
> Can you please explain what does the SMRTportal repository entry refers to?

Currently, the `pacbio_assembly.py` script implements the following main steps
of creating genome assembly.

* `smrtanalysis_filtering()`
* `pacbio_tools_get_cutoff()`
* `preassembly()`
* `assembly()`
* `polishing()`

In the `polishing()` stage, aligned reads (`aligned_reads.cmp.h5`) are generated
in the `$polishing_round_directory/data`. This directory can be directly used as
an input source for the `kineticsTools` scripts and the output can be stored in
the same directory for later access by `MotifMaker`.

We will add the functions to handle the `kineticsTools` programs input and
output as `bfx/kineticstools.py` with two main functions corresponding to the
two programs. Similarly, we will add functions for MotifMaker’s `find` and
`reprocess` commands in `bfx/motifmaker.py`.

* all input arguments will consume file path to the respective alignment,
    reference FASTA, output and other accessory files, extra options may be
    supported as required.

```python
>>> ktools_idpSummary.__doc__
""" Run kineticsTools on the input files to generate base modification iDP
    pattern.

    Args:
    reference: Path to reference FASTA file
    outfile: Path to output file
    aligned_reads: Path to aligned reads *.cmp.h5 file
    options: `dict` containing other options e.g., {numworkers, pvalue}

    Returns:

    `Job` object which when executed creates the necessary output file as
    provided in the input arguments.
"""

>>> motifmaker_find.__doc__
""" Run MotifMaker’s find program to search for motifs.

    Args:
    fasta - file path to FASTA file
    modifications - file path to modifications.gff or .gff.gz file
    min_score - Minimum Qmod score to use in motif finding (Default: 40.0)

    Returns:

    `Job` object which when executed saves the necessary CSV output to the
    file path provided in the input arguments.
"""
```

### Documentation

* Study code and (re)write function and module level docstrings conforming to
    [Google Python Style
    Guide](https://google.github.io/styleguide/pyguide.html) that follows pep
    proposals.

* Incorporate the description of the added tools in the pipeline workflow.

### Testing

> ### Request comment:
>
> How to verify the results of the coding? In other words, testing changes?

### Challenges

* **Unfamiliarity with working on clusters**

    The pipelines and their algorithms rely heavily on use of multi-node
    clusters for parallel processing and fast computing. I believe it would
    require a bit of exposure to learn about necessary cluster operations, how
    **jobs** are organized, submitted and executed.

* **Navigating through the code**

    The existing documentation for functions and module describe the structure
    in a very high-level manner, which might be a bit confusing to someone
    inexperienced. I plan to heavily document the code to be added from this
    proposal, write verbose commits, and maintain a detailed weekly log of my
    activities. Additionally, as the time permits I would like to pursue
    detailed documentation of the rest of the pipelines as well, write short
    tutorials (using information from my weekly log), and improve existing
    READMEs.

* **De-duplication and code quality**

    The code is quite redundant at places (e.g., pacbio_assembly.py), increasing
    overall complexity and reducing the readability. By careful use of
    Python decorators relevant sections of the code can be abstracted into
    higher-level objects.

    Additionally, following [pep8](https://www.python.org/dev/peps/pep-0008/)
    style guide and using Pythonic styles should allow us to write cleaner,
    quality and easily maintainable code. To automate these, we may use to use
    a continuous delivery platform. Unfortunately, the options for BitBucket are
    limited but [drone.io](https://drone.io) seems promising. On the plus side,
    [Code climate](https://codeclimate.com/) for code quality score and
    [coveralls](https://coveralls.io) both can be integrated with BitBucket.

## Timeline

### Community Bonding Period

Spend time revising and expanding the proposal adding necessary details (for
example, TODO and request for comments sections!). Communicate with the mentors
and other members of C3G, learn about the work and research culture, challenges
they face etc., For example, running the pipeline on smaller datasets, ensuring
that it works.

The main purpose of this period would be further refine the timeline, create
milestones, create a documentation plan and chalk out the implementation in more
details.

### Week 1 - Week 2

* Update project documentation, setup blog/journal for logging progress
* Improve documentation of `pacbio_assembly` pipeline and the files in `bfx/*`
    module.
* Setup code quality, style guide checker tools
* Bi-weekly summary

### Week 3 - Week 4

* Work on implementing `kineticsTools` module.
* Work on improving code quality and readability.
* Bi-weekly summary

### Week 5 - Week 6

* Work on overall project documentation.
* Test code by running on bigger datasets.
* Bi-weekly summary

**Mid term evaluations**

### Week 7 - Week 8

* Work on implementing `motifmaker` module.
* Bi-weekly summary

### Week 9 - Week 10

* Test code by running on bigger datasets.
* Bi-weekly summary

### Week 11 - Week 12

* Improve other modules as time permits.

**Week to scrub code, write tests, focus on documentation.**

**End term evaluations**

The timeline is sufficiently spaced with buffer periods to account for any
inevitable delays. Consistently discussing and documenting my progress through
the project will be crucial for successful and timely completion.

In a worst scenario where we hit a major roadblock (possibly due to upstream
issues in the tools we are dependent on), I request to continue the beyond
beyond the official timeline as well.

## Management of Coding Project

Since my proposed project plans to add verbose documentation and some code
refactoring as well, I am expecting to commit frequently. However, as the volume
of the commits increases one must be careful of the staged changes. Based on my
experience, following guidelines help mitigate general development issues:

* **Never push directly to the master.** Always create a pull request, have it
    reviewed at least once and only then commit the changes.

* **Verbose commit messages.** One line summary followed by a description of 
    changes introduced in the code (and why).

* **Monitor large code changes.** If a pull request makes a huge volume of code
    change, it usually indicates a wrong file is added or removed from the
    project.

* **Run tests (as available).** Always test your code before pushing.

* **Know your tools.** Git is awesome. Knowing basic tools like commands
    `reflog`, `stash`, `reset --soft`, `reset --hard`, `blame` can help address
    a lot of mishaps.


## Selection Test

A demo analysis step was implemented in the *pacbio_assembly* pipeline. The
changes are intended to perform the following steps:

✓ Read the path of a reference sequence from the config `.ini` file.

✓ `BLAT` the largest contig against the reference sequence from the previous step.

The changes are available in the [GitHub
repository](https://github.com/vivekiitkgp/mugqic-demo/pull/1/files) as a pull
request.

## References

[1]: [http://nar.oxfordjournals.org/content/early/2011/12/07/nar.gkr1146.full](http://nar.oxfordjournals.org/content/early/2011/12/07/nar.gkr1146.full)
[2]: [https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst#reference-sequence](https://github.com/PacificBiosciences/kineticsTools/blob/master/doc/manual.rst#reference-sequence)

