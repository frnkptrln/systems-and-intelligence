# P vs NP as Generator Search (Framing Note)

Status: Working Note
Scope: Careful bridge between complexity-theoretic witness search and trace-to-generator reconstruction.
Epistemic status: Formal analogy constrained to search/verification structure; not a proof claim.
Related files:
- theory/reference/open-problems.md
- theory/emergence/trace-to-generator.md
- theory/core/emergence-manifesto-v1.3.md
Failure conditions:
- Any statement implying the repository solves P vs NP.
- Mapping complexity results directly to identity/explanation claims.

For SAT:
- Instance: Boolean formula F (the trace-like constraint object).
- Witness/certificate: assignment w.
- Verification: check F(w)=true efficiently.
- Construction/search: find such w.

If P=NP, efficient search exists whenever efficient verification exists (for NP languages).  
If P≠NP, some witnesses may remain efficiently verifiable but not efficiently findable.

Why many witnesses are fine: complexity asks whether **some** valid witness can be found efficiently, not whether the witness is unique.

Why this differs from explanation/identity:
- A satisfying assignment can verify a formula without being a unique causal history.
- Engineering explanations often require runtime context, robustness, and continuity constraints beyond satisfiability.

Why this does not settle replicator/transporter debates:
- Ordinary replication often executes known descriptions; it does not require universal inverse search.
- Even if efficient witness search existed, that would not by itself resolve continuity-of-identity constraints in transporter scenarios.

Caution: this note does not prove or disprove P vs NP and does not reduce intelligence to that question.

> **Related work.** The cost of generator search is formalized in Levin's universal search (1973). Practical generator recovery in *constrained* spaces is the working subject of program induction — Lake, Salakhutdinov & Tenenbaum (2015, Bayesian Program Learning), Ellis et al. (2021, DreamCoder) — and of open-ended symbolic regression (Schmidt & Lipson, 2009; Cranmer's PySR, 2023); Chollet (2019) frames intelligence measurement around exactly this search efficiency. The repo-internal counterpart is the [inverse-reconstruction benchmark](../../lab/benchmarks/inverse-reconstruction/README.md); the concept-by-concept mapping lives in the [Related Work Map](../../meta/research-alignment/related-work-map.md).
