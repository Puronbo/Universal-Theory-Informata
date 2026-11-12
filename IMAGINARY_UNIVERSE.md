# Imaginary Math Universe — Integration and Audit

> **Source:** `Imaginary Math Universe Analysis.docx` (received 2026-11-12).
> **Status:** external critique and repair notes, not an axiom set and not
> evidence. The source is quoted only where it states a checkable mathematical
> or physical fact.

## 1. Verdict

The source is strongest when it corrects the original "imaginary universe"
draft. It is weakest when it treats a metaphor as a mechanism. The integration
therefore keeps two rigorous structures and quarantines the rest:

| Kept | Why |
|---|---|
| Complex amplitude, hidden phase, observable modulus | Standard complex arithmetic and the Born rule |
| Liouvillian `L_H(A) = [H, A]`, zero modes = commutant | Standard finite-dimensional linear algebra |

Everything else is labelled as analogy, candidate, or rejected. No new
physical claim is introduced.

## 2. Claim ledger

| Source claim | Status | Where it lives |
|---|---|---|
| `1 / 0` yields infinitely many answers | **Rejected as stated.** `1 / 0` is undefined in the complex field; near a pole the limit is path-dependent. On the Riemann sphere, `1 / 0 = infinity` as one compactified point. | `model.mobius` models inversion and poles; `model.antithesis` models one-way limits |
| The imaginary part is physically active but hidden | **Grounded.** A complex wave carries phase; intensity is `|psi|^2`. | `model.phase`: `intensity`, `phase_angle`, `wave_sample` |
| Photon wavelength is "imaginary height" | **Corrected.** Wavelength is a real spatial period; phase is the imaginary coordinate conjugate to the real oscillation. | `model.phase`: `wavenumber_from_wavelength`, `phase_factor`, `imaginary_height` |
| The vacuum is a perfect mirror | **Corrected.** The vacuum reacts without net cost; a ledger is a better metaphor than a mirror. | `model.antithesis` (entropy), `model.ternary` (net zero) |
| The hidden register is exhausted energy | **Analogy.** Entropy is unavailable energy, not a literal registry. | `model.antithesis.entropy`, `model.clock.entropy_brake` |
| Zeta zeros are the architecture | **Candidate only.** The Hilbert–Pólya spectral programme is real research, not a derivation of physics. | `model.prized_problems.zeta_partial` is numerical evidence only |
| `26` dimensions or registers | **Not derived.** Bosonic string theory uses 26 dimensions; the Standard Model has roughly 26 free parameters. Neither is a prediction of this framework. | `model.duality`, `model.lattice` are taxonomies, not physics |
| "Self-adjoint operator for self-adjoint operators" | **Grounded as linear algebra.** The Liouvillian is self-adjoint under the Hilbert–Schmidt product, and its kernel is the commutant. | `model.superoperator`: `liouvillian`, `zero_mode_pairs`, `commutant_dimension` |
| Zero creates one | **Rejected as a mechanism.** Zero is a reference frame. Set theory contains zero; QFT excites the vacuum; cosmology borrows a fluctuation. | `model.ternary.VOID`, `model.duality`, `model.mobius` |
| A four-step master cycle | **Not integrated.** It has no failure state and no measurable prediction. | None; recorded here as poetry |
| DNA is a binary code | **Corrected.** DNA is quaternary (`A/T/C/G`) read in triplets, with error correction. | None; biology is outside the engine |
| CPT is a perfect mirror | **Grounded, with one crack.** CPT is exact; CP is violated in the weak sector, and the baryon residual is why structure survives. | `model.clock.cp_violation_tilt` is a schematic tilt, not a derivation |
| Holography, quantum error correction, decoherence | **Real research programmes.** They are analogies for the framework, not consequences of it. | `CONNECTIONS.md` rows; no dedicated engine module |

## 3. What was added

### 3.1 `model.phase`

Standard complex arithmetic for the "visible front / hidden back" language:

- `wave_sample(amplitude, k, x, omega, t)` returns the complex sample, its
  intensity `|amplitude|^2`, and its phase.
- `phase_factor` is the unit phase `exp(i(kx - omega t))`.
- `wavenumber_from_wavelength` and `wavelength_from_wavenumber` are exact
  round-trip helpers.
- `rotate_quarter_turn` is multiplication by `i`; `conjugate` cancels the
  imaginary part; `real_width` and `imaginary_height` expose the two axes.

This is the corrected version of "photon wavelength as imaginary height":
wavelength is real width, phase is imaginary height, and observation sees the
modulus.

### 3.2 `model.superoperator`

Finite-dimensional matrices of complex numbers, with no third-party
dependencies:

- `commutator` / `liouvillian` implement `[H, A] = H A - A H`.
- `hilbert_schmidt`, `dagger`, and `is_self_adjoint` make the self-adjointness
  statement checkable.
- `liouvillian_eigenvalues` returns the transition frequencies `E_m - E_n`.
- `zero_mode_pairs` and `commutant_dimension` describe the kernel: the
  observables that commute with `H`.

The zero-mode identity is the rigorous version of "the void observing itself":
what survives the operator acting on its own algebra is the commutant, not a
mystical residue.

## 4. Mapping to existing modules

| Source theme | Existing module |
|---|---|
| Reciprocal involution and poles | `model.mobius`, `model.antithesis`, `model.fold` |
| Duality and pole strings | `model.duality`, `model.lattice` |
| Net-zero / ternary bookkeeping | `model.ternary` |
| Entropy and information loss | `model.antithesis`, `model.clock` |
| Zeta numerical evidence | `model.prized_problems` |
| UV/IR and cosmic loop | `model.self_looping` |
| CP tilt and the broken mirror | `model.clock` |
| Hidden phase and intensity | `model.phase` (new) |
| Operator-for-operators | `model.superoperator` (new) |

## 5. What is deliberately not integrated

- The four-step "curiosity → fold → projection → result" cycle as a physical
  process.
- Any claim that zero is an agent or that the universe "wants" to observe
  itself.
- The `26` register count as a derivation. It is a coincidence between bosonic
  string theory, Standard-Model parameter counting, and the source's symbolic
  alphabet.
- "Division by zero gives infinitely many answers" as arithmetic. The
  path-dependent limit is the defensible statement.
- DNA as a binary code. It is a quaternary code with triplet codons.
- The claim that holography, AdS/CFT, or TQFT validates the framework
  retroactively. Those fields make their own predictions; they do not confirm
  this model.

## 6. Verification

```bash
python -m pytest tests/test_phase.py tests/test_superoperator.py -q
python -m pytest tests -q --cov-fail-under=90
ruff check .
black --check model cli.py validate_claims.py tests examples
mypy model cli.py
python validate_claims.py
cd lean && lake build
```

The tests check unit-modulus phases, global-phase invariance of intensity,
quarter-turn order four, Liouvillian self-adjointness under the
Hilbert–Schmidt product, zero-mode/commutant dimensions, and input validation.

## 7. Open questions

1. Can the phase layer be tied to the existing `impedance` complex response
   without turning the analogy into a claim?
2. Is there a useful finite-dimensional model of the commutant tower
   `L_H`, `L_{L_H}`, ... that stays within the standard library?
3. Which parts of the source's vacuum-ledger language survive contact with the
   existing entropy brake, and which are only metaphor?
4. Should the `26` coincidence be recorded as a numerical curiosity or removed
   from the framework's vocabulary entirely?

These are design questions, not results.

## 8. References

- Born rule and complex amplitudes: <https://en.wikipedia.org/wiki/Born_rule>
- Riemann sphere and the point at infinity: <https://en.wikipedia.org/wiki/Riemann_sphere>
- Quantum vacuum state: <https://en.wikipedia.org/wiki/Quantum_vacuum_state>
- Hilbert–Pólya conjecture: <https://en.wikipedia.org/wiki/Hilbert%E2%80%93P%C3%B3lya_conjecture>
- Holographic principle: <https://en.wikipedia.org/wiki/Holographic_principle>
- CPT symmetry: <https://en.wikipedia.org/wiki/CPT_symmetry>
- Baryon asymmetry: <https://en.wikipedia.org/wiki/Baryon_asymmetry>
