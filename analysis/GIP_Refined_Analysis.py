import uproot
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

# Parameter
luminosity = 3000.0  # fb^-1
sigma_signal = 1.0   # fb (Annahme)
# Realistischerer Wirkungsquerschnitt aus MadGraph (ca. 158 pb = 158.000 fb)
sigma_signal_real = 158113.0 
sigma_bg = 2342.0 * 1000.0  # fb

signal_file = "GIP_13TeV_Delphes.root"
bg_file = "SM_Background_Delphes.root"

def analyze_asymmetry(filename, met_min=10.0, met_max=30.0, eta_cut=2.0):
    with uproot.open(filename) as f:
        tree = f["Delphes"]
        met = ak.to_numpy(ak.fill_none(ak.pad_none(tree["MissingET.MET"].array(), 1, axis=1), 0)[:, 0])
        jet_eta = tree["Jet.Eta"].array()
        
        # Filter: MET Fenster und Jet vorhanden
        met_mask = (met > met_min) & (met < met_max)
        has_jets = ak.num(jet_eta) > 0
        combined_mask = met_mask & has_jets
        
        filtered_jet_eta = jet_eta[combined_mask]
        if len(filtered_jet_eta) == 0:
            return 0, 0, len(met)
            
        leading_jet_eta = ak.to_numpy(filtered_jet_eta[:, 0])
        
        # Asymmetrie-Komponenten im Vorwärtsbereich
        fwd = np.sum(leading_jet_eta > eta_cut)
        bwd = np.sum(leading_jet_eta < -eta_cut)
        
        return fwd, bwd, len(met)

# Teste verschiedene MET-Fenster
windows = [(0, 15), (10, 30), (30, 50), (10, 50)]

print(f"{'Fenster [GeV]':<15} | {'S (1fb)':<10} | {'S (158pb)':<12} | {'B':<12} | {'Sig (Asym)':<10}")
print("-" * 75)

for w_min, w_max in windows:
    sf, sb, stot = analyze_asymmetry(signal_file, w_min, w_max)
    bf, bb, btot = analyze_asymmetry(bg_file, w_min, w_max)
    
    # Signal-Überschuss in der Asymmetrie (N_bwd - N_fwd)
    # Wir nehmen an, das GIP-Signal ist asymmetrisch
    s_asym_eff = abs(sb - sf) / stot
    b_total_eff = (bf + bb) / btot
    
    # Erwartete Events
    S_asym_1fb = luminosity * sigma_signal * s_asym_eff
    S_asym_real = luminosity * sigma_signal_real * s_asym_eff
    B_total = luminosity * sigma_bg * b_total_eff
    
    # Signifikanz der Asymmetrie
    # Da B statistisch symmetrisch ist, ist die Unsicherheit auf die Differenz sqrt(B_total)
    sig_1fb = S_asym_1fb / np.sqrt(B_total) if B_total > 0 else 0
    sig_real = S_asym_real / np.sqrt(B_total) if B_total > 0 else 0
    
    print(f"{w_min:2d} - {w_max:2d} GeV    | {sig_1fb:10.4f} | {sig_real:12.2f} | {B_total:12.0f} | {sig_real:10.2f}")

