# Mother-Daughter Analysis and Overlay Plotting

This directory contains scripts to analyze daughter particles from specific mother PDG IDs and create overlay plots.

## Overview

The analysis pipeline consists of:
1. **ROOT Analysis**: Runs `analyze_mother_daughters_toROOT.C` on all nanoGEN ROOT files for PDG IDs 25, 35, and 36
2. **Overlay Plotting**: Creates styled overlay plots comparing results across different MH3 values

## Files

### Analysis Scripts
- `analyze_mother_daughters_toROOT.C`: ROOT macro that analyzes daughters and saves histograms to ROOT files
- `run_analysis.sh`: Bash script to run the analysis on all files for all PDG IDs
- `plot_overlay.py`: Python script to create overlay plots from histogram ROOT files
- `run_full_analysis.sh`: Master script to run the complete pipeline

### Original Files
- `analyze_mother_daughters.C`: Original analysis script (creates PNG/PDF directly)

## Usage

### Quick Start - Run Everything
```bash
./run_full_analysis.sh
```

This will:
1. Create `histograms/` directory with ROOT files containing histograms
2. Create `plots/` directory with PNG and PDF overlay plots

### Step-by-Step Execution

#### Step 1: Run ROOT Analysis
```bash
./run_analysis.sh
```

This processes all `nanoGEN_*.root` files and creates histogram ROOT files in `histograms/`:
- `hist_<filename>_pdg25.root` - Histograms for PDG ID 25
- `hist_<filename>_pdg35.root` - Histograms for PDG ID 35
- `hist_<filename>_pdg36.root` - Histograms for PDG ID 36

Each ROOT file contains:
- `h_daughter_pdgId`: PDG IDs of daughter particles
- `h_daughter_pt`: Transverse momentum (pT) distribution
- `h_daughter_eta`: Pseudorapidity (η) distribution
- `h_invariant_mass`: Invariant mass of daughter pairs
- `h_vertex_r`: Vertex radial distance

#### Step 2: Create Overlay Plots
```bash
python3 plot_overlay.py
```

This creates overlay plots in `plots/`:
- One set of plots for each PDG ID (25, 35, 36)
- Each histogram type gets its own overlay plot
- Output in both PNG and PDF formats
- CMS-style formatting with proper labels and legends

## Output Structure

```
nanoGEN_H2toH1toInvH3to2Mu/
├── histograms/              # Histogram ROOT files (intermediate)
│   ├── hist_*_pdg25.root
│   ├── hist_*_pdg35.root
│   └── hist_*_pdg36.root
└── plots/                   # Final overlay plots
    ├── h_daughter_pdgId_pdg25_overlay.png
    ├── h_daughter_pdgId_pdg25_overlay.pdf
    ├── h_daughter_pt_pdg25_overlay.png
    ├── h_daughter_pt_pdg25_overlay.pdf
    └── ... (similar for pdg35 and pdg36)
```

## Customization

### Modify PDG IDs
Edit `run_analysis.sh` and change the `PDGIDS` variable:
```bash
PDGIDS="25 35 36"  # Add or remove PDG IDs as needed
```

Also update `plot_overlay.py`:
```python
pdg_ids = [25, 35, 36]  # Match the PDG IDs
```

### Modify Plot Style
Edit `plot_overlay.py`:
- `setCMSStyle()`: Adjust CMS style settings
- `addCMSText()`: Customize CMS label text
- Color palette in `colors` list
- Legend position and size

### Change Histogram Binning
Edit `analyze_mother_daughters_toROOT.C` and modify histogram definitions, e.g.:
```cpp
TH1F* h_daughter_pt = new TH1F("h_daughter_pt", "...", 100, 0, 200);
//                                                       ^^^  ^  ^^^
//                                                       bins min max
```

## Requirements

- ROOT 6.x (for C++ macros and PyROOT)
- Python 3.x
- Bash shell

## Notes

- The analysis automatically sorts files by MH3 value for consistent plotting
- Log scale is applied to all overlay plots
- CMS style formatting matches the reference `plot_cutflow_overlay.py`
- Histograms are normalized for better comparison in overlays
