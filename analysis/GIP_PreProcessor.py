import numpy as np

class GIP_PreProcessor:
    def __init__(self, energy_scale_gev, fano_symmetries=168):
        self.Q = energy_scale_gev
        self.fano_symmetries = fano_symmetries
        self.omega_gip = 750.0  # GeV (Sättigungslimit)
        self.alpha_sm = 1.0 / 137.036
        
    def calculate_associator_deficit(self):
        """
        Simuliert das Tr([X,Y,Z]) Defizit basierend auf der Energie.
        Unterhalb von Omega_GIP ist die Raumzeit assoziativ (Defizit = 0).
        Darüber "bricht" das Gitter.
        """
        if self.Q < self.omega_gip:
            return 0.0
        
        # Logarithmisches Anwachsen des Defizits nach dem Bruch
        # Normiert über die 168 Symmetrien der Fano-Ebene
        deficit_amplitude = np.log(self.Q / self.omega_gip) / self.fano_symmetries
        return deficit_amplitude

    def get_effective_kappa(self, base_kappa_na=0.015):
        """
        Berechnet den effektiven Kopplungs-Tensor (kappa_NA) für MadGraph.
        """
        deficit = self.calculate_associator_deficit()
        
        if deficit == 0.0:
            return 0.0 # Reine SM-Physik
            
        # GIP-Modifikation greift
        kappa_eff = base_kappa_na * (1 + deficit)
        return kappa_eff

    def generate_madgraph_param_card(self, output_file="param_card_GIP.dat"):
        """
        Schreibt die Werte in das Format, das MadGraph5 lesen kann.
        """
        kappa_eff = self.get_effective_kappa()
        
        card_content = f"""
######################################################################
## PARAMETER CARD FÜR GIP-EFT MODELL (MadGraph5_aMC@NLO)
######################################################################

Block GIPPARAMS
    1 {kappa_eff:.6e} # kappaNA (Effective Non-Associative Deficit)
    2 {self.omega_gip:.2f} # OmegaGIP (Saturation Scale in GeV)
"""
        with open(output_file, 'w') as f:
            f.write(card_content)
        print(f"[+] GIP Parameter Card für Q = {self.Q} GeV generiert.")
        print(f"    Kappa_effektiv: {kappa_eff:.6e}")

# ==========================================
# Ausführung für ein 800 GeV Kollisions-Event
# ==========================================
if __name__ == "__main__":
    # Test bei 800 GeV (knapp über der GIP Schwelle)
    gip_sim = GIP_PreProcessor(energy_scale_gev=800.0)
    gip_sim.generate_madgraph_param_card()
    
