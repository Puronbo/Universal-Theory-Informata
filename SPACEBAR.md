# The Spacebar's Parameter — What a Real Argument Can Be

> **Source:** the becoming-one passage's closing line, "there was never a
> finger on the spacebar" (received 2026-11-13).
> **Status:** formal bookkeeping. This memo enumerates the candidate
> parameters of the press and separates the checkable ones from the metaphor.

## 1. Verdict

If the spacebar is an operator that advances "now," then its press is

\[
U(\theta)=e^{-i\theta}.
\]

The question "what real parameter would it take?" has a precise answer with a
precise catch:

- The **physical** parameter is a phase, \(\theta=S/\hbar\), and a phase lives
  on a circle, not on the real line.
- A real number is a **lift** of that circle. The natural lift is proper time
  \(\tau\), and one full press is the Compton period
  \(T_C=2\pi\hbar/(mc^2)\).
- A single real parameter is only scale-free if it is the dimensionless phase,
  equivalently the count \(n=\tau/T_C\). A dimensionful \(\tau\) needs a mass
  to become a phase, and a freely chosen mass is exactly the "finger" the
  passage denies.
- A **free** real parameter is therefore rejected: it relocates the finger
  rather than removing it.

## 2. The press

For a Hamiltonian \(H\),

\[
U(\tau)=e^{-iH\tau/\hbar}.
\]

For a free particle at rest, \(H=mc^2\), so

\[
U(\tau)=e^{-i\,mc^2\tau/\hbar}
=e^{-2\pi i n},\qquad
n=\frac{\tau}{T_C},\qquad
T_C=\frac{2\pi\hbar}{mc^2}.
\]

A larger mass gives a shorter period, hence a faster rest-frame clock. The
proton's period is shorter than the electron's by \(m_p/m_e\approx1836\).

A real \(\theta\) gives \(|U|=1\): the press is unitary, and the clock ticks.
An imaginary \(\theta\) gives a real exponential: after the standard Wick
rotation \(\tau=-i\hbar\beta\), the operator is \(e^{-\beta H}\), a thermal
weight. A complex \(\theta\) does both. So the requirement that the parameter
be **real** is exactly the requirement that the press be a clock rather than a
cooling or heating operator.

## 3. Every candidate

| Candidate | Domain | Status | Why |
|---|---|---|---|
| Proper time \(\tau\) | real, dimensionful | **physical** | A lift of the phase; needs a mass/clock to fix the phase |
| Phase \(\theta=S/\hbar\) | circle (mod \(2\pi\)) | **fundamental** | Real \(\theta\) is unitary |
| Tick count \(n=\tau/T_C\) | real (mod 1) | **fundamental** | The scale-free real coordinate of the phase |
| Affine parameter \(\lambda\) | real | **gauge** | Reparametrization label; not observable |
| Mass \(m\) | positive real | **fixed** | Eigenvalue of \(p^2=m^2c^2\), not a knob |
| Baryon asymmetry \(\eta\) | positive real | **measured** | \(\eta\approx 6.1\times10^{-10}\); the passage's "one part in a billion" |
| Imaginary time \(i\beta\) | imaginary | **thermal** | Gives \(e^{-\beta H}\), not a phase |
| Complex time | complex | **non-unitary** | Oscillation plus decay or growth |
| Free knob \(\varepsilon\) | real | **rejected** | A freely chosen parameter is the finger |

The catalog is implemented in `model.spacebar.candidate_parameters` and the
test file asserts that every status is represented.

## 4. The no-finger argument

The worldline action is

\[
S=-mc^2\int d\tau.
\]

The phase is \(\theta=-S/\hbar\), and the mass-shell constraint

\[
p_\mu p^\mu=m^2c^2
\]

is the generator of proper-time reparametrizations. So \(m^2\) is the conserved
value of the constraint, not a free input.

A dimensionful proper time therefore cannot determine the press by itself:
the same \(\tau\) gives different phases for an electron and a proton. The
tests check this directly. What removes the ambiguity is the dimensionless
phase, equivalently the ratio \(\tau/T_C\). The tick count is its scale-free
real coordinate; a dimensionful \(\tau\) alone needs a second, freely chosen
scale.

This is the precise content of "no finger": the admissible parameter is an
eigenvalue fixed by a constraint, or a dimensionless count. A knob that can be
set to any real value is the finger.

## 5. The one measured number

If the spacebar means the first deviation that produced the universe, the
passage supplies an empirical candidate: the baryon-to-photon ratio

\[
\eta\approx 6.1\times10^{-10}.
\]

It is real, dimensionless, and measured. It is not derived here, and this
memo does not claim that it is the spacebar's parameter. It is simply the only
number in the passage's closing sentence that can be checked against data.

## 6. What is deliberately not taken

- A **freely chosen** real parameter. That is the finger.
- A **dimensionful** parameter without a clock. Proper time alone does not fix
  a phase.
- A **complex** parameter as a clock. Complex time is not unitary.
- The claim that the baryon asymmetry is derived from the framework. It is
  measured, and the mechanism that produces it is a separate question.
- The claim that the metaphor is a physical theory. It is a bookkeeping device
  for the operator's argument.

## 7. Mapping to code

| Theme | Module / function |
|---|---|
| Compton clock | `model.spacebar.compton_period`, `compton_frequency` |
| Action and phase | `model.spacebar.action_from_proper_time`, `phase_from_action` |
| Tick count | `model.spacebar.ticks_from_proper_time`, `wrap_ticks` |
| The press | `model.spacebar.spacebar_from_ticks`, `spacebar_from_proper_time` |
| Imaginary time | `model.spacebar.thermal_weight` |
| Mass shell | `model.spacebar.mass_shell_residual`, `is_on_mass_shell` |
| Candidate catalog | `model.spacebar.candidate_parameters` |

## 8. Verification

```bash
python -m pytest tests/test_spacebar.py -q
python -m pytest tests -q --cov-fail-under=90
ruff check .
black --check model cli.py validate_claims.py tests examples
mypy model cli.py
python validate_claims.py
```

The tests check unitarity, the group law, periodicity, the electron Compton
period, the electron/proton phase difference at fixed proper time, the thermal
companion, the mass shell at rest and in motion, and the full candidate
catalog.

## 9. References

- Compton wavelength: <https://en.wikipedia.org/wiki/Compton_wavelength>
- Unitarity: <https://en.wikipedia.org/wiki/Unitary_operator>
- Wick rotation: <https://en.wikipedia.org/wiki/Wick_rotation>
- Mass shell: <https://en.wikipedia.org/wiki/On_shell_and_off_shell>
- Baryon asymmetry: <https://en.wikipedia.org/wiki/Baryon_asymmetry>
