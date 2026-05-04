# 🌿 Ecosystem Regulation Models

This folder contains simulations that illustrate **regulation**,  
**stability**, and **homeostasis** in artificial ecosystems.

The central idea is that a system can maintain stable global behavior  
(e.g., population density) through **feedback loops** between local interactions  
and global state measurements.

---

## 📜 Included Models

### **`homeostatic_life.py`**
A modified cellular automaton combining:

- local update rules (B3/S234-like)
- global density feedback
- probabilistic survival at higher neighbor counts
- adaptive birth probability to maintain a target fill ratio

The result is a robust, self-regulating system that maintains stable population
levels while still producing rich local dynamics.

Key concepts:

- Negative feedback
- Emergent robustness
- Controlled activity
- Global–local interaction

Run:

```bash
python3 homeostatic_life.py

