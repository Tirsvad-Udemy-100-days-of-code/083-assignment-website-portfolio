[English](Step-5-Preview) · **Dansk** · [Bahasa Malaysia](Step-5-Preview-ms)

# Trin 5: Forhåndsvisning

## Hvad dette trin bygger

Én kommando viser siden. `python -m portfolio serve` starter en Flask-server på <http://127.0.0.1:8000>. Den har indstillingerne `--db`, `--data`, `--host` og `--port`. Hver forespørgsel læser databasen og tegner siden med en Jinja-skabelon, så der er intet build-trin. Når databasen mangler, giver `serve` en enkelt linje besked, der nævner kommandoerne `init` og `import`, og en exitkode forskellig fra nul.

![Serve-kommandoen og en manglende database](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-serve-command.png)

![Siden på den lokale forhåndsvisningsserver](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-preview-server.png)

## Hvad vi har lært

- En kommandolinjegrænseflade med `argparse`, med hjælpetekst gratis.
- Serveren lytter som standard på `127.0.0.1`, så kun din egen computer kan nå den.
- Kompositionsroden (`__main__.py`) er det eneste sted, der forbinder lagene; resten af koden kender ikke de konkrete klasser.

## Prøv det

```text
python -m portfolio --help
python -m portfolio serve --db data/portfolio.db --data data --port 8000
```

Næste: [Trin 6: Tests](Step-6-Tests-da).
