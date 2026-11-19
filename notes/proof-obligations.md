# Proof obligations

The general results are conditional on the stated assumptions. Section 2 fixes the recursion, kernel and norms; Section 3 proves contraction; Section 4 treats stationary Adam calibration; Section 5 develops parameter perturbation and Poisson regularity; Section 6 proves adaptive ODE tracking. Model-specific verification remains separate.

## DERIVED IN MANUSCRIPT

- [x] Lift a geometrically contracting driver trajectory coupling through contractive memory: Section 3, `thm-wasserstein-lifting`. The coupling and geometric convolution remain in the main proof.
- [x] Existence and uniqueness in $\mathcal P_1$ and geometric Wasserstein convergence of the augmented law: Section 3, `thm-wasserstein-lifting`.
- [x] Augmented first-order Lyapunov drift: Section 3, `lem-augmented-drift`; calculation in Appendix B.
- [x] Stationary EMA memories from a finite second innovation moment: Section 4, `lem-stationary-memories`; Tonelli, tail and Jensen estimates in Appendix A.
- [x] Stationary augmented-law identification and uniqueness among all invariant probabilities under the frozen driver assumptions: Section 4, `cor-stationary-memory-law`.
- [x] Momentum preservation and covariance identity at Robbins--Monro roots: Section 4.
- [x] Square-root second-moment coordinates, contractive spatial update and bounded Lipschitz Adam readout for bounded innovations: Section 4.
- [x] One-step augmented-kernel parameter regularity and invariant-law Lipschitz dependence: Section 5. The driver/memory operator decomposition and power telescoping calculation remain in the body.
- [x] Eccentricity comparison between centred Lipschitz functions and weighted-growth spaces: Section 5.
- [x] Centred frozen Poisson solution, uniqueness in the centred Lipschitz class and weighted-growth bound: Section 5.
- [x] Log-Lipschitz parameter regularity of the augmented Poisson solution: Section 5, `prp-poisson-parameter`. The uniform $O(\delta)$ and geometrically decaying iterate bounds, telescoping calculation and logarithmic split remain explicit.
- [x] Almost-sure convergence of weighted centred noise and ODE tracking under quadratic drift, bounded increments, stability and logarithmically corrected gain summability: Section 6, `thm-augmented-ode-tracking`. Martingale, summation-by-parts, feedback and Euler/flow comparisons remain in the body.

## DEPENDENCIES AND PROOF REVIEW

- Section 2.1 defines uniform contraction in the memory argument and derives geometric forgetting along a common driving trajectory. Assumption 3.2 separately adds spatial regularity in the observation argument and the one-step first moment; the joint update bound follows by the triangle inequality.
- The stationary Adam representation uses `asm-frozen-driver` and fixed EMA coefficients below one. It is independent of driver trajectory coupling, spatial Lipschitz forcing, parameter perturbation and adaptive drift. In particular, its finite innovation moment does not impose a first moment for an arbitrary driver metric.
- The lifting theorem requires a single consistent coupling of driver trajectories, contractive and spatially regular memory, and a one-step augmented first moment. It asserts uniqueness in $\mathcal P_1$; the Adam stationary argument separately gives uniqueness among all invariant probabilities.
- Spatial Lipschitz regularity of the affine or square-root memory map verifies the joint update bound. The one-step moment clause of `asm-memory-lipschitz` must also be checked; for bounded square-root memories it reduces to the driver's first moment.
- The invariant-law perturbation proof uses geometric contraction, weighted one-step perturbation and finite invariant weighted moments directly. Its corollary now states those sufficient assumptions explicitly, allowing the general Poisson proposition to invoke it without requiring a particular driver-level verification.
- The Poisson result uses $d_Z(z,z_0)\leq c\mathcal V(z)$ and uniform invariant $\mathcal V$-moments to bound eccentricity, together with a uniform first-order drift to bound all $Q_\theta^n\mathcal V$. The telescoping sum is bounded uniformly in $n$ by summing the decaying Lipschitz seminorms. Splitting at $\lceil\log(1/\delta)/|\log\rho|\rceil$ gives the stated logarithmic modulus.
- The tracking proof needs quadratic drift along the adaptive path and stability in the compact parameter set. The gain convention is $\theta_n-\theta_{n-1}=\gamma_nG_{\theta_{n-1}}(Z_n)$; hence the feedback term has size $\gamma_n^2(1+|\log\gamma_n|)\mathcal V(Z_n)$. Nonincreasing gains control the gain-variation series. The ODE conclusion also uses the stated Lipschitz extension and forward flow.
- No unresolved algebraic proof issue was found in the retained core arguments during the reorganisation. The added details make the sufficient hypotheses and final flow comparison explicit; they do not verify a sampler's assumptions or establish convergence to a particular equilibrium.

## REFERENCE RESULTS

- Rudolf--Schweizer (2018), Theorem 3.1 and Corollary 3.1: quantitative Wasserstein perturbation and stationary specialisation.
- Hofstadler (2026), Theorems 3.4--3.5: centred Lipschitz Poisson solution and Wasserstein/eccentricity estimates.
- Carè et al. (2026; arXiv:1906.09464), Theorem 2: parameter-dependent Poisson regularity using weighted norms; comparison of centred iterates motivates the proof in Section 5.
- Laitinen--Vihola (2024; arXiv:2408.14903), Lemma 4: Poisson martingale differences and conditional variance identity, used in Section 6 with augmented kernels and quadratic moment control.
- Andrieu--Moulines (2006) and Benveniste--Métivier--Priouret (1990): stochastic approximation and adaptive stability.
- Fuh (2021): Markovian iterated-function-system comparison and contraction-on-average motivation.

## APPLICATION-SPECIFIC VERIFICATION

- [ ] Verify a uniform driver trajectory coupling for the chosen Metropolis--Hastings kernel and metric on a parameter localisation set.
- [ ] Verify driver/innovation parameter perturbation assumptions for the sampler.
- [ ] Verify invariant moments, the one-step metric moment and squared-drift inequality, including auxiliary proposal variables where needed. The bounded square-root Adam readout is handled in Section 4.
- [ ] Establish parameter stability or a localisation argument compatible with the unprojected recursion in the tracking theorem. Projection requires a corresponding ODE treatment.
- [ ] Check the limiting field's ODE extension, flow and equilibrium attraction for the chosen model.
- [ ] Quantify the covariance correction or root displacement in a concrete model.

## FINAL CHECKS

- [x] Check shared result numbering in HTML and PDF: theorems, propositions, lemmas and corollaries use one sequence per section; definitions and assumptions retain their own sequences. All eight result headings agree between formats and all 19 HTML result cross-references match their targets. Semantic labels remain unchanged.
- [x] Review the retained lifting, parameter-Poisson and tracking proofs, including uniform constants and the gain-index convention.
- [x] Render and visually review the restructured Quarto PDF/HTML (20 pages), using a clean temporary source copy to avoid the existing checkout resource-scan failure. All 14 checker tests pass.
- [x] Check cross-references, appendix links and bibliography after rendering. All local HTML anchors resolve; the PDF was reviewed for theorem and equation numbering. A citation immediately following an equation cross-reference was moved before it so Quarto renders both.
