# Forensic Position Status Dossier: Prof. Dr. Marion Koopmans (Feb 1 2020 Teleconference)

> **Document Status:** Standalone Forensic Audit  
> **Repository:** TriggerMinds / dutch-virology-network-analysis  
> **Last Updated:** 30 July 2026  
> **Primary Source Base:** Fauci Diary Release (Rand Paul Release, July 2026, 1141 pp, SHA-256: `27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e`), House Oversight FOIA releases, WOO records.

---

## Executive Summary

This dossier documents the systematic audit regarding the presence, role, and explicit position of **Prof. Dr. Marion Koopmans** (Head of Department of Viroscience, Erasmus Medical Center) during the international teleconference held on **1 February 2020 at 2:00 PM EST (20:00 CET)** organized by Sir Jeremy Farrar and Dr. Anthony Fauci regarding the origins and furin cleavage site of SARS-CoV-2.

### Primary Forensic Findings
1. **Attendance Confirmed:** Contemporaneous primary documentation (*Tony's Diary*, p. 14, released July 2026) explicitly confirms that **M.P.G. Koopmans** attended the teleconference alongside Dr. Francis Collins, Dr. Anthony Fauci, Sir Jeremy Farrar, Sir Patrick Vallance, Dr. Kristian Andersen, Dr. Christian Drosten, Dr. Edward Holmes, Dr. Andrew Rambaut, Dr. Ron Fouchier, Dr. Robert Garry, and Dr. Mike Ferguson.
2. **Stance/Position Unrecorded:** In the primary contemporaneous text of the diary (pp. 14–15), Dr. Anthony Fauci explicitly describes the positions taken by Dr. Ron Fouchier (who argued natural origin and urged against diverting efforts to GOF/deliberate insertion) and Dr. Christian Drosten ("was with Ron"), as well as "the rest" who favored further investigation of deliberate insertion. **No individual quote, argument, or vote by Marion Koopmans is recorded.**
3. **Formal Status:** Under strict TEAMDYNAMICA OSINT guidelines (no inferential leaps, default to unknown), Marion Koopmans' position during the 1 February 2020 teleconference remains **`UNKNOWN`** (Unrecorded Blind Spot).

---

## 1. Primary Source Analysis (*Tony's Diary*, July 2026 Release)

### 1.1 Source Provenance
- **Document Title:** *Tony's Diary Package (Fauci Diary Release)*
- **Publication Date:** 24 July 2026 (Released by Chairman Rand Paul / U.S. Senate Committee)
- **Local File Path:** `data/raw/fauci_diary/2026.07.24_Tonys-Diary-Package.pdf`
- **SHA-256 Checksum:** `27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e`
- **Total Pages:** 1141

### 1.2 Verbatim Text Excerpt (Page 14)
```text
Feb. 1, 2020 - Conference call at 2:00 PM with Jeremy, Francis and several other scientists gathered by Jeremy (see below).
Participants in the Feb., 2020 call included:
• Francis Collins, Director of the U.S. National Institutes of Health, U.S.;
• Anthony Fauci, Director of the U.S. National Institute of Allergy and Infectious Diseases, U.S.;
• Jeremy Farrar, Director of the Wellcome Trust;
• Patrick Vallance, U.K. Chief Scientific Adviser and Head of the Government Science and Engineering;
• Kristian Anderson, Director of Infectious Disease Genomics, Scripps Research Translational Institute, CA, U.S.;
• Christian Drosten, Director of Human Virology at the German Center for Infection Research at Charité – Universitätsmedizin, Germany;
• Edward Holmes, Professor of Viral Evolution at University of Sydney;
• Andrew Rambaut, Professor of Molecular Evolution, University of Edinburgh’s Institute of Evolutionary Biology, U.K.;
• Ron Fouchier, Deputy Head of Department of Viroscience, Erasmus Medical Center, NL;
• Robert Garry, Professor of Virology, Tulane University School of Medicine, Louisana, U.S. ;
• Mike Ferguson, Professor of Life Sciences at University of Dundee, U.K.; and
• M.P.G. Koopmans, Head of Department of ViroScience, Erasmus Medical Center, NL.

There was not total agreement about the likelihood of deliberate insertion. Ron Fouchier said he was sure that this could occur naturally and we should not waste our time and divert effort to pursue this. This is expected of him since he was the original GOF person with Yoshi Kawaoka. Also, Christian Drosten was with Ron; the rest felt that deliberate insertion was possible and given the fact that Dr. Zheng-Li Shi at the University of Wuhan has been working for years in GOF in coronaviruses to allow adaptation of the spike protein to bind to the human ACE2 receptor, we could not let this go.
```

---

## 2. Evaluation of Secondary Claims & Common Misconceptions

### 2.1 The "9 February 2020 Email" Claim
- **Claim:** Secondary commentary occasionally references a "9 February 2020 email from Koopmans" regarding early origin consensus.
- **Audit Result:** Forensic scan of the full 1141-page Fauci Diary package confirms that **no 9 February 2020 email from Koopmans exists** in this release. The diary entries for Feb 9, 2020 (p. 19) deal strictly with US quarantine measures, cruise ships, and domestic case counts. The claim represents a confusion between Washington Post FOIA releases and the Fauci Diary.

### 2.2 Functional Split: GOF Virologists vs. Zoonotic Surveillance Virologists
- **Context:** Unlike Ron Fouchier, whose lab specialization centers on functional gain-of-function (GOF) airborne transmission experiments, Marion Koopmans' core institutional expertise is in **veterinary epidemiology, foodborne viruses, and zoonotic surveillance**.
- **Assessment:** Her presence on the call was aligned with international disease surveillance (WHO/Viroscience), but because Fauci's notes focused specifically on the GOF / deliberate insertion debate (where Fouchier took the lead for Erasmus MC), Koopmans' specific comments were omitted from the summary.

---

## 3. Database & Graph Representation

In `data/network_data.db` and `data/graph.json`:
- **Table `koopmans_feb1_audit`:** Contains 29 extracted reference pages from raw files with `position_indicated = 'unknown'`.
- **Table `informal_interactions`:** Logs `entity_name = 'Marion Koopmans'`, `interaction_type = 'UNRECORDED_PARTICIPATION (BLIND_SPOT)'`, `date = '2020-02-01'`.
- **Knowledge Graph (`data/graph.json`):**
  - Node: `Marion Koopmans` -> `feb1_2020_position_status: "UNKNOWN"`, `blind_spot_flag: true`.
  - Edge: `Marion Koopmans` <-> `Feb 1 2020 Teleconference` -> `status: "BLIND_SPOT"`.

---

## 4. Actionable Next Steps to Bridge the Blind Spot

1. **Submit Formal WOO Requests:** Execute the ready-to-submit WOO requests in `docs/WOO_REQUESTS_FEB2020.md` targeting Erasmus MC, RIVM, and VWS for all internal notes, emails, and calendar entries between 28 Jan and 15 Feb 2020.
2. **Monitor Parliamentary Inquiry Transcripts:** Cross-examine future stenograms and witness testimony of the Dutch Parliamentary Inquiry Committee Corona (*Parlementaire Enquêtecommissie Corona*).
