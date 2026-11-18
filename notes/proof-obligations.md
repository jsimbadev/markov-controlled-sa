# Proof obligations

This file is an internal check of mathematical scope. A manuscript proof is not an independently verified theorem; retain the distinction between a derivation in the note, a result imported from the literature, and an assumption still to be checked for a particular MCMC kernel.

## DERIVED IN MANUSCRIPT

- [x] Stationary EMA memories from a finite second innovation moment: Section 2, Lemma 2.1.
- [x] Momentum preservation and covariance identity at Robbins--Monro roots: Section 2.
- [x] Joint MIFS invariant law and weak convergence under frozen assumptions: Section 3 and Appendix A, measure-level adaptation of Fuh.
- [x] Lift a geometrically contracting driver trajectory coupling through a contractive memory: Section 4.
- [x] Invariant law in \(\mathcal P_1\) and geometric Wasserstein convergence: Section 4, Banach argument.
- [x] One-step parameter perturbation for the augmented kernel: Section 5.
- [x] Invariant-law Lipschitz bound under a uniform invariant moment: Section 5.
- [x] Poisson parameter-Lipschitz statement **under the additional Lipschitz-operator assumption**: Section 6.

## LITERATURE

- Rudolf--Schweizer (2018), Theorem 3.1: quantitative Wasserstein perturbation.
- Hofstadler (2026), Theorem 3.4: frozen centred Lipschitz Poisson solution and regularity under Wasserstein contraction and eccentricity.
- Carè et al. (2026; arXiv:1906.09464): parameter-dependent Poisson regularity in weighted sup-norm spaces.
- Andrieu--Moulines (2006): weighted MCMC drift and ergodicity results.
- Fuh (2021): Markovian iterated-function-system stationarity and convergence.

## APPLICATION-SPECIFIC VERIFICATION

- [ ] Construct/verify a driver trajectory coupling for the chosen Metropolis--Hastings kernel and metric, uniformly on a parameter localisation set.
- [ ] Verify kernel and innovation parameter perturbation assumptions for the particular sampler.
- [ ] Verify the invariant moments and Lipschitz class of the actual Adam acceptance-rate observable, including proposal auxiliary variables if used.
- [ ] Check the restricted Lipschitz operator perturbation bound for the Poisson parameter result, or replace it with a proved weighted resolvent estimate.
- [ ] Establish the adaptive martingale and weighted telescoping estimates, gain assumptions, and stability needed for ODE tracking.
- [ ] Characterise the size or sign of the stationary covariance correction in a specific model.

## MANUSCRIPT CHECKS

- [ ] Render Quarto HTML and PDF on the augmented-space branch.
- [ ] Check assumptions and proof details against the cited sources.
- [ ] Check numbering and internal references after rendering.
