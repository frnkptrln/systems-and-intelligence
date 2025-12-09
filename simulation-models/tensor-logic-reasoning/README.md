# Tensor Logic Reasoning

Kleines Experiment inspiriert von Pedro Domingos' Paper  
**"Tensor Logic: The Language of AI"** und seinem Auftritt bei  
**Machine Learning Street Talk**.

Ziel: Auf minimaler Fläche zeigen, wie

- Fakten (`Parent(Alice, Bob)`)
- Regeln (`Ancestor(x, z)` als transitive Hülle von `Parent`)
- logische Inferenz
- Embeddings
- reasoning im Embedding-Space

in einem gemeinsamen Tensor-Formalismus gedacht werden können.

## Idee

Das Script `tensor_logic_demo.py`:

1. Definiert eine kleine Welt mit vier Entitäten:
   - Alice, Bob, Charlie, David

2. Legt eine `Parent`-Relation als boolsche Matrix an.

3. Berechnet die `Ancestor`-Relation als transitiven Abschluss von `Parent`.

4. Erzeugt zufällige, normierte Embeddings für jede Entität.

5. Baut einen Relationstensor `EmbParent[i, j]`, der
   die Superposition der Tensorprodukte aller Parent-Paare enthält.

6. Beantwortet Queries `Parent(a, b)` auf zwei Arten:
   - **Logisch:** direkt aus der Parent-Matrix
   - **Embedding-basiert:** via

     \[
     \text{score}(a,b) = Emb[a]^T \cdot EmbParent \cdot Emb[b]
     \]

     und einer logistischen Funktion mit Temperatur \(T\).

## Nutzung

```bash
cd simulation-models/tensor-logic-reasoning
python3 tensor_logic_demo.py

