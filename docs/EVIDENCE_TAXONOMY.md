# Evidence Verifiability Taxonomy

To maintain analytical rigor and prevent misleading interpretations in scientific network forensics, all claims, nodes, and edges are classified into three distinct tiers of verifiability:

## 1. Level 1: Documented Fact [FACT]
* **Definition:** Direct, verifiable primary source evidence exists that is contemporaneously recorded.
* **Example:** "Ron Fouchier and Marion Koopmans participated in the Feb 1, 2020 conference call." 
* **Source:** Page 14 of Dr. Anthony Fauci's diary (Congressional release), listing the participant names.

## 2. Level 2: Source-Derived Claim [CLAIM]
* **Definition:** A claim or summary stated by a specific actor in a source document, representing their personal or contemporary perspective. It is not an independently verified fact.
* **Example:** "Ron Fouchier argued that the furin cleavage site could occur naturally."
* **Source:** Fauci's diary text (p14), summarizing Fouchier's statements. This is Fauci's narrative representation, not a verbatim transcript or scientific proof.

## 3. Level 3: Algorithmic Inference [INFERENCE]
* **Definition:** A categorization or ranking derived mathematically from the network topology or clustering algorithms.
* **Example:** "Marion Koopmans belongs to the 'deliberate insertion' policy community."
* **Source:** Derived dynamically via Louvain/Leiden community detection based on policy-edge co-occurrence. This does *not* represent her actual scientific position or personal views, which remain unrecorded in the primary text.
