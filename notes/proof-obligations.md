# Proof obligations

The abstract results below are conditional on the stated assumptions. Their verification for a particular adaptive MCMC kernel is recorded separately.

## DERIVED IN MANUSCRIPT

- [x] Stationary EMA memories from a finite second innovation moment: Section 2.
- [x] Momentum preservation and covariance identity at Robbins--Monro roots: Section 2.
- [x] Stationary augmented-law identification and uniqueness under frozen assumptions: Section 3.
- [x] Lift a geometrically contracting driver coupling through contractive memory: Section 4.
- [x] Invariant law in $\mathcal P_1$ and geometric Wasserstein convergence: Section 4.
- [x] One-step augmented-kernel parameter regularity and invariant-law Lipschitz dependence: Section 5.
- [x] Eccentricity comparison and weighted-growth bound for the Poisson solution: Section 6.
- [x] Log-Lipschitz parameter regularity of the augmented Poisson solution under uniform weighted drift and perturbation assumptions: Section 6.
- [x] Almost-sure convergence of weighted centred noise and ODE tracking under quadratic drift, bounded increments, stability and gain assumptions: Section 6.

## REFERENCE RESULTS

- Rudolf--Schweizer (2018), Theorem 3.1: quantitative Wasserstein perturbation.
- Hofstadler (2026), Theorems 3.4--3.5: frozen Poisson solution and its Wasserstein/eccentricity estimates.
- Carè et al. (2026; arXiv:1906.09464), Theorem 2: parameter-dependent Poisson regularity using weighted norms; comparison of centred iterates.
- Laitinen--Vihola (2024; arXiv:2408.14903), Lemma 4: Poisson martingale differences and conditional variance identity.
- Andrieu--Moulines (2006) and Benveniste--Métivier--Priouret (1990): stochastic approximation and adaptive stability.
- Fuh (2021): Markovian iterated-function-system comparison and contraction-on-average motivation.

## APPLICATION-SPECIFIC VERIFICATION

- [ ] Verify a uniform driver trajectory coupling for the chosen Metropolis--Hastings kernel and metric on a parameter localisation set.
- [ ] Verify driver/innovation parameter perturbation assumptions for the sampler.
- [ ] Verify invariant moments, the squared-drift inequality and the Lipschitz class of the augmented Adam readout, including auxiliary proposal variables where needed.
- [ ] Establish parameter stability or a localisation construction compatible with the unprojected recursion in the tracking theorem.
- [ ] Quantify the covariance correction or root displacement in a concrete model.

## FINAL CHECKS

- [ ] Read through the two new Section 6 proofs independently, checking uniformity of constants and the gain-index convention.
- [ ] Render and review the updated Quarto PDF/HTML.
- [ ] Check cross-references and bibliography after rendering.
