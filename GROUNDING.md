# GROUNDING — Empirical Anchors for the Model

> Companion to `AXIOMS.md`. Purpose: tie the model's claims to currently testable physics, starting with the most tractable anchor.

---

## 1. Which part to ground first — recommendation

**Focus first on the Canvas: dynamic dark energy (Axiom A2.2, \(\rho_\Lambda(t)\)).**

Reasoning:

1. **It is the only part of the model that makes a claim currently under active, quantitative experimental test.** A2.2 asserts the "cosmic constant" is not constant: \(\rho_\Lambda(t)=\rho_{\Lambda,0}+\delta(t)\) with \(\delta(t)\neq\text{const}\). This is precisely the question DESI is answering right now.
2. **The data are moving in the model's direction.** DESI DR2 (first 3 years, ~15M galaxies/quasars) + CMB + supernovae + weak lensing give a 2.8–4.2σ preference for evolving dark energy over \(\Lambda\)CDM, with best-fit \(w_0\in[-0.85,-0.66]\), \(w_a\in[-1.11,-0.61]\). The standard constant-\(\Lambda\) point \((w_0=-1, w_a=0)\) is excluded at 3.1σ (DESI+CMB) and 2.8–4.2σ with SNe.
3. **It is falsifiable on a short horizon.** DESI runs through 2026 (5 years, ~50M targets); Euclid, Rubin/LSST, and Roman will cross-check. The model can be confirmed or killed within ~2–5 years.
4. **The Geometry (spin-\(\tfrac12\), 720° rotation, A3.4) is already empirically solid** (topological, Dirac/quantum-mechanical) — it needs no new grounding, only correct statement. Treat as established, not as a research front.
5. **The Time-Locked Sync Point (A6) and vessel identity (A6.4) are metaphysical/phenomenological.** They cannot be grounded by physics experiments; they should be held as axiomatic narrative, not presented as empirical claims. Mixing them with the testable parts would weaken the whole model's credibility.

Therefore: **ground the Canvas first; keep Geometry as settled background; quarantine the Sync Point as non-empirical.**

---

## 2. Grounded sub-model: \(\delta(t)\) linked to observations

### 2.1 Standard parametrization (CPL)
Cosmology commonly writes dark energy equation of state
\[
w(a) \;=\; w_0 + w_a(1-a) \;=\; w_0 + w_a\frac{z}{1+z},
\]
where \(a=1/(1+z)\) is the scale factor, \(z\) redshift. \(\Lambda\)CDM is the point \(w_0=-1,\; w_a=0\).

DESI DR2 (with CMB + SNe) prefers the "quintom B" quadrant \(w_0>-1,\; w_a<0\): best-fits range \(w_0\in[-0.85,-0.66]\), \(w_a\in[-1.11,-0.61]\) depending on SNe sample (Pantheon+/Union3/DESY5). Significance: 3.1σ (DESI+CMB alone), 2.8–4.2σ (with SNe). Dark energy's influence has been weakening as the universe expands.

### 2.2 Mapping to this model's \(\rho_\Lambda(t)\)
Define the model's tension (A2.2) as
\[
\rho_\Lambda(t) \;=\; \rho_{\Lambda,0}\bigl(1+\epsilon(t)\bigr),\qquad \epsilon(t_0)=0 \text{ at present,}
\]
with sign convention \(\epsilon>0\) meaning *stronger* than today. Since \(w<-1\) in the past corresponds to energy density *growing* as \(a\) increases (phantom-like), the DESI preference implies \(\rho_\Lambda\) was higher in the past and is decaying toward today:
\[
\epsilon(t<t_0) > 0,\qquad \epsilon'(t_0) < 0.
\]
So the model's "breathing canvas" (A2.2) is, in its first grounded form, a **decaying dark-energy density** rather than a constant — consistent with the "Vanishing Constant" intuition, but now with a sign and a slope.

**Formal \(\delta\) (engine `delta_norm`):** with \(z\) redshift (present \(z=0\), past \(z>0\)),
\[
\delta_{\rm norm}(z) \;=\; \frac{\rho_\Lambda(z)}{\rho_{\Lambda,0}}-1
\;=\; (1+z)^{3(1+w_0+w_a)}\exp\!\left(-\frac{3 w_a z}{1+z}\right)-1.
\]
Grounded case (quintom B, \(w_0>-1,\;w_a<0\)): \(\delta_{\rm norm}(z>0)>0\) and \(\delta_{\rm norm}'(0)>0\) (density higher in past, decaying toward present). The purge/flat condition corresponds to \(\delta\to 0\) at late times.

### 2.3 Testable predictions (falsifiable)
- **P1 (sign):** Future DESI/Euclid data should keep \(w_a<0\) (dark energy weakening) at \(\ge 3\sigma\) combined; if \(w_a\to 0\) (constant \(\Lambda\)), A2.2's non-constancy claim is falsified.
- **P2 (magnitude):** \(|w_0+1| \gtrsim 0.1\) at \(\ge 3\sigma\) combined; if \(w_0\) converges to \(-1\) within 0.05, the "breathing" amplitude \(\epsilon\) is consistent with zero.
- **P3 (no phantom crossing hard wall):** If data instead prefer \(w<-1\) today and growing density (phantom), the model's "decaying toward present" sign (§2.2) must be revised; the architecture survives but the direction of breath flips.
- **P4 (anisotropy test):** If the apparent acceleration is confirmed to be directional (Sarkar et al. 2026), a uniform \(\delta(t)\) is insufficient; the canvas model must acquire a directional/flow term. If isotropy is confirmed (Vincenzi et al. 2026), A2.2 stands.

---

### 2.4 Best-fit \(\delta\) by SNe sample (DESI DR2)

| SNe sample | \(w_0\) | \(w_a\) | \(\delta_{\rm norm}(z=1)\) | \(\delta'_{\rm norm}(0)\) |
|---|---|---|---|---|
| Pantheon+ | -0.839 | -0.61 | -0.0185 | +0.483 |
| Union3 | -0.661 | -1.11 | +0.0637 | +1.017 |
| DESY5 | -0.750 | -0.87 | +0.0159 | +0.750 |

**Caveat:** the near-present derivative \(\delta'_{\rm norm}(0)>0\) is consistent across all three samples (density increasing backward from today), but the integrated \(\delta\) at \(z\sim1\) is sample-dependent and can cross zero (Pantheon+). The "decaying toward present" claim (A2.2 \(\epsilon'(t_0)<0\)) therefore holds **locally near \(t_0\)** only; the global sign over cosmic time is not yet settled and must be tracked as DESI/Euclid improve.

### 2.5 Euclid outlook (cross-check)

Euclid's Q1 release (March 2025) covered 0.45% of the nominal survey (63 deg², ~26M galaxies). Its cosmology likelihood (CLOE) forecasts a dark-energy figure of merit \(F_{\rm oM}(w_0,w_a) > 400\) when combining all primary probes — roughly an order of magnitude tighter than DESI alone. The model's P1–P3 (§2.3) should be re-evaluated against Euclid's first cosmology data release (expected ~2026–2027); until then, the DESI-anchored claims stand.

## 3. Geometry — settled background (no new work needed)

- Spin-\(\tfrac12\) requires \(720^\circ\) to return to initial state (topological belt trick; Dirac spinor sign change under \(2\pi\)). This is standard, experimentally confirmed quantum mechanics.
- Maps directly onto A3.4 (topological knot, two halves twist). No modification needed; cite as established.

---

## 4. What remains ungrounded (do not present as physics)

- A6.1–A6.4 (timestamp Oct 26 2000 10:26:20, "True Observer download", 26-year milestone, vessel identity). These are phenomenological/axiomatic within the model. Keep them out of any empirical claims or comparisons with data.
- A5.x awakening/closure (E≡I) — conceptual; may later be framed as an information-theoretic fixed point, but not currently testable.

---

## 5. Next concrete step

Draft a formal extension of Axiom A2.2 adding:
- the CPL link \(w(a)\) and the condition \(\epsilon'(t_0)<0\),
- predictions P1–P3 with their falsification criteria,
- a note that the model's "breathing canvas" is, in its grounded form, a decaying dark-energy density consistent with DESI DR2.

*Sources: DESI DR2 (LBL newscenter, 2025-03-19); Springer EPJC "Did DESI DR2 truly reveal dynamical dark energy?"; Nature Astronomy "Dynamical dark energy in light of DESI DR2 BAO" (SNR 3.9, Bayesian evidence 5.2±0.7 for w(z)CDM over ΛCDM).*
