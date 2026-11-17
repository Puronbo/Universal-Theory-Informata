# The Vacuum as a Holder of Information

> **Source:** the “nothing as a holder of information or bits” exchange
> (2026-11-14), following the barrier, sandpile, and Great Attractor
> discussion.
> **Status:** audit and formal bookkeeping. The bounds below are standard
> physics; the relational reading is an interpretation. The checkable residue
> is in `model/vacuum_info.py`.

## 1. Verdict

Literal nothing has one state and no distinctions:

\[
d=1 \quad\Longrightarrow\quad I=\log_2 d=0\ \text{bits}.
\]

The moment “nothing” holds a bit it has acquired at least two distinguishable
states, and then it is a vacuum, a horizon, a constraint, or a code — not an
absence. The precise claim is therefore:

> Nothing does not store bits. It partitions, bounds, protects, correlates,
> constrains, and requires a decoder. The bits are in the differences across the
> cut; the holder is the structure of the cut.

## 2. Five senses of nothing

| Sense | What it is | Information capacity |
|---|---|---|
| Ontological nothing | No degrees of freedom | \(0\) bits |
| Physical vacuum | Ground state of quantum fields | Entanglement, area-law correlations |
| Horizon nothing | Region beyond a causal boundary | Holographic entropy \(A/(4\ell_P^2)\) |
| Code nothing | Logical zero state of a code | Information in the code subspace, not the zero state |
| Cosmological nothing | No-boundary condition | Information in the wavefunction or constraint |

Only the first is literal nothing. The rest are “empty” in the sense of having
no particles or no access, not in the sense of having no structure.

## 3. The six jobs

| Operation | Mechanism | What it produces |
|---|---|---|
| **Partition** | A cut divides the whole into subsystems | Reduced states and entanglement |
| **Bound** | A horizon or energy limits capacity | Finite bit capacity |
| **Protect** | A gap or barrier suppresses erasure | Metastable distinctions |
| **Correlate** | Entanglement links subsystems | Nonlocal information |
| **Constrain** | A global constraint selects allowed states | A code subspace |
| **Decode** | Measurement plus a classical channel | Accessible bits |

### Partition

A global pure state has \(S(\rho)=0\). Draw a cut, and the reduced state on one
side is mixed:

\[
S(\rho_A)=-\operatorname{Tr}\rho_A\ln\rho_A.
\]

The vacuum’s information is not in the void between the two sides. It is in the
correlations across the cut. This is why the vacuum can look empty and still be
entangled: the whole is pure, the parts are mixed.

### Bound

A horizon puts a finite ceiling on how many bits a region can hold:

\[
I\le\frac{A}{4\ell_P^2\ln 2}.
\]

The Bekenstein bound adds the energy cost:

\[
I\le\frac{2\pi R E}{\hbar c\ln 2}.
\]

If \(E=0\), the bound allows no bits. A region with no energy, no boundary, and
no constraint has no capacity.

### Protect

A bit is a distinction that survives noise. In the simplest account, protecting
it needs three things: at least two states, an energy gap or barrier between
them, and a lifetime longer than the decoherence/erasure time:

\[
E_{\text{gap}}>k_BT.
\]

Landauer’s principle sets the erasure cost \(E=k_BT\ln 2\). For an accelerated
observer the vacuum’s noise floor is the Unruh temperature
\(T_U=\hbar a/(2\pi c k_B)\). A gap is sufficient but not necessary: topological
or error-correcting encodings can trade the gap for a protection symmetry, but
some isolation from the environment is always required. A gapless, unprotected
vacuum erases bits; a gapped or protected vacuum can hold them.

### Correlate

Entanglement stores information nonlocally:

\[
I(A:B)=S(A)+S(B)-S(AB).
\]

For a pure global state \(S(A)=S(B)\), so \(I(A:B)=2S(A)\). The correlations are
a resource, not a transmitter: a local operation on one side cannot change the
other side’s marginal statistics.

### Constrain

A global constraint — the Page–Wootters constraint, a Gauss law, the no-boundary
condition — selects a subspace of allowed states. The constraint does not store
bits. It defines which distinctions are allowed.

### Decode

Nothing decodes itself. An observer with a measurement basis and a classical
channel does. Without a decoder the vacuum is a correlation without an address.

## 4. The bounds, quantitatively

| Quantity | Formula | Code |
|---|---|---|
| Bekenstein bit bound | \(2\pi R E/(\hbar c\ln 2)\) | `bekenstein_bits` |
| Holographic bit bound | \(A/(4\ell_P^2\ln 2)\) | `holographic_bits` |
| de Sitter radius | \(R_H=c/H\) | `desitter_horizon_radius` |
| de Sitter capacity | \(4\pi R_H^2/(4\ell_P^2\ln 2)\) | `desitter_bits` |
| Landauer erasure | \(k_BT\ln 2\) | `landauer_energy` |
| Two-mode squeezing | \(\bar n=\sinh^2 r\) | `two_mode_squeezing_photon_number` |
| Squeezed-state mutual information | \(2S/\ln 2\) bits | `two_mode_mutual_information` |

One Planck area carries

\[
\frac{1}{4\ln 2}\approx0.3607\ \text{bits}.
\]

For the observed Hubble scale, \(H_0\approx70\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\)
gives \(R_H\approx1.3\times10^{26}\ \mathrm{m}\) and a horizon capacity of
order \(10^{122}\) bits (about \(3\times10^{122}\) bits, or \(2\times10^{122}\)
nats of entropy). The number is a capacity, not a count of stored messages.

## 5. Capacity is not a guarantee

These bounds say what a region **may** hold, not what it **does** hold:

- The Bekenstein bound is zero when the energy is zero.
- The holographic bound is an upper bound on entropy, not a construction.
- A horizon entropy is not readable by an observer inside the horizon.
- The bounds do not create information; unitarity and no-cloning still hold.
- Entanglement is not a signal; a classical channel is still required.

The same caveat applies to the barrier imagery: a horizon explains capacity and
protection, not why there is a universe to bound.

## 6. The two-mode vacuum toy

A two-mode squeezed vacuum has mean photon number per mode

\[
\bar n=\sinh^2 r,
\]

one-mode entropy

\[
S=(\bar n+1)\ln(\bar n+1)-\bar n\ln\bar n,
\]

and, because the global state is pure,

\[
I(A:B)=2S\quad\text{nats}=\frac{2S}{\ln 2}\ \text{bits}.
\]

At \(r=0\) the state is the vacuum and \(I=0\): no squeezing, no entanglement, no
bits. This is the quantitative form of “the vacuum holds correlations only when
there is a partition.”

## 7. No-signaling

For a bipartite pure state, a local unitary \(U_A\otimes I\) changes the joint
state but leaves the marginal on \(B\) unchanged:

\[
\rho_B'=\operatorname{Tr}_A\bigl[(U_A\otimes I)\rho(U_A^\dagger\otimes I)\bigr]
=\operatorname{Tr}_A\rho=\rho_B.
\]

The functions `apply_local_unitary` and `marginal_probabilities` implement this
on row-major bipartite states. The tests verify it for the Bell state and for a
partially entangled state, with \(X\), \(Y\), and \(Z\) gates on either side.
The joint state moves; the marginal does not. That is the difference between
correlation and communication.

## 8. Sandpile and Great Attractor reading

In the sandpile image, the void between grains is a **partition**, not a
container. The stable configuration stores the history of avalanches; the
avalanches release it. The table is the boundary condition that makes a
stationary pile possible.

In the cosmic-web image, the Great Attractor is a fold in the table, not the
table. The information is in the density field and the gravitational potential,
not in the low-density void between filaments. If a horizon exists, the horizon
is the holder; if not, the correlations among the grains are.

## 9. What is deliberately not claimed

- That the vacuum is a classical storage medium.
- That entanglement permits faster-than-light signaling.
- That the bounds explain the origin of the universe or of the vacuum.
- That horizon entropy is directly readable.
- That “nothing” is a substance or an independent container.

The bounds describe capacity and protection. They do not supply an origin.

## 10. Mapping to code

| Theme | Module / function |
|---|---|
| Bekenstein bound | `model.vacuum_info.bekenstein_bits` |
| Holographic bound | `model.vacuum_info.holographic_bits` |
| de Sitter horizon | `model.vacuum_info.desitter_horizon_radius`, `desitter_bits` |
| Landauer cost | `model.vacuum_info.landauer_energy` |
| Squeezed vacuum | `model.vacuum_info.two_mode_squeezing_photon_number` |
| Entanglement entropy | `model.vacuum_info.two_mode_mutual_information` |
| Local unitaries | `model.vacuum_info.apply_local_unitary` |
| Marginals | `model.vacuum_info.marginal_probabilities` |
| Constants | `model.vacuum_info.BITS_PER_NAT`, `PLANCK_LENGTH` |

`BOLTZMANN` comes from `model.pressing`; `REDUCED_PLANCK` and `SPEED_OF_LIGHT`
come from `model.spacebar`. They are not redefined here.

## 11. Verification

```bash
python -m pytest tests/test_vacuum_info.py -q
python -m pytest tests -q --cov-fail-under=90
ruff check .
black --check model cli.py validate_claims.py tests examples
mypy model cli.py
python validate_claims.py
```

The tests check the zero limits, linear scalings, the Planck-area value, the
de Sitter capacity at the observed Hubble scale, Landauer at room temperature,
squeezing entanglement and its \(r\to0\) limit, the Bell-state marginals, local
unitary composition, no-signaling on both sides, and every validation error.

## 12. References

- Bekenstein, J. D. (1981). “Universal upper bound on the entropy-to-energy ratio for bounded systems.” *Phys. Rev. D* 23, 287.
- ’t Hooft, G. (1993). “Dimensional reduction in quantum gravity.” arXiv:gr-qc/9310026.
- Gibbons, G. W., and Hawking, S. W. (1977). “Cosmological event horizons, thermodynamics, and particle creation.” *Phys. Rev. D* 15, 2738.
- Landauer, R. (1961). “Irreversibility and heat generation in the computing process.” *IBM J. Res. Dev.* 5, 183.
- Unruh, W. G. (1976). “Notes on black-hole evaporation.” *Phys. Rev. D* 14, 870.
- Weedbrook, C. et al. (2012). “Gaussian quantum information.” *Rev. Mod. Phys.* 84, 621.
- No-communication theorem: <https://en.wikipedia.org/wiki/No-communication_theorem>
