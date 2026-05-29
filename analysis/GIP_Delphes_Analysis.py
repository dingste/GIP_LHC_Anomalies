import uproot
import matplotlib.pyplot as plt
import numpy as np
import awkward as ak

root_file = "GIP_Run03_Delphes.root"

print(f"[+] Analysiere Delphes-Output: {root_file}")

with uproot.open(root_file) as f:
    tree = f["Delphes"]
    
    # MET auslesen
    met_array = tree["MissingET.MET"].array()
    met = ak.to_numpy(ak.fill_none(ak.pad_none(met_array, 1, axis=1), 0)[:, 0])
    
    # Jets auslesen
    jet_eta = tree["Jet.Eta"].array()
    jet_pt = tree["Jet.PT"].array()
    
    # Wir brauchen Events mit mindestens einem Jet
    has_jets = ak.num(jet_pt) > 0
    
    # MET Gate
    met_gate = met > 50.0
    
    combined_mask = met_gate & has_jets
    
    filtered_jet_eta = jet_eta[combined_mask]
    
    # Extrahiere eta des führenden Jets
    leading_jet_eta = ak.to_numpy(filtered_jet_eta[:, 0])
    
    # Filter für Vorwärtsjets (|eta| > 2.0) wie im Parton-Level Script
    eta_mask = np.abs(leading_jet_eta) > 2.0
    final_eta = leading_jet_eta[eta_mask]
    
    # Asymmetrie berechnen
    forward = np.sum(final_eta > 0)
    backward = np.sum(final_eta < 0)
    ratio = forward / backward if backward > 0 else 0
    
    print(f"\n--- Delphes (ATLAS) Validierung ---")
    print(f"Events unter MET-Gate (>50 GeV) und |eta| > 2.0: {len(final_eta)}")
    print(f"Forward Jets (eta > 0): {forward}")
    print(f"Backward Jets (eta < 0): {backward}")
    print(f"Forward/Backward-Ratio (nach Detektor): {ratio:.4f}")
    
    # Plot zum Vergleich
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(met, bins=50, range=(0, 300), color='blue', alpha=0.7)
    plt.axvline(x=50, color='red', linestyle='--', label='MET Gate (50 GeV)')
    plt.title('MET Distribution (Delphes)')
    plt.xlabel('MET [GeV]')
    plt.ylabel('Events')
    
    plt.subplot(1, 2, 2)
    plt.hist(final_eta, bins=50, range=(-5, 5), color='purple', alpha=0.7)
    plt.title('Leading Jet η (Delphes, MET > 50 GeV, |η| > 2.0)')
    plt.xlabel('η')
    plt.ylabel('Events')
    
    plt.tight_layout()
    plt.savefig('GIP_Delphes_Validation_Plot.png')
    print(f"\n[+] Analyse abgeschlossen. Plot in 'GIP_Delphes_Validation_Plot.png' gespeichert.")
