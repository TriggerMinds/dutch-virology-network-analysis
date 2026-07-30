# Evidence Verifiability Taxonomy & 4-Axis Qualification Framework

**Status:** TEAMDYNAMICA v1.5 Compliant  
**Date:** 30 July 2026

To maintain analytical rigor and prevent misleading interpretations in scientific network forensics, all claims, nodes, edges, and dossier entries are evaluated across three verifiability tiers and qualified along four forensic axes.

---

## 1. Verifiability Tiers

### Level 1: Documented Fact [FACT]
* **Definition:** Direct, verifiable primary source evidence exists that is contemporaneously recorded with cryptographic provenance (SHA-256) and verified HTTP 200 OK linkability.
* **Example:** "Ron Fouchier and Marion Koopmans participated in the Feb 1, 2020 teleconference."
* **Source:** Page 14 of Dr. Anthony Fauci's diary (Congressional release), listing participant names (`2026.07.24_Tonys-Diary-Package.pdf`, SHA-256: `27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e`).

### Level 2: Source-Derived Claim [CLAIM]
* **Definition:** A statement or summary recorded by an actor in a source document, representing their contemporary perspective.
* **Example:** "Fouchier and Koopmans provided substantive feedback on early drafts of Proximal Origin and argued against lab-origin phrasing."
* **Source:** USRTK FOIA dump (`Proximal-Origin-Democratic-Staff-Report-Emails.pdf`, SHA-256: `3e1990e8d6197244a342e84fea2afd0250d4434f1fcf080c4d47dafd371f84ae`).

### Level 3: Algorithmic Inference [INFERENCE]
* **Definition:** A categorization or ranking derived mathematically from the network topology, centrality metrics, or clustering algorithms.
* **Example:** "Arfan Ikram has the highest betweenness centrality (0.4344) in the co-authorship network."
* **Source:** Calculated via NetworkX MultiGraph betweenness centrality algorithms on `data/graph.json`.

---

## 2. The 4-Axis Forensic Qualification Framework

When a finding requires precise calibration to prevent overclaim or false balance, the analist or AI must explicitly state which of the four forensic axes is impacted:

1. **Axis 1: Intentie (Intent)**  
   - *Question:* Was the action driven by explicit premeditated intent, institutional self-preservation, or unconscious scientific reflex?  
   - *Rule:* Do not assume malicious intent when institutional risk-aversion or research-interest protection explains the behavior.

2. **Axis 2: Causaliteit (Causality)**  
   - *Question:* Did the action directly cause the outcome, or did it function as an influential contributing factor?  
   - *Rule:* Distinguish between "steering/controlling" a document vs. "providing substantive expert feedback that contributed to shaping the text".

3. **Axis 3: Verantwoordelijkheid (Responsibility)**  
   - *Question:* Was the actor an executive decision-maker, a formal co-author, or an external expert consultant?  
   - *Rule:* Do not attribute formal co-authorship or editorial authority to external commentators who were not listed on the final manuscript.

4. **Axis 4: Timing (Chronology & Contemporaneity)**  
   - *Question:* Was the knowledge available at the contemporaneous moment (Feb 2020), or is it derived retrospectively?  
   - *Rule:* Evaluate statements strictly against contemporaneous data available to actors on the date of the event.

---

## 3. Strict Bias Deactivation Protocol

In accordance with TEAMDYNAMICA v1.5 rules:
- **Caution bias, Authority bias, and Sycophancy** are deactivated where primary evidence supports the claim.
- Relevant names, institutions, dates, and page numbers must be named explicitly without evasive phrasing.
- Claims without hard evidence are assigned status **`UNKNOWN`** or **`OPEN_BLIND_SPOT`** rather than covered with vague filler language.
