import uproot
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

# Parameter
luminosity = 3000.0  # fb^-1 (HL-LHC)
sigma_signal = 1.0   # fb (Annahme)
sigma_bg = 2342.0 * 1000.0  # fb

signal_file = "GIP_13TeV_Delphes.root"
bg_file = "SM_Background_Delphes.root"

def analyze(filename, label, met_cut=200.0, eta_cut=2.0):
    print(f"[+] Verarbeite {filename}...")
    with uproot.open(filename) as f:
        tree = f["Delphes"]
        met = ak.to_numpy(ak.fill_none(ak.pad_none(tree["MissingET.MET"].array(), 1, axis=1), 0)[:, 0])
        jet_eta = tree["Jet.Eta"].array()
        jet_pt = tree["Jet.PT"].array()
        
        has_jets = ak.num(jet_pt) > 0
        met_gate = met > met_cut
        combined_mask = met_gate & has_jets
        
        filtered_jet_eta = jet_eta[combined_mask]
        if len(filtered_jet_eta) == 0:
            return 0, len(met), []
            
        leading_jet_eta = ak.to_numpy(filtered_jet_eta[:, 0])
        eta_mask = np.abs(leading_jet_eta) > eta_cut
        final_eta = leading_jet_eta[eta_mask]
        
        return len(final_eta), len(met), met[combined_mask][eta_mask]

# Scan MET cuts
for mcut in [50, 100, 200, 300, 500]:
    n_s, tot_s, met_s = analyze(signal_file, "Signal", met_cut=mcut)
    n_b, tot_b, met_b = analyze(bg_file, "BG", met_cut=mcut)
    
    s_exp = luminosity * sigma_signal * (n_s / tot_s)
    b_exp = luminosity * sigma_bg * (n_b / tot_b)
    sig = s_exp / np.sqrt(b_exp) if b_exp > 0 else 0
    
    print(f"MET > {mcut} GeV: S={s_exp:.2f}, B={b_exp:.2f}, Sig={sig:.4f}")
