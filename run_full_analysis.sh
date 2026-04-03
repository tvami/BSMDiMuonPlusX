#!/bin/bash

# Master script to run full analysis pipeline:
# 1. Run ROOT analysis on all files for PDG IDs 25, 35, 36
# 2. Create overlay plots from histogram ROOT files

set -e  # Exit on error

BASEDIR="/home/users/tvami/work/DarkShowerSimulation/CMSSW_14_0_18/src/nanoGEN_H2toH1toInvH3to2Mu"

echo "=========================================="
echo "Starting Full Analysis Pipeline"
echo "=========================================="
echo ""

# Step 1: Run ROOT analysis
echo "Step 1: Running ROOT analysis on all files..."
echo "----------------------------------------------"
${BASEDIR}/run_analysis.sh

if [ $? -ne 0 ]; then
    echo "Error: Analysis step failed!"
    exit 1
fi

echo ""
echo "Step 1 completed successfully!"
echo ""

# Step 2: Create overlay plots
echo "Step 2: Creating overlay plots..."
echo "----------------------------------------------"
python3 ${BASEDIR}/plot_overlay.py

if [ $? -ne 0 ]; then
    echo "Error: Plotting step failed!"
    exit 1
fi

echo ""
echo "Step 2 completed successfully!"
echo ""

echo "=========================================="
echo "Full Analysis Pipeline Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  - Histogram ROOT files: ${BASEDIR}/histograms/"
echo "  - Overlay plots:        ${BASEDIR}/plots/"
echo ""
