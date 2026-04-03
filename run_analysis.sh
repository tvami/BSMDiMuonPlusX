#!/bin/bash

# Script to run analyze_mother_daughters_toROOT.C on all ROOT files
# for PDG IDs 25, 35, and 36

# Directory containing ROOT files
DIR="/home/users/tvami/work/DarkShowerSimulation/CMSSW_14_0_18/src/nanoGEN_H2toH1toInvH3to2Mu"

# Output directory for histogram ROOT files
OUTDIR="${DIR}/histograms"
mkdir -p ${OUTDIR}

# PDG IDs to analyze
PDGIDS="25 35 36"

echo "Starting analysis..."
echo "Input directory: ${DIR}"
echo "Output directory: ${OUTDIR}"
echo "PDG IDs: ${PDGIDS}"
echo ""

# Loop over all ROOT files
for rootfile in ${DIR}/nanoGEN_*.root; do
    if [ ! -f "$rootfile" ]; then
        echo "No ROOT files found!"
        exit 1
    fi

    basename=$(basename ${rootfile} .root)
    echo "Processing: ${basename}"

    # Loop over PDG IDs
    for pdgid in ${PDGIDS}; do
        outfile="${OUTDIR}/hist_${basename}_pdg${pdgid}.root"
        echo "  - PDG ${pdgid} -> ${outfile}"

        # Run ROOT macro
        root -l -b -q "${DIR}/analyze_mother_daughters_toROOT.C(\"${rootfile}\", ${pdgid}, \"${outfile}\")"
    done
    echo ""
done

echo "Analysis complete!"
echo "Histogram files saved in: ${OUTDIR}"
