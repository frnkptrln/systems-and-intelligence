Tensor-Logik als einheitliches Modell für symbolisches und kontinuierliches Schließen
Frank Peterlein — 2025

Abstract

Dieses Kurzpapier führt in die Grundidee der Tensor-Logik ein, ein Rahmenwerk von Pedro Domingos, das symbolisches Schließen, neuronale Einbettungen und probabilistische Inferenz in einer einzigen mathematischen Sprache zusammenführt: Tensoralgebra.

Logische Relationen werden zu Booleschen Tensoren.
Logische Regeln werden zu Tensor-Kontraktionen.
Einbettungsvektoren verwandeln diese Relationen in kontinuierliche Operatoren, die zwischen strenger Logik und analogem, graduiertem Schließen vermitteln.

Der zugehörige Python-Code in diesem Repository (simulation-models/tensor-logic-reasoning) zeigt das Konzept anhand einer minimalen Vier-Entitäten-Welt mit einer einfachen Parent-Relation.


# 1. Einleitung

Die aktuelle KI-Landschaft ist von einem grundlegenden Gegensatz geprägt:

Symbolische KI — diskret, regelbasiert, transparent, aber fragil

Neuronale KI — kontinuierlich, gelernt, robust, aber schwer erklärbar

Tensor-Logik legt nahe, dass dieser Gegensatz nicht fundamental ist.
Auf der richtigen Abstraktionsebene gilt:

Relationen, Regeln, Einbettungen und Schlussfolgerungen besitzen dieselbe Tensorstruktur.

Eine logische Regel wie:

Ancestor(x, z) ← Parent(x, y), Parent(y, z)

lässt sich als Tensor-Kontraktion über der Booleschen Adjazenzmatrix der Parent-Relation formulieren.

Dieses Dokument verfolgt drei Ziele:

• die Kernintuition der Tensor-Logik präzise herauszuarbeiten
• sie anhand eines minimalen Experiments zu illustrieren
• sie in einen systemtheoretischen Kontext einzubetten


# 2. Relationen als Tensoren

## 2.1 Symbolische Ebene

Eine binäre Relation R(x, y) über einer endlichen Menge von Entitäten lässt sich als Boolesche Matrix darstellen.

R_xy = 1, wenn das Paar (x, y) in der Relation enthalten ist
R_xy = 0, sonst

Logische Schlussregeln, die in klassischen Logik- oder Datalog-Systemen durch Join- und Projektionsoperationen definiert werden, entsprechen hier algebraischen Operationen auf diesen Matrizen.

Wenn die Parent-Relation als Matrix P_xy dargestellt wird, kann eine einstufige Ancestor-Relation durch Summation über ein gemeinsames Zwischenobjekt y und anschließende Schwellenbildung bestimmt werden.

Durch wiederholte Anwendung entsteht die transitive Hülle der Parent-Relation.

Damit gilt:

Symbolisches Schließen = Boolesche Tensoralgebra.

## 2.2 Kontinuierliche Ebene

Nun sei jede Entität x durch einen Einbettungsvektor Emb[x] in R^d repräsentiert.

In dieser Darstellung kann eine Relation R als reellwertiger Tensor dargestellt werden, indem man für jedes Faktum (x, y) das äußere Produkt Emb[x] ⊗ Emb[y] addiert. Das Ergebnis ist:

Ein Relationstensor = Überlagerung der äußeren Produkte aller beteiligten Einbettungsvektoren.

Jedes einzelne Faktum erzeugt damit einen kleinen „Flecken“ im Tensor.
Die Gesamtrelation ergibt sich als Superposition all dieser Flecken.

Dieses Konstrukt ist eng verwandt mit einer Tucker-Zerlegung:

• die Einbettungsmatrix sammelt alle Emb[x]
• der Relationstensor EmbR spielt die Rolle des Kern­tensors

Die Konsequenz:

Relationen = Superpositionen von äußeren Produkten der Einbettungsvektoren.

Damit ist die erste Brücke zwischen symbolischer und kontinuierlicher Darstellung geschlagen.


# 3. Schlussfolgern im Einbettungsraum

Hat man:

• einen Relationstensor EmbR
• Einbettungsvektoren für alle Entitäten

dann lässt sich für ein Kandidatenpaar (a, b) ein Schlussfolgerungs-Score berechnen:

Score(a, b) = Emb[a]^T · EmbR · Emb[b]

Hohe Scores bedeuten, dass das Paar (a, b) gut mit der im Tensor codierten Struktur der Relation übereinstimmt.
Niedrige oder negative Scores deuten auf mangelnde Kompatibilität hin.

Um diesen Score in eine Wahrscheinlichkeit zu überführen, zieht man einen Basiswert μ (z. B. den mittleren Score über alle Paare) ab und wendet eine logistisches Aktivierungsfunktion mit Temperatur T an:

p(a, b) = σ( (Score(a, b) − μ) / T )

wobei σ(z) = 1 / (1 + exp(−z)).

Die Temperatur T steuert die „Härte“ der Entscheidung:

• T → 0 führt zu einem fast sprunghaften, booleschen Verhalten.
Dies entspricht strengem logischen Schließen.

• Größere T-Werte führen zu weicheren, graduellen Übergängen.
Ähnlichkeiten und fast-passende Muster werden dann noch teilweise akzeptiert.

Die zentrale Einsicht lautet daher:

Schlussfolgern = ähnlichkeitssensitive Tensor-Kontraktion mit Temperatur.

Strikte Logik erscheint als Spezialfall der Tensoralgebra, wenn T gegen Null geht.


# 4. Mini-Experiment: Eine Vier-Entitäten-Welt

Das Skript simulation-models/tensor-logic-reasoning/tensor_logic_demo.py konstruiert eine minimale Welt mit vier Entitäten:

• Alice
• Bob
• Charlie
• David

und der linearen Abstammungskette:

Alice → Bob → Charlie → David

Dies führt zu folgenden Fakten in der Parent-Relation:

Parent(Alice, Bob)
Parent(Bob, Charlie)
Parent(Charlie, David)

Das Skript führt anschließend die folgenden Schritte aus:

Aufbau der Booleschen Matrixdarstellung der Parent-Relation.

Berechnung der logischen Ancestor-Relation durch Bildung der transitiven Hülle.

Erzeugung zufälliger, normierter Einbettungen für alle vier Entitäten.

Konstruktion des Relationstensors EmbParent durch Überlagerung der äußeren Produkte.

Bewertung verschiedener Parent-Anfragen mittels:
• rein logischem Lookup (0 oder 1)
• embedding-basiertem Score
• Wahrscheinlichkeit über eine Logistikfunktion mit Temperatur

Ein exemplarisches Ergebnis eines typischen Durchlaufs (zentrische Scores, T = 1.0):

Parent(Alice, Bob):
– Logischer Wahrheitswert = 1
– Zentrierter Score = +0.54
– Wahrscheinlichkeit ≈ 0.63

Parent(Bob, Charlie):
– Logischer Wahrheitswert = 1
– Zentrierter Score = +0.62
– Wahrscheinlichkeit ≈ 0.65

Parent(Alice, Charlie):
– Logischer Wahrheitswert = 0
– Zentrierter Score = +0.29
– Wahrscheinlichkeit ≈ 0.57

Parent(Alice, David):
– Logischer Wahrheitswert = 0
– Zentrierter Score = −0.18
– Wahrscheinlichkeit ≈ 0.46

Interpretation:

• Direkte Eltern-Kind-Paare erhalten die stärksten positiven Scores.
• Indirekte Abstammungsbeziehungen (z. B. Alice → Charlie) erzeugen immer noch einen positiven Score — ein Hinweis auf latente Struktur, die im strikten Parent-Prädikat verborgen bleibt.
• Nicht gestützte Paare liegen nahe der Basislinie oder darunter.

Damit zeigt dieses kleine Beispiel bereits die Kernintuition der Tensor-Logik:
symbolische Struktur erscheint als emergentes Muster geometrischer Ausrichtung im Einbettungsraum.


# 5. Eine systemtheoretische Perspektive

Die Tensor-Logik erlaubt es, intelligentes Verhalten aus der Sicht der Systemtheorie neu zu interpretieren.
Anstatt Intelligenz in einzelnen Komponenten zu lokalisieren — beispielsweise in:

• symbolischen Regeln, oder
• neuronalen Gewichten —

verschiebt sich der Fokus auf die Interaktionen zwischen Strukturen, Zuständen und Operationen.

Tensor-Logik lässt sich in drei Bausteine zerlegen:

Einbettungen (Embeddings)
Sie repräsentieren die möglichen Zustände oder Identitäten eines Systems.

Relationstensoren
Sie kodieren die strukturellen Kopplungen, Abhängigkeiten und Beschränkungen zwischen diesen Zuständen.

Kontraktionsoperationen
Sie definieren die Dynamik der Informationsverarbeitung:
wie Zustände kombiniert, projiziert oder weitergegeben werden.

Aus dieser Perspektive entsteht Schlussfolgern nicht in den Einbettungen selbst
und nicht im Tensor allein,
sondern in deren Kopplung — genau dort, wo Systeme sich berühren.

In den Worten der Systemtheorie:

Intelligenz ist eine emergente Eigenschaft der relationalen Struktur eines Systems.

Die Tensor-Logik liefert hierfür eine präzise mathematische Form:

• Struktur = Relationstensor
• Zustand = Einbettungsvektor
• Dynamik = Kontraktionen
• Beobachtung = Score oder Entscheidung

Die beobachtbare „Vernunft“ ist also eine Projektion dieser tieferen Kopplungsdynamik.

Damit lässt sich Tensor-Logik auch als Brückentechnologie verstehen:
Sie verbindet formale Logik, geometrische Repräsentationen und systemtheoretische Konzepte in einer einheitlichen Sprache.


# 6. Schlussfolgerung

Die Tensor-Logik bietet eine einheitliche mathematische Perspektive, in der symbolisches und neuronales Schließen nicht als Gegensätze erscheinen, sondern als zwei Regime desselben Mechanismus.

Ihre Grundideen lassen sich so zusammenfassen:

Logische Relationen sind Boolesche Tensoren.

Logische Regeln entsprechen spezifischen Mustern von Tensor-Kontraktionen.

Einbettungen faktorisieren diese Tensoren in kontinuierliche Räume.

Temperaturgesteuerte Aktivierungsfunktionen vermitteln zwischen strenger Logik und graduierter Analogie.

Der scheinbare Gegensatz zwischen Symbolik und Neuronik ist daher nicht fundamental.
Stattdessen entsteht Logik als Grenzfall kontinuierlicher Tensoralgebra, wenn die Temperatur gegen Null geht.

Tensor-Logik wird damit zu einem potenziellen Rahmen für zukünftige KI-Systeme:

• streng genug für logische Strukturen
• flexibel genug für analoges Denken
• mathematisch kohärent über beide Welten hinweg

Mögliche Erweiterungen umfassen:

• Lernen der Einbettungen direkt über Tensor-Logik-Optimierungsziele
• Umgang mit höherstelligen Relationen oder zeitlicher Dynamik
• adaptive, kontextabhängige Temperaturen
• Verbindung zu ökologischen, agentenbasierten oder zirkulären Systemen
• Integration in bestehende Architekturen wie Transformer, GFlowNets oder differentiable logic systems

Tensor-Logik dient somit als Brücke — zwischen Logik, Geometrie und Systemtheorie.

Appendix: Kontext im Repository

Dieses Mini-Paper gehört zum systems-and-intelligence-Projekt.

Relevante Dateien:

• theory/tensor-logic-mini-paper.de.md — diese Datei
• theory/tensor-logic-mini-paper.en.md — englische Version
• theory/tensor-logic-visual.html — interaktive HTML-Visualisierung
• simulation-models/tensor-logic-reasoning/ — Python-Implementierung des Beispielmodells

Die Struktur verfolgt das Ziel, Theorie, Simulation, Visualisierung und systemtheoretische Einordnung in einem konsistenten Rahmen zu verbinden.
