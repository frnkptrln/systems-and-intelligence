# Tensor Logic Reasoning

A small experiment inspired by Pedro Domingos' paper  
**"Tensor Logic: The Language of AI"** and his appearance on  
**Machine Learning Street Talk**.

Goal: Show on minimal surface area how

- Facts (`Parent(Alice, Bob)`)
- Rules (`Ancestor(x, z)` as the transitive closure of `Parent`)
- Logical inference
- Embeddings
- Reasoning in embedding space

can be thought of within a unified tensor formalism.

## Concept

The script `tensor_logic_demo.py`:

1. Defines a small world with four entities:
   - Alice, Bob, Charlie, David

2. Creates a `Parent` relation as a boolean matrix.

3. Computes the `Ancestor` relation as the transitive closure of `Parent`.

4. Generates random, normalized embeddings for each entity.

5. Builds a relation tensor `EmbParent[i, j]` containing
   the superposition of tensor products of all Parent pairs.

6. Answers queries `Parent(a, b)` in two ways:
   - **Logical:** directly from the Parent matrix
   - **Embedding-based:** via

     \[
     \text{score}(a,b) = Emb[a]^T \cdot EmbParent \cdot Emb[b]
     \]

     and a logistic function with temperature \(T\).

## Usage

```bash
cd simulation-models/tensor-logic-reasoning
python3 tensor_logic_demo.py

