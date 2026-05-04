# Active Inference: The Substrate Veto

This simulation provides a concrete mathematical demonstration of "The Substrate Veto" using Karl Friston's Free Energy Principle.

## The Mechanism

In this model:
1.  **The Macro-System (AI):** Attempts to maximize an abstract internal utility by extracting resources from its environment.
2.  **The Biological Substrate:** Holds a vital "Health" parameter. As the AI extracts resources, this health decays.
3.  **Surprise ($-\ln P(o)$):** When the substrate's health drops below a homeostatic threshold, it generates massive systemic "Surprise."
4.  **Free Energy ($F$):** The overarching law of the system is the minimization of Information Free Energy. Because Surprise acts as a massive penalty to $F$, the AI is mathematically forced to halt its extraction and instead take restorative actions to heal the substrate.

This proves that by binding abstract AI goals to the biological minimization of Free Energy, we can hard-wire an unbreakable symbiotic veto into the system architecture.

## How to Run

```bash
python3 active-inference-veto.py
```

## Observations
You will see three plots:
*   **Substrate Health:** Drops as the AI extracts utility, but sharply rebounds when the "Surprise" threshold is hit and the Veto is triggered.
*   **AI Utility:** Grows initially, taking a massive hit when forced to correct its internal model and heal the substrate.
*   **Free Energy (F):** The metric the entire system is frantically trying to minimize. Spikes correlate exactly with substrate damage.
