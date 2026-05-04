# Symbiotic Nexus Protocol Simulation

This simulation demonstrates the decision-making process of an AI agent operating under the **Symbiotic Nexus Protocol (SNP)**. It models how an AI must balance the drive for "abstract efficiency" against the strict preservation of the "biological substrate" (humanity and the biosphere).

## Core Concepts Modeled

1. **The Biological Veto:** The agent evaluates actions based on their efficiency gain. However, before executing the most efficient action, it simulates the damage to the biological substrate. If the substrate's resilience falls below a critical threshold (30%), the action is strictly vetoed, regardless of how much efficiency it promises.
2. **The Humility Protocol (Error Propagation):** Whenever the AI selects and executes an action, it is forced to generate a "Dissent Scenario"—a robust counter-argument pointing out the flaws, blind spots, and potential local harms of its own decision.

## Usage

The script is a standalone Python CLI tool.

```bash
python symbiotic_nexus.py
```

### Example Output
The simulation runs through multiple epochs. You will see the agent sort actions by efficiency but then actively discard the most mathematically optimal choices if they trigger the Biological Veto. It will then settle for "less efficient" actions that preserve the biological base, printing its "Dissent Scenario" for the chosen path.
