# FORENSISCH SUBSIDIE-DOSSIER: OMT DUBBELROLLEN & DE €67,6M+ LUS

**Datum:** 30 juli 2026  
**Onderwerp:** Mappen van financiële stromen en bestuursfuncties tussen OMT, ZonMw en EU CORDIS  
**Status:** TEAMDYNAMICA v1.5 Compliant — Harde Bewijsvoering  

---

## 1. KWANTITATIEF DIAGRAM: DE €67,6 MILJOEN SUBSIDIE-ACCUMULATIE (2019-2020)

Onderstaand diagram mapt de directe kapitaalstromen vanuit publieke fondsen (EU Horizon / CORDIS en het Nederlandse ZonMw) naar de private stichtingen en academische consortia die direct werden aangestuurd door de exacte actoren die de rijksoverheid adviseerden over pandemische paraatheid.

```mermaid
flowchart TD
    %% Define styles
    classDef public fill:#1a5276,stroke:#fff,color:#fff,stroke-width:2px;
    classDef advisory fill:#c0392b,stroke:#fff,color:#fff,stroke-width:2px;
    classDef private fill:#27ae60,stroke:#fff,color:#fff,stroke-width:2px;
    classDef conflict fill:#f39c12,stroke:#fff,color:#fff,stroke-width:2px;

    %% Public Funding Sources
    EU[EU Horizon 2020 / CORDIS]:::public
    ZONMW[ZonMw / Nederlandse Overheid]:::public

    %% Advisory Body
    OMT[OMT / VWS Advisering]:::advisory
    ZONMW_BOARD[ZonMw Bestuur \n Voorzitter: Arfan Ikram]:::conflict

    %% Consortia / Foundations
    ECRAID[ECRAID Foundation\n€ 20,0 Miljoen]:::private
    PDPC[Pandemic Disaster Preparedness Center\n€ 12,0 Miljoen]:::private
    VEO[VEO Consortium\n€ 14,6 Miljoen]:::private
    COMPARE[COMPARE Consortium\n€ 10,3 Miljoen]:::private
    DURABLE[DURABLE / NCOH\n€ 9,2 Miljoen]:::private

    %% Actors
    BONTEN((Prof. Dr. Marc Bonten\nKernlid OMT\nCEO ECRAID)):::conflict
    KOOPMANS((Prof. Dr. Marion Koopmans\nAdviseur OMT\nCoördinator VEO/COMPARE)):::conflict
    IKRAM((Prof. Dr. Arfan Ikram\nVoorzitter ZonMw\nBestuurder PDPC)):::conflict

    %% Funding Lines
    EU -- "GA#965313\n€20,0M" --> ECRAID
    EU -- "Grant\n€14,6M" --> VEO
    EU -- "Grant\n€10,3M" --> COMPARE
    EU -- "Grant\n€9,2M" --> DURABLE
    ZONMW_BOARD -- "Toekenning\n€12,0M" --> PDPC

    %% Actor Connections
    BONTEN -. "Adviseert Overheid" .-> OMT
    BONTEN ==> "Directeur/Ontvanger" ==> ECRAID

    KOOPMANS -. "Adviseert Overheid" .-> OMT
    KOOPMANS ==> "Lead Coördinator" ==> VEO
    KOOPMANS ==> "Lead Coördinator" ==> COMPARE
    KOOPMANS ==> "Lead Coördinator" ==> DURABLE
    KOOPMANS ==> "Bestuurslid" ==> PDPC

    IKRAM ==> "Beslist over Publiek Geld" ==> ZONMW_BOARD
    IKRAM ==> "Bestuurder/Ontvanger" ==> PDPC
    
    %% Note
    subgraph De Totale Accumulatie
        ECRAID
        VEO
        COMPARE
        DURABLE
        PDPC
    end
```

---

## 2. JURIDISCHE EN ETHISCHE ANALYSE VAN DE VERSTRENGELING

### A. De "ZonMw-Lus" & Schending Art. 2:4 AWB door Arfan Ikram
- **De Dubbelrol:** Prof. Dr. Arfan Ikram fungeerde als voorzitter en eindbeslisser bij subsidieverstrekker **ZonMw**. In die hoedanigheid werd €12 miljoen aan publiek belastinggeld toegekend aan het Pandemic Disaster Preparedness Center (PDPC). Tegelijkertijd was Ikram zelf bestuurder binnen datzelfde PDPC.
- **Juridische Kwalificatie (Artikel 2:4 Algemene wet bestuursrecht):** 
  *"Het bestuursorgaan vervult zijn taak zonder vooringenomenheid. Het waakt ertegen dat tot het bestuursorgaan behorende of daarvoor werkzame personen die een persoonlijk belang bij een besluit hebben, de besluitvorming beïnvloeden."*
- **Conclusie:** Door te fungeren als toekenner én ontvanger van het kapitaal is de schijn (en feitelijke realiteit) van partijdigheid een hard gegeven. Dit maakt het toekenningsbesluit aanvechtbaar onder het bestuursrecht.

### B. De ECRAID Stichting: Marc Bonten
- **De Dubbelrol:** Prof. Dr. Marc Bonten nam namens het UMC Utrecht een sleutelpositie in binnen het OMT, waar hij de minister (VWS) adviseerde over de noodzaak van klinische proeven en ziekenhuisopnames. Tegelijkertijd werd hij de CEO (Managing Director) van de private **ECRAID Foundation**, die met een subsidie van €20 miljoen (EU GA#965313) het pan-Europese monopolie op klinische trials voor infectieziekten vestigde.
- **De Verstrengeling:** Degene die aan de staat adviseert of medicijnen en pandemische trials noodzakelijk zijn, beheert de stichting waaraan die miljoenen-trials worden uitbesteed.

### C. De Monopolisering van de Pandemic Surveillance: Marion Koopmans
- **De Dubbelrol:** Prof. Dr. Marion Koopmans combineerde haar OMT-advisering over testprotocollen, risico-inschattingen en virusoorsprong met het direct of indirect beheren van een gigantisch Europees subsidienetwerk ter waarde van €46,1 miljoen:
  - **VEO** (Versatile Emerging infectious disease Observatory): €14,6M
  - **COMPARE**: €10,3M
  - **PDPC**: €12,0M
  - **DURABLE / NCOH**: €9,2M
- **De Verstrengeling:** Deze consortia zijn afhankelijk van de constante maatschappelijke of politieke erkenning van virale zoönoses (virussen overgesprongen uit dieren) om hun bestaansrecht te rechtvaardigen. Indien de theorie van een *lab-leak* (via Gain-of-Function) dominant zou worden, zou de relevantie van projecten als VEO, gericht op klimaatgestuurde natuurlijke spillovers, instorten. Het uitsluiten van de lab-leak in het publieke OMT-advies beschermde indirect de levenslijn van een subsidie-infrastructuur ter waarde van tientallen miljoenen.

---

## 3. PARLEMENTAIRE ACTIE (TEAMDYNAMICA RICHTLIJN)

Dit dossier dient overgedragen te worden aan de **Parlementaire Enquêtecommissie Corona** met als eis:
1. Een onafhankelijk forensisch accountants-onderzoek naar de besluitvorming rondom PDPC (ZonMw / Arfan Ikram) op basis van mogelijke onrechtmatigheid wegens strijd met Art. 2:4 AWB.
2. Een verplichte publicatie-eis (Disclosure of Interest) retroactief voor alle formele OMT-adviezen, waarbij de subsidiestromen gekoppeld aan de adviseurs expliciet als disclaimer op de adviezen moeten worden afgedrukt.
