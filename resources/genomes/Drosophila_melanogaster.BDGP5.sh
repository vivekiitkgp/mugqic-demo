#!/bin/bash
# Exit immediately on error
set -eu -o pipefail

SPECIES=Drosophila_melanogaster
COMMON_NAME="Fruit fly"
ASSEMBLY=BDGP5
ASSEMBLY_SYNONYMS=dm3
SOURCE=Ensembl
VERSION=77
BIOMART_HOST=oct2014.archive.ensembl.org

GENOME_INSTALL_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $GENOME_INSTALL_SCRIPT_DIR/install_genome.sh

install_genome "$SPECIES" "$COMMON_NAME" "$ASSEMBLY" "$ASSEMBLY_SYNONYMS" "$SOURCE" "$VERSION"

################################################################################
# Write below all commands to install additional data files specific to this genome assembly
