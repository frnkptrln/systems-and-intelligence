# Symbiotic Breathing Toy Simulation

*Status: designed comparison between two compute schedules. It is not evidence that a real agent
will discover the schedule, that the schedule is uniquely optimal, or that "true symbiosis" has
been achieved.*

## Question

Can alternating periods of high and low activity keep a slow-recovering substrate within a selected
health range while still allowing useful work? The script represents this as a coupled dynamical
system with a compute-rate variable $\gamma$ and a host-health variable.

The language of **cognitive breathing** names the periodic schedule. The TEO dissipation limit
$D_{\max}$ supplies a model parameter, not a measured universal capacity. References to a
"Gödelian agent" in earlier versions were metaphorical: Gödel's incompleteness theorems do not imply
that an agent will recognize substrate limits or choose cooperation.

## Compared Conditions

1. **Monotone schedule:** compute demand rises according to the stipulated rule, and host health falls
   in the selected parameter regime.
2. **Oscillating schedule:** compute alternates between active and recovery periods, and host health
   approaches a bounded rhythm in that regime.

The second outcome follows from a schedule designed around the recovery equation. A fair follow-up
should match total work, vary delays and noise, sweep parameters, compare adaptive non-periodic
controllers, and test failure when the health signal is wrong or manipulable.

## Run

```bash
python symbiotic_breathing.py
```

The script writes `symbiosis_plot.png`. Read the image as a demonstration that rate scheduling can
alter trajectories in this toy model—not as a biological or governance theorem.
