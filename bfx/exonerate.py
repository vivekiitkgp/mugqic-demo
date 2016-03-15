#!/usr/bin/env python

################################################################################
# Copyright (C) 2014, 2015 GenAP, McGill University and Genome Quebec Innovation Centre
#
# This file is part of MUGQIC Pipelines.
#
# MUGQIC Pipelines is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MUGQIC Pipelines is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MUGQIC Pipelines.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

# Python Standard Modules

# MUGQIC Modules
from core.config import *
from core.job import *

def fastareformat(input, output):
    return Job(
        input_files=[input],
        output_files=[output],
        command="fastareformat " + input + " > " + output,
        module_entries=[['DEFAULT' , 'module_exonerate']]
    )

def fastasplit(fasta, output_directory, output_basename, num_fasta_chunks):
    return Job(
        [fasta],
        # fastasplit creates FASTA chunk files numbered with 7 digits and padded with leading 0s
        [ os.path.join(output_directory, output_basename + "_{:07d}".format(i)) for i in range(num_fasta_chunks) ],
        [['exonerate_fastasplit', 'module_exonerate']],
        command="fastasplit -f " + fasta + " -o " + output_directory + " -c " + str(num_fasta_chunks)
    )


def fastalength(fasta, output_f):
    """ Return a file containing length|sequence-id pair of sequences in FASTA.

    Args:

    fasta: Path to FASTA file
    output_f: Path to output file containing length|seq-id pair
    """

    return Job(
        [fasta],
        [output_f],
        [['exonerate_fastalength', 'module_exonerate']],
        command="fastalength -f {} > {}".format(fasta, output_f)
    )


def fastaindex(fasta, output_f):
    """ Create an Index file given a FASTA file.

    Args:

    fasta: Path to FASTA file.
    output_f: Path to generated Index file.
    """

    return Job(
        [fasta],
        [output_f],
        [['exonerate_fastaindex', 'module_exonerate']],
        command="fastaindex -f {} -i {}".format(fasta, output_f)
    )


def fastafetch(query, fasta, index_f, output_f):
    """ Fetch the query from given FASTA file. Requires index.

    Args:

    query: Query string, a FASTA sequence id
    fasta: Path to FASTA file
    index_f: Path to Index file
    output_f: Path to Output file
    """

    return Job(
        [fasta, index_f],
        [output_f],
        [['exonerate_fastafetch', 'module_exonerate']],
        command=("fastafetch -f {} -q {} -i {} > {}").format(fasta,
                                                             query,
                                                             index_f,
                                                             output_f)
    )
