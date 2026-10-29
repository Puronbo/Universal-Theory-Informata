# RUBBER-BALL CALIBRATION — Photon-Sized Rubber Ball Physics

> Source: `Puronbo/Photon-Rubber-Ball-Research` (GitHub, 2026).

---

## 1. What it is

Physics research on a photon-sized rubber ball: r = 275 nm, E = 50 MPa,
ν = 0.5, mass 9.6e-17 kg. One solid object where impact, Mie scattering,
thermal motion, and relativistic recoil act at intermediate (5-100) micron-Hertz
scales. Independently re-verified; discrepancies cataloged in `CORRIGENDUM.md`
(never silently fixed). 58 assert-style checks, exit 0.

Key verified numbers:
- mass M = 9.583e-17 kg
- E*, E*_two = 66.7 / 33.3 MPa
- Hertz d_max / P_max (rigid plane) = 5.807 nm / 20.63 nN
- compliant plane d / P = 7.662 nm / 15.63 nN
- thermal speed sqrt(3kT/m) = 11.4 mm/s
- Mie Qe = Qs (x=π, m=1.5+0i) = 3.4822
- melting shift = 0.661 K

**Honest audit:** the "comparable energies" abstract claim is **false** (~37 orders
of magnitude apart). What survives: per-photon recoil KE ~ ball zeropoint (9.9x),
JKR adhesion >> kT (6.3e5x), trap contraction 0.22 nm = 6.4x trap thermal RMS.

---

## 2. Mapping to our model

| Rubber-ball concept | Our construct | Alignment |
|---|---|---|
| Photon-sized ball (275 nm) | Equator of scale (A9.1, 10^-4.5 m) | Sits at the biological/quantum midpoint |
| Contact surface (Hertz) | Contact surface defines unit (A3.1) | Particle = contact with vacuum |
| Mie scattering (Q=3.48 at x=π) | Crease/resonance (A5.2, universal impedance) | Resonance at a boundary |
| Thermal motion (11.4 mm/s) | Erosion (A7.4), canvas boiling (A2.1) | Thermal noise = slow erosion |
| Relativistic recoil | Lorentz transformation (A2.4) | Motion on the canvas |
| Honest audit (CORRIGENDUM) | validate_claims.py, honest-audit discipline | Never silently fix errors |
| Law Apprehension of Works (A0-F1) | Proven vs. conjecture labels | Epistemic status tracking |
| Formal axioms (A–G) | Our axiom set (A0–A12) | Minimal axiom skeleton |

---

## 3. What it adds

- **A concrete mesoscale object:** the rubber ball sits at the equator of scale
  (A9.1), bridging quantum and cosmic. It's a real, measurable thing at the
  midpoint where our model says information hardens into matter.
- **Hertz contact mechanics:** a computable formula for contact surface deformation
  (A3.1) — the "contact surface defines the unit."
- **Mie scattering resonance:** a verified resonance (Q=3.48 at x=π) at a boundary
  — connects to universal impedance (L.O.R.E.) and crease (Folding-Calculus).
- **Honest-audit methodology:** the CORRIGENDUM approach (never silently fix,
  catalog all errors) is the gold standard for our `validate_claims.py`.
- **Law Apprehension of Works:** a framework for mapping proven vs. conjecture
  nodes (A0–F1) — could be adopted for our axiom epistemic tracking.

---

## 4. Recommended additions

1. **Add `hertz_contact(R, E_star, P)` to engine** — contact radius and indentation.
2. **Add `thermal_speed(m, T)` to engine** — sqrt(3kT/m).
3. **Adopt CORRIGENDUM-style error tracking** — never silently fix; catalog in a file.
4. **Add Lean theorem for Hertz formula** — `native_decide` on a numeric example.

---

## 5. Sources

- Repo: `Puronbo/Photon-Rubber-Ball-Research` (GitHub, 2026).
- `Photon_Rubber_Ball_PAPER.pdf`, `CORRIGENDUM.md`, `CLAIM_REGISTER.md`.
- Cross-reference: `FOLDING_CALIBRATION.md`, `LORE_CALIBRATION.md`, `EQUATOR` (A9).
