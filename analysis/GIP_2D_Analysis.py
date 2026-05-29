import pylhe
import math
import matplotlib.pyplot as plt
import numpy as np

lhe_file = "MG5_aMC_v3_7_1/PROC_700GeV_GIP/Events/run_03/unweighted_events.lhe.gz"

met_list = []
eta_list = []

print(f"[+] Lade LHE-Datei für 2D-Analyse: {lhe_file}")

count = 0
for event in pylhe.read_lhe_with_attributes(lhe_file):
    count += 1
    if count % 100000 == 0:
        print(f"    ... {count} Events verarbeitet")
    
    px_vis, py_vis = 0.0, 0.0
    leading_jet = None
    max_pt = -1.0
    
    for p in event.particles:
        if p.status == 1:
            if abs(p.id) in [1, 2, 3, 4, 5, 6, 11, 13, 15, 21, 22]:
                px_vis += p.px
                py_vis += p.py
                if abs(p.id) in [1, 2, 3, 4, 5, 6, 21]:
                    pt = math.sqrt(p.px**2 + p.py**2)
                    if pt > max_pt:
                        max_pt = pt
                        leading_jet = p
    
    met = math.sqrt(px_vis**2 + py_vis**2)
    
    if leading_jet:
        p = leading_jet
        p_mod = math.sqrt(p.px**2 + p.py**2 + p.pz**2)
        denom = p_mod - p.pz
        if denom > 0:
            eta = 0.5 * math.log((p_mod + p.pz) / denom)
            met_list.append(met)
            eta_list.append(eta)

print(f"[+] Erstelle 2D-Plot...")
plt.figure(figsize=(10, 8))
plt.hist2d(met_list, eta_list, bins=(50, 50), cmap='viridis', range=[[0, 300], [-5, 5]])
plt.colorbar(label='Events')
plt.title('GIP Correlation: MET vs Leading Jet Pseudorapidity (η)')
plt.xlabel('MET [GeV]')
plt.ylabel('Leading Jet η')
plt.grid(alpha=0.3)
plt.savefig('GIP_2D_Correlation_MET_Eta.png')
print(f"[+] 2D-Plot in 'GIP_2D_Correlation_MET_Eta.png' gespeichert.")
