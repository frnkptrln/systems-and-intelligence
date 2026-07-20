# Thermodynamic Hardware: A Safety Design Hypothesis

*Status: engineering proposal, not a requirement derived from TEO.*

Digital computers are physical systems. Their abstractions make logic robust to many variations in
voltage, temperature, and device noise; they do not isolate computation from physics. Power limits,
thermal throttling, sensors, firmware, operating systems, and external infrastructure already couple
logical work to a substrate.

The proposal explored here is narrower: safety-critical resource limits may be harder to bypass when
enforcement is placed below the agent software and exposed through a small, auditable interface.
Possible mechanisms include power caps, independent watchdogs, rate limiters, capability hardware,
tamper evidence, and physically separate authorization paths.

Analog, neuromorphic, reversible, and fluctuation-driven computers may offer different energy and
failure characteristics. None is aligned by virtue of being thermodynamic. A device that relaxes to
a low-energy state minimizes a physical energy function chosen by its construction; that function
need not represent ecological viability or human values.

## Evaluation Contract

Compare software-only and lower-layer enforcement under the same threat model. Measure bypass rate,
fail-safe behavior, sensor spoofing, recovery, performance cost, and harm exported to other
substrates. Include failures of the watchdog and the human authorization channel.

The hypothesis gains support if lower-layer constraints reduce successful bypass without introducing
worse common-mode failures. It fails as a necessity claim if equivalent robustness is achieved by a
simpler architecture, or if hardware coupling merely moves the vulnerable policy into sensors and
firmware.

Physics supplies finite limits. Turning selected limits into safe, legitimate control remains a
design and governance problem.
