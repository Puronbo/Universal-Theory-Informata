# Two Experiments on the Topological Reading

> **Source:** the architecture translation of the zero/holes arc (2026-11-18).
> **Status:** measurement report. Two proposals were tested on synthetic data;
> one survives as a diagnostic in a toy setting, one does not survive as a
> sizing rule. The checkable residue is in `model/cache_topology.py`,
> `model/latent_topology.py`, and `examples/topology_experiments.py`.

## 1. What was proposed

The architecture reading made two claims that can be measured:

1. **Cache.** The reuse-distance profile of a trace is a finite point set on
   the line. Its 0-dimensional persistence selects a scale, and the number of
   distances below that scale should predict the cache capacity that captures
   most of the hits. If true, a static scan of the trace would size a cache
   without simulating every capacity.
2. **Latent space.** A point cloud with a hole has a long-lived \(H_1\) bar; a
   cloud without one does not. The dominant \(H_1\) persistence is therefore a
   scale-labelled out-of-distribution diagnostic, including for points that
   land inside the hole where a nearest-neighbour rule is blind.

Both are cheap to test, so both were tested. Seeds are fixed and the example
reproduces every number below.

## 2. Experiment 1: cache working set

**Setup.** 4000 accesses over 400 keys, Zipf-like weights
\(w_r \propto r^{-s}\), seed 7. LRU simulated at capacities
\(4, 8, \ldots, 400\). Two estimates from the same reuse-distance profile:

- **A:** count the distinct distances at or below the lower edge of the
  earliest widest gap. `working_set_candidates` lists the counts for every tied
  widest gap.
- **B:** count the keys whose median reuse gap is at or below each candidate
  threshold (the midpoint of a widest gap).

The target is `sat90`, the smallest capacity that reaches 90% of the peak hit
rate (the peak occurs at capacity 400 in this sweep). `sat95` is the same at
95%.

| \(s\) | distinct keys | hit plateau | gap threshold | A (tied) | B (tied) | sat90 | sat95 |
|---|---|---|---|---|---|---|---|
| 0.8 | 393 | 0.902 | 273.5 | 272-376 | 129-181 | 256 | 320 |
| 1.0 | 370 | 0.907 | 347.0 | 319 | 116 | 192 | 256 |
| 1.2 | 317 | 0.921 | 249.5 | 226-244 | 66-70 | 128 | 192 |
| 1.5 | 207 | 0.948 | 168.5 | 137 | 28 | 48 | 64 |

### Result

Neither estimate predicts `sat90`:

| \(s\) | A / sat90 | B / sat90 | threshold / sat90 | threshold / sat95 |
|---|---|---|---|---|
| 0.8 | 1.06-1.47 | 0.50-0.71 | 1.07 | 0.85 |
| 1.0 | 1.66 | 0.60 | 1.81 | 1.36 |
| 1.2 | 1.77-1.91 | 0.52-0.55 | 1.95 | 1.30 |
| 1.5 | 2.85 | 0.58 | 3.51 | 2.63 |

- **A** overestimates by \(1.06\)–\(2.85\times\). For two traces the widest gap
  is tied, so A is an interval rather than a number. The gap sits high in the
  distance range, so the count below it includes many cold keys whose extra
  hits barely move the LRU curve.
- **B** stays below `sat90`: \(0.50\)–\(0.71\) across tied thresholds, so it is
  a lower bound at best, not a predictor.
- The threshold itself sits between `sat90` and `sat95` only for the flat
  exponent; as the distribution steepens, the widest gap is no longer near the
  saturation point.

### The deeper problem

For points on the line, 0-dimensional persistence is exactly the sorted list of
consecutive gaps. All components are born at zero, so the "persistence" of a
gap is just its width. The topological language adds nothing here beyond
"look at the largest gap in the reuse histogram."

That is a real negative result about the proposal, not about topology: **the
interesting persistence in systems traces would have to come from a filtration
that is not 0-dimensional on the line** — for example a filtration of the
working-set *sets* ordered by inclusion, or a 1-dimensional complex built from
temporal adjacency. Reuse distance alone has no higher-dimensional structure to
recover.

Because reuse distances are integers, equal-width gaps are common: two of the
four traces have a tied maximum, and the tied counts differ by up to 38%. The
experiment therefore reports A as an interval, and B inherits the ambiguity: at
the tied thresholds it ranges 129–181 for \(s=0.8\) and 66–70 for \(s=1.2\).
The conclusion does not depend on which tie is chosen; the claim that a single
gap sizes the cache does.

## 3. Experiment 2: latent-hole diagnostic

**Setup.** 40 points sampled uniformly by area. The ring has inner radius 0.75
and outer radius 1.0; the disk has radius 1.0. Exact \(\mathbb{Z}_2\) Rips
persistence in dimensions 0 and 1.

### Ring versus disk

| seed | annulus (birth, death, persistence) | disk (birth, death, persistence) |
|---|---|---|
| 0 | (0.45, 1.44, 0.99) | (0.39, 0.59, 0.20) |
| 1 | (0.71, 1.42, 0.71) | (0.29, 0.44, 0.15) |
| 2 | (0.59, 1.53, 0.95) | (0.56, 0.95, 0.39) |
| 3 | (0.73, 1.43, 0.70) | (0.53, 0.74, 0.21) |
| 4 | (0.49, 1.45, 0.96) | (0.47, 0.63, 0.16) |
| 5 | (0.55, 1.38, 0.82) | (0.37, 0.54, 0.17) |
| 6 | (0.42, 1.40, 0.98) | (0.39, 0.57, 0.18) |
| 7 | (0.41, 1.42, 1.01) | (0.39, 0.66, 0.27) |

The annulus persistence is 0.70–1.01; the disk is 0.15–0.39. A threshold at
0.5 separates all 16 clouds in this sample. The gap is not huge — the largest
disk bar reaches 0.39 — so the threshold is a sample statistic, not a constant.

### Hole scale versus inner radius

| inner radius | mean birth | mean death |
|---|---|---|
| 0.4 | 0.555 | 0.884 |
| 0.5 | 0.596 | 1.049 |
| 0.6 | 0.617 | 1.213 |
| 0.7 | 0.653 | 1.364 |
| 0.8 | 0.689 | 1.500 |

The death scale grows at about \(1.54\) per unit of inner radius over this
range \((1.500-0.884)/0.4\). The birth scale grows more slowly, so persistence
also grows with hole size. Both are expected: the cycle closes when the
longest edge across the hole appears, and that edge is set by the inner
diameter plus sampling noise.

### Nearest-neighbour baseline inside the hole

The threshold \(\tau\) is the 95th percentile of in-distribution
nearest-neighbour distance. Probes are sampled inside the hole, at radius
`inner - [0.02, 0.15]`, 200 probes per case.

| inner radius | \(\tau\) | missed probes | miss rate |
|---|---|---|---|
| 0.60 | 0.213 | 64 / 200 | 0.32 |
| 0.75 | 0.213 | 100 / 200 | 0.50 |

The nearest-neighbour rule misses a third to a half of the points that lie in
the hole, because in this thin ring the hole's interior is close to its inner
edge. This is the case where topology is supposed to help: the point is near
the data in distance but outside it in connectivity. A hole-aware rule can
reject those points, while a distance rule cannot.

## 4. What the experiments support

- **The latent diagnostic works in the toy case.** A dominant \(H_1\) bar
  separates a ring from a disk at this sample size, and the persistence tracks
  hole size. The nearest-neighbour baseline fails on the same points.
- **The cache estimate does not work as a sizing rule.** The threshold is a
  coarse scale, not a capacity predictor, and 0-dimensional persistence on the
  line is a restatement of the largest histogram gap.
- **The negative result is informative.** It says the next cache experiment
  must build a filtration with actual higher-dimensional structure, not reuse
  a 0-dimensional statistic and call it topology.

## 5. What the experiments do not support

- That a topology-derived capacity estimate beats LRU, ARC, or any deployed
  sizing heuristic.
- That `hole_scale` is a calibrated OOD score; the 0.5 threshold is fitted to
  this sample and this embedding dimension.
- That persistence scales to production traces or real model latents. The
  implementation enumerates all edges and triangles; 40 points take about
  0.04 s, and the triangle count grows cubically.
- That a truncated filtration is safe: simplices above `max_scale` are dropped,
  so a cycle that would die beyond the cutoff is reported as essential. The
  docstring and tests record this, and the demo uses the untruncated default.
- That the architecture translation is validated as a whole. Two toy
  experiments do not test Spectre, CAP, or the branch-counting proposal.

## 6. Reproduce

```bash
python examples/topology_experiments.py
python -m pytest tests/test_cache_topology.py tests/test_latent_topology.py -q
python -m pytest tests -q --cov-fail-under=90
```

The example prints both tables, the radius sweep, the OOD miss rates, and the
wall-clock time. Both modules are at 100% line and branch coverage in the
suite.

## 7. Mapping to code

| Theme | Module / function |
|---|---|
| Reuse distance | `model.cache_topology.reuse_distances` |
| 0-D gap persistence | `model.cache_topology.merge_gaps` |
| Distance split | `model.cache_topology.working_set_estimate` |
| Tied-gap splits | `model.cache_topology.working_set_splits` |
| Tied-gap counts | `model.cache_topology.working_set_candidates` |
| Key-count split | `model.cache_topology.working_set_keys` |
| LRU simulation | `model.cache_topology.simulate_lru`, `hit_rate_curve` |
| Saturation point | `model.cache_topology.saturation_capacity` |
| Distance matrix | `model.latent_topology.distance_matrix` |
| Rips persistence | `model.latent_topology.rips_persistence` |
| Betti numbers | `model.latent_topology.betti_at` |
| Dominant bar | `model.latent_topology.dominant_bar` |
| Hole scale | `model.latent_topology.hole_scale` |
| Demo | `examples/topology_experiments.py` |

## 8. References

- Belady, L. A. (1966). “A study of replacement algorithms for a virtual-storage computer.” *IBM Systems Journal* 5(2), 78–101.
- Mattson, R. L., Gecsei, J., Slutz, D. R., and Traiger, I. L. (1970). “Evaluation techniques for storage hierarchies.” *IBM Systems Journal* 9(2), 78–117.
- Edelsbrunner, H., Letscher, D., and Zomorodian, A. (2002). “Topological persistence and simplification.” *Discrete & Computational Geometry* 28, 511–533.
- Zomorodian, A., and Carlsson, G. (2005). “Computing persistent homology.” *Discrete & Computational Geometry* 33, 249–274.
- Otter, N., Porter, M. A., Tillmann, U., Grindrod, P., and Harrington, H. A. (2017). “A roadmap for the computation of persistent homology.” *EPJ Data Science* 6, 17.
- Belkin, M., and Niyogi, P. (2003). “Laplacian eigenmaps for dimensionality reduction and data representation.” *Neural Computation* 15(6), 1373–1396.
