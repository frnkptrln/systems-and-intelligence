# 🧠 systems-and-intelligence

Dieses Repository ist eine Sammlung von Projekten, die sich mit **komplexen adaptiven Systemen (CAS)**, **emergenter Intelligenz** und **Selbstregulierung** in Software- und Simulationsmodellen beschäftigen. Der Fokus liegt darauf, zu verstehen, wie einfache Regeln zu komplexem, intelligentem oder stabilen globalen Verhalten führen können.

## 📂 Struktur des Repositories

| Ordner | Beschreibung |
| :--- | :--- |
| `simulation-models/` | Projekte, die ökologische oder physikalische Prozesse simulieren, um emergentes Verhalten zu untersuchen. |
| `neural-networks/` | Implementierungen von neuronalen Netzen und Lernalgorithmen. |
| `data-analysis/` | Tools und Skripte zur Analyse der Ergebnisse der Simulationsmodelle. |
| `tools/` | Hilfsskripte oder -bibliotheken zur Visualisierung oder Verarbeitung. |

---

## 🔬 Hervorgehobenes Projekt: Ökosystem-Regulierung

**Pfad:** `simulation-models/ecosystem-regulation/`

Dieses Projekt demonstriert die **Homeostase** in einem zellulären Automaten. Es erweitert das klassische *Game of Life* um einen globalen Feedback-Mechanismus, der die Population des Systems auf einem vordefinierten Füllgrad hält, während lokale, komplexe Dynamiken (Wachstum und Zerfall von Mustern) beibehalten werden.

### 📜 Das Modell: Robuste Dynamik (B3/S234 Mod.)

Das Skript `homeostatic_life.py` verwendet eine modifizierte Regel, um eine langanhaltende, aber stabile Aktivität zu gewährleisten, die einem Ökosystem ähnelt.

#### Regeln

| Zustand | Nachbar-Anzahl | Ergebnis (Nächste Generation) |
| :---: | :---: | :---: |
| **Lebende Zelle** (`#`) | $2$ oder $3$ | Überlebt (100% Chance) |
| **Lebende Zelle** (`#`) | $4$ | Überlebt mit $50\%$ Wahrscheinlichkeit |
| **Lebende Zelle** (`#`) | $<2$ oder $>4$ | Stirbt (Unter-/Überbevölkerung) |
| **Leere Zelle** (` `) | $3$ | Geburt, **aber nur mit dynamischer Wahrscheinlichkeit** ($P_{Geburt}$) |

#### Homeostase-Mechanismus

Die Wahrscheinlichkeit einer Geburt ($P_{Geburt}$) wird in jeder Generation dynamisch angepasst. Dies ist der Mechanismus zur Selbstregulierung:

$$
P_{Geburt} = \text{max} \left( 0.0, \text{min} \left( 1.0, \text{BASE\_BIRTH\_PROB} + \text{ADJUST\_FACTOR} \cdot (TARGET\_FILL - \text{Füllgrad}) \right) \right)
$$

* Ist der **Füllgrad zu niedrig**, steigt $P_{Geburt}$.
* Ist der **Füllgrad zu hoch**, sinkt $P_{Geburt}$.

---

## 🚀 Installation & Ausführung

### Voraussetzungen
Stellen Sie sicher, dass Sie Python 3 installiert haben. Es sind keine externen Bibliotheken erforderlich.

### Ausführung der Homeostase-Simulation

```bash
cd simulation-models/ecosystem-regulation
python3 homeostatic_life.py
