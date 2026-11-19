[English](Step-5-Preview) · **Dansk** · [Bahasa Malaysia](Step-5-Preview-ms)

# Trin 5: Forhåndsvisning

## Hvad dette trin bygger

To kommandoer gør værktøjet færdigt. `python -m portfolio build` læser data og skriver `index.html`, `about.html` og `style.css` til en mappe. `python -m portfolio serve` viser mappen med standardbibliotekets `http.server` på <http://127.0.0.1:8000>. Begge har indstillinger (`--data`, `--out`, `--host`, `--port`) og giver en enkelt linje besked og en exitkode forskellig fra nul, når noget er galt, fx en manglende datafil.

![Build-kommandoen og dens output](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-build-command.png)

![Siden på den lokale forhåndsvisningsserver](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-preview-server.png)

## Hvad vi har lært

- En kommandolinjegrænseflade med `argparse`, med hjælpetekst gratis.
- Serveren lytter som standard på `127.0.0.1`, så kun din egen computer kan nå den.
- Kompositionsroden (`__main__.py`) er det eneste sted, der forbinder lagene; resten af koden kender ikke de konkrete klasser.

## Prøv det

```text
python -m portfolio --help
python -m portfolio build --data data --out build
python -m portfolio serve --out build
```

Næste: [Trin 6: Tests](Step-6-Tests-da).
