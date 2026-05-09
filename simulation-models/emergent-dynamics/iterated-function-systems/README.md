# Iterated Function Systems

This model demonstrates how a small set of contractive functions can generate a stable global form.

The point is not the decorative fractal image. The point is that a global structure can be the attractor of repeated local transformations.

---

## Idea

An Iterated Function System (IFS) consists of affine maps:

```text
x' = a*x + b*y + e
y' = c*x + d*y + f
```

At each step, one map is selected. After many steps, the sampled points converge toward an attractor such as the Barnsley fern or Sierpinski triangle.

No individual point contains the form. The form exists in the operator and its long-run distribution.

---

## Connection to the Repository

| IFS concept | Repository concept |
|:---|:---|
| Contractive map | Constraint on possible trajectories |
| Attractor | Stable identity / stable organism / stable institution |
| Chaos game | Local events revealing global structure statistically |
| Box dimension | Measurable structural complexity |
| Failed convergence | Weak or incoherent constraints |

This is the cleanest mathematical bridge from "fractal architecture" to a measurable proof artifact.

---

## Run

```bash
cd simulation-models/emergent-dynamics/iterated-function-systems
python3 ifs_attractors.py --preset barnsley --points 120000 --output barnsley.png
```

Presets:

- `barnsley`
- `sierpinski`
- `dragon`

The script prints a rough box-counting dimension estimate and writes a PNG.

---

## What It Shows

- repeated local transformations can produce a stable global attractor,
- global form can be measured statistically,
- the generated structure is sensitive to the operator set.

## What It Does Not Show

- that minds are literally fractals,
- that visual self-similarity is enough for intelligence,
- that an attractor alone constitutes consciousness or identity.

The useful claim is narrower: stable form can be a fixed point of constrained iteration.

