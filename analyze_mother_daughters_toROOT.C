
// Function to map PDG ID to categorical bin
int pdgToBin(int pdg) {
  int abs_pdg = abs(pdg);

  // Leptons
  if (abs_pdg == 11) return 1;  // electron/positron
  if (abs_pdg == 13) return 2;  // muon
  if (abs_pdg == 15) return 3;  // tau
  if (abs_pdg == 12 || abs_pdg == 14 || abs_pdg == 16) return 4;  // neutrinos

  // Quarks
  if (abs_pdg == 1) return 5;   // down
  if (abs_pdg == 2) return 6;   // up
  if (abs_pdg == 3) return 7;   // strange
  if (abs_pdg == 4) return 8;   // charm
  if (abs_pdg == 5) return 9;   // bottom
  if (abs_pdg == 6) return 10;  // top

  // Gauge bosons
  if (abs_pdg == 21) return 11; // gluon
  if (abs_pdg == 22) return 12; // photon
  if (abs_pdg == 23) return 13; // Z
  if (abs_pdg == 24) return 14; // W

  // Higgs bosons
  if (pdg == 25) return 15;  // H1 (SM-like Higgs)
  if (pdg == 35) return 16;  // H2
  if (pdg == 36) return 17;  // H3 (pseudoscalar)

  // Other
  return 18;
}

void analyze_mother_daughters_toROOT(const char* filename, int mother_pdg_id, const char* output_filename = "") {
// Usage:
// root -l
// .L analyze_mother_daughters_toROOT.C
// analyze_mother_daughters_toROOT("NanoGen_v1.root", 36, "output_pdg36.root")


  gROOT->SetBatch(kTRUE);
    // Open the ROOT file
  TFile* file = TFile::Open(filename);
  if (!file || file->IsZombie()) {
    cout << "Error: Cannot open file " << filename << endl;
    return;
  }

    // Get the tree
  TTree* tree = (TTree*)file->Get("Events");
  if (!tree) {
    cout << "Error: Cannot find tree in file" << endl;
    file->Close();
    return;
  }

    // Create output filename if not provided
  TString outfile;
  if (strlen(output_filename) == 0) {
    TString basename = gSystem->BaseName(filename);
    basename.ReplaceAll(".root", "");
    outfile = Form("hist_%s_pdg%d.root", basename.Data(), mother_pdg_id);
  } else {
    outfile = output_filename;
  }

    // Create histograms with dynamic titles
  TString title_base = Form("daughters of PDG %d", mother_pdg_id);
  TH1F* h_daughter_pdgId = new TH1F("h_daughter_pdgId", Form("Particle Type of %s;Particle Type;Daughter GenParticles", title_base.Data()), 18, 0.5, 18.5);

  // Set bin labels for categorical PDG ID histogram
  h_daughter_pdgId->GetXaxis()->SetBinLabel(1, "e^{#pm}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(2, "#mu^{#pm}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(3, "#tau^{#pm}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(4, "#nu");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(5, "d");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(6, "u");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(7, "s");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(8, "c");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(9, "b");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(10, "t");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(11, "g");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(12, "#gamma");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(13, "Z");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(14, "W^{#pm}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(15, "H_{1}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(16, "H_{2}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(17, "H_{3}");
  h_daughter_pdgId->GetXaxis()->SetBinLabel(18, "Other");
  TH1F* h_daughter_pt = new TH1F("h_daughter_pt", Form("p_{T} of %s;p_{T} [GeV];Daughter GenParticles", title_base.Data()), 100, 0, 200);
  TH1F* h_daughter_eta = new TH1F("h_daughter_eta", Form("#eta of %s;#eta;Daughter GenParticles", title_base.Data()), 100, -5, 5);

  // Set mass range based on mother PDG ID
  float mass_max = 600;  // default for H1 and H2
  if (mother_pdg_id == 36) {
    mass_max = 160;  // H3 daughters
  }
  TH1F* h_invariant_mass = new TH1F("h_invariant_mass", Form("Invariant Mass of PDG %d Daughter Pairs;Mass [GeV];Daughter GenParticle Pairs", mother_pdg_id), 100, 0, mass_max);

  TH1F* h_vertex_r = new TH1F("h_vertex_r", Form("Vertex Radial Distance of %s;R [cm];Daughter GenParticles", title_base.Data()), 100, 0, 0.1);

    // Counters
  int total_events = 0;
  int events_with_mother = 0;
  int total_daughters = 0;
  int total_pairs = 0;

    // Get number of entries
  Long64_t nEntries = tree->GetEntries();
  cout << "Processing " << nEntries << " events..." << endl;

    // Use TTreeReader approach (more robust)
  tree->SetScanField(0); // Unlimited output

    // First, let's just scan for the mother particle and see what we have
  cout << "\nScanning for PDG " << mother_pdg_id << " particles..." << endl;

    // Now let's manually loop through events
  for (Long64_t iEvent = 0; iEvent < nEntries; iEvent++) {
    tree->GetEntry(iEvent);
    total_events++;
    if (total_events % 10000 == 0) std::cout << "We are at event " << total_events << std::endl;


      // Get branch values using GetLeaf
    TLeaf* leaf_nGenPart = tree->GetLeaf("nGenPart");
    TLeaf* leaf_pdgId = tree->GetLeaf("GenPart_pdgId");
    TLeaf* leaf_mother = tree->GetLeaf("GenPart_genPartIdxMother");
    TLeaf* leaf_pt = tree->GetLeaf("GenPart_pt");
    TLeaf* leaf_eta = tree->GetLeaf("GenPart_eta");
    TLeaf* leaf_phi = tree->GetLeaf("GenPart_phi");
    TLeaf* leaf_mass = tree->GetLeaf("GenPart_mass");
    TLeaf* leaf_status = tree->GetLeaf("GenPart_status");
    TLeaf* leaf_statusFlags = tree->GetLeaf("GenPart_statusFlags");
    TLeaf* leaf_vtx_x = tree->GetLeaf("GenVtx_x");
    TLeaf* leaf_vtx_y = tree->GetLeaf("GenVtx_y");
    TLeaf* leaf_vtx_z = tree->GetLeaf("GenVtx_z");

    if (!leaf_nGenPart || !leaf_pdgId || !leaf_mother) {
      cout << "Error: Cannot find required leaves" << endl;
      continue;
    }

    int nGenPart = (int)leaf_nGenPart->GetValue();

    bool found_mother = false;

      // Find mother particles
    for (int i = 0; i < nGenPart; i++) {
      int pdgId = (int)leaf_pdgId->GetValue(i);
      if (pdgId == mother_pdg_id) {
        found_mother = true;

          // Store daughter information for invariant mass calculation
        vector<TLorentzVector> daughters;
        vector<int> daughter_pdgs;

          // Look for its daughters
        for (int j = 0; j < nGenPart; j++) {
          int mother_idx = (int)leaf_mother->GetValue(j);
          if (mother_idx == i) {
            int daughter_pdg = (int)leaf_pdgId->GetValue(j);
            float daughter_pt = leaf_pt ? leaf_pt->GetValue(j) : 0;
            float daughter_eta = leaf_eta ? leaf_eta->GetValue(j) : 0;
            float daughter_phi = leaf_phi ? leaf_phi->GetValue(j) : 0;
            float daughter_mass = leaf_mass ? leaf_mass->GetValue(j) : 0;
            int daughter_status = leaf_status ? (int)leaf_status->GetValue(j) : 0;
            UShort_t daughter_statusFlags = leaf_statusFlags ? (UShort_t)leaf_statusFlags->GetValue(j) : 0;
            float vtx_x = leaf_vtx_x ? leaf_vtx_x->GetValue(j) : 0;
            float vtx_y = leaf_vtx_y ? leaf_vtx_y->GetValue(j) : 0;
            float vtx_z = leaf_vtx_z ? leaf_vtx_z->GetValue(j) : 0;
            float vtx_r = TMath::Sqrt(vtx_x*vtx_x + vtx_y*vtx_y + vtx_z*vtx_z);

            if (!(daughter_statusFlags & (1 << 0))) continue;
            total_daughters++;

              // Fill histograms
            int bin_num = pdgToBin(daughter_pdg);
            if (total_daughters <= 10) {  // Print first 10 for debugging
              cout << "  Daughter PDG: " << daughter_pdg << " -> Bin: " << bin_num << endl;
            }
            h_daughter_pdgId->Fill(bin_num);
            if (leaf_pt) h_daughter_pt->Fill(daughter_pt);
            if (leaf_eta) h_daughter_eta->Fill(daughter_eta);
            if (leaf_vtx_x && leaf_vtx_y && leaf_vtx_z) h_vertex_r->Fill(vtx_r);

              // Create TLorentzVector for invariant mass calculation
            TLorentzVector p4;
            p4.SetPtEtaPhiM(daughter_pt, daughter_eta, daughter_phi, daughter_mass);
            daughters.push_back(p4);
            daughter_pdgs.push_back(daughter_pdg);
          }
        }

          // Calculate invariant mass for all daughter pairs
        for (size_t k = 0; k < daughters.size(); k++) {
          for (size_t l = k + 1; l < daughters.size(); l++) {
            TLorentzVector pair = daughters[k] + daughters[l];
            float inv_mass = pair.M();
            h_invariant_mass->Fill(inv_mass);
            total_pairs++;
          }
        }
      }
    }

    if (found_mother) events_with_mother++;
  }

    // Print summary
  cout << "\n=== ANALYSIS SUMMARY ===" << endl;
  cout << "Total events processed: " << total_events << endl;
  cout << "Events with PDG " << mother_pdg_id << ": " << events_with_mother << endl;
  cout << "Total daughters of PDG " << mother_pdg_id << " found: " << total_daughters << endl;
  cout << "Total daughter pairs analyzed: " << total_pairs << endl;

    // Save histograms to ROOT file
  TFile* fout = new TFile(outfile, "RECREATE");
  h_daughter_pdgId->Write();
  h_daughter_pt->Write();
  h_daughter_eta->Write();
  h_invariant_mass->Write();
  h_vertex_r->Write();
  fout->Close();

  cout << "\nHistograms saved to: " << outfile << endl;

    // Clean up
  file->Close();
  delete file;
  delete fout;

  cout << "\nAnalysis complete!" << endl;
}
