# The One-Step Expansion of \(n/n^n\)

> **Source:** the instruction "expand in one step divide by step \(n/n^n\)"
> (2026-11-24).
> **Status:** exact arithmetic with one rigorous enclosure. The additive limit
> is bounded and decomposed into standard series, not evaluated in closed form;
> the interpretive sentences are labelled.

## 1. The step

The step at index \(n\) is

\[
s_n=\frac{n}{n^n}=n^{1-n}=\frac{1}{n^{n-1}},\qquad n\ge 1.
\]

The first step is exactly one, \(s_1=1\). The zero-th expression is
\(0/0^0\). Under the usual convention \(0^0=1\) it would be \(0\), but its
reciprocal \(0^{-1}\) is a pole, so the recurrence has no finite value there.
The expansion therefore starts at the identity, not at zero.

## 2. Divide in one step

Dividing the previous value by the step multiplies it by \(n^{n-1}\):

\[
A_0=1,\qquad
A_n=\frac{A_{n-1}}{s_n}=A_{n-1}\,n^{n-1}.
\]

One step is therefore the integer multiplication

\[
A_n=A_{n-1}\,n^{n-1}.
\]

After \(n\) steps the product telescopes:

\[
A_n=\prod_{k=1}^{n}k^{k-1}
=\frac{\prod_{k=1}^{n}k^k}{n!}
=\frac{H(n)}{n!},
\]

where \(H(n)\) is the hyperfactorial. The reciprocal collapses just as
cleanly:

\[
B_n=\prod_{k=1}^{n}s_k=\frac{1}{A_n}\longrightarrow 0.
\]

The collapse is superexponential: \(B_n=1/A_n\), and
\(\log A_n=\sum_{k=1}^{n}(k-1)\log k\).

## 3. The same step, added

The additive expansion is

\[
S_n=\sum_{k=1}^{n}s_k=\sum_{k=1}^{n}\frac{1}{k^{k-1}}.
\]

It converges. For \(k\ge n+1\),

\[
s_k=\frac{1}{k^{k-1}}\le (n+1)^{1-k},
\]

so the geometric tail gives the exact bound

\[
0<S_\infty-S_n\le
\sum_{k=n+1}^{\infty}(n+1)^{1-k}
=\frac{1}{n\,(n+1)^{n-1}}.
\]

At \(n=20\) the enclosure is

\[
1.628473712901584447055889139602
<S_\infty<
1.628473712901584447055889143376,
\]

with width \(3.774013109365947\times10^{-27}\). The decimals are shown to 30
places; the functions return exact `Fraction` endpoints, and the displayed
interval still encloses the limit.

## 4. An exact integral reformulation

Using

\[
\int_0^1 x^{n-1}(-\log x)^{n-1}\,dx=\frac{(n-1)!}{n^n},
\]

and summing the resulting power series, the additive limit is also

\[
S_\infty
=\int_0^1(1-x\log x)\,x^{-x}\,dx.
\]

The interchange is legitimate because the series
\(\sum_n n(-x\log x)^{n-1}/(n-1)!\) converges uniformly on \([0,1]\). This is
a reformulation, not a new evaluation: it moves the same limit into an
integral and does not evaluate it in elementary terms.

Splitting \(n/n^n=1/n^n+(n-1)/n^n\) gives the exact decomposition

\[
S_\infty
=\underbrace{\sum_{n\ge1}\frac{1}{n^n}}_{\text{A073009}}
+\underbrace{\sum_{n\ge1}\frac{n-1}{n^n}}_{\text{A358191}}
=1.2912859970626635\ldots+0.3371877158389209\ldots
\]

The first sum is the Sophomore's Dream constant
\(\int_0^1x^{-x}\,dx\); the second is the OEIS constant A358191,
\(-\int_0^1x\log x\,x^{-x}\,dx\). Their sum is the integral above. This is an
exact decomposition into two standard series, not a closed form.

## 5. Values

| \(n\) | \(s_n\) | \(1/s_n\) | \(A_n\) | \(S_n\) |
|---:|---:|---:|---:|---:|
| 1 | \(1\) | \(1\) | \(1\) | \(1\) |
| 2 | \(1/2\) | \(2\) | \(2\) | \(3/2\) |
| 3 | \(1/9\) | \(9\) | \(18\) | \(29/18\) |
| 4 | \(1/64\) | \(64\) | \(1152\) | \(937/576\) |
| 5 | \(1/625\) | \(625\) | \(720000\) | \(586201/360000\) |
| 6 | \(1/7776\) | \(7776\) | \(5598720000\) | \(15828677/9720000\) |

The multiplicative column is exact integer arithmetic at every \(n\). The
additive column is an exact rational partial sum.

Using the exact enclosure at \(n=220\), whose width is below \(10^{-515}\), the
limit to 120 decimal places is

\[
S_\infty=
1.628473712901584447055889143261883031650540310954621416474136430092385970518119804864326440312962053436521799388389568087\ldots
\]

The same 120 digits are obtained from every cut between \(n=200\) and
\(n=300\).

## 6. Further structure

### Tail sharpness

The tail bound is exactly the first omitted term times \(1+1/n\):

\[
\frac{1/(n(n+1)^{n-1})}{s_{n+1}}
=\frac{n+1}{n}.
\]

Since every later term is far smaller, the bound is asymptotically sharp, not
merely valid. This identity is checked in `tests/test_step_expansion.py`.

### Asymptotic logarithm

With the Glaisher–Kinkelin constant \(A\), the hyperfactorial asymptotic gives

\[
\log A_n=
\left(\frac12n^2-\frac12n-\frac5{12}\right)\log n
-\frac14n^2+n+\log A-\frac12\log(2\pi)
-\frac{1}{12n}+O(n^{-2}).
\]

The exact-minus-asymptotic error is \(1.66\times10^{-5}\),
\(3.82\times10^{-6}\), and \(1.42\times10^{-7}\) at \(n=10,20,100\),
respectively, decreasing like \(n^{-2}\). This is an asymptotic statement, not
an exact identity.

### Combinatorial reading

Cayley's formula counts \(n^{n-1}\) rooted labeled trees on \(n\) vertices.
Therefore \(1/s_n=n^{n-1}\) is exactly that count, and \(A_n\) is the product
of the rooted-tree counts up to \(n\). This is a standard identification, not
an explanation of why the expansion was chosen.

### The projective zero-th step

With \(0^0=1\), the zero-th step itself is \(s_0=0/0^0=0\). Its reciprocal
multiplier is \(1/s_0=0^{-1}=\infty\). Running the recurrence one step
backward from \(A_0=1\) multiplies by \(s_0\):

\[
A_{-1}=A_0\,s_0=1\cdot0=0.
\]

In the projective line this is the collapse \(1/\infty=0\). That is the pole
doing its exact job; it is not a value in a field. `model.unit_group` supplies
the projective reciprocal.

## 7. What is claimed

- The recurrence \(A_n=A_{n-1}/s_n=A_{n-1}n^{n-1}\) is exact.
- The product is \(H(n)/n!\), and the reciprocal product tends to zero.
- The additive limit lies in the stated rational interval; the tail bound is
  proved above and is exactly \(1+1/n\) times the first omitted term.
- The integral representation and the split into A073009 and A358191 are exact.
- The asymptotic logarithm is asymptotic, not exact.

## 8. What is not claimed

- That \(S_\infty\) has a known closed form. The module encloses it and
  decomposes it into standard series; it does not evaluate it in elementary
  terms.
- That the convergence rate is a physical clock or a sampling law.
- That \(0/0^0\) is defined by this construction. The zero-th step is excluded
  because its reciprocal is a pole, not because a value has been assigned.
- That the rooted-tree count explains why this step was chosen. It is a
  standard combinatorial identification.
- That the expansion explains the Fold corpus, the observer split, or any
  cosmological quantity. It is arithmetic.

## 9. References

- Graham, R. L., Knuth, D. E., and Patashnik, O. (1994). *Concrete
  Mathematics*. Addison-Wesley. (Hyperfactorials and finite products.)
- Abramowitz, M., and Stegun, I. A. (1964). *Handbook of Mathematical
  Functions*. Dover. (The gamma integral used in §4.)
- Finch, S. R. (2003). *Mathematical Constants*. Cambridge University Press.
  (Sophomore's Dream and the hyperfactorial asymptotic.)
- OEIS A073009 (Sophomore's Dream constant) and A358191
  (\(\sum_{n\ge2}(n-1)/n^n\)).
- Cayley, A. (1889). "A theorem on trees." *Quarterly Journal of Mathematics*
  23, 376–378. (The rooted-tree count \(n^{n-1}\).)
- `model/step_expansion.py`, `tests/test_step_expansion.py`, and
  `examples/step_expansion.py` for the executable form.
