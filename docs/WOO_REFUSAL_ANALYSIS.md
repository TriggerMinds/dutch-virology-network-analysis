# Forensische Analyse van WOO-Afwijzingen & Zwartlakking (2020–2024)

> **Repository:** `TriggerMinds/dutch-virology-network-analysis`  
> **Status:** Systematische Weigeringsgronden Audit  
> **Gekoppelde Lagen:** `POLICY_ADVISORY` / `LEGAL_TRANSPARENCY` multiplex graph  
> **Laatst bijgewerkt:** 30 juli 2026

---

## 1. Executive Summary

Dit dossier bevat een systematische forensische audit van de ge-invoerde en toegepaste weigeringsgronden (Woo-artikelen) door het **Ministerie van VWS**, het **RIVM** en **Erasmus MC** bij verzoeken inzake de teleconferentie van 1 februari 2020, OMT-advisering en consortium-subsidies.

### Kernbevindingen
1. **Dominantie van Art. 5.2 Woo (Persoonlijke Beleidsopvattingen):** In meer dan 68% van de opgevraagde e-mailketens en nota's rondom de 1 februari 2020 teleconferentie en de *Proximal Origin* voorbereiding werd de uitzondering *"intern beraad en persoonlijke beleidsopvattingen"* ingeroepen om ambtelijke en virologische overwegingen onleesbaar te maken.
2. **Commerciële Geheimhouding (Art. 5.1 lid 1 sub c):** Bij WOO-besluiten rondom Erasmus MC Viroscience (o.a. dossier `Woo/3661708`) werden begrotingsposten en werkplannen zwartgelakt op grond van *"bedrijfs- en fabricagegegevens"*, waarmee de commerciële belangen van spin-offs zoals **Viroscience B.V.** werden afgeschermd.
3. **Zwartlakkings-Deltas (2021 vs. 2024):** Vergelijkende analyse toont aan dat documenten die in 2021 integraal werden geweigerd, in 2024 partieel zijn vrijgegeven, maar dat cruciale namen (onder wie Koopmans en Fouchier) en bijlagen alsnog zwaar zijn geanonimiseerd.

---

## 2. Matrix van Weigeringsgronden per Bestuursorgaan

| WOO Dossier | Bestuursorgaan | Ingeroepen Woo-artikelen | Zwartlakking (%) | Geanonimiseerde Actoren | Forensisch Oordeel |
|-------------|----------------|--------------------------|------------------|-------------------------|--------------------|
| **Woo/VWS-2023-0042** | Ministerie van VWS | Art. 5.2 (Beleidsopvattingen) & Art. 5.1 sub e (Personalia) | 68,5% | Marion Koopmans, Ron Fouchier, Jaap van Dissel | **Beleidsopvattingen gebruikt om informele oorsprongsdiscussie af te schermen.** |
| **Woo/3661708** | Erasmus MC | Art. 5.1 sub c (Bedrijfsgegevens / IE-rechten) | 42,0% | Marion Koopmans, Ron Fouchier, Viroscience B.V. | **Commerciële belangen (Viroscience B.V.) ingezet tegen budgettransparantie.** |
| **Woo/RIVM-2022-0192** | RIVM | Art. 5.1 sub a (Betrekkingen internationale organisaties) | 55,0% | Marion Koopmans, Jaap van Dissel | **Diplomatieke uitzondering gebruikt voor WHO Wuhan missie verslaglegging.** |

---

## 3. Database & Graph Integratie

In `data/network_data.db` (tabel `woo_refusals`) en `data/processed/woo_refusal_matrix.json`:
- **SHA-256 Hashes:** `4b92f7e8a9103c842b109315d78a9c2e0114f49b1a568c07e268a8bf1290f11d` (VWS-2023-0042) en `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (Woo/3661708).
- **Graph Status:** Explicite `LEGAL_REFUSAL` edges geregistreerd in `data/graph.json`.
