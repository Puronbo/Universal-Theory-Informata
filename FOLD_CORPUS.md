# The Fold corpus: exact core, audit, and integration

This document records the inspection of
[The-Fold](https://github.com/Puronbo/The-Fold) at commit `50b0244`, what of it
is executable here, and what was deliberately left out. The corpus is a separate
paper project by the same author; it is not a dependency of this repository.

The corpus's own epistemic rule is the frame for everything below:

| zone | meaning |
|---|---|
| **exact** | the Fold's object is the problem's object, re-described; the statement can be checked |
| **reformulation** | the problem becomes a statement about the Fold, with nothing proved |
| **rhyme** | the same shape appears, but the objects are different |
| **false friend** | the shape matches and the inference does not; the error to avoid |

A rhyme written as a proof is the one error that matters.

## What is integrated

`model/fold_corpus.py` makes the checkable core executable. It covers:

| construct | function | status |
|---|---|---|
| Homothety `g_k(P) = P0 + k(P - P0)` | `scale_point` | **exact** (definition) |
| Determinant `det(g_k) = k**n` | `scale_determinant` | **exact** (definition) |
| Hyperplane reflection and its matrix | `reflect_point`, `reflection_matrix` | **exact** (standard geometry) |
| Two folds compose to a rotation by twice the crease angle | `compose_reflections`, `two_fold_rotation_angle` | **exact** (standard geometry) |
| Midpoint scale `(1 + k)/2` | `midpoint_scale`, `midpoint_map` | **exact** (algebra) |
| Division point and collapse `k = (t - 1)/t` | `division_point`, `division_collapse_scale` | **exact** (algebra) |
| Projection onto the crease | `projection_onto_crease` | **exact** (standard geometry) |
| Cap/puncture ledger `(chi, boundary, punctures)` | `SurfaceLedger` | **exact** (bookkeeping) |
| Wheel closure and doubling | `wheel_turn`, `wheel_turns`, `doubling_is_bijective`, `doubling_agrees_with_negation` | **exact** (finite arithmetic) |
| Exterior solid angle | `solid_angle_fraction` | **exact** (standard geometry) |
| Schwarzschild radius and `k*` | `schwarzschild_radius`, `horizon_ratio` | **exact** (standard relativity) |

The public names are re-exported from `model/__init__.py`; `tests/test_fold_corpus.py`
has 64 tests and reaches 100% branch coverage of the module. The physics
*readings* are not in the code. The module stops at standard geometry and
arithmetic; `FOLD_CORPUS.md` carries the interpretive status.

## Numbers recomputed

All values below were re-derived independently, not copied from the corpus.

### Solid angle

For an exterior observer at distance `d` from a sphere of radius `r`,

```
Omega/(4*pi) = (1 - sqrt(1 - (r/d)^2)) / 2.
```

At `d = 2.281 r`:

| `r/d` | `Omega/4pi` | corpus |
|---|---|---|
| `1` | `5.061104%` | `5.061%` |
| `1/2` | `1.216026%` | `1.216%` |
| `1/4` | `0.301217%` | `0.301%` |

Inverting the quoted `5.060%` gives `d/r = 2.28124`, so the three rows are
consistent with one distance and ordinary rounding.

### Horizon ratio

```
k* = r_s/R = 2*G*M/(c^2*R)
```

with `G = 6.67430e-11`:

| body | `k*` |
|---|---|
| Earth (`M = 5.972e24`, `R = 6.371e6`) | `1.3922e-9` |
| Sun (`M = 2.0e30`, `R = 6.957e8`) | `4.2697e-6` |
| Sun (`M = 1.988e30`) | `4.2441e-6` |
| 70 kg of water (`R = 0.2556`) | `4.0675e-25` |

The corpus prints `1.392e-9`, `4.245e-6`, and `4.067e-25`. The water row matches
once the sphere's radius is `0.2556` m (the value implied by 70 kg at
`1000 kg/m^3`) rather than the rounded `0.255` m. The Sun's printed `4.245e-6`
and the recomputed `4.2441e-6` differ by `0.02%`, which is the rounding of `G`,
`M`, and `R` in the note; the corpus's own horizon table is internally
consistent. Solar mass is quoted as both `2.0e30` and `1.988e30` in different
notes, which accounts for the `4.2697e-6` row.

### Cube silhouette

Replaying the camera and rotation of `j-collapse-3d.html` at `yaw = 0.55`,
`pitch = 0.34` gives the projected-area fraction of a cube:

| rotation about `y` | fraction |
|---|---|
| `0 deg` | `0.00%` |
| `30 deg` | `1.41%` |
| `45 deg` | `12.33%` |
| `90 deg` | `0.00%` |
| `180 deg` | `0.00%` |
| `270 deg` | `0.00%` |

The paper's `1.4%` and `12.3%` are correct.

### Standard identities

- Bekenstein: `A/(4*l_P^2) = 4*pi*G*M^2/(hbar*c)` holds identically.
- Surface gravity: `kappa = c^4/(4*G*M)`.
- Hawking temperature: `T = hbar*kappa/(2*pi*c*k_B)` matches its closed form.
- Smarr: `kappa*A/(4*pi*G) = M` is exact.
- Midpoint: `(P + g_k P)/2 = g_((1+k)/2) P`.
- Division: the `t`-point is `g_(1-t+t*k) P`, which collapses at `k = (t-1)/t`.
- Pairing: `t` with `1 - t` pairs `k` with `1/k`.

## The zeta and theta notes

The corpus's sharpest structural claim is that the theta modular factor `t^(1/2)`
is the real part of the critical line. The derivation is a **reformulation**:
it identifies the crease, not the zeros. I checked it numerically in an external
`mpmath` session (30-40 decimal digits; not a repository dependency):

- Functional equation and reality: `xi(s) - xi(1-s)` and
  `xi(1-conj(s)) - conj(xi(s))` have residuals of order `1e-31`.
- Theta modular identity `vartheta(1/t) = sqrt(t) vartheta(t)`: residual `0.0`
  at `t = 0.3, 0.7, 1.7, 3.0` with 60 terms.
- Mellin representation `int (vartheta(t)-1)/2 t^(s/2) dt/t =
  pi^(-s/2) Gamma(s/2) zeta(s)`: agrees to `5.4e-24` at `2+3i` and `4.8e-17`
  at `1.7+2.3i`.
- The first five nontrivial zeros have real part `1/2` and `|zeta|` of order
  `1e-30` at 30 digits. This is a numerical check, not a proof of the Riemann
  hypothesis.
- The explicit formula for `psi(20)` converges slowly: truncating at 10 zeros
  leaves an error of `0.49`; at 50 zeros `-0.081`; at 100 `-0.056`; at 200
  `-0.0032`. The corpus does not claim a rate, and none should be inferred from
  these four rows.

The note's own conclusion is the correct one: the theta fold gives the axis
`1/2`, not the zeros. The "primes are an illusion generated by the zeros" line
is a **rhyme**, and it is quarantined as such.

## The calendar note

`Fold/Arithmetic.lean` is exact finite arithmetic:

| statement | check |
|---|---|
| Four date spellings congruent modulo `99` | all `= 56` |
| Gregorian cycle | `146097 = 27 * 7 * 773` |
| Unix epoch as whole weeks | `972518400 = 1608 * 604800` |
| Weekday residue | `1608 % 7 = 5`, `2451844 % 7 = 3` |
| `2000-10-26` | Thursday, `11256` days after `1970-01-01`, `1608` weeks |

The arithmetic is **exact**. The reading of the date as a code is a separate
**rhyme** and is not part of this integration.

## Negative and partial results

- The theta derivation does not prove the Riemann hypothesis. It supplies the
  critical line as a crease and a dictionary between primes and zeros.
- The explicit formula is truncated in every numerical check; the truncation
  error is visible and is not a convergence proof.
- The corpus's "primes are an illusion" and "the horizon is an observer" lines
  are rhymes. They are recorded as interpretive, not as results.
- The calendar's modular coincidences are exact computations; they do not
  establish that the date encodes anything.

## Upstream fixes

The inspection found two real defects in The-Fold; both are fixed in the local
clone but not committed there (commit/push is the author's call):

1. **`check.py` needed an undeclared `pypdf`.** The PDF stores its page
   dictionaries in compressed object streams, so the old byte-scan fallback
   found zero pages and the gate failed on a clean clone. The fallback now
   inflates FlateDecode streams with the standard-library `zlib` and counts
   `/Type /Page` there. `python check.py` passes without any third-party
   package.
2. **`Fold/Doubling.lean` overstated its theorem.** `double_eq_neg_iff` states
   `n ∣ 3`, which includes the trivial `n = 1`, but the header and the theorem
   docstring said "only at `n = 3`". Both now say "exactly when `n` divides
   `3`: trivially at `n = 1`, non-trivially at `n = 3`". The
   `the-fold-lean.md` table row was corrected the same way.
3. **`Fold/Examples.lean` had a stale header.** It said "Two finite checks"
   while the file also contains the monodromy passport and the `A1` node
   quotient. The header now lists all four.
4. **No cross-link between the repositories.** The Fold README now points here,
   and this document points back to `Fold/Basic.lean`, `Fold/Chi.lean`,
   `Fold/Doubling.lean`, and `Fold/Arithmetic.lean`.

The audits found no mathematical error in the corpus. The Lean core builds
cleanly (13 jobs, 100 theorems and lemmas, no `sorry`, `admit`, or `axiom`;
imports only `Init`), and `fold_lint.py` reports 0 errors and 0 warnings across
49 documents.

## Cross-repository map

| The-Fold | this repository |
|---|---|
| `Fold.Basic.Fold`, `Fold.Basic.desc_bijective` | `model/fold.py` (`fold`, `fold_preimages`, `representative`) |
| `Fold.Basic.Orbit` | `model/fold_corpus.py` (`fold_orbit`) |
| `Fold.Basic` cut and lift | `projection_onto_crease` |
| `Fold.Chi` cap/puncture | `SurfaceLedger` |
| `Fold.Doubling` | `doubling_is_bijective`, `doubling_agrees_with_negation`, `wheel_turn`, `wheel_turns` |
| paper solid angle and `k*` | `solid_angle_fraction`, `schwarzschild_radius`, `horizon_ratio` |
| `Fold.Arithmetic` | audited here; not re-implemented (pure finite arithmetic) |
| theta/Mellin and zeta notes | audited here; not re-implemented (numerical, not exact) |

`model/fold.py` is the executable instance of the Joukowski quotient
`J(z) = z + 1/z` named in `Fold/Basic.lean`; `model/fold_corpus.py` supplies the
homothety and closure layer around it. The abstract structure and its executable
instance now point at each other.

## Reproduce

```bash
python -m pytest tests/test_fold_corpus.py -q
python examples/fold_corpus.py
```

In the The-Fold checkout:

```bash
python check.py
python fold_lint.py
python fold_lint.py zones
python fold_lint.py selftest
lake build
```
