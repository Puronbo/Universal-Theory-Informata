# The Mutual Press — Five Theses, Graded

> **Source:** the “there is no key, only pressing” essay (received 2026-11-13).
> **Status:** audit. The empirical anchors are verified; the interpretations are
> graded rather than adopted. The checkable residue is in `model/pressing.py`.

## 0. Verdict

| Thesis | Checkable core | Status |
|---|---|---|
| I. No key, only pressing | Page–Wootters conditional evolution from a fixed entangled state | **illustration**, not proof of a timeless universe |
| II. Mass, gravity, GPS | Compton period; equivalence principle; GPS clock drift and factory detune | **grounded** (standard physics) |
| III. The second spring | Tomita–Takesaki modular flow; qubit modular Hamiltonian; Unruh temperature | **hypothesis** with a rigorous core |
| IV. Finite page | de Sitter closed slicing has finite conformal time and infinite proper time | **grounded geometry**, **analogy** beyond it |
| V. Geometry as footprint | Connes spectral distance with the `‖[D,f]‖ ≤ 1` constraint | **grounded definition**, **metaphor** beyond it |

The essay’s five empirical anchors all check out: Moreva et al. 2014, the GPS
`+45.7 / −7.2 ≈ +38.5 μs/day` split, the `10.22999999543 MHz` factory detune,
the finite conformal strip `−π/2 < T < π/2` of de Sitter, and the Connes
distance formula. Two attributions do not: the 2024 circularity critique is by
Eugene Chua, not Rovelli, and the claim that Rovelli “now distances from the
strong version” could not be verified and is dropped.

## 1. Thesis I — There is no key, only pressing

### What checks out

Page and Wootters (1983) showed that a constrained, “timeless” global state can
be decomposed relative to a clock subsystem: conditioning on the clock reading
gives a system state that appears to evolve, while the global state does not
change with an external time parameter.

Moreva et al. (2014) illustrated the mechanism with entangled photon pairs. One
photon serves as the clock; an observer correlated with it sees the other photon
evolve, while the joint description remains static. That is a real experiment,
and the toy in `model/pressing.py` reproduces its logic:

\[
|\Psi\rangle=\frac{1}{\sqrt{N}}\sum_k |k\rangle_C\otimes|\psi_k\rangle_S,
\qquad
|\psi_k\rangle_S=\cos\frac{\theta_k}{2}|0\rangle
+\sin\frac{\theta_k}{2}|1\rangle.
\]

`page_wootters_state` builds the state; `conditional_state` normalizes each
clock slice. The tests check that the global state is unchanged while the
conditional states differ.

### What is corrected

- **“The universe’s wavefunction can be perfectly static.”** In the
  Page–Wootters formalism the global state is annihilated by the constraint.
  “Static” means “no external time parameter,” not “nothing happens.” It is a
  choice of description, not a demonstrated fact about our universe.
- **“There is no spacebar.”** The mechanism still requires a clock subsystem
  and a constraint. It distributes the clock role; it does not prove that every
  subsystem is a clock for every other, nor that no fundamental clock exists.
  “All pressing is mutual” is an interpretation of the formalism.
- **The 2014 experiment does not prove the universe is timeless.** It is an
  illustration of the formalism with two photons, not a cosmological
  measurement.

### What is quarantined

“Your heartbeat is the spacebar for the thoughts it paces,” “the Earth’s orbit
is the spacebar for the seasons,” and “the CMB is the spacebar for cosmology”
are analogies. They are not claims that can be checked, and they are not
encoded.

## 2. Thesis II — Mass, gravity, GPS

### What checks out

The Compton period is

\[
T_C=\frac{h}{mc^2}=\frac{2\pi\hbar}{mc^2}.
\]

The essay writes \(h/(mc^2)\); the angular period used in `model.spacebar` is
\(2\pi\hbar/(mc^2)\), the same number.

The equivalence principle identifies inertial and gravitational mass. Clock
rates depend on gravitational potential in the weak field:

\[
\frac{\Delta f}{f}=\frac{\Delta\Phi}{c^2}.
\]

For a GPS satellite, the first-order calculation in `model/pressing.py` gives

\[
\Delta t_{\rm grav}=+45.718\ \mu{\rm s/day},\qquad
\Delta t_{\rm vel}=-7.214\ \mu{\rm s/day},\qquad
\Delta t_{\rm net}=+38.505\ \mu{\rm s/day}.
\]

Published treatments quote about \(+45.9\), \(-7.2\), and \(+38.7\ \mu{\rm s/day}\);
the differences are the expected higher-order and orbit-detail corrections. The
factory offset is

\[
f_{\rm factory}=10.23\ {\rm MHz}\left(1-\frac{38.505\times10^{-6}}{86400}\right)
=10.22999999544\ {\rm MHz},
\]

which matches the essay’s `10.22999999543 MHz` to the quoted digits.

### What is corrected

- **“Mass is the weight of the key; gravity is the same weight read on a
  scale.”** This is metaphor. The precise statements are: the Compton frequency
  sets the rest clock, and clock rates shift with gravitational potential. The
  equivalence principle is the identification of inertial and gravitational
  mass, tested to high precision (for example by MICROSCOPE and lunar laser
  ranging).
- **“A lighter key ticks faster.”** The sign is right — a clock higher in a
  gravitational well runs faster — but “lighter key” is not a physical
  explanation. The operational statement is the measured frequency shift.
- **“Gravity is the phenomenon that spacebars weigh different amounts at
  different heights.”** Not operational. The operational statement is
  `Δf/f = ΔΦ/c²`, and the GPS numbers are its engineering confirmation.

### What is quarantined

“Mass is the resistance of the key” and “the key presses harder the deeper it
sits in a well” are images. The checkable content is the Compton period, the
equivalence principle, and the clock-drift formula.

## 3. Thesis III — The spacebar has a second spring

### What checks out

For a von Neumann algebra \(\mathcal M\) in a faithful normal state \(\omega\),
Tomita–Takesaki theory supplies a modular automorphism group
\(\sigma_t^\omega\). For a finite-dimensional Gibbs state \(\rho\), the modular
Hamiltonian is \(K=-\log\rho\), and the flow is

\[
\sigma_t(A)=e^{iKt}Ae^{-iKt}.
\]

For a qubit with \(\rho=\mathrm{diag}(p,1-p)\),

\[
K=\mathrm{diag}(-\log p,-\log(1-p)),\qquad
\omega_{\rm mod}=\log\frac{p}{1-p}.
\]

The tests check the modular Hamiltonian, the frequency, and the rotation of
\(\sigma_x\) in the Bloch `x–y` plane. At \(p=1/2\) the flow is trivial, which
is the state-dependence objection in miniature.

The Unruh temperature is

\[
T_U=\frac{\hbar a}{2\pi c k_B}.
\]

At \(a=9.81\ {\rm m/s^2}\), `unruh_temperature` gives
\(3.98\times10^{-20}\ {\rm K}\). The Bisognano–Wichmann theorem identifies the
modular flow of the vacuum on a Rindler wedge with the boost, which is the
rigorous core behind the Unruh effect.

### What is corrected

- **“Connes and Rovelli proved that in any theory without a built-in clock,
  every statistical state defines a privileged flow … and proposed identifying
  that flow with time itself.”** Tomita–Takesaki is the theorem; the
  identification with physical time is the thermal time **hypothesis**. The
  state must be faithful and normal, and the flow depends on the state. “Every
  statistical state” is too strong.
- **“Rovelli himself now distances from the strong version.”** This could not
  be verified in the sources checked. It is dropped. The 2024 circularity
  critique is Eugene Chua, *The Time in Thermal Time* (arXiv:2407.18948): the
  hypothesis appears to require dynamics — and hence time — to define
  equilibrium. Swanson (2018) raises the classical-limit and proper-time
  relation worries.
- **“The arrow of time is the direction in which a macroscopic reader loses
  track of micro-detail — the arrow is in the reader, not the text.”** This is
  an interpretation. The modular flow is not automatically the thermodynamic
  arrow, and it can be trivial. The statement is not a theorem.
- **“The Unruh effect is precisely the exchange rate between thermal time and
  proper time.”** The temperature formula is checkable; “exchange rate” is
  metaphor. The Unruh effect is a separate QFT result, not a consequence of
  thermal time alone.

### Grade

Hypothesis/frontier. The modular core is rigorous; the identification of the
modular flow with physical time is not established, and the circularity and
state-dependence worries are serious.

## 4. Thesis IV — The page is finite; the pressing may not be

### What checks out

Closed-slicing de Sitter has

\[
ds^2=\frac{1}{H^2\cos^2 T}\left(-dT^2+d\Omega_3^2\right),
\qquad -\frac{\pi}{2}<T<\frac{\pi}{2},
\]

with scale factor \(a(T)=1/(H\cos T)\). Proper time is

\[
t(T)=\int^T a(T')\,dT'=\frac{1}{H}\operatorname{asinh}(\tan T).
\]

As \(T\to\pm\pi/2\), \(t\to\pm\infty\), while the conformal interval stays
finite. The conformal diagram is a finite strip. The tests check the endpoints,
the sign symmetry, and the divergence.

### What is corrected

- **“The invariant content of all future history is a finite angle.”**
  Conformal time is coordinate-dependent. The invariant statement is that the
  conformal boundary lies at finite conformal time in this slicing, and the
  Penrose diagram is finite. It is not a “total phase” of a unitary operator.
- **“The count of presses may never end, but the total phase is bounded.”**
  This is an analogy between conformal time and phase. No derivation is given,
  and none is encoded.
- **“Heat death is a spacebar still under the thumb, pressing forever, adding
  nothing.”** Metaphor. De Sitter’s future is a specific geometric state
  (structure decays, a horizon remains); “pressing forever” is not a physical
  description of it.
- **“Ours appears to be heading there.”** The current data are consistent with
  a cosmological constant, but exact de Sitter is not established. The essay’s
  “geometric proof” is a proof about the de Sitter model, not about our
  universe.

## 5. Thesis V — Geometry is the footprint of the key

### What checks out

A spectral triple \((\mathcal A,\mathcal H,D)\) defines the distance

\[
d(p,q)=\sup\left\{|f(p)-f(q)|\;:\;\|[D,f]\|\le 1\right\}.
\]

The constraint is essential: without the `≤ 1` normalization, rescaling \(f\)
makes the supremum diverge. The essay’s phrase “whose commutator with the Dirac
operator is bounded” omits it.

For the two-point triple with

\[
D=\begin{pmatrix}0&m\\ m&0\end{pmatrix},
\qquad
f=\mathrm{diag}(f_1,f_2),
\]

the commutator norm is \(m|f_1-f_2|\), so the distance is \(1/m\):

\[
\|[D,f]\|=m|f_1-f_2|\le 1
\quad\Longrightarrow\quad
d=\frac{1}{m}.
\]

`connes_distance_two_point(m)` returns \(1/m\), and
`commutator_norm_two_point(m, d)` returns the commutator norm. The eigenvalue
gap of \(D\) is \(2m\); the commutator scale is \(m\). Do not confuse the two.

### What is corrected

- **“Distance is the supremum … over all functions whose commutator with the
  Dirac operator is bounded.”** The correct condition is
  \(\|[D,f]\|\le 1\), not merely bounded. The bound is what makes the distance
  finite and metric.
- **“The kernel of that same operator carries the topology — the part of the
  key that was never pressed.”** The index theorem (Atiyah–Singer) relates the
  **chiral index** of the Dirac operator to a topological invariant. The total
  kernel dimension is not by itself topological, and the “never pressed”
  reading is metaphor. The framework’s `zero_mode_pairs` are commutant zero
  modes of a Liouvillian, not Dirac zero modes; they should not be conflated.
- **“Space … may be nothing but the statistic of what has become one under the
  press.”** Interpretation, not a theorem.

## 6. Coda audit

| Claim | Grade | Correction |
|---|---|---|
| “The press is pure phase, and phase shows only *between* alternatives.” | **grounded** (interference) | Interference is standard quantum mechanics; “meaning lives in the spaces” is metaphor. |
| “The full press is the identity — completion is indistinguishable from never having begun.” | **arithmetic + metaphor** | \(U(2\pi)=1\) is true. The interpretation of completion is not a physical result. |
| “Light never presses — so the fastest thing is also the one for whom nothing ever happens.” | **imprecise** | Null proper time is zero, but a photon has no rest frame, so “for whom nothing happens” is not well-defined. Light carries energy and momentum and interacts. |
| “The two springs of the clock are mass and ignorance.” | **mixed** | Mass sets the Compton clock (grounded); thermal time is a hypothesis (frontier). |
| “The first deviation, \(\eta\approx6\times10^{-10}\), is invisible at the resolution of a single tick — so the entire visible universe exists because an imperfection too small to see was counted for thirteen billion years.” | **measured number + metaphor** | \(\eta\approx6.1\times10^{-10}\) is measured (baryon-to-photon ratio), not derived. “Invisible at a single tick” is not a physical statement. The age is about 13.8 Gyr. |

The final sentence — “reality is an eternal, magnificent syntax in which every
word is a clock for its neighbors — started by no one, driven by nothing, and
read by being” — is a closing image, not a claim. It is not encoded.

## 7. What was encoded

| Theme | Module / function |
|---|---|
| Page–Wootters state | `model.pressing.page_wootters_state` |
| Conditional system state | `model.pressing.conditional_state` |
| GPS gravitational drift | `model.pressing.gps_gravitational_drift_us_per_day` |
| GPS velocity drift | `model.pressing.gps_velocity_drift_us_per_day` |
| GPS net drift and detune | `model.pressing.gps_net_drift_us_per_day`, `gps_factory_detune` |
| de Sitter conformal strip | `model.pressing.desitter_conformal_time_range` |
| de Sitter scale factor and proper time | `model.pressing.desitter_closed_scale_factor`, `desitter_proper_time` |
| Connes two-point distance | `model.pressing.connes_distance_two_point`, `commutator_norm_two_point` |
| Modular Hamiltonian and flow | `model.pressing.modular_hamiltonian`, `modular_frequency`, `modular_flow_bloch` |
| Unruh temperature | `model.pressing.unruh_temperature` |

## 8. What was deliberately not encoded

- The metaphysics of “no key” and “all pressing is mutual.”
- The claim that the arrow of time is “in the reader.”
- The claim that conformal time is a “total phase” or that the count of presses
  is bounded.
- The claim that space is “the statistic of what has become one.”
- The Rovelli attribution for the 2024 critique.
- The claim that our universe is exactly de Sitter.
- Any derivation of the baryon-to-photon ratio.
- Any claim that the toys establish a metaphysical thesis.

## 9. Verification

```bash
python -m pytest tests/test_pressing.py -q
python -m pytest tests -q --cov-fail-under=90
ruff check .
black --check model cli.py validate_claims.py tests examples
mypy model cli.py
python validate_claims.py
```

The pressing tests check normalization, conditional slices, the GPS drift
components and detune, the de Sitter strip and proper-time divergence, the Connes
two-point distance and commutator norm, the modular Hamiltonian and flow, and
the Unruh temperature.

## 10. References

- D. N. Page and W. K. Wootters, “Evolution without evolution: Dynamics
  described by stationary observables,” *Phys. Rev. D* **27**, 2885 (1983).
- E. Moreva et al., “Time from quantum entanglement: An experimental
  illustration,” *Phys. Rev. A* **89**, 052122 (2014); arXiv:1311.2833.
- N. Ashby, “Relativity in the Global Positioning System,” *Living Reviews in
  Relativity* **6**, 1 (2003).
- A. Connes and C. Rovelli, “Von Neumann algebra automorphisms and
  time-thermodynamics relation without a global quantum description,”
  *Classical and Quantum Gravity* **11**, 2899 (1994); arXiv:gr-qc/9406019.
- E. Y. S. Chua, “The Time in Thermal Time,” arXiv:2407.18948 (2024).
- N. Swanson, “Can Quantum Thermodynamics Save Time?”, PhilSci-Archive (2018).
- J. J. Bisognano and E. H. Wichmann, “On the duality condition for a Hermitian
  scalar field,” *J. Math. Phys.* **16**, 985 (1975).
- W. G. Unruh, “Notes on black-hole evaporation,” *Phys. Rev. D* **14**, 870
  (1976).
- A. Connes, *Noncommutative Geometry* (Academic Press, 1994).
- M. F. Atiyah and I. M. Singer, “The index of elliptic operators I,” *Ann. of
  Math.* **87**, 484 (1968).
- Planck Collaboration, “Planck 2018 results VI: Cosmological parameters,”
  *Astron. Astrophys.* **641**, A6 (2020).
