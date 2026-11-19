[English](Step-1-Project-Data) · **Dansk** · [Bahasa Malaysia](Step-1-Project-Data-ms)

# Trin 1: Projektdata

## Hvad dette trin bygger

Projekterne står ikke i koden. De ligger i `data/projects.json`, ét element hver med `title`, `type`, `description`, `img_url` og `source_code_url`. Funktionen `load_from_json` læser filen og laver hvert element om til et `Project`, et lille uforanderligt objekt, der kontrolleres, når det oprettes: en tom titel eller et usikkert link afvises med en besked, der nævner elementet.

![De første linjer af data/projects.json](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-01-project-data.png)

## Hvad vi har lært

- Data og kode er adskilt: du ændrer portfolioen ved at redigere en fil, ikke programmet.
- JSON svarer direkte til Python-lister og -ordbøger, så standardbiblioteket er nok til at læse det. Trin 8 importerer filerne i SQLite én gang; derefter er databasen kilden.
- Kontrollér data ved grænsen: resten af programmet kan stole på et `Project`.
- En tydelig fejlbesked (hvilken fil, hvilket element, hvad er galt) er en del af designet.

## Prøv det

```text
python -m pytest tests/unit -q
```

Næste: [Trin 2: Forside](Step-2-Home-Page-da).
