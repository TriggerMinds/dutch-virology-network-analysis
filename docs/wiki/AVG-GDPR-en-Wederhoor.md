# AVG/GDPR en Wederhoor

## Juridische Onderbouwing
Dit project verwerkt namen, institutionele affiliaties en professionele rollen van personen die:
- **Publieke figuren** zijn (senior wetenschappers, overheidsadviseurs, gepubliceerde academici)
- Handelend in hun **professionele hoedanigheid**
- Geidentificeerd via **openbaar toegankelijke** databases (OpenAlex, NIH, Congressional records)

**Geen persoonlijke data** (adressen, telefoonnummers, privécorrespondentie, gezondheidsdata, politieke voorkeuren) wordt verzameld, opgeslagen of gepubliceerd.

## Level 1 Fact-Taxonomie
| Level | Label | Betekenis | Voorbeeld |
|-------|-------|-----------|-----------|
| L1 | [Documented Fact] | Direct geciteerd uit primaire bron met paginanummer | "Fauci noteert op p14: 'Conference call at 2:00 PM with Jeremy'" |
| L2 | [Inferred] | Logische conclusie uit L1-feiten | "Farrar organiseerde de call (gebaseerd op 'gathered by Jeremy')" |
| L3 | [Hypothesis] | Interpretatieve inschatting, gemarkeerd als onzeker | "Koopmans' positie was mogelijk neutraal (positie niet genoteerd)" |

## Wederhoor Procedure
1. **Open een GitHub Issue** via het template `.github/ISSUE_TEMPLATE/data_correction.yml`
2. **Vermeld**: uw e-mail (niet openbaar), betwist knooppunt, exacte fout, bewijsstuk URL
3. Het team onderzoekt de correctie binnen 14 werkdagen
4. Bij aantoonbare onjuistheid wordt de dataset gecorrigeerd + changelog bijgewerkt

## Takedown Policy
Indien u van mening bent dat uw persoonsgegevens onrechtmatig zijn verwerkt:
1. Dien een Woo-verzoek-gemotiveerd verzoek in via bovenstaand Issue template
2. Vermeld welke specifieke edge of node betwist wordt
3. Het verzoek wordt binnen 30 dagen behandeld conform AVG Art. 17 (Recht op vergetelheid)

## Verifieerbaarheid
Alle bewijscitaten in deze dataset bevatten een `page_number` veld dat linkt naar de bron-PDF.
SHA-256 hash van de bron-PDF: `27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e`
