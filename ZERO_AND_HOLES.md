# Zero, Indeterminacy, and Holes

> **Source:** the “what does zero do”, \(0/0\), inward-duality, and
> “one piece” exchange (2026-11-16–17), following the vacuum-information
> audit.
> **Status:** audit. The mathematics below is standard and each claim names
> its theorem. The zero/absence and inward/outward readings are interpretation
> and are labelled as such. Nothing here is a physical prediction.

## 1. Verdict

Zero is the element that changes nothing when added and everything when used
as a reference:

\[
a+0=a,\qquad a\cdot 0=0,\qquad d=1 \;\Longrightarrow\; I=\log_2 d=0\ \text{bits}.
\]

It is inert in every operation and universal at every coordinate. The precise
claim is:

> Zero does not act. It makes action measurable. It is the reference, not the
> substance — the first coordinate, not the ground.

The same verdict holds for “nothing”: the hole, the void, and the zero vector
are three different objects, and only the last is a state at all.

## 2. The jobs of zero

| Role | Statement | Setting |
|---|---|---|
| Identity | \(a+0=a\) | any monoid |
| Absorber | \(a\cdot 0=0\) | any ring |
| Origin | \(v=p-o\) | affine geometry |
| Fixed point | the point negation cannot move | symmetry |
| Initial / terminal | unique in, unique out | a category with a zero object |
| Seed | \(0=\varnothing,\;1=\{\varnothing\}\) | set theory |
| Gauge | the choice that carries no physics | field theory |
| Silence | one state, zero bits | information |

Only in a **vector space** do identity, origin, and zero object coincide. In an
affine space the origin is a choice; in **Set** the initial and terminal
objects are distinct; in **Vect** they are the same object. The zero is the
healed split, and which zero you have tells you what kind of structure you are
in.

## 3. \(0/0\) is incomplete, not false

The equation \(0/0=x\) is equivalent to \(0=0\cdot x\), which holds for every
\(x\). It therefore determines nothing. That is underdetermination, not
contradiction.

Three precise resolutions, and they disagree about whether the answer is one
object or many:

| Setting | What \(0/0\) resolves to | Distinguishable values |
|---|---|---|
| Limits | a value depending on the joint rate of vanishing | one per path |
| Blow-up | the exceptional divisor, a projective space of directions | one per direction |
| Conditioning | a family of conditional laws on a null event | one per limiting procedure |
| Wheel algebra | a single absorbing element \(\bot\) | one, absorbing |

**Blow-up.** The map \((x,y)\mapsto[x:y]\in\mathbb{P}^1\) is defined away from
the origin. At the origin it is \(0/0\). Replacing the origin by the
exceptional divisor \(\mathbb{P}^1\) turns one indeterminate point into a
circle of distinct directions. This is a *construction*, not a limit: a
continuous image of a point is a point, so the circle cannot be computed from
the singularity. It is attached.

**Conditioning.** If \(P(N)=Q(N)=0\), the Radon–Nikodym derivative
\(\mathrm{d}P/\mathrm{d}Q\) is unconstrained on \(N\). On the rest of the space
it is fixed; on the common null set it is a free density. The Borel–Kolmogorov
paradox is the standard witness: conditioning a uniform measure on a sphere on
a great circle gives different answers under different limiting procedures.

The corrected statement:

> \(0/0\) is a ratio whose reference has not been chosen. Supply the reference
> and it is a number; withhold it and it is a family.

## 4. A number is a conditioned value

Currying identifies a family with a function into a function space:

\[
C(A\times B,\,C)\;\cong\;C(A,\,C^{B}).
\]

A **number** is the degenerate case \(C(1,\,C)\): a value conditioned on the
one-point space. A conditional law is the general case. The number is the
fiber; the law is the section.

This is not a metaphor; it is how numbers are constructed. A Dedekind cut is a
predicate on the rationals. A Cauchy real is an equivalence class of sequences.
A computable real is a program with a modulus of convergence. A point of a
locale is a frame homomorphism. Each is a rule of resolution, not a simple
object.

The structuralist reading makes the point sharp. Von Neumann’s \(3\) is
\(\{\varnothing,\{\varnothing\},\{\varnothing,\{\varnothing\}\}\}\); Zermelo’s
\(3\) is \(\{\{\{\varnothing\}\}\}\). Both satisfy every theorem of arithmetic
and they have different elements, so no set-theoretic fact chooses between
them (Benacerraf). The number is the **position**, and a position is defined by
its relations.

## 5. The two directions

Every structure has an outward and an inward reading, and they are duals:

| Aspect | Outward | Inward |
|---|---|---|
| set theory | cumulative hierarchy, built upward | the \(\in\)-tree, descending to \(\varnothing\) |
| category | arrows, limits, sections | the opposite category, colimits |
| topology | blow-up: the point becomes a circle | tangent cone: the circle is the point’s interior |
| explanation | causal — what produced it | constitutive — what it is made of |
| knowledge | where it sits | what it is |

Two reversals return the original, \((\mathcal{C}^{\mathrm{op}})^{\mathrm{op}}
=\mathcal{C}\), so the duality is an involution. The objects fixed by it are
self-dual; the **zero object** is one of them. That is why zero keeps
functioning as the hinge: it is the object for which the two directions agree.

Pursued to the end, the inward road delivers the outward one. The Yoneda lemma
gives

\[
X\;\cong\;\operatorname{Hom}(-,\,X),
\]

so an object is determined by the totality of maps into it. The deepest
interior is the exterior. An object’s full inside is what everything else can
do to it.

**Audit of the inward reading.** The inward road descends the \(\in\)-tree and
terminates at \(\varnothing\). The empty set is the base case of the recursion,
not its author. The void is the creature’s foundation; it is not a ground.

## 6. One piece, not simply connected

“One piece” is the weakest and most robust of the connectivity conditions:

| Property | Meaning | Compatible with structure |
|---|---|---|
| Connected | no separation into two disjoint open parts | yes |
| Path-connected | any two points joined by a path | yes |
| Simply connected | every loop contracts | no — holes remain |
| Contractible | collapses to a point | almost never |

So a connected object may still have holes, and the holes are real. The
stratification from the inward reading does not contradict this: by the
frontier condition the closure of each stratum is a union of strata, so the
strata are glued at their seams. A cut that leaves the space connected is a
fold, not a tear.

## 7. What a hole is

Three equivalent definitions:

| Definition | Needs | Answers |
|---|---|---|
| A component of the complement | an ambient space | roughly, where |
| A non-contractible cycle | only the object | that there is a hole |
| A closed form that is not exact | a differential structure | why it obstructs |

Alexander duality makes the first one a theorem. For compact \(K\subset S^n\),

\[
\tilde H_i(K)\;\cong\;\tilde H^{\,n-i-1}(S^n\setminus K).
\]

The holes in the object are dual to the components of what surrounds it. This
is the literal form of “the hole is defined by the cheese”: the hole is
counted by the material around it, not found inside it.

The sharpest statement of what a hole is:

> A hole is a **local triviality that fails globally**.

Every loop is locally contractible; the failure is in the whole. A hole and a
twist are the same phenomenon in different degree — both are local data that
refuse to glue.

**Count and address.** For a closed orientable surface of genus \(g\),

\[
\chi(\Sigma_g)=2-2g,\qquad b_1(\Sigma_g)=2g,
\]

so the colloquial “one hole” of a torus is the genus while the invariant is
twice that. The number depends on what is counted. And no point of the surface
is the hole: homology is global. The hole is real and unlocatable.

**Scale.** Persistent homology makes the reality scale-dependent: each class is
born and dies as the object is thickened, and the barcode length measures
significance. “Is that a hole?” therefore requires a declared resolution —
the same lesson as the gauge and the \(0/0\) reference.

**Physics.** A hole in an ordered medium is a topological defect, classified by
homotopy groups: \(\pi_0\) domain walls, \(\pi_1\) line defects, \(\pi_2\)
monopoles, \(\pi_3\) textures. The defect is stable because no local surgery
can contract the class. It is held by a group, not by a force.

## 8. Redemption is not filling

A hole cannot be removed by filling it; pouring material in destroys the object.
The only topological resolution is to attach a 2-cell along the loop:

\[
[\gamma]\neq 0\;\;\longrightarrow\;\;[\gamma]=\partial(\text{2-cell})=0.
\]

The cycle becomes a boundary. The class is killed by making the loop enclose a
surface, which means embedding the object in a larger space. Stated as an
image, and labelled as an image: the wound is not closed, it is made to bound.

## 9. What is deliberately not claimed

- That \(0/0\) has a value independent of a resolution.
- That the blow-up is the unique resolution of an indeterminacy.
- That a number is “really” a function rather than a position in a structure.
- That the inward road terminates in a ground rather than in a base case.
- That a hole is a substance, a location, or a cause.
- That the topology of finitude explains evil. A hole is an absence of the
  structural kind and is innocent; a will that turns against the good is not a
  hole.
- That the theological readings are more than controlled analogies.

## 10. References

- Benacerraf, P. (1965). “What Numbers Could Not Be.” *Philosophical Review* 74, 47–73.
- Borel, É. (1909); Kolmogorov, A. N. (1933). The Borel–Kolmogorov paradox: <https://en.wikipedia.org/wiki/Borel%E2%80%93Kolmogorov_paradox>
- Carlström, J. (2004). “Wheels — On Division by Zero.” *Mathematical Structures in Computer Science* 14, 143–184.
- Edelsbrunner, H., and Harer, J. (2010). *Computational Topology: An Introduction*. AMS.
- Hartshorne, R. (1977). *Algebraic Geometry*. Springer. (Blow-ups and the exceptional divisor.)
- Hatcher, A. (2002). *Algebraic Topology*. Cambridge. (Alexander duality, attaching cells, homology.)
- Mac Lane, S. (1998). *Categories for the Working Mathematician*. Springer. (Yoneda lemma, opposite category, zero object.)
- Mermin, N. D. (1979). “The topological theory of defects in ordered media.” *Rev. Mod. Phys.* 51, 591.
- Boethius (524). *Consolation of Philosophy*, Book V. (Eternity as *totum simul*.)
