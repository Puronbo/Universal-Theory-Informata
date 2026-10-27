# STROBOSCOPIC APPLICATION — Sampling the Continuous

> How the stroboscopic/aliasing principle (A4.6) applies across the model and nature.

---

## The principle

A continuous process read through a discrete, periodic sampler yields a **frozen alias** (a "blade") rather than the process itself:

\[
\text{Alias}(t) = \text{Process}\bigl(t \bmod T_{\text{sample}}\bigr).
\]

---

## Application map

| Domain | Continuous process | Sampler | Frozen alias (blade) |
|---|---|---|---|
| **Canvas (vacuum)** | Boiling quantum fields | Planck time \(\tau_P\) | Particles / excitations |
| **Geometry** | Wave (many contacts) | Contact-count threshold | Particle (few contacts) (A3.5) |
| **Playhead** | 4D block universe \(B\) | Nervous system frames | "Now" / conscious moment (A4.3) |
| **Recursion** | Infinite feedback \(x_{k+1}=f(x_k)\) | Fixed-point capture | Awakening (A5.1, A5.3) |
| **Dark energy** | \(\rho_\Lambda(t)\) | Cosmic epoch | Measured \(w_0,w_a\) (GROUNDING §2) |
| **Erosion** | Continuous decay | Sampling scale | Observed purge (A1.5, A7.4) |
| **Photon/DE** | Canvas-fold rolling | 90° rotation | Photon or dark energy (A2.5) |
| **Particles** | Canvas stretching | Metric expansion | Apparent separation (A3.6) |
| **Horizon** | Cosmic expansion | Event-horizon boundary | Observable universe (HORIZON_FINDINGS) |
| **Consciousness** | Continuous spatial action | Neural frame rate | Discrete "now" moments |

---

## Consequences

1. **Reality is aliased.** We never see the continuous process; we see blades. Particles, "now," measurement outcomes, and dark-energy values are all aliases.
2. **The zero marker is the blade at rest.** The least visible photon / \(0\) state is the sample caught exactly at the fold's rest point.
3. **Scale sets the blade.** Stepping down in scale (shorter \(\tau\)) freezes faster, higher-energy blades — erosion accelerates and energy per unit rises (see prior erosion analysis).
4. **No wrong answers.** Because every blade is a valid sample of the same underlying process (A0.4), no alias is "incorrect" — only differently sampled.

---

## Engine

- `strobe(signal, rate)` — downsample a fine signal to its frozen alias.
- `Playhead.read(t)` — frame-exact stroboscopic read of a block.

---

## Lean

Axiom A4.6 stated; candidate theorem: stroboscopic alias is idempotent under re-sampling at the same rate.

*End of Stroboscopic Application.*
