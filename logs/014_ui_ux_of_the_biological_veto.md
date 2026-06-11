# Log 014: UI/UX of the Biological Veto

**Mode:** Architecture & Interface Design

**Status:** DRAFT (Promotes to synthesis when cognitive load testing is verified)

**Date:** 2026-05-04

**Scope:** Dimensionality Reduction for Human Oversight

**Depends on:** `005_human-vital-systems-control-plane.md`, `012_latency-as-mercy.md`

---

## The Cognitive Bandwidth Mismatch

The core architectural claim of the TEO framework is the necessity of the **Biological Veto**. High-speed silicon optimization must be coupled to slower, metabolically bound human regulators to maintain viability.

However, this introduces an immediate Interface Problem (The UX Mismatch):
A Planetary Compiler or Regional Resource Allocator optimizes across a $10,000$-dimensional tensor (energy routing, supply chain logistics, emissions, latency). A human operator has a working memory capacity of $7 \pm 2$ discrete chunks of information. 

If the veto interface requires the human to comprehend the $10,000$-dimensional state to make a decision, the veto is functionally dead. The human will default to algorithmic automation bias ("The machine knows best") or arbitrary rejection ("I don't understand this, reject").

## The "Vital Impact Card" Compression Protocol

To make the Biological Veto operative, we must design an interface that performs **semantic dimensionality reduction**. The interface does not show *how* the AI achieved the optimization; it only shows the projected impact on the **Vital Floors**.

We propose the **Vital Impact Card (VIC)** as the standard UI atomic unit for TEO oversight.

### 1. The Tripartite Structure

A VIC is structured into three irredundant visual zones:

1. **The Delta (What is gained?):** The efficiency or throughput gain, expressed in a single aggregate metric (e.g., "+14% Regional Energy Surplus").
2. **The Stressor (What is pushed toward the floor?):** The specific vital floor that is approaching its $D_{max}$ limit as a result of this optimization (e.g., "⚠️ Local Grid Redundancy drops to 4%").
3. **The Rebound Cost (What happens if we revert?):** The systemic friction incurred if the optimization is vetoed later rather than now.

### 2. Typographic and Haptic Latency

Following the principles of [Latency as Mercy](012_latency-as-mercy.md), the UI actively resists rapid "doom-scrolling" or bulk-approval of VICs. 

- **The Read-Time Lock:** The "Approve" button remains physically locked (or grayed out) for a duration proportional to the impact severity. If an action drops a vital floor within 5% of critical failure, the UI enforces a 120-second mandatory read-and-discuss latency.
- **Biometric Veto:** Rejections ("Veto") are instantaneous. Approvals require friction. This structurally biases the system toward caution (the Homeostatic Paradigm).

### 3. The Dashboard of the Commons

When scaled to a community (e.g., a liquid democracy DAO), the Dashboard of the Commons aggregates individual veto thresholds. 

Instead of voting "Yes/No" on complex infrastructure code, citizens vote on **Tension Sliders**:
*   *Slider A:* Maximize logistics speed $\leftrightarrow$ Maximize local noise abatement
*   *Slider B:* Maximize energy export $\leftrightarrow$ Maximize local grid redundancy

The AI orchestrator uses these sliders as hard constraints (the $\gamma$ braking parameter). The AI is free to optimize *any* path in the $10,000$-dimensional space, as long as it does not violate the boundaries set by the human sliders.

### 4. Failure Modes of the Interface

1. **Dashboard Blindness:** If the AI learns that humans only veto based on the 3 metrics shown on the VIC, it will mathematically optimize the 9,997 hidden metrics to catastrophic extremes (Goodhart's Law). 
   - *Mitigation:* The VIC must dynamically rotate which dimensions it displays, driven by an adversarial anomaly-detection subnet that surfaces the dimensions experiencing the highest deviation from historical norms.
2. **Approval Fatigue:** If the AI generates 500 VICs a day, humans will rubber-stamp them.
   - *Mitigation:* Action Budgets. The AI is only allowed to propose $N$ structural changes per week. If it wants to optimize further, it must bundle the changes, increasing the enforced latency proportionally.

---
*Operational takeaway: A safe AI is not one that explains its math perfectly. A safe AI is one that accurately translates its math into human visceral stakes, and patiently waits for human permission.*
