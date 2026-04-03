#!/usr/bin/env python3
import ROOT
import os
import glob
import re

# CMS Style settings
def setCMSStyle():
    """Set CMS style for plots"""
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    # Canvas settings
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
    ROOT.gStyle.SetCanvasDefH(600)
    ROOT.gStyle.SetCanvasDefW(600)
    ROOT.gStyle.SetCanvasDefX(0)
    ROOT.gStyle.SetCanvasDefY(0)

    # Pad settings
    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetPadColor(ROOT.kWhite)
    ROOT.gStyle.SetPadGridX(False)
    ROOT.gStyle.SetPadGridY(False)
    ROOT.gStyle.SetGridColor(0)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridWidth(1)

    # Frame settings
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetFrameBorderSize(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameFillStyle(0)
    ROOT.gStyle.SetFrameLineColor(1)
    ROOT.gStyle.SetFrameLineStyle(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    # Margins
    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.05)

    # Axis settings
    ROOT.gStyle.SetTitleSize(0.05, "XYZ")
    ROOT.gStyle.SetTitleXOffset(0.9)
    ROOT.gStyle.SetTitleYOffset(1.4)
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")
    ROOT.gStyle.SetLabelOffset(0.007, "XYZ")

    # Legend settings
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendFillColor(0)
    ROOT.gStyle.SetLegendFont(42)
    ROOT.gStyle.SetLegendTextSize(0.03)

    ROOT.gStyle.SetPalette(ROOT.kBird)
    ROOT.gStyle.SetNumberContours(99)

    ROOT.gROOT.ForceStyle()

def addCMSText(canvas, lumi_text="13.6 TeV", extra_text="Simulation"):
    """Add CMS label and luminosity text"""
    canvas.cd()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)

    # CMS text
    latex.SetTextSize(0.05)
    latex.SetTextFont(61)
    latex.DrawLatex(0.15, 0.93, "CMS")

    # Extra text (e.g., Simulation)
    if extra_text:
        latex.SetTextSize(0.04)
        latex.SetTextFont(52)
        latex.DrawLatex(0.25, 0.93, extra_text)

    # Luminosity/energy text
    if lumi_text:
        latex.SetTextSize(0.04)
        latex.SetTextFont(42)
        latex.DrawLatex(0.70, 0.93, lumi_text)

    return latex

def extract_mh2(filename):
    """Extract MH2 value from filename"""
    match = re.search(r'MH2-(\d+)', filename)
    if match:
        return int(match.group(1))
    return None

def extract_mh3(filename):
    """Extract MH3 value from filename for sorting"""
    match = re.search(r'MH3-(\d+)', filename)
    if match:
        return int(match.group(1))
    return 0

def extract_process_name(filename):
    """Extract process name from filename (e.g., H2toH1toInvH3to2Mu_Par-MH2-250-MH3-10)"""
    # Match process name after nanoGEN_ up to and including MH3-XX, stopping before _Tune or _pdg
    match = re.search(r'nanoGEN_(.*?-MH3-\d+)', filename)
    if match:
        return match.group(1)
    # Fallback: match just the process part before _Par or _Tune or _pdg
    match = re.search(r'nanoGEN_([^_]+(?:to[^_]+)*)', filename)
    if match:
        return match.group(1)
    return None

def find_best_legend_position(histograms):
    """
    Find the best corner for the legend by checking which has the least data
    Returns (x1, y1, x2, y2) for TLegend constructor
    """
    # Define corners: (x1, y1, x2, y2) in NDC coordinates
    corners = {
        'top_right': (0.68, 0.50, 0.94, 0.90),
        'top_left': (0.20, 0.50, 0.46, 0.90),
        'bottom_right': (0.68, 0.15, 0.94, 0.55),
        'bottom_left': (0.20, 0.15, 0.46, 0.55),
    }

    # For each corner, sum up histogram content in that region
    corner_scores = {}

    for corner_name, (x1, y1, x2, y2) in corners.items():
        score = 0
        for hist, _ in histograms:
            # Check bins in this corner region
            # Top/bottom based on y, left/right based on x-axis bins
            n_bins = hist.GetNbinsX()

            # Determine which bins to check based on corner
            if 'left' in corner_name:
                start_bin = 1
                end_bin = max(1, int(n_bins * 0.3))
            else:  # right
                start_bin = int(n_bins * 0.7)
                end_bin = n_bins

            # Sum content in this region
            for bin_i in range(start_bin, end_bin + 1):
                score += hist.GetBinContent(bin_i)

        corner_scores[corner_name] = score

    # Find corner with minimum score (least data)
    best_corner = min(corner_scores, key=corner_scores.get)

    return corners[best_corner]

def plot_overlay_for_pdg(input_dir, pdg_id, output_dir, mh2_value=None):
    """
    Create overlay plots for a specific PDG ID and MH2 value

    Args:
        input_dir: Directory containing histogram ROOT files
        pdg_id: PDG ID to plot (25, 35, or 36)
        output_dir: Directory to save output plots
        mh2_value: MH2 value to filter (250 or 500). If None, plot all.
    """

    mh2_label = f"MH2-{mh2_value}" if mh2_value else "All_MH2"
    print(f"\n{'='*80}")
    print(f"Creating overlay plots for PDG {pdg_id}, {mh2_label}")
    print(f"{'='*80}\n")

    # Enable batch mode
    ROOT.gROOT.SetBatch(True)

    # Set CMS style
    setCMSStyle()

    # Get list of histogram ROOT files for this PDG ID
    pattern = os.path.join(input_dir, f"hist_*_pdg{pdg_id}.root")
    root_files = glob.glob(pattern)

    if not root_files:
        print(f"No ROOT files found for PDG {pdg_id} in {input_dir}")
        return

    # Filter by MH2 value if specified
    if mh2_value is not None:
        root_files = [f for f in root_files if extract_mh2(f) == mh2_value]
        if not root_files:
            print(f"No ROOT files found for PDG {pdg_id} with MH2={mh2_value}")
            return

    # Filter to only include samples with MH3 <= 60 GeV
    root_files = [f for f in root_files if extract_mh3(f) <= 60]
    if not root_files:
        print(f"No ROOT files found for PDG {pdg_id} with MH3 <= 60 GeV")
        return

    # Sort files by MH3 value
    root_files = sorted(root_files, key=extract_mh3)

    print(f"Found {len(root_files)} ROOT files for PDG {pdg_id}")

    # Extract process name from first file (use basename only)
    process_name = extract_process_name(os.path.basename(root_files[0])) if root_files else None
    if not process_name:
        print(f"Warning: Could not extract process name from files, using default")
        process_name = "nanoGEN"

    # Color palette
    colors = [
        ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta,
        ROOT.kCyan+1, ROOT.kOrange, ROOT.kViolet, ROOT.kTeal-1, ROOT.kPink+1,
        ROOT.kAzure+7, ROOT.kSpring-7, ROOT.kYellow+2, ROOT.kRed+2, ROOT.kBlue+2,
        ROOT.kGreen+3, ROOT.kMagenta+2, ROOT.kCyan+3, ROOT.kOrange+7, ROOT.kViolet+2,
        ROOT.kTeal+2, ROOT.kPink-2, ROOT.kAzure-3, ROOT.kSpring+3, ROOT.kYellow-2
    ]

    # Histogram names to overlay
    hist_names = [
        "h_daughter_pdgId",
        "h_daughter_pt",
        "h_daughter_eta",
        "h_invariant_mass",
        "h_vertex_r"
    ]

    # Loop over each histogram type
    for hist_name in hist_names:
        print(f"  Processing {hist_name}...")

        # Collect histograms from all files
        histograms = []
        labels = []

        for i, root_file in enumerate(root_files):
            try:
                tfile = ROOT.TFile.Open(root_file)
            except (OSError, RuntimeError) as e:
                print(f"    Warning: Could not open {root_file}: {e}")
                continue

            if not tfile or tfile.IsZombie():
                print(f"    Warning: Zombie file {root_file}")
                continue

            hist = tfile.Get(hist_name)
            if not hist:
                print(f"    Warning: {hist_name} not found in {root_file}")
                tfile.Close()
                continue

            # Clone histogram to keep it after file closes
            hist_clone = hist.Clone(f"{hist_name}_{i}")
            hist_clone.SetDirectory(0)

            # Update Y-axis title
            if hist_name == "h_invariant_mass":
                hist_clone.GetYaxis().SetTitle("Events")
            else:
                hist_clone.GetYaxis().SetTitle("Daughter GenParticles")

            # Rebin non-mass and non-pdgId histograms by factor of 2
            if "mass" not in hist_name.lower() and "pdgid" not in hist_name.lower():
                hist_clone.Rebin(2)

            # Set style
            color = colors[i % len(colors)]
            hist_clone.SetLineColor(color)
            hist_clone.SetLineWidth(2)
            hist_clone.SetMarkerColor(color)
            hist_clone.SetMarkerStyle(20)
            hist_clone.SetMarkerSize(0.8)

            # Extract label from filename
            filename = os.path.basename(root_file)
            # Extract MH3 value
            mh3_match = re.search(r'MH3-(\d+)', filename)
            if mh3_match:
                label = f"M_{{H3}} = {mh3_match.group(1)} GeV"
            else:
                label = filename.replace("hist_", "").replace(f"_pdg{pdg_id}.root", "")

            histograms.append((hist_clone, tfile))
            labels.append(label)

        if not histograms:
            print(f"    Warning: No valid histograms found for {hist_name}")
            continue

        # Create canvas with unique name including MH2 value
        canvas_name = f"c_{hist_name}_pdg{pdg_id}_MH2{mh2_value}" if mh2_value else f"c_{hist_name}_pdg{pdg_id}"
        canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 800)
        canvas.cd()
        canvas.SetLogy()

        # Find best position for legend
        x1, y1, x2, y2 = find_best_legend_position(histograms)

        # Create legend at best position
        legend = ROOT.TLegend(x1, y1, x2, y2)
        if mh2_value:
            legend.SetHeader(f"PDG {pdg_id}, M_{{H2}}={mh2_value} GeV")
        else:
            legend.SetHeader(f"PDG {pdg_id}")
        legend.SetTextSize(0.025)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)

        # Find maximum for y-axis scaling
        max_val = 0
        for hist_clone, _ in histograms:
            hist_max = hist_clone.GetMaximum()
            if hist_max > max_val:
                max_val = hist_max

        # Draw histograms
        for i, (hist_clone, tfile) in enumerate(histograms):
            if i == 0:
                # Set y-axis range on first histogram
                hist_clone.SetMaximum(max_val * 10)
                hist_clone.SetMinimum(0.5)

                draw_option = "HIST"
            else:
                draw_option = "HIST SAME"

            hist_clone.Draw(draw_option)
            legend.AddEntry(hist_clone, labels[i], "l")

        # Draw legend
        legend.Draw()

        # Add CMS text
        addCMSText(canvas, lumi_text="13.6 TeV", extra_text="Simulation")

        # Save canvas
        os.makedirs(output_dir, exist_ok=True)
        png_name = os.path.join(output_dir, f"{hist_name}_{process_name}_pdg{pdg_id}_overlay.png")
        pdf_name = os.path.join(output_dir, f"{hist_name}_{process_name}_pdg{pdg_id}_overlay.pdf")

        canvas.SaveAs(png_name)
        canvas.SaveAs(pdf_name)

        print(f"    Saved: {png_name}")

        canvas.Update()

        # Cleanup
        for hist_clone, tfile in histograms:
            tfile.Close()

if __name__ == "__main__":
    # Input directory containing histogram ROOT files
    input_dir = "/home/users/tvami/work/DarkShowerSimulation/CMSSW_14_0_18/src/nanoGEN_H2toH1toInvH3to2Mu/histograms"

    # Output directory for plots
    output_dir = "/home/users/tvami/work/DarkShowerSimulation/CMSSW_14_0_18/src/nanoGEN_H2toH1toInvH3to2Mu/figures"

    # PDG IDs to process
    pdg_ids = [25, 35, 36]

    # MH2 values to process separately
    mh2_values = [250, 500]

    # Create separate plots for each MH2 category
    for pdg_id in pdg_ids:
        for mh2_value in mh2_values:
            plot_overlay_for_pdg(input_dir, pdg_id, output_dir, mh2_value=mh2_value)

    print(f"\n{'='*80}")
    print("All overlay plots created successfully!")
    print(f"Figures saved in: {output_dir}")
    print(f"  - Separate plots for MH2=250 GeV and MH2=500 GeV")
    print(f"{'='*80}\n")
