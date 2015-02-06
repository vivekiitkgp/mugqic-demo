#!/usr/bin/env python

import argparse
import csv
import glob
import httplib
import logging
import os
import re

log = logging.getLogger(__name__)

def get_nanuq_file(nanuq_auth_file, nanuq_url, nanuq_file):

    if os.path.exists(nanuq_file):
        log.warning("File " + nanuq_file + " already exists! Skipping...")
    else:
        https_connection = httplib.HTTPSConnection("genomequebec.mcgill.ca")
        https_connection.set_debuglevel(1)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        log.info("Fetching Nanuq file from server...")

        with open(nanuq_auth_file) as auth_file:
            https_connection.request("POST", nanuq_url, auth_file, headers)

        http_response = https_connection.getresponse()

        log.info("HTTP Response Status: " + str(http_response.status))
        log.info("HTTP Response Reason: " + http_response.reason)

        with open(nanuq_file, 'w') as file:
            file.write(http_response.read())

        https_connection.close()


def get_nanuq_readset_file(nanuq_auth_file, nanuq_project_id, nanuq_readset_file, seq_type):
    get_nanuq_file(nanuq_auth_file, "/nanuqMPS/csv/technology/" + seq_type + "/project/" + nanuq_project_id + "/filename/" + nanuq_readset_file, nanuq_readset_file)


def get_nanuq_bed_file(nanuq_auth_file, bed_file):
    get_nanuq_file(nanuq_auth_file, "/nanuqLimsCgi/targetRegion/downloadBed.cgi?bedName=" + bed_file, bed_file)


def create_readsets(nanuq_readset_file, seq_type, mugqic_pipelines_readset_file="readsets.tsv", args_nanuq_auth_file=None):
    # Lowercase the first seq_type character
    lcfirst_seq_type = seq_type[0].lower() + seq_type[1:]

    nanuq_readset_root_directory = "/lb/robot/" + lcfirst_seq_type + "Sequencer/" + lcfirst_seq_type + "Runs"
    raw_reads_directory = "raw_reads"
    symlinks = []
    mugqic_pipelines_readset_csv_rows = []
    bed_files = set()  # Only used for HiSeq/MiSeq sequencing type

    # Parse Nanuq readset file and list symlinks to be created
    log.info("Parse Nanuq readset file " + nanuq_readset_file + " ...")
    nanuq_readset_csv = csv.DictReader(open(nanuq_readset_file, 'rb'), delimiter=',', quotechar='"')

    for line in nanuq_readset_csv:
        if line['Status'] and line['Status'] == "Data is valid":
            mugqic_pipelines_readset_csv_row = {}

            if seq_type == "Pacbio":
                nanuq_vs_mugqic_pipelines_readset_keys = [
                    ['Name', 'Sample'],
                    ['Filename Prefix', 'Readset'],
                    ['Run', 'Run'],
                    ['Well', 'Smartcell'],
                    ['Collection Protocol', 'Protocol']
                ]
                formats = ['BAS', 'BAX']

                fieldnames = [key[1] for key in nanuq_vs_mugqic_pipelines_readset_keys] + ['NbBasePairs', 'EstimatedGenomeSize'] + formats

                nb_basepairs = re.search("^\([^/]*/[^/]*/(.*)\)$", line['Longest Subreads (count mean bp)'])
                mugqic_pipelines_readset_csv_row['NbBasePairs'] = re.sub(",", "", nb_basepairs.group(1))

                if line.get('Results Directory', None):
                    nanuq_readset_prefix = os.path.normpath(os.path.join(nanuq_readset_root_directory, line['Results Directory'], line['Movie name']))
                    for format in formats:
                        nanuq_readset_paths = sorted(glob.glob(nanuq_readset_prefix + "*." + format.lower() + ".h5"))
                        mugqic_pipelines_readset_paths = [os.path.join(raw_reads_directory, line['Name'], os.path.basename(nanuq_readset_path)) for nanuq_readset_path in nanuq_readset_paths]
                        mugqic_pipelines_readset_csv_row[format] = ",".join(mugqic_pipelines_readset_paths)
                        for nanuq_readset_path, mugqic_pipelines_readset_path in zip(nanuq_readset_paths, mugqic_pipelines_readset_paths):
                            symlinks.append([nanuq_readset_path, mugqic_pipelines_readset_path])

            else:  # seq_type = HiSeq or MiSeq
                nanuq_vs_mugqic_pipelines_readset_keys = [
                    ['Name', 'Sample'],
                    ['Filename Prefix', 'Readset'],
                    ['Library Barcode', 'Library'],
                    ['Run Type', 'RunType'],
                    ['Run', 'Run'],
                    ['Region', 'Lane'],
                    ['Adaptor Read 1 (NOTE: Usage is bound by Illumina Disclaimer found on Nanuq Project Page)', 'Adapter1'],
                    ['Adaptor Read 2 (NOTE: Usage is bound by Illumina Disclaimer found on Nanuq Project Page)', 'Adapter2'],
                    ['Quality Offset', 'QualityOffset'],
                    ['BED Files', 'BED']
                ]
                formats = ['FASTQ1', 'FASTQ2', 'BAM']

                fieldnames = [key[1] for key in nanuq_vs_mugqic_pipelines_readset_keys] + formats

                for format in formats:
                    if line.get(format, None):
                        nanuq_readset_path = os.path.normpath(os.path.join(nanuq_readset_root_directory, line[format]))
                        if os.path.isfile(nanuq_readset_path):
                            mugqic_pipelines_readset_path = os.path.join(raw_reads_directory, line['Name'], os.path.basename(nanuq_readset_path))
                            symlinks.append([nanuq_readset_path, mugqic_pipelines_readset_path])
                            mugqic_pipelines_readset_csv_row[format] = mugqic_pipelines_readset_path

                            # Add BAM index to symlinks if it exists, log a warning otherwise
                            if format == 'BAM':
                                nanuq_readset_index_path = re.sub("\.bam$", ".bai", nanuq_readset_path)
                                if os.path.isfile(nanuq_readset_index_path):
                                    symlinks.append([nanuq_readset_index_path, re.sub("\.bam$", ".bai", mugqic_pipelines_readset_path)])
                                else:
                                    log.warning("Nanuq readset index path " + nanuq_readset_index_path + " is invalid!")
                        else:
                            raise Exception("Error: Nanuq readset path " + nanuq_readset_path + " is invalid!")

                # BED files
                # Filter empty strings returned by split with string ";" separator
                for bed_file in filter(None, line['BED Files'].split(';')):
                    # Retrieve BED file if not previously done
                    if bed_file not in bed_files:
                        if args_nanuq_auth_file:
                            get_nanuq_bed_file(args_nanuq_auth_file.name, bed_file)
                        else:
                            log.warning("Nanuq authentication file missing: skipping retrieval of " + bed_file + "...")
                        bed_files.add(bed_file)

            for nanuq_key, mugqic_pipelines_key in nanuq_vs_mugqic_pipelines_readset_keys:
                value = line.get(nanuq_key, None)
                if value:
                    mugqic_pipelines_readset_csv_row[mugqic_pipelines_key] = value

            mugqic_pipelines_readset_csv_rows.append(mugqic_pipelines_readset_csv_row)
        else:
            log.warning(str(line) + " line data is not valid... skipping")

    # Create symbolic links and parent directories if necessary
    for target, link_name in symlinks:
        if os.path.islink(link_name):
            log.warning("Symlink " + link_name + " already exists! Skipping...")
        else:
            link_directory = os.path.dirname(link_name)
            if not os.path.isdir(link_directory):
                os.makedirs(link_directory)
            log.info("Creating symlink " + link_name + " ...")
            os.symlink(target, link_name)
            log.info("Symlink " + link_name + " created successfully.")

    # Write mugqic_pipelines readset file if necessary
    if os.path.exists(mugqic_pipelines_readset_file):
        log.warning("File " + mugqic_pipelines_readset_file + " already exists! Skipping...")
    else:
        mugqic_pipelines_readset_csv = csv.DictWriter(open(mugqic_pipelines_readset_file, 'wb'), fieldnames=fieldnames, delimiter='\t')
        mugqic_pipelines_readset_csv.writeheader()
        mugqic_pipelines_readset_csv.writerows(mugqic_pipelines_readset_csv_rows)

#-------------------------------------------------------------------------------
# Main script

# Parse options
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--nanuq-project-id", help="Nanuq project ID used to fetch readset file from server (incompatible with --nanuq-readset-file)")
group.add_argument("-r", "--nanuq-readset-file", help="Nanuq readset file to use instead of fetching it from server (incompatible with --nanuq-project-id)", type=file)

parser.add_argument("-s", "--seq-type", help="Sequencing type (default: HiSeq)", choices=["HiSeq", "MiSeq", "Pacbio"], default="HiSeq")
parser.add_argument("-a", "--nanuq-auth-file", help="Nanuq authentication file containing your Nanuq username and password e.g. $HOME/.nanuqAuth.txt\nTo create it:\n$ echo -n \"user=<USERNAME>&password=<PASSWORD>\" > $HOME/.nanuqAuth.txt ; chmod u+r,go-rwx $HOME/.nanuqAuth.txt\nNote '-n' option since trailing newline is not allowed at the end of the file.", type=file)
parser.add_argument("-nl", "--no-links", help="Do not create raw_reads directory and symlinks (default: false)", action="store_true")
parser.add_argument("-l", "--log", help="log level (default: info)", choices=["debug", "info", "warning", "error", "critical"], default="info")

args = parser.parse_args()

logging.basicConfig(level=getattr(logging, args.log.upper()))

if args.nanuq_project_id:
    if not args.nanuq_auth_file:
        raise Exception("Error: missing Nanuq authentication file (use -a or --nanuq-auth-file)!")

    nanuq_readset_file = "project.nanuq." + args.nanuq_project_id + ".csv"
    mugqic_pipelines_readset_file = "readsets." + args.nanuq_project_id + ".tsv"

    get_nanuq_readset_file(args.nanuq_auth_file.name, args.nanuq_project_id, nanuq_readset_file, args.seq_type)

elif args.nanuq_readset_file:
    nanuq_readset_file = args.nanuq_readset_file.name
    mugqic_pipelines_readset_file = "readsets.tsv"

if not args.no_links:
    create_readsets(nanuq_readset_file, args.seq_type, mugqic_pipelines_readset_file, args.nanuq_auth_file)
