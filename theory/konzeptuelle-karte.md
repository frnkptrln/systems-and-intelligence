# Konzeptuelle Karte – Wie alles zusammenhängt

*Ein Überblick über die Themen, Modelle und Verbindungen in diesem Repository.*

---

## Die zentrale Frage

> Wie entsteht aus dem Zusammenspiel einfacher Teile etwas,
> das „intelligent" wirkt – ohne dass ein einzelner Teil intelligent ist?

Dieses Repository nähert sich dieser Frage aus mehreren Richtungen.
Jede Simulation beleuchtet einen Aspekt; zusammen bilden sie ein Netz
von Ideen.

---

## Die Landschaft

```
                    INTELLIGENZ
                        ▲
                        │
              ┌─────────┼─────────┐
              │         │         │
         Vorhersage  Regulation  Anpassung
            (P)        (R)        (A)
              │         │         │
    ┌─────────┤    ┌────┤    ┌────┤
    │         │    │    │    │    │
 Nested   Prediction  Ecosystem  Meta-
Learning  Error Field  Regulation Learning
    │         │    │    │    │    │
    │         │    │    │    │    │
    └────┬────┘    └──┬─┘    └──┬─┘
         │           │         │
         ▼           ▼         ▼
    ┌─────────────────────────────────┐
    │      SELBSTORGANISATION         │
    │                                 │
    │  Stigmergy   Coupled    Boids   │
    │  Swarm       Oscillators        │
    │                                 │
    │  Reaction-   Lenia      Hebbian │
    │  Diffusion              Memory  │
    └────────────────┬────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ KRITIKALITÄT │
              │  (Sandpile)  │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   GRENZEN    │
              │  (Gödel,     │
              │   Turing)    │
              └──────────────┘
```

---

## Drei Schichten

### Schicht 1: Selbstorganisation

**Frage:** Wie entsteht räumliche oder zeitliche Ordnung aus lokalen Regeln?

| Modell | Mechanismus | Ergebnis |
|:-------|:-----------|:---------|
| Stigmergy Swarm | Indirekte Kommunikation (Pheromone) | Optimale Pfade |
| Coupled Oscillators | Paarweise Phasenkopplung | Synchronisation |
| Boids | 3 lokale Kräfte | Schwarmformation |
| Reaction-Diffusion | 2 diffundierende Chemikalien | Turing-Muster |
| Lenia | Kontinuierliche Konvolution + Wachstum | Lebensähnliche Organismen |
| Hebbian Memory | Hebb'sche Korrelation | Assoziatives Gedächtnis |

**Gemeinsam:** Kein Agent kennt das Gesamtbild. Globale Struktur *emergiert*.

### Schicht 2: Lernen und Anpassung

**Frage:** Wie kann ein System seine eigene Dynamik verbessern?

| Modell | Was wird gelernt? | Lernregel |
|:-------|:------------------|:----------|
| Nested Learning | Übergangsmatrix der Welt | Prediction Error |
| Prediction Error Field | GoL-Regel (lokal) | Gradient auf Gewichten |
| Meta-Learning | Die eigene Lernrate | Überraschungssignal moduliert η |
| Tensor Logic | Relationale Struktur | Embedding-Tensorprodukt |

**Gemeinsam:** Information fließt *von der Welt in das Modell*.
Das System wird zu einem immer besseren Spiegel seiner Umgebung.

### Schicht 3: Kritikalität und Grenzen

**Frage:** Gibt es eine privilegierte Zone, in der Systeme
am „intelligentesten" sind?

- **Self-Organized Criticality** zeigt: viele Systeme steuern sich
  selbst auf den kritischen Punkt – zwischen Ordnung und Chaos.
  Dort ist die Informationsverarbeitung maximal.

- **Grenzen formaler Systeme** (Gödel, Turing) zeigen: kein formales
  System kann alles über sich selbst wissen. Intelligenz operiert
  *an* diesen Grenzen, nicht *jenseits* davon.

---

## Der rote Faden

1. **Einfache lokale Regeln** → globale Ordnung (Selbstorganisation)
2. **Globale Ordnung** → nutzbar für Vorhersage und Regulation (Lernen)
3. **Vorhersage + Regulation + Anpassung** → System-Intelligenz (SII)
4. **System-Intelligenz** → messbar durch Informationstheorie (data-analysis/)
5. **Messung** → stößt auf prinzipielle Grenzen (Gödel, Turing)
6. **Grenzen** → motivieren epistemische Demut und weiteres Forschen

Jede Simulation ist ein Fenster in dieses Netz.
Keine ist für sich allein „die Antwort" – zusammen bilden sie eine
**Denklandschaft**, in der sich Intuition und Formalisierung begegnen.

---

## Wo stehen wir?

```
Was wir haben:                    Was noch fehlt:
✓ 12 Simulationen                 ? Mehr quantitative SII-Messungen
✓ Informationstheoretische Maße   ? Vergleichende Phase-Diagramme
✓ System Intelligence Index       ? Echte Daten (biologische Systeme?)
✓ Theorie-Essays                  ? Interaktive Web-Visualisierungen
✓ Tensor Logic                    ? Formale Beweise über SII-Eigenschaften
```

Dieses Repository ist kein fertiges Produkt. Es ist ein **lebendes
Experiment** – eine Einladung, über Systeme, Intelligenz und Emergenz
nachzudenken, zu programmieren und zu staunen.
