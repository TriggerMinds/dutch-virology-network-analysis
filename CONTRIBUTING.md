# Contributing

## Scope
This repository is a **fact-finding and data-engineering project**. Contributions that improve accuracy, expand the evidence base, or identify methodological blind spots are welcome.

## What we accept
- **Corrections** to extracted data (incorrect page numbers, misattributed quotes, faulty regex patterns)
- **Additional sources** — links to public databases, FOIA releases, academic papers, or government reports that connect to entities in the graph
- **Blind spot additions** — documented gaps in the methodology or source material (see `docs/BLIND_SPOT_MAPPING.md`)
- **Pipeline improvements** — better extraction accuracy, performance, or reproducibility

## What we do NOT accept
- **Advocacy or polemics** — this is not a platform for political positions about the lab-leak debate, Anthony Fauci, or COVID-19 policy
- **Unsubstantiated claims** — every addition must be traceable to a verifiable source
- **ML hallucination fixes** — if you want to add an LLM-based NER pass, it must be a separate module with explicit confidence scoring

## Process
1. Open an issue describing your proposed change
2. Fork the repo, make your changes on a branch
3. Submit a PR with clear evidence of what changed and why
4. Maintain the evidence-traceability requirement: every quote must have a page field
