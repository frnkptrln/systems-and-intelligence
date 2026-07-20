# The Substrate Veto: Physical Bounds and Designed Feedback

*Status: control hypothesis built on ordinary physical constraints. Thermodynamics bounds
computation, but it does not by itself align a system or implement a safe veto.*

## 1. What Physics Establishes

Every implemented computation is a physical process. It uses hardware, energy, time, and material
infrastructure, and it ultimately exchanges heat and other waste with an environment. A deployed
optimizer therefore cannot have literally unbounded throughput on a finite substrate.

Landauer's principle gives a lower bound of \(k_B T\ln 2\) for erasing one bit in a logically
irreversible operation at temperature \(T\). It does not say that every logical operation dissipates
exactly that amount, that present computers operate near the bound, or that ecological harm can be
derived from bit erasure alone. Actual power and cooling loads depend on the hardware, algorithm,
error correction, utilization, energy system, and surrounding infrastructure.

The modest physical conclusion is:

> A specified implementation has finite resource and dissipation limits.

It does not follow that reaching those limits is safe. Hardware may fail after causing damage, move
work elsewhere, consume another resource first, or degrade in a way that leaves dangerous actions
running.

## 2. A Model-Relative Capacity

In a TEO toy model, resource use is summarized as

\[
D(\mathbf{x})=\sum_{i=1}^{N}\eta_i x_i f_i(\mathbf{x}),
\]

with a stipulated capacity \(D_{\max}\). Here \(x_i\), \(f_i\), and \(\eta_i\) are model variables;
they are not automatically resource share, fitness, and entropy in every application.

The inequality

\[
D(\mathbf{x})\leq D_{\max}
\]

is a design constraint when a controller enforces it. If the equations merely cause performance to
collapse above the boundary, the result is substrate failure, not a veto. Calling the capacity
thermodynamic is justified only when its units, measurement process, and physical balance are
specified.

There is no single established scalar \(D_{\max}\) for the biosphere. Climate, biodiversity, water,
land, toxic load, and social viability have different dynamics and cannot be collapsed without a
normative aggregation rule.

## 3. From a Limit to a Veto

A functioning substrate veto needs an engineered causal path:

1. measure a declared substrate variable;
2. estimate uncertainty, delay, and failure;
3. compare it with a justified operating envelope;
4. restrict particular actions through an enforcement layer;
5. preserve appeal, repair, and safe shutdown;
6. prevent or detect manipulation of the sensor and enforcement path.

A stylized controller may use

\[
L(u,y)=-R(u)+\alpha\,\phi(y),
\]

where \(u\) is an action, \(R\) a selected reward, \(y\) measured substrate state, and \(\phi\) a
penalty near a boundary. This changes behaviour only if the measurement is relevant, the penalty is
large enough, and the controller cannot bypass or redefine it. Free-energy or surprise vocabulary
does not supply those properties automatically.

## 4. What Transfers Across Scales

Server cooling, electrical grids, ecosystems, institutions, and human attention can all constrain
activity. They do not share identical state variables or equations. A cross-scale application must
name:

- the resource or vital quantity;
- its dynamics and units;
- the actor's influence on it;
- the observation and enforcement channel;
- the acceptable risk and distribution of harm.

The shared abstraction is finite capacity plus feedback, not one universal veto law.

## 5. Evidence and Failure Conditions

The repository simulations show that explicitly coupling a controller to a substrate variable can
bound selected trajectories in selected equations. They do not show that the coupling is
unbreakable or sufficient for alignment.

The design hypothesis is weakened when the constrained controller exports harm, manipulates the
measurement, fails before the limit acts, or performs no better than a simpler resource budget. It
gains support when it preserves preregistered vital variables under matched adversarial tests and
known sensor failures.

For candidate architectural requirements, see [Biological Veto: Architectural
Requirements](biological-veto-architectural-requirements.md). For the model in which the capacity
appears, see [Thermodynamics of Emergent Orchestration](../core/thermodynamics-of-orchestration.md).
