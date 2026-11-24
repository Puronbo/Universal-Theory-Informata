# Puncture or Hole? A Resolution Test for the Cap/Puncture Ledger

> **Source:** the cap/puncture ledger of `model.fold_corpus.SurfaceLedger`, tested
> against the lattice module `model.grid_topology.py` (2026-11-19).
> **Status:** measurement report. The ledger is exact in the continuum. On a
> finite cell complex the puncture is not an object: removing a cell creates a
> boundary, so every lattice hole is a small annulus. The puncture survives only
> as a hole whose inradius is one lattice step. The checkable residue is in
> `model/grid_topology.py`, `tests/test_grid_topology.py`, and
> `examples/grid_topology.py`.

## 1. What was proposed

The Fold corpus tracks three invariants, not one:

```text
(chi, boundary, punctures)
```

Capping a boundary raises `chi` and consumes a boundary component. Puncturing
lowers `chi` and adds a puncture. On `chi` alone the two operations cancel; on
the triple they do not. `SurfaceLedger` implements the bookkeeping, and it is
exact.

The testable question is what happens when the same surfaces are sampled by a
square lattice of closed cells. Does the triple survive? In particular, can a
finite lattice tell a point puncture from a small annulus?

## 2. The lattice model

`model/grid_topology.py` uses the following definitions:

- **Foreground:** the union of the present closed unit cells.
- **Euler characteristic:** `chi = V - E + F`, with vertices, unit edges, and
  cells counted once. A disk has `chi = 1`.
- **Background components:** the four-connected components of the complement.
  A component that touches the border is connected to the outside and is not a
  hole.
- **Depth:** the largest four-step distance from a foreground cell to a cell of
  a bounded background component, in lattice cells.
- **Scale:** `depth * step`, where `step` is the physical width of one cell.

A one-cell puncture whose four neighbours are foreground has depth exactly one:
the missing cell is one step from the foreground and there is no other
background cell. Its physical scale is therefore the lattice step, and it
shrinks to zero under refinement.

## 3. Result

At size 161 the lattice step is `0.01875`:

| mask | `chi` | bounded components | depth | scale | resolved |
|---|---|---|---|---|---|
| disk, radius 1 | 1 | 0 | 0 | 0 | no |
| puncture, radius 1 | 0 | 1 | 1 | 0.01875 | no |
| annulus, inner 0.3 | 0 | 1 | 16 | 0.30000 | yes |
| annulus, inner 0.1 | 0 | 1 | 6 | 0.11250 | yes |

The first three columns already show the problem. The disk is `chi = 1` with no
hole. The puncture and both annuli are `chi = 0` with exactly one bounded
background component. The combinatorial data does not separate a point
puncture from a thin annulus.

The depth does. Over sizes `21, 41, 81, 161`:

| size | step | puncture depth | annulus 0.3 depth | annulus 0.1 depth |
|---|---|---|---|---|
| 21 | 0.15000 | 1 | 2 | 1 |
| 41 | 0.07500 | 1 | 4 | 2 |
| 81 | 0.03750 | 1 | 8 | 3 |
| 161 | 0.01875 | 1 | 16 | 6 |

| size | step | puncture scale | annulus 0.3 scale | annulus 0.1 scale |
|---|---|---|---|---|
| 21 | 0.15000 | 0.15000 | 0.30000 | 0.15000 |
| 41 | 0.07500 | 0.07500 | 0.30000 | 0.15000 |
| 81 | 0.03750 | 0.03750 | 0.30000 | 0.11250 |
| 161 | 0.01875 | 0.01875 | 0.30000 | 0.11250 |

The log-log slope of scale against step is `1.0000` for the puncture, `0.0000`
for the fixed `0.3` annulus, and `0.1660` for the `0.1` annulus.

The puncture scales exactly with the sampling. The fixed annulus does not. The
`0.1` annulus is the partial case: at size 21 it has depth one, and at size 41
it has depth two. Its measured scale is still `0.1125` at size 161, not `0.1`;
the slope is not converged. The depth sequence `1, 2, 3, 6` is the reliable
part of that row.

### The exact collapse at coarse resolution

At size 21 the `0.1` annulus and the puncture are not merely similar. They are
the **same cell set**:

```python
disk_cells(21, 1.0, inner=0.1) == disk_cells(21, 1.0, puncture=True)
```

With step `0.15`, no cell lies between the centre and the next ring, so the
annulus mask is the disk minus the centre cell. Two different surfaces produce
one lattice object. No function of that object can distinguish them, and none
does.

## 4. What is exact, what is a rhyme

Using the corpus's own taxonomy:

- **Exact:** `chi` of the sampled disk is 1; `chi` of the sampled puncture and
  annulus is 0. Each has one bounded background component. This is bookkeeping
  on the cell complex.
- **Exact:** a one-cell puncture with four foreground neighbours has depth 1 at
  every size, so its scale equals the step. The slope of 1 is not fitted.
- **Exact:** the `0.1` annulus and the puncture are the same cell set at size
  21. The collapse is an identity, not a near miss.
- **Reformulation:** "a hole is bounded background" is the standard
  distance-transform reading, not a new invariant.
- **Rhyme:** calling the depth-1 lattice hole a *puncture*. In the continuum the
  operation removes a point; on the lattice it removes a two-cell and creates a
  boundary. The lattice object is always a small annulus. The puncture is the
  limit of a hole whose radius tends to zero, not a lattice object.
- **Rhyme:** "the lattice sees the puncture." It sees the puncture only in the
  refinement limit, when the depth grows without bound and the scale stays
  fixed for a real hole, or the depth stays one and the scale goes to zero for
  the puncture.

The ledger's third column has no exact lattice counterpart. Its lattice shadow
is a depth-1 hole. That is the honest boundary between the exact ledger and the
sampled surface.

## 5. The resolution criterion

A hole is **resolved** when its depth is at least two. Depth one is the minimal
nonzero value, and it is produced both by a one-cell puncture and by any hole
whose inradius is one step. A two-by-two block, for example, is a genuine hole
with depth one. The criterion is therefore a small-hole detector, not an exact
classifier:

```text
depth 1  ->  the hole is one step across; it cannot be told from a puncture
depth >= 2  ->  the hole has an interior at least two steps from the foreground
```

**Engineering rule R4:** a hole carries its depth. Report the depth in lattice
cells next to the hole; do not report a depth-1 hole as structure. Its size is
the sampling scale.

This is the same discipline as R1, never let an indeterminate value travel
without its resolution. A hole without its depth is an indeterminate absence:
it may be a point, a small annulus, or one missing sample.

## 6. What this does not support

- It is not a new theorem. The depth is the digital distance transform, and the
  inradius reading is standard.
- It is not a continuum statement. The lattice is a sampling of a surface, and
  the `chi` of the sampled union need not equal the `chi` of the surface in
  general. It does for these masks because the sampling is fine enough away from
  the boundary.
- The depth-2 threshold is a convention. A two-by-two hole is real and has
  depth one; the measure under-reports it. The threshold detects *resolved*
  holes, not all holes.
- The `0.1` annulus slope `0.1660` is not converged. Only the depth transition
  is established.
- Nothing here is evidence for the Fold's physical reading. The ledger is
  bookkeeping; this report tests its discretization, not its interpretation.
- No claim is made about three-dimensional holes or about sampling noise on a
  real point cloud. The masks are noiseless.

## 7. Reproduce

```bash
python examples/grid_topology.py
python -m pytest tests/test_grid_topology.py -q
python -m pytest tests -q --cov-fail-under=90
```

The example prints the full 16-row table and the two refinement tables. The
module is at 100% line and branch coverage in the suite.

## 8. Mapping to code

| Theme | Module / function |
|---|---|
| Lattice step | `model.grid_topology.lattice_step` |
| Disk, annulus, puncture masks | `model.grid_topology.disk_cells` |
| Bounded background components | `model.grid_topology.bounded_background_components` |
| Hole depth | `model.grid_topology.grid_hole_depth` |
| Physical hole scale | `model.grid_topology.grid_hole_scale` |
| Resolution criterion | `model.grid_topology.hole_is_resolved` |
| Euler characteristic | `model.grid_topology.lattice_euler_characteristic` |
| Ledger it tests | `model.fold_corpus.SurfaceLedger` |
| Demo | `examples/grid_topology.py` |
| Tests | `tests/test_grid_topology.py` |

## 9. References

- Rosenfeld, A., and Pfaltz, J. L. (1966). “Sequential operations in digital picture processing.” *Journal of the ACM* 13(4), 471–494.
- Borgefors, G. (1986). “Distance transformations in digital images.” *Computer Vision, Graphics, and Image Processing* 34(3), 344–371.
- Hatcher, A. (2002). *Algebraic Topology*. Cambridge University Press. (Euler characteristic of a cell complex.)
- The Fold corpus's `Fold/Chi.lean`, mapped in `FOLD_CORPUS.md`.
