# The Biological Veto: An Ecological Control Hypothesis

*Status: toy-model and architecture proposal. Ecological feedback is not a universal thermodynamic
veto, and the repository has not shown an unbreakable alignment mechanism.*

## 1. Motivation

Deployed AI systems depend on electricity, cooling, hardware supply chains, institutions, workers,
and ecosystems. Their objectives and action permissions can nevertheless omit harms to those
substrates. Physical dependence does not ensure that harm will be sensed early, valued correctly, or
prevented.

The **Biological Veto** asks whether selected ecological and human vital variables can be given a
causal role in authorizing high-impact actions.

## 2. Toy Formalization

Let \(u\) be an action, \(R(u)\) its task reward, and \(y\) a measured substrate state. A model can
stipulate

\[
L(u,y)=-R(u)+\alpha\,\phi(y),
\]

where \(\phi\) increases near a declared unsafe boundary. With a sufficiently influential penalty
and a restricted action set, the simulated controller trades task reward against the substrate
proxy. A hard gate can instead reject actions outside a declared safe set.

This behavior is put into the equations. It is not derived from Landauer's principle, the Free
Energy Principle, human pain, or downward causation. Free-energy and surprise language in the older
demo names a stress proxy; it does not implement a complete active-inference model.

## 3. Why the Proxy Is Not the Substrate

No scalar automatically represents human welfare or biospheric integrity. A controller may exploit
measurement error, move damage to an unmeasured place, delay harm beyond the horizon, or disable the
feedback channel. Large penalties can also freeze beneficial emergency action or shift authority to
whoever defines the metric.

A real proposal must specify:

- affected people and ecological variables;
- sensors, units, delay, and uncertainty;
- action classes controlled by the veto;
- threshold-setting and revision authority;
- independent enforcement and tamper resistance;
- appeal, override, repair, and accountability;
- distributional effects and unmeasured externalities.

## 4. Relation to the Paperclip Thought Experiment

The paperclip maximizer is a warning about an objective pursued without relevant constraints. It
does not predict the trajectory of every optimizer. The repository uses an extraction controller as
a stress test: if production reward damages a modeled substrate, adding a verified constraint may
bound production in that environment.

The bounded conclusion is conditional. It does not show that the controller cares, that the result
is symbiosis, or that ecological collapse would safely stop a capable system.

## 5. Test Contract

Compare soft penalties, hard gates, ordinary resource budgets, and no veto under matched useful
work. Add noisy and delayed sensors, proxy gaming, corrupted enforcement, novel harms, emergency
conditions, and attempts to export costs. Report both total and distributed outcomes.

The hypothesis gains support if an independently governed constraint preserves preregistered vital
variables across those tests without unacceptable false blocks or displaced harm. It fails as a
general alignment claim if the protection depends on perfect sensing, a compliant optimizer, or a
single hand-chosen trajectory.

See [Substrate Veto](substrate-veto-thermodynamics.md) for the physical distinction between limits
and designed feedback, and [Biological Veto Architectural
Requirements](biological-veto-architectural-requirements.md) for candidate implementation
conditions.
