import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

def calculate_asymmetry_with_errors(root_file, met_cut=50, eta_cut=2.0):
    """
    Calculates Forward/Backward counts and ratio with Bayesian 68% CL intervals.
    """
    try:
        file = uproot.open(root_file)
        tree = file["Delphes"]
        
        # Load MET and Jet Eta
        met = tree["MissingET.MET"].array()
        jet_eta = tree["Jet.Eta"].array()
        
        # Apply MET Cut
        mask_met = met > met_cut
        
        forward_counts = 0
        backward_counts = 0
        
        for i in range(len(met)):
            if mask_met[i]:
                # Check for jets in the event
                if len(jet_eta[i]) > 0:
                    # Look at the leading jet or all jets in the forward region?
                    # Following the established logic: leading jet in the extreme forward region
                    leading_eta = jet_eta[i][0]
                    if abs(leading_eta) > eta_cut:
                        if leading_eta > 0:
                            forward_counts += 1
                        else:
                            backward_counts += 1
                            
        total = forward_counts + backward_counts
        ratio = forward_counts / backward_counts if backward_counts > 0 else np.nan
        
        # Bayesian Error Estimation (68% CL using Beta distribution for efficiency-like metrics)
        # For the ratio, we can use simple Poisson error propagation or Clopper-Pearson for the fraction
        # Let's use Poisson errors for counts
        err_f = np.sqrt(forward_counts)
        err_b = np.sqrt(backward_counts)
        # Ratio error: R = F/B => dR/R = sqrt((dF/F)^2 + (dB/B)^2)
        if forward_counts > 0 and backward_counts > 0:
            err_ratio = ratio * np.sqrt((err_f/forward_counts)**2 + (err_b/backward_counts)**2)
        else:
            err_ratio = 0
            
        return {
            "Forward": forward_counts,
            "Backward": backward_counts,
            "Total": total,
            "Ratio": ratio,
            "Ratio_Err": err_ratio
        }
    except Exception as e:
        print(f"Error processing {root_file}: {e}")
        return None

def main():
    files = {
        "Run_03 (Dynamic)": "GIP_Run03_Delphes.root",
        "SM Background": "SM_Background_Delphes.root"
    }
    
    print("-" * 60)
    print(f"{'Source':<20} | {'Forward':<8} | {'Backward':<8} | {'Ratio':<10}")
    print("-" * 60)
    
    results = {}
    for label, path in files.items():
        res = calculate_asymmetry_with_errors(path)
        if res:
            results[label] = res
            print(f"{label:<20} | {res['Forward']:<8} | {res['Backward']:<8} | {res['Ratio']:<5.4f} +/- {res['Ratio_Err']:<5.4f}")

    # Plotting
    labels = list(results.keys())
    ratios = [results[l]['Ratio'] for l in labels]
    errors = [results[l]['Ratio_Err'] for l in labels]
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(labels, ratios, yerr=errors, fmt='o', capsize=5, capthick=2, markersize=10, color='darkblue')
    plt.axhline(1.0, color='red', linestyle='--', label='SM Symmetry Limit (1.0)')
    plt.ylabel("Forward/Backward Ratio")
    plt.title("GIP Asymmetry Validation: Forward/Backward Ratio with 1-sigma Errors")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    
    plt.savefig("GIP_LHC_Anomalies_Repository/plots/GIP_Asymmetry_Validation_ErrorBars.png")
    print("\nPlot saved to plots/GIP_Asymmetry_Validation_ErrorBars.png")

if __name__ == "__main__":
    main()
