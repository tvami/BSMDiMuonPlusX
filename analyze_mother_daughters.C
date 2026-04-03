
void analyze_mother_daughters(const char* filename, int mother_pdg_id) {
// Usage:
// root -l
// .L analyze_mother_daughters.C
// analyze_mother_daughters("NanoGen_v1.root", 36)

  
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
  
    // Print tree structure
    //  cout << "Tree structure:" << endl;
    //  tree->Print();
    //  return;
  
    // Create histograms with dynamic titles
  TString title_base = Form("daughters of PDG %d", mother_pdg_id);
  TH1F* h_daughter_pdgId = new TH1F("h_daughter_pdgId", Form("PDG ID of %s;PDG ID;Count", title_base.Data()), 40, -15, 25);
  TH1F* h_daughter_pt = new TH1F("h_daughter_pt", Form("p_{T} of %s;p_{T} [GeV];Count", title_base.Data()), 100, 0, 200);
  TH1F* h_daughter_eta = new TH1F("h_daughter_eta", Form("#eta of %s;#eta;Count", title_base.Data()), 100, -5, 5);
  TH1F* h_invariant_mass = new TH1F("h_invariant_mass", Form("Invariant Mass of PDG %d Daughter Pairs;Mass [GeV];Count", mother_pdg_id), 100, 0, 600);
  TH1F* h_vertex_r = new TH1F("h_vertex_r", Form("Vertex Radial Distance of %s;R [cm];Count", title_base.Data()), 100, 0, 0.1);
  
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
//   Long64_t n_scan = tree->Scan("GenPart_pdgId:GenPart_pt:GenPart_eta", Form("GenPart_pdgId==%d", mother_pdg_id), "", 10);
//   cout << "\nFound " << n_scan << " entries with PDG " << mother_pdg_id << endl;
  
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
        // cout << "Event " << iEvent << ": Found PDG " << mother_pdg_id << " at index " << i << endl;
        
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
//            *Br   36 :GenPart_statusFlags :                                              *
//            *         | UShort_t gen status flags stored bitwise, bits are: 0 :          *
//            *         |  isPrompt, 1 : isDecayedLeptonHadron, 2 : isTauDecayProduct, 3 : *
//            *         |  isPromptTauDecayProduct, 4 : isDirectTauDecayProduct, 5 :       *
//            *         |  isDirectPromptTauDecayProduct, 6 :                              *
//            *         |  isDirectHadronDecayProduct, 7 : isHardProcess, 8 :              *
//            *         |  fromHardProcess, 9 : isHardProcessTauDecayProduct, 10 :         *
//            *         |  isDirectHardProcessTauDecayProduct, 11 :                        *
//            *         |  fromHardProcessBeforeFSR, 12 : isFirstCopy, 13 :                *
//            *         |  isLastCopy, 14 : isLastCopyBeforeFSR,                           *
            total_daughters++;
            
            // cout << "  Daughter " << j << ": PDG=" << daughter_pdg
            // << ", pT=" << daughter_pt
            // << ", eta=" << daughter_eta
            // << ", phi=" << daughter_phi
            // << ", mass=" << daughter_mass
            // << ", status=" << daughter_status
            // << ", statusFlag=" << daughter_statusFlags
            // << ", vtx=(" << vtx_x << "," << vtx_y << "," << vtx_z << ")"
            // << ", r=" << vtx_r << endl;
            
              // Fill histograms
            h_daughter_pdgId->Fill(daughter_pdg);
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

            // cout << "  Pair (" << k << "," << l << "): PDG(" << daughter_pdgs[k]
            // << "," << daughter_pdgs[l] << ") -> Invariant Mass = "
            // << inv_mass << " GeV" << endl;
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

    // Create canvas
  TCanvas* c1 = new TCanvas("c1", Form("PDG %d Daughter Analysis", mother_pdg_id), 1600, 1000);
  c1->Divide(3, 2);
  
  c1->cd(1);
  gPad->SetLogy();
  h_daughter_pdgId->Draw();

  c1->cd(2);
  gPad->SetLogy();
  h_daughter_pt->Draw();

  c1->cd(3);
  gPad->SetLogy();
  h_daughter_eta->Draw();

  c1->cd(4);
  gPad->SetLogy();
  h_invariant_mass->Draw();
  h_invariant_mass->SetLineColor(kRed);
  h_invariant_mass->SetLineWidth(2);

  c1->cd(5);
  gPad->SetLogy();
  h_vertex_r->Draw();
  h_vertex_r->SetLineColor(kOrange);
  h_vertex_r->SetLineWidth(2);

    // Save canvas
  c1->SaveAs(Form("pdg%d_daughters_analysis.png", mother_pdg_id));
  c1->SaveAs(Form("pdg%d_daughters_analysis.pdf", mother_pdg_id));
  
    // Clean up
  file->Close();
  delete file;
  
  cout << "\nAnalysis complete!" << endl;
}
