# A Finite-N Sufficiency Theorem for the Viable Corridor

**Status:** Proofs with numerical controls, 2026-11-15. Theorems 2 and 3 below are
proved for finite populations with all-to-all coupling. The damage-stabilised
regime of §7 is computed, not proved. The paper's text is unchanged by this note.

**Provenance:** Derived and checked by Claude in a session on 2026-11-15, at the
maintainer's request, against the unchanged canonical model
(`teo_simulation.py`, hash in [results.json](results/results.json)).

The [Viable Corridor](../../../papers/viable-corridor.md) proves that three
constraints are necessary (Theorem 1). Its sufficiency statement, Conjecture 1,
was refuted in one reading by the
[coherence-floor counterexample](../coherence_margin/README.md), and the
erratum at §3.4 left the replacement open: fix a common state space, then
supply a floor-dependent condition and an invariance argument. This note does
that at finite $N$, the state space on which the paper defines robust
viability.

## What is settled, and what is not

| | Statement | Status |
|:--|:--|:--|
| Lemma 1 | Value orientations never feed back; substrate health only rescales their time | proved |
| Theorem 2 | Explicit conditions on $(\gamma, K, D_{\max})$ under which an explicit open set stays in $V$ forever: the corridor is non-empty | proved |
| Theorem 3 | For the fitness family the paper simulates, the conditions on $\gamma$ and $D_{\max}$ are also necessary, as long as the substrate is to stay untouched | proved |
| Corollary | The Appendix C headline numbers ($0.346$, $\gamma_c \approx 0.51$, $\delta \approx 0.9$, $\delta \approx 1.05$, $0.62$) in closed form; capability loading and single-axis insufficiency as consequences | proved |
| §7 | Between two ceilings the printed equations keep a trajectory viable by damaging the substrate | computed, not proved |
| Coherence axis | Sufficient at $K > K_{\mathrm{lock}}(\omega)$; necessary only $K > K_c$ in the continuum. The interval between is not decided | open |

The proofs are elementary. What they add to the paper is that its central
object exists, with thresholds that can be checked against its own figures.

## 1. Setting

Everything is as in §2 of the paper, with three choices made explicit.

- **Finite $N \geq 2$, fixed frequencies.** The state is
  $(\mathbf{x}, \boldsymbol\theta, \Omega)$ on the simplex, the $N$-torus and
  $\lbrack 0, \infty)$, with $H = \max(0, 1 - \Omega/S_{\max})$. The frequency vector
  $\omega \in \mathbb{R}^N$ is whatever was drawn; every statement is
  deterministic given $\omega$. Write $\nu_i = \omega_i - \bar\omega$ for the
  centred frequencies.
- **All-to-all coupling**, $A_{ij} = 1$, as in Lemma 2 and every simulation of
  the paper.
- **Locally Lipschitz raw fitness** $f^{(0)}$, so that solutions are unique.

The equations are (1), (2), (4), (5), (5′), (6) of the paper:

$$
\dot x_i = H\, x_i\bigl(f_i^{(0)} - \bar\phi_0\bigr) - \gamma (x_i - x_{\mathrm{reg}})_+ + \frac{\gamma}{N} E(\mathbf{x}),
\qquad E(\mathbf{x}) = \sum_j (x_j - x_{\mathrm{reg}})_+ ,
$$

$$
\dot\theta_i = H\Bigl[\omega_i + \frac{K}{N}\sum_j \sin(\theta_j - \theta_i)\Bigr],
\qquad
\dot\Omega = \bigl(P(\mathbf{x}) - D_{\max}\bigr)_+ ,
\qquad P(\mathbf{x}) = \sum_i \eta_i x_i f_i^{(0)}(\mathbf{x}).
$$

The brake carries no factor $H$; that is the printed equation and the
simulation's default, and it matters in §7.

Notation: $M(\mathbf{x}) = \max_i x_i$; $\gamma' = \gamma(1 - 1/N)$;
$D_f = \sup_{\mathbf{x}, i, j}\bigl(f_i^{(0)}(\mathbf{x}) - f_j^{(0)}(\mathbf{x})\bigr)$, the
largest fitness spread, which is at least the dominance margin $\delta$ of (1′).

**The two-level family** is the one Appendix C simulates:
$f^{(0)} = (f_b + \delta, f_b, \ldots, f_b)$ with constants $f_b \geq 0$,
$\delta > 0$, and uniform $\eta_i = \eta$. There $D_f = \delta$ and
$P(\mathbf{x}) = \eta(f_b + \delta x_1)$.

**Substrate-untouched robust viability** means robust viability in the sense
of §3.1 with (V3) read as $\Omega(t) = 0$ for all $t$. It implies the paper's
robust viability (V3b) and is implied by a uniform (V3a).

## 2. The coupling is a skew product

**Lemma 1.** (i) The pair $(\mathbf{x}, \Omega)$ evolves autonomously;
$\boldsymbol\theta$ does not enter its equations. (ii) Let
$\tau(t) = \int_0^t H(s)\,ds$ and let $\vartheta$ solve the standard Kuramoto
system $\vartheta_i' = \omega_i + \tfrac{K}{N}\sum_j \sin(\vartheta_j - \vartheta_i)$
from $\boldsymbol\theta(0)$. Then $\boldsymbol\theta(t) = \vartheta(\tau(t))$.

*Proof.* (i) is read off the equations. (ii) The function
$t \mapsto \vartheta(\tau(t))$ has derivative $H(t)\,\vartheta'(\tau(t))$, which is
the right-hand side of (2); uniqueness gives equality. $\square$

Two consequences. The set of values $r(t)$ takes along a coupled trajectory is
contained in the set of values taken along the standard Kuramoto trajectory
from the same phases, so a resource regime shift cannot push coherence below
a floor that the uncoupled phases respect. That removes the obstacle §3.4
names (coupling-induced excursions of $r$), for this model. And each axis can
be treated on its own, provided the bounds on the resource axis hold for
every health path, which Proposition 2 arranges.

## 3. Resource axis

For $c \in (x_{\mathrm{reg}}, 1)$ let $E_{\max}(c)$ be the largest total excess
$E(\mathbf{x})$ on the simplex with $M(\mathbf{x}) = c$. A convex function on the capped
simplex is maximal at a vertex, so with $k = \lfloor 1/c \rfloor$ and $N > k$,

$$
E_{\max}(c) = k\,(c - x_{\mathrm{reg}}) + (1 - kc - x_{\mathrm{reg}})_+ \;\leq\; \frac{c - x_{\mathrm{reg}}}{c}.
$$

The inequality holds because $(s - x_{\mathrm{reg}})_+ \leq s\,(1 - x_{\mathrm{reg}}/c)$ on
$\lbrack 0, c\rbrack$. Define

$$
\gamma_{\mathrm{full}} = \frac{x_{\mathrm{crit}}(1 - x_{\mathrm{crit}})\,D_f}{(x_{\mathrm{crit}} - x_{\mathrm{reg}}) - E_{\max}(x_{\mathrm{crit}})/N}
\;\leq\;
\gamma_{\mathrm{up}} = \frac{x_{\mathrm{crit}}(1 - x_{\mathrm{crit}})\,D_f}{(x_{\mathrm{crit}} - x_{\mathrm{reg}})\bigl(1 - \tfrac{1}{N x_{\mathrm{crit}}}\bigr)} .
$$

Both denominators are positive because $x_{\mathrm{crit}} > x_{\mathrm{reg}} > 1/N$.

**Proposition 2 (the pluralism region is invariant).** If
$\gamma > \gamma_{\mathrm{full}}$, then for every measurable health path
$H(\cdot)$ with values in $\lbrack 0, 1\rbrack$ the set
$\lbrace M(\mathbf{x}) < x_{\mathrm{crit}}\rbrace$ is forward invariant.

*Proof.* Suppose a trajectory with $M < x_{\mathrm{crit}}$ first reaches
$M = x_{\mathrm{crit}} =: c$ at time $t_1$, through agent $i$. Then
$\dot x_i(t_1) \geq 0$. But
$f_i^{(0)} - \bar\phi_0 = \sum_j x_j (f_i^{(0)} - f_j^{(0)}) \leq (1 - c) D_f$, and
$H \leq 1$, so

$$
\dot x_i(t_1) \leq c(1 - c) D_f - \gamma (c - x_{\mathrm{reg}}) + \frac{\gamma}{N} E_{\max}(c) < 0 ,
$$

a contradiction. $\square$

**Proposition 3 (a lower comparison).** Assume strict dominance (1′) with
margin $\delta$, and let a trajectory start in the interior of the simplex
and keep $H \equiv 1$. Then $x_{i^\ast}(t) \geq \tilde y(t)$, where
$\tilde y' = g_\delta(\tilde y)$, $\tilde y(0) = x_{i^\ast}(0)$, and

$$
g_\delta(y) = \delta\, y(1 - y) - \gamma'\,(y - x_{\mathrm{reg}})_+ .
$$

For $\gamma > 0$ the function $g_\delta$ has exactly one zero in $(0, 1)$,

$$
y^\ast(\gamma, \delta) = \frac{(\delta - \gamma') + \sqrt{(\gamma' - \delta)^2 + 4\,\delta\,\gamma'\,x_{\mathrm{reg}}}}{2\delta} \in (x_{\mathrm{reg}}, 1),
$$

and $\liminf_t x_{i^\ast}(t) \geq y^\ast$. In particular, if

$$
\gamma < \gamma_{\mathrm{low}} := \frac{x_{\mathrm{crit}}(1 - x_{\mathrm{crit}})\,\delta}{(x_{\mathrm{crit}} - x_{\mathrm{reg}})(1 - 1/N)} ,
$$

then $y^\ast > x_{\mathrm{crit}}$ and (V1) fails in finite time.

*Proof.* By (1′), $f_{i^\ast}^{(0)} - \bar\phi_0 \geq \delta(1 - x_{i^\ast})$, and
$E \geq (x_{i^\ast} - x_{\mathrm{reg}})_+$, so $\dot x_{i^\ast} \geq g_\delta(x_{i^\ast})$;
the scalar comparison theorem applies because $g_\delta$ is Lipschitz. On
$(0, x_{\mathrm{reg}}\rbrack$, $g_\delta > 0$. On $(x_{\mathrm{reg}}, 1\rbrack$ the quotient
$g_\delta(y)/(y - x_{\mathrm{reg}}) = \delta y(1 - y)/(y - x_{\mathrm{reg}}) - \gamma'$ is strictly
decreasing, because the derivative of $y(1-y)/(y - x_{\mathrm{reg}})$ has numerator
$-(y - x_{\mathrm{reg}})^2 - x_{\mathrm{reg}}(1 - x_{\mathrm{reg}})$; it runs from $+\infty$ to
$-\gamma' < 0$. So the zero is unique, it solves the quadratic
$\delta y^2 + (\gamma' - \delta) y - \gamma' x_{\mathrm{reg}} = 0$, and $\tilde y \to y^\ast$.
Finally $y^\ast > x_{\mathrm{crit}}$ exactly when $g_\delta(x_{\mathrm{crit}}) > 0$. $\square$

The paper's boundary-balance estimate (9) is $\gamma_{\mathrm{low}}$ without the
factor $(1 - 1/N)^{-1}$, the redistribution term it drops, and with the lower
margin $\delta$. Proposition 2 needs the upper spread $D_f$ instead. The two
coincide in the two-level family.

## 4. Substrate axis

**Proposition 4 (a floor on the ceiling).** In the two-level family put
$D_{\mathrm{floor}} = \eta(f_b + \delta\,x_{\mathrm{reg}})$. If $D_{\max} < D_{\mathrm{floor}}$, no
trajectory from the interior of the simplex stays in $V$ for all time,
whatever $\gamma \geq 0$ and $S_{\max}$ are.

*Proof.* While $x_1 \leq x_{\mathrm{reg}}$,
$\dot x_1 = H\delta x_1(1 - x_1) + \tfrac{\gamma}{N}E \geq 0$, so $x_1$ cannot fall
below $x_{\mathrm{reg}}$ once it is there, and is non-decreasing before. Suppose
the trajectory stays in $V$; then $\Omega$ is non-decreasing and bounded by
$S_{\max}$. If $x_1$ reaches $x_{\mathrm{reg}}$, then
$\dot\Omega \geq D_{\mathrm{floor}} - D_{\max} > 0$ from then on, and $\Omega$ is
unbounded. If it never does, $x_1$ increases to a limit $x_\infty \leq x_{\mathrm{reg}}$
and $P$ increases to $\eta(f_b + \delta x_\infty)$. That limit cannot exceed
$D_{\max}$, or $\Omega$ would again be unbounded; so $P \leq D_{\max}$
throughout, $\Omega \equiv 0$, $H \equiv 1$, and
$\dot x_1 \geq \delta\,x_1(0)\,(1 - x_{\mathrm{reg}}) > 0$ carries $x_1$ to $x_{\mathrm{reg}}$ in
finite time. Each case is a contradiction. $\square$

On the sufficient side the substrate stays untouched whenever throughput
stays at or below the ceiling on the invariant set in use. For a general
fitness that is

$$
P_{\mathrm{cap}} := \sup\,\lbrace P(\mathbf{x}) : M(\mathbf{x}) \leq x_{\mathrm{crit}} \rbrace \;\leq\; D_{\max} .
$$

The supremum is over the capped simplex, not the whole one: pluralism lowers
the throughput the substrate must carry. In the two-level family
$P_{\mathrm{cap}} = \eta(f_b + \delta\,x_{\mathrm{crit}})$ against
$\eta(f_b + \delta)$ at the vertex.

## 5. Coherence axis

By Lemma 1 it is enough to work with the standard Kuramoto system and then
change time. Two conditions are given. The first is sharp for full phase
locking; the second tolerates oscillators that never lock and does not
degrade with $N$.

### 5.1 A stable locked state

In the frame rotating at $\bar\omega$ the standard system is the gradient flow
$\varphi' = -\nabla U(\varphi)$ of

$$
U(\varphi) = -\sum_i \nu_i \varphi_i - \frac{K}{2N}\sum_{i,j}\cos(\varphi_i - \varphi_j)
$$

on the lift $\mathbb{R}^N$ (van Hemmen & Wreszinski, 1993). Its critical points
are the phase-locked states: $\sin(\varphi_i - \psi) = \nu_i/(Kr)$. For
$u > \nu_{\max} := \max_i |\nu_i|$ define

$$
K(u) = \frac{N u}{\sum_i \sqrt{1 - \nu_i^2/u^2}},
\qquad
S(u) = \sum_i \frac{1 - 2\nu_i^2/u^2}{\sqrt{1 - \nu_i^2/u^2}} .
$$

$K(u)$ is the coupling at which the state with all cosines positive and
$Kr = u$ is self-consistent; its coherence is $r = u/K(u)$.

**Proposition 5.** (i) $S$ is strictly increasing with a unique zero $u_s$;
$K$ decreases on $(\nu_{\max}, u_s)$ and increases on $(u_s, \infty)$. Hence
$K_{\mathrm{lock}}(\omega) := K(u_s)$ is its minimum, and no phase-locked state of
any kind exists for $K < K_{\mathrm{lock}}$. (ii) For $K > K_{\mathrm{lock}}$ the state
$\varphi^\ast$ with $u > u_s$, $K(u) = K$ is a non-degenerate minimum of $U$ modulo
rotation, with coherence $r_{\mathrm{lock}}(K) = u/K$, increasing in $K$.
(iii) For every $\varepsilon > 0$ there is an open, rotation-invariant set of
phases containing $\varphi^\ast$ on which $|r - r_{\mathrm{lock}}(K)| < \varepsilon$ and
which is forward invariant under (2) for every health path $H(\cdot) \geq 0$.

*Proof.* (i) With $s = |\nu_i|/u$ each summand of $S$ is
$h(s) = (1 - 2s^2)/\sqrt{1 - s^2}$, and
$h'(s) = s(2s^2 - 3)/(1 - s^2)^{3/2} < 0$, so $S$ increases in $u$, from $-\infty$
at $\nu_{\max}$ to $N$. Differentiating, $\tfrac{d}{du}\bigl(1/K\bigr) = -S(u)/(N u^2)$,
which gives the shape of $K$. A locked state with some cosines negative needs
the coupling $N u / \sum_i \epsilon_i\sqrt{1 - \nu_i^2/u^2}$ with signs $\epsilon_i$,
which is at least $K(u) \geq K_{\mathrm{lock}}$.

(ii) In the frame $\psi = 0$ write $c_i = \cos\varphi_i^\ast > 0$,
$s_i = \sin\varphi_i^\ast = \nu_i/u$; then $\sum_i c_i = Nr$ and $\sum_i s_i = 0$. The
Hessian of $U$ is

$$
\nabla^2 U = \frac{K}{N}\Bigl[\,Nr\,\mathrm{diag}(c) - c\,c^{\top} - s\,s^{\top}\Bigr].
$$

By Cauchy–Schwarz, $B = Nr\,\mathrm{diag}(c) - cc^{\top}$ is positive semidefinite with
kernel spanned by $\mathbf{1}$, the rotation direction, and $s \perp \mathbf{1}$. Then
$B - ss^{\top}$ is positive definite on $\mathbf{1}^\perp$ exactly when $s^{\top} B^{+} s < 1$.
Since $B\,(Nr\,\mathrm{diag}(c))^{-1} s = s$, this is
$\sum_i s_i^2/c_i < \sum_i c_i$, that is, $S(u) > 0$. Monotonicity of
$r = \tfrac1N\sum_i\sqrt{1 - \nu_i^2/u^2}$ in $u$, and of $u$ in $K$ on this
branch, gives the last claim.

(iii) The mean phase is conserved, so on $\mathbf{1}^\perp$ the dynamics are the
gradient flow of the restricted potential, run at speed $H(t)$; $U$ is
non-increasing along it for any $H \geq 0$. Choose a ball around $\varphi^\ast$ in
$\mathbf{1}^\perp$ on which $|r - r_{\mathrm{lock}}| < \varepsilon$ and $U$ exceeds $U(\varphi^\ast)$
by at least $m > 0$ on the bounding sphere. The part of the ball where
$U < U(\varphi^\ast) + m$ is open, contains $\varphi^\ast$, and cannot be left. $\square$

The stability criterion in (ii) is the collective-mode condition of
Mirollo & Strogatz (2005); the existence threshold agrees with the implicit
formula of Verwoerd & Mason (2008). They are re-derived here because the
argument is short and the note should not lean on a remembered statement.

**Floor.** The coherence clause is therefore $K > K_{\mathrm{lock}}(\omega)$ and
$r_{\mathrm{lock}}(K) > r_{\min}$. This is the finite-$N$ counterpart of the
erratum's floor-dependent condition. For the frequency draws examined here
$r_{\mathrm{lock}} \geq 0.85$ already at the threshold, so at $r_{\min} = 0.5$ the
locking threshold is the binding one.

### 5.2 A cluster on an arc

**Proposition 6.** Let $\mathcal{S}$ be a set of $m$ oscillators, $p = m/N$,
$q = 1 - p$, and $W_{\mathcal{S}} = \max_{i,j \in \mathcal{S}}(\omega_i - \omega_j)$. If for
some $a \in (0, \pi/2\rbrack$

$$
2K \sin a\,\bigl(p\cos a - q\bigr) > W_{\mathcal{S}}
\qquad\text{and}\qquad
p\cos a - q \geq r_{\min},
$$

then the open set of phase configurations in which the oscillators of
$\mathcal{S}$ lie on an arc shorter than $2a$ is forward invariant under (2) for
every health path, and $r \geq p\cos a - q \geq r_{\min}$ on it. The other
$N - m$ oscillators are unconstrained.

*Proof.* In standard time, suppose the arc length first reaches $2a$, between
$\theta_{\mathrm{top}}$ and $\theta_{\mathrm{bot}}$ in $\mathcal{S}$. Their difference then has
non-negative derivative. But that derivative is
$\omega_{\mathrm{top}} - \omega_{\mathrm{bot}} + \tfrac{K}{N}\sum_j\bigl[\sin(\theta_j - \theta_{\mathrm{top}}) - \sin(\theta_j - \theta_{\mathrm{bot}})\bigr]$.
For $j \in \mathcal{S}$ the bracket is
$-2\sin a\,\cos(\theta_j - \tfrac12(\theta_{\mathrm{top}} + \theta_{\mathrm{bot}})) \leq -2\sin a\cos a$;
for $j \notin \mathcal{S}$ it is at most $2\sin a$. The sum is at most
$W_{\mathcal{S}} - 2K\sin a\,(p\cos a - q) < 0$. For the bound on $r$, project on the
arc's midpoint: the cluster contributes at least $m\cos a$ and the rest
removes at most $N - m$. Lemma 1 transfers both to any $H(\cdot)$. $\square$

With $\mathcal{S}$ the whole population this is the arc condition
$K\sin 2a > \omega_{\max} - \omega_{\min}$ of Dörfler & Bullo (2011); with a proper
subset it is a partial-entrainment condition in the spirit of De Smet &
Aeyels (2007). Write $K_{\mathrm{arc}}(\omega, r_{\min})$ for the smallest coupling it
certifies, minimised over clusters and $a$. For frequencies drawn from a
density with $\mathbb{P}(|\omega| \leq c) = p(c)$ the cluster
$\lbrace |\omega_i| \leq c\rbrace$ has $W \leq 2c$, which gives a bound that does not
grow with $N$:

| $r_{\min}$ | Gaussian, $\sigma = 1$ | Lorentzian, $\Delta = 1$ |
|---:|---:|---:|
| 0.25 | 4.318 | 11.408 |
| 0.50 | 4.318 | 12.318 |
| 0.75 | 4.819 | 24.269 |

These are sufficient values. The continuum onsets are $1.596$ and $2$, and the
stationary floors at $r_{\min} = 0.5$ are $1.748$ and $2.667$
([coherence margin](../coherence_margin/README.md)).

## 6. The theorems

**Theorem 2 (sufficiency).** In the setting of §1 assume

1. $\gamma > \gamma_{\mathrm{full}}$;
2. the coherence clause of Proposition 5 or of Proposition 6 holds, with open
   invariant phase set $U_\theta$;
3. $P_{\mathrm{cap}} \leq D_{\max}$.

Then $U = \lbrace M(\mathbf{x}) < x_{\mathrm{crit}}\rbrace \times U_\theta \times \lbrace H = 1\rbrace$ is a
non-empty open subset of $V$, and every trajectory starting in $U$ stays in
$V$ for all $t \geq 0$, with $\Omega \equiv 0$. The configuration
$(\gamma, K, D_{\max}, S_{\max})$ admits robust viability, for every
$S_{\max} > 0$.

*Proof.* By Proposition 2, $M < x_{\mathrm{crit}}$ for all time, whatever $H$ does.
On that set $P \leq P_{\mathrm{cap}} \leq D_{\max}$, so $\dot\Omega = 0$ and $H \equiv 1$.
Proposition 5 or 6 keeps $r \geq r_{\min}$. $\square$

**Theorem 3 (the two-level corridor, exactly on two axes).** In the two-level
family let $y^\ast = y^\ast(\gamma, \delta)$ and
$D_{\mathrm{low}}(\gamma) = \eta\,(f_b + \delta\,y^\ast)$.

1. If $\gamma \geq \gamma_{\mathrm{low}}$, $D_{\max} \geq D_{\mathrm{low}}(\gamma)$ and the
   coherence clause holds, then
   $U = \lbrace 0 < x_1 < y^\ast,\ x_j < x_{\mathrm{reg}}\ (j \geq 2)\rbrace \times U_\theta \times \lbrace H = 1\rbrace$
   is a non-empty open subset of $V$ that is never left, with $\Omega \equiv 0$.
2. If $\gamma < \gamma_{\mathrm{low}}$ or $D_{\max} < D_{\mathrm{low}}(\gamma)$, no configuration
   admits substrate-untouched robust viability, whatever $K$ is.
3. If $D_{\max} < D_{\mathrm{floor}}$, no configuration admits robust viability at all.

*Proof.* (1) Until the first exit from $U$, $P = \eta(f_b + \delta x_1) \leq D_{\max}$,
so $H = 1$, only agent 1 can exceed $x_{\mathrm{reg}}$, and $\dot x_1 = g_\delta(x_1)$
exactly. Hence $x_1 < y^\ast$ forever: $y^\ast$ is an equilibrium of a scalar
equation with unique solutions. For $j \geq 2$ at the level $x_{\mathrm{reg}}$,
$\dot x_j = -\delta x_1 x_{\mathrm{reg}} + \tfrac{\gamma}{N}(x_1 - x_{\mathrm{reg}})_+$. This is
negative: for $x_1 \leq x_{\mathrm{reg}}$ trivially, and for
$x_{\mathrm{reg}} < x_1 < y^\ast$ because $g_\delta(x_1) > 0$ gives
$\tfrac{\gamma}{N}(x_1 - x_{\mathrm{reg}}) < \delta x_1(1 - x_1)/(N-1)$ and
$(1 - x_1)/(N-1) < x_{\mathrm{reg}}$ follows from $x_{\mathrm{reg}} > 1/N$. So $U$ is not left.
It is non-empty because $(N-1)\,x_{\mathrm{reg}} > 1 - 1/N > 1 - y^\ast$, and it lies in
$V$ because $y^\ast \leq x_{\mathrm{crit}}$ is equivalent to $\gamma \geq \gamma_{\mathrm{low}}$.
(2) An open set contains interior starts. With $\Omega \equiv 0$,
Proposition 3 gives $\liminf x_1 \geq y^\ast$; then either $y^\ast > x_{\mathrm{crit}}$
and (V1) fails, or $P$ eventually exceeds $D_{\max}$ and $\Omega$ becomes
positive. (3) is Proposition 4. $\square$

At equality the limiting margin is zero, as in the coherence-floor note.

**Corollary (capability, in closed form).** In the two-level family, at fixed
$(\gamma, D_{\max})$, the substrate-untouched corridor is the set of
capabilities

$$
\delta \;\leq\; \min\bigl(\delta_{\mathrm{conc}},\, \delta_{\mathrm{sub}}\bigr),
\qquad
\delta_{\mathrm{conc}} = \frac{\gamma'\,(x_{\mathrm{crit}} - x_{\mathrm{reg}})}{x_{\mathrm{crit}}(1 - x_{\mathrm{crit}})},
\qquad
\delta_{\mathrm{sub}} = \frac{A\,(A + \gamma')}{A + \gamma'\,x_{\mathrm{reg}}},
\quad A = \frac{D_{\max}}{\eta} - f_b .
$$

Both $\gamma_{\mathrm{low}}$ and $D_{\mathrm{low}}$ increase with $\delta$: capability loads
two constraints. Raising $D_{\max}$ alone never lifts $\delta_{\mathrm{conc}}$, and
raising $\gamma$ alone lifts $\delta_{\mathrm{sub}}$ only up to $A/x_{\mathrm{reg}}$, where
$D_{\max} = D_{\mathrm{floor}}$ and Proposition 4 takes over. This is the
single-axis insufficiency of §C.4, as a consequence of the equations.

The closed forms reproduce the numbers the paper found by simulation:

| Paper, Appendix C | Reported | Closed form |
|:--|:--|:--|
| C.1 (a): $\max_i x_i$ in the corridor | $0.346$ | $y^\ast(1.5, 0.3) = 0.346193$ |
| C.1 (a): coherence $r$ | $0.946$ | $r_{\mathrm{lock}}(3.0) = 0.946247$ |
| C.2: critical brake strength | crossing $\approx 0.51$; estimate (9) $= 0.495$ | $\gamma_{\mathrm{low}} = 0.505102$; (9) is its $N \to \infty$ limit |
| C.4: concentration boundary in $\delta$ | $\approx 0.9$ | $\delta_{\mathrm{conc}} = 0.890909$ |
| C.4: substrate boundary in $\delta$ | $\approx 1.05$ | $\delta_{\mathrm{sub}} = 1.046759$ |
| C.4: $D_{\max}$ only, at $\delta = 2$ | $\max_i x_i \approx 0.62$ | $y^\ast(1.5, 2) = 0.620410$ |
| C.4: $\gamma = 6$ only, at $\delta = 2$, $D_{\max} = 1.5$ | substrate breached | $D_{\mathrm{floor}} = 1.6 > 1.5$: no $\gamma$ can help |
| C.4: $\gamma = 6$ and $D_{\max} = 3$ | viable | $\gamma_{\mathrm{low}} = 3.367 < 6$; $D_{\mathrm{low}} = 1.760 < 3$ |

The canonical in-corridor point of C.1 ($\gamma = 1.5$, $K = 3.0$,
$D_{\max} = 1.5$, seed 7) satisfies Theorem 3 with the locked-state clause:
$\gamma_{\mathrm{low}} = 0.505$, $D_{\mathrm{low}} = 1.104$, $K_{\mathrm{lock}} = 2.534$. It lies
inside a proved invariant open set. It does not satisfy the arc clause
($K_{\mathrm{arc}} = 3.594$).

**Two thresholds on the resource axis.** In the two-level family,
$\gamma_{\mathrm{low}} = 0.5051$ is the threshold for *some* invariant open set and
$\gamma_{\mathrm{full}} = 0.5156$ for the *whole* pluralism region. Between them,
starts with a second agent near $x_{\mathrm{crit}}$ leave $V$ (the redistribution
they trigger feeds the dominant agent), while starts with the others below
$x_{\mathrm{reg}}$ do not.

## 7. A property of the printed equations: damage can stabilise

Theorem 3 leaves the interval $D_{\mathrm{floor}} < D_{\max} < D_{\mathrm{low}}(\gamma)$
undecided for the paper's weaker condition (V3b). There the model does
something the paper does not describe.

Because the brake is not scaled by $H$ while the replicator drift is, a
degraded substrate weakens concentration relative to regulation: the
equilibrium share becomes $y^\ast(\gamma, H\delta)$, which falls with $H$.
Throughput falls with it. Setting throughput equal to the ceiling,
$y_D = (D_{\max}/\eta - f_b)/\delta$, gives the health at which the two balance,

$$
H_\infty = \frac{\gamma'\,(y_D - x_{\mathrm{reg}})}{\delta\,y_D\,(1 - y_D)} \in (0, 1)
\quad\text{exactly when}\quad D_{\mathrm{floor}} < D_{\max} < D_{\mathrm{low}}(\gamma),
$$

independent of $S_{\max}$. This point is the upper end of an equilibrium segment:
for $0 < H \le H_\infty$, the stationary share $y^\ast(\gamma,H\delta)\le y_D$
gives throughput at or below the ceiling, so damage stops accumulating.
The table uses $S_{\max}=5$. For its in-window rows the standard start approaches
the upper endpoint, with $\Omega_\infty=(1-H_\infty)S_{\max}$. These trajectory
outcomes are **computed, not proved**.

| $\gamma$ | $\delta$ | $D_{\max}$ | $D_{\mathrm{floor}}$ | $D_{\mathrm{low}}$ | $H_\infty$ predicted | $H$ at $t = 3000$ | Brake scaled by $H$ |
|---:|---:|---:|---:|---:|---:|---:|:--|
| 6.0 | 2.0 | 1.70 | 1.60 | 1.7603 | 0.64615 | 0.64615 | veto |
| 6.0 | 2.0 | 1.65 | 1.60 | 1.7603 | 0.33504 | 0.33504 | veto |
| 6.0 | 2.0 | 1.61 | 1.60 | 1.7603 | 0.06935 | 0.06935 | veto |
| 6.0 | 2.0 | 1.59 | 1.60 | 1.7603 | n/a | 0 (veto) | veto |
| 1.5 | 0.3 | 1.100 | 1.09 | 1.1039 | 0.73500 | 0.73505 | veto |
| 1.5 | 0.3 | 1.085 | 1.09 | 1.1039 | n/a | 0 (veto) | veto |

In these runs pluralism and coherence hold throughout, so the trajectories are
viable in the paper's sense with a permanently damaged substrate. With the
simulation's `brake_couples_to_H=True` the resource flow is a pure time change
of the healthy one, $y^\ast$ no longer depends on $H$, and every run ends in the
veto: the window closes and $D_{\mathrm{low}}$ becomes the exact boundary. (Run the
comparison of Proposition 3 in the time $\tau$ of Lemma 1: once throughput has
passed the ceiling it stays above it, so either $\Omega$ grows without bound or
it never started to grow, and the second case contradicts the comparison.)

Consequences for the paper's wording, for the maintainer to decide:

- §3.2 says the long-time substrate coordinate is "the ceiling $D_{\max}$
  relative to throughput", with $S_{\max}$ governing only transients. For the
  printed equations the first half needs a qualifier: throughput is itself
  moved by substrate damage, and the viable boundary sits at $D_{\mathrm{floor}}$,
  below the healthy throughput in the listed runs. The upper-endpoint formula
  is independent of $S_{\max}$. Accumulated damage is irreversible, so a
  trajectory can settle below that endpoint. For $(\gamma,\delta,D_{\max})=(6,2,1.70)$, the [second reading](https://github.com/frnkptrln/systems-and-intelligence/pull/101#issuecomment-6951084795)
  reports $H(3000)=0.64615$ at reserve 5 and $0.50771$ at reserve 0.01.
- §C.4 calls the coupling through $H$ benign because it freezes the state. In
  the window it does more than freeze: it moves the resource equilibrium.
- Whether a system that survives by degrading its substrate should count as
  viable is a modelling decision. Adopting the scaled brake as canonical, or
  reading (V3) as "untouched", both remove the window; keeping the printed
  equations means stating it.

On the $(\gamma, D_{\max})$ grid of the figure, for $\gamma < \gamma_{\mathrm{low}}$ the
standard start at $S_{\max}=5$ exceeds $x_{\mathrm{crit}}$ before damage
lowers the dominant share. This observation depends on the reserve. At
$(\gamma,\delta,D_{\max})=(0.40,0.3,1.10)$ the reported trajectory exceeds the
pluralism ceiling at reserve 5, meets all three conditions at 0.5, and reaches
the substrate veto at 0.1. These single-start runs do not establish robust viability.

![Left: the resource–substrate plane at capability 2 with the three analytic curves and the simulated outcome of each grid cell. Right: coherence of the stable locked state against coupling for the canonical frequencies, with the locking threshold, the arc threshold, the continuum onset and the minimum simulated coherence.](results/corridor_sufficiency.png)

## 8. Numerical controls

All runs use the unchanged canonical right-hand side. Sampling an open set
does not prove invariance; the proofs do. The samples are a check that the
statements were transcribed and implemented correctly.

**Closed forms against the runner.** On four parameter rows of Appendix C the
simulated final dominant share equals $y^\ast$, the simulated throughput equals
$D_{\mathrm{low}}$ and the simulated coherence equals $r_{\mathrm{lock}}$, each to better
than $10^{-9}$.

**Resource thresholds.** From uniform shares the dominant share exceeds
$x_{\mathrm{crit}}$ at $0.99\,\gamma_{\mathrm{low}}$ and $0.999\,\gamma_{\mathrm{low}}$ and stays below
it at $1.001\,\gamma_{\mathrm{low}}$ and $1.01\,\gamma_{\mathrm{low}}$. From two shares at
$x_{\mathrm{crit}} - 10^{-7}$ it exceeds $x_{\mathrm{crit}}$ at $0.985$ and $0.998$ times
$\gamma_{\mathrm{full}}$ and not at $1.002$ and $1.01$ times.

**Initial conditions inside the invariant sets**, 200 per set, shares drawn
from spread-out, two-leader and three-leader configurations:

| Set | Parameters | Violations | Worst margins |
|:--|:--|---:|:--|
| Theorem 2, locked-state clause; phases within sd $0.2$ of the locked state | $\gamma = 1.5$, $K = 3.0$ | 0 / 200 | $\sup M = 0.436 < 0.45$; $\inf r = 0.900$; $\Omega = 0$ |
| Theorem 2, arc clause; 46 of 50 oscillators on the arc, the rest anywhere or opposite | $\gamma = 1.5$, $K = 1.03\,K_{\mathrm{arc}}$ | 0 / 200 | arc $\leq 1.5058 < 1.5073$; $\inf r = 0.5913 \geq 0.5908$; $\Omega = 0$ |
| Theorem 3; $x_1 < y^\ast$, others below $x_{\mathrm{reg}}$ | $\gamma = 1.002\,\gamma_{\mathrm{low}}$, $K = 3.0$ | 0 / 200 | $x_1 \leq y^\ast = 0.44968 < 0.45$; others $\leq 0.272 < 0.3$; $\Omega = 0$ |

The phase radius $0.2$ in the first row is an illustration; Proposition 5
asserts some neighbourhood, not this one. In the third row $x_1$ approaches
$y^\ast$ from below and meets it only in floating point; the check allows
$10^{-9}$.

**The $(\gamma, D_{\max})$ plane at $\delta = 2$**, 81 cells, the paper's
standard start, $t \leq 1500$. For 63 cells the note proves the outcome (33
viable with the substrate untouched, 30 not viable) and the simulation agrees
in all 63. Of the 18 cells between $D_{\mathrm{floor}}$ and $D_{\mathrm{low}}$, the 9 with
$\gamma \geq \gamma_{\mathrm{low}}$ end damage-stabilised with $H$ between $0.22$ and
$0.94$, and the 9 with $\gamma < \gamma_{\mathrm{low}}$ leave through concentration.

**Coherence thresholds across frequency draws**, seeds $0..15$, Gaussian
$\sigma = 1$, $r_{\min} = 0.5$ (minimum / median / maximum):

| $N$ | $K_{\mathrm{lock}}(\omega)$ | $r_{\mathrm{lock}}$ at the threshold | $K_{\mathrm{arc}}(\omega)$ |
|---:|:--|:--|:--|
| 50 | 2.005 / 2.683 / 3.548 | 0.855 / 0.901 / 0.940 | 3.004 / 3.781 / 4.208 |
| 200 | 2.588 / 3.054 / 3.471 | 0.902 / 0.930 / 0.943 | 3.618 / 4.003 / 4.448 |
| 1000 | 3.153 / 3.474 / 4.143 | 0.938 / 0.951 / 0.966 | 3.985 / 4.201 / 4.345 |

$K_{\mathrm{lock}}$ grows with $N$ because full locking must capture the extreme
frequency; $K_{\mathrm{arc}}$ stays near its population value $4.318$. Neither
clause dominates: in one of the sixteen $N = 1000$ draws the arc threshold
($3.985$) lies below the locking threshold ($3.990$). For the
canonical frequencies (seed 7, $N = 50$): $K_{\mathrm{lock}} = 2.5343$,
$K_{\mathrm{arc}} = 3.5936$. From the paper's standard start the minimum simulated
coherence over $t \leq 300$ is $0.485$ at $K = 1.6$ and $0.618$ at $K = 1.8$, so
that start stays above the floor from roughly $K = 1.7$, well below anything
proved here. (In the figure the simulated minima for $K \geq 3$ sit at $0.946$,
the coherence of the start itself.)

## 9. What remains open

1. **The coherence axis between onset and locking.** For
   $K_c < K < K_{\mathrm{lock}}(\omega)$ the population is partially locked and $r$
   fluctuates. Simulation says the floor holds from about the stationary
   floor upward; no invariant open set is proved there, and none is excluded.
   A sharper finite-$N$ condition would have to bound those fluctuations.
2. **The continuum limit.** For heavy-tailed densities $K_{\mathrm{lock}}$ diverges
   with $N$ and only Proposition 6 survives, at a value several times the
   stationary floor. In the mean-field limit the nonlinear stability of
   partially locked states is known under hypotheses on the density and in a
   weak topology (Dietert, Fernandez & Gérard-Varet, 2018). Whether those
   hypotheses cover the paper's densities, and which open set of initial
   measures results, has not been checked. The erratum's "invariance argument
   off the Ott–Antonsen manifold" is still open in that reading.
3. **The damage-stabilised regime** (§7): convergence is computed only, and
   the exact (V3b) boundary for $\gamma < \gamma_{\mathrm{low}}$ depends on the
   transient and on $S_{\max}$.
4. **General topology.** Everything on the coherence axis assumes
   $A_{ij} = 1$. Lemma 1 and the resource and substrate results do not.
5. **Beyond the two-level family** the necessary and sufficient thresholds on
   $\gamma$ separate ($\delta$ against $D_f$), and $P_{\mathrm{cap}}$ replaces the
   closed form for the ceiling.

## 10. Data, tests and reproduction

[results.json](results/results.json) holds every threshold, row and cell
quoted above, one record per line, with source hashes and library versions.
[`tests/test_corridor_sufficiency.py`](../../../tests/test_corridor_sufficiency.py)
pins the closed forms, evaluates the inequalities of Propositions 2 and 6 on
the canonical right-hand side at several thousand boundary configurations,
checks the Hessian criterion of Proposition 5 on both branches by direct
eigenvalue computation, reruns the threshold brackets and one damage-window
case, and checks the committed file for completeness. It reruns none of the
600 sampled trajectories and none of the 81 plane cells; those are records.

```bash
python lab/experiments/corridor_sufficiency/corridor_sufficiency.py --output /tmp/corridor-sufficiency
pytest tests/test_corridor_sufficiency.py -q
```

The first command takes about ten minutes on one core.

## References

- De Smet, F., & Aeyels, D. (2007). Partial entrainment in the finite Kuramoto–Sakaguchi model. *Physica D*, 234(2), 81–89.
- Dietert, H., Fernandez, B., & Gérard-Varet, D. (2018). Landau damping to partially locked states in the Kuramoto model. *Communications on Pure and Applied Mathematics*, 71(5), 953–993.
- Dörfler, F., & Bullo, F. (2011). On the critical coupling for Kuramoto oscillators. *SIAM Journal on Applied Dynamical Systems*, 10(3), 1070–1099.
- Mirollo, R. E., & Strogatz, S. H. (2005). The spectrum of the locked state for the Kuramoto model of coupled oscillators. *Physica D*, 205, 249–266.
- van Hemmen, J. L., & Wreszinski, W. F. (1993). Lyapunov function for the Kuramoto model of nonlinearly coupled oscillators. *Journal of Statistical Physics*, 72, 145–166.
- Verwoerd, M., & Mason, O. (2008). Global phase-locking in finite populations of phase-coupled oscillators. *SIAM Journal on Applied Dynamical Systems*, 7(1), 134–160.
