import uproot
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

# Parameter
luminosity = 3000.0  # fb^-1 (HL-LHC)
sigma_signal = 1.0   # fb (Annahme)
sigma_bg = 2342.0 * 1000.0  # fb (MadGraph Cross-Section für pp > j vv)

signal_file = "GIP_Run03_Delphes.root"
bg_file = "SM_Background_Delphes.root"

def get_surviving_events(filename, met_cut=50.0, eta_cut=2.0):
    print(f"[+] Verarbeite {filename}...")
    with uproot.open(filename) as f:
        tree = f["Delphes"]
        
        # MET auslesen
        met_array = tree["MissingET.MET"].array()
        met = ak.to_numpy(ak.fill_none(ak.pad_none(met_array, 1, axis=1), 0)[:, 0])
        
        # Jets auslesen
        jet_eta = tree["Jet.Eta"].array()
        jet_pt = tree["Jet.PT"].array()
        
        # Filter
        has_jets = ak.num(jet_pt) > 0
        met_gate = met > met_cut
        combined_mask = met_gate & has_jets
        
        filtered_jet_eta = jet_eta[combined_mask]
        
        # Mindestens ein Jet muss da sein für eta-Schnitt
        if len(filtered_jet_eta) == 0:
            return 0, len(met), []
            
        leading_jet_eta = ak.to_numpy(filtered_jet_eta[:, 0])
        eta_mask = np.abs(leading_jet_eta) > eta_cut
        
        final_eta = leading_jet_eta[eta_mask]
        
        return len(final_eta), len(met), final_eta

# Signal Analyse
n_s_pass, n_s_total, eta_s = get_surviving_events(signal_file)
eff_s = n_s_pass / n_s_total
s_exp = luminosity * sigma_signal * eff_s

# Hintergrund Analyse
n_b_pass, n_b_total, eta_b = get_surviving_events(bg_file)
eff_b = n_b_pass / n_b_total
b_exp = luminosity * sigma_bg * eff_b

# Signifikanz
significance = s_exp / np.sqrt(b_exp) if b_exp > 0 else 0

print(f"\n--- HL-LHC Signifikanz-Bericht (3000 fb^-1) ---")
print(f"Signal (GIP):")
print(f"  Total Events (simuliert): {n_s_total}")
print(f"  Events nach Schnitt:      {n_s_pass}")
print(f"  Effizienz:                {eff_s:.6f}")
print(f"  Erwartete Events (S):     {s_exp:.2f}")

print(f"\nHintergrund (SM pp > j vv):")
print(f"  Total Events (simuliert): {n_b_total}")
print(f"  Events nach Schnitt:      {n_b_pass}")
print(f"  Effizienz:                {eff_b:.6f}")
print(f"  Erwartete Events (B):     {b_exp:.2f}")

print(f"\nRESULTAT:")
print(f"  Signifikanz S/sqrt(B):    {significance:.4f} sigma")

# Plot
plt.figure(figsize=(10, 6))
plt.hist(eta_s, bins=30, range=(-5, 5), alpha=0.5, label='Signal (GIP) η', density=True, color='red')
plt.hist(eta_b, bins=30, range=(-5, 5), alpha=0.5, label='Background (SM) η', density=True, color='blue')
plt.title('Normalized η Distribution: Signal vs Background')
plt.xlabel('Leading Jet η')
plt.ylabel('Normalized Density')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('GIP_Significance_Plot.png')
print(f"\n[+] Vergleichsplot in 'GIP_Significance_Plot.png' gespeichert.")
