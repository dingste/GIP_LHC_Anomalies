# Systematic Uncertainties and Robustness Analysis

Experimental verification at ATLAS/CMS requires a rigorous treatment of systematic uncertainties. The GIP model, while featuring a unique topological signature, must be evaluated against standard detector and LHC environment challenges.

## 1. Soft MET Window (10–30 GeV) and Pile-Up

The soft MET regime is traditionally considered "noisy" due to Pile-Up flucuations and instrumental effects.

### Robustness Strategy:
*   **Asymmetry as a Noise-Filter:** Pile-Up and electronic noise are inherently isotropic (statistically symmetric). By using the asymmetry filter $N_{\text{Asym}} = |N_F - N_B|$, the majority of symmetric noise cancels out.
*   **Vertex Association:** In a full ATLAS/CMS analysis, MET can be "cleaned" by associating tracks with the primary vertex (PFlow MET). Since the GIP signal is associated with the hard scattering process, track-based MET cleaning will significantly suppress Pile-Up contributions while preserving the signal.
*   **High-Luminosity Scaling:** At HL-LHC, while Pile-Up increases, the statistical power of the asymmetry filter grows, allowing for a clearer separation of the non-isotropic signal from the isotropic background flucuations.

## 2. Forward Jet Energy Scale (JES) and Instrumental Asymmetry

Jets in the extreme forward region ($|\eta| > 2.0$) have higher energy scale uncertainties compared to the central barrel.

### Robustness Strategy:
*   **Calibration via Z/Gamma + Jet:** The Forward JES can be calibrated using standard candles like $Z \to ee/\mu\mu$ or Photon + Jet events where the boson is central and the jet is forward.
*   **Detector Hermeticity:** Modern upgrades for HL-LHC (like the ATLAS High-Granularity Timing Detector - HGTD) are specifically designed to improve vertex association and energy resolution in the forward region.
*   **Systematic Null-Hypothesis:** Any instrumental asymmetry (e.g., one endcap having a slightly different response than the other) is typically at the percent level and is well-mapped by the collaborations. The GIP predicted asymmetry ($F/B \approx 0.64$) is orders of magnitude larger than known detector-induced spatial biases.

## 3. Signal vs. Standard Model Monojet Tails

The dominant background $pp \to j \nu \bar{\nu}$ is well-understood.

### Robustness Strategy:
*   **PDF Uncertainties:** Parton Distribution Function (PDF) uncertainties are the primary theory systematic for forward production. However, these affect the absolute cross-section more than the spatial $F/B$ ratio.
*   **Higher-Order Corrections (NLO/NNLO):** While the current GIP simulation is LO, the robust nature of the topological asymmetry (driven by the Albert Algebra rank-loss) is expected to persist at higher orders, as QCD radiation is primarily central or follows the hard-jet direction.

---
**Summary:** The GIP search strategy is designed to be **systematically robust** by shifting the discovery focus from absolute "bump hunting" (sensitive to JES/MET noise) to **topological symmetry breaking** (where noise cancels out).
