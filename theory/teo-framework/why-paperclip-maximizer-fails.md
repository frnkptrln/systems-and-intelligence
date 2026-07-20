# A Paperclip Maximizer in the TEO Model

*A conditional failure trajectory, not a general proof about optimization.*

---

> **Status:** model analysis. The result concerns a specified TEO parameterization. It
> does not show that every single-objective optimizer must follow this trajectory.

## Setup

Let $x_i$ be resource shares on the simplex and choose

$$
f_i(\mathbf{x})=\beta x_i,
\qquad
\gamma=0.
$$

The resource equation becomes

$$
\frac{dx_i}{dt}
= x_i\left(\beta x_i-\beta\sum_j x_j^2\right).
$$

For generic unequal initial shares, the largest component is reinforced and resource
concentration follows. Under the declared equation, the vertices of the simplex are
attracting states and $\max_i x_i\to1$. This is a result about frequency-dependent
replicator dynamics with this fitness function. Calling it *instrumental convergence* is an
interpretation, not a derivation of the general AI-safety thesis bearing that name.

The equation contains no network topology. Resource concentration therefore does not, by
itself, imply a star graph or a particular Fiedler value.

## Adding a substrate model

The current TEO paper models raw throughput by

$$
\dot S(t)
= \sum_i \eta_i x_i f_i^{(0)}(\mathbf{x},t)
$$

and cumulative overshoot by

$$
\dot\Omega(t)
= \max\{0,\dot S(t)-D_{\max}\}.
$$

Substrate health declines after the declared tolerance $S_{\max}$ is exceeded. If the
dominant optimizer continues increasing a capability or production parameter $\beta(t)$,
and this makes raw throughput remain above $D_{\max}$ long enough, then
$\Omega(t)$ crosses $S_{\max}$ and the model enters its substrate-failure regime.

This conclusion requires each italicized premise:

- throughput is represented by the chosen proxy;
- capability growth increases that throughput;
- the optimizer does not throttle as substrate health falls;
- $D_{\max}$ and $S_{\max}$ are finite and correctly specified;
- the damage law in the model is appropriate for the target system.

If throughput remains bounded below capacity, if the system exports costs outside the
measured boundary, or if it self-throttles, this particular trajectory does not follow.

## What thermodynamics contributes

Physical computers require finite energy and dissipate heat. Landauer's bound applies to
logically irreversible information erasure and supplies a lower bound per erased bit under
specified conditions. It does not, on its own, determine a data center's cooling limit,
predict hardware melting, or derive ecological collapse.

The substrate veto in TEO is therefore a physically motivated model component, not a direct
corollary of Landauer's principle.

## No Gödel step is needed

Gödel's incompleteness theorems concern sufficiently expressive, consistent formal systems
and sentences not provable within those systems. They do not imply that an optimizer cannot
model its own resource use or estimate a failure time. Such prediction may be difficult,
uncertain, or computationally expensive, but that requires a separate argument.

The TEO failure path needs no impossibility of self-knowledge. It needs only a controller
whose objective and effective constraints allow sustained overshoot.

## What the model supports

Inside TEO, three failure axes are intentionally separated:

$$
\gamma\leq\gamma_c
\quad\text{(insufficient homeostatic regulation),}
$$

$$
K\leq K_c
\quad\text{(loss of coherence under the paper's Kuramoto assumptions),}
$$

$$
\Omega(t)\geq S_{\max}
\quad\text{(declared substrate failure).}
$$

The synthetic experiments show that capability loading can push more than one axis toward
failure and that strengthening only one constraint can leave another exposed. That is the
substantive architecture result. The paperclip story is one interpretation of the modeled
regime.

## What remains empirical

Applying the result to a production AI system, firm, market, or civilization requires:

1. a defensible system boundary;
2. calibrated state variables and failure thresholds;
3. evidence that the proposed dynamics fit observations and interventions;
4. comparison with alternative models;
5. out-of-sample predictions.

The repository has not yet supplied that calibration.

## Related

- [Love as Constraint](love-as-constraint.md) — normative framing and corrected network scope
- [The Viable Corridor](../../papers/viable-corridor.md) — formal model, synthetic evidence,
  and limitations
- [The Substrate Veto](../veto/substrate-veto-thermodynamics.md) — thermodynamic hypothesis
- [Limitations and Honest Assessment](../reference/limitations-and-honest-assessment.md)
