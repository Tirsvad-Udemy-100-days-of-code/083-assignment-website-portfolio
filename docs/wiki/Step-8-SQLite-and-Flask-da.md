[English](Step-8-SQLite-and-Flask) · **Dansk** · [Bahasa Malaysia](Step-8-SQLite-and-Flask-ms)

# Trin 8: SQLite og Flask

## Hvad dette trin bygger

Siden er dynamisk. Data ligger i en SQLite-database, `data/portfolio.db`, som Python læser med sit eget `sqlite3`-modul. `python -m portfolio init` opretter databasen, og `python -m portfolio import` kopierer eksempel-JSON-filerne ind i den én gang. Derefter er databasen den eneste kilde. Du ændrer den med kommandoer: `project list`, `project add`, `project set`, `project remove` og `profile set`. `serve` starter en Flask-applikation, der åbner databasen skrivebeskyttet ved hver forespørgsel, kører use casen `home` eller `about` og tegner en Jinja-skabelon. Et projekt, du tilføjer med en kommando, vises derfor ved næste indlæsning, uden build og uden genstart.

![Opret databasen, importér eksempeldata og list projekterne](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-08-database-commands.png)

![Et projekt tilføjet med en kommando vises ved næste indlæsning](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-08-project-added.png)

## Hvad vi har lært

- En database adskiller data fra filer: ét sted at læse og skrive, med regler, programmet kan stole på.
- Hver SQL-sætning er skrevet på forhånd og får sine værdier som parametre, aldrig klistret ind i teksten, så en titel som `'; DROP TABLE project; --` bare er en titel.
- Webserveren læser kun. Den har ingen rute, der ændrer data, intet login og ingen session, så der er lidt at angribe.
- Flask er én fastlåst afhængighed. Use cases og domænet importerer den ikke, og en lagkontrol beviser det, så weblaget kan udskiftes uden at røre reglerne.
- Serveren sender headerne `Content-Security-Policy`, `X-Content-Type-Options` og `Referrer-Policy` på hvert svar.

## Prøv det

```text
python -m portfolio init
python -m portfolio import
python -m portfolio project list
python -m portfolio project add --title "My new project" --kind Website --description "Added with a command while the server runs." --source-code-url https://example.com/my-new-project --tag Flask --skill SQLite
python -m portfolio serve
```

Genindlæs forsiden efter kommandoen `project add`, og det nye kort er der.
