[English](Step-2-Home-Page) · **Dansk** · [Bahasa Malaysia](Step-2-Home-Page-ms)

# Trin 2: Forside

## Hvad dette trin bygger

Use casen `home` beder projekt-repositoriet om alle projekter og returnerer en `HomePage` med ét kort af almindelige data pr. projekt. En Jinja-skabelon omsætter det til HTML. Billedet viser siden uden stylesheet, så du ser den nøgne struktur: en overskrift, en liste af projekter og for hvert en titel, et billede, en beskrivelse og et link.

![Forsiden uden stylesheet](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-02-home-page-structure.png)

## Hvad vi har lært

- En use case rummer det, programmet gør; skabelonen bestemmer kun, hvordan det ser ud.
- Jinja escaper alt, der kommer fra data, før det når siden (autoescape), så en titel med `<script>` vises som tekst og aldrig køres.
- Semantisk HTML (overskrifter, lister, links) virker uden CSS, og en side kan testes uden en browser.

## Prøv det

```text
python -m portfolio serve
# open http://127.0.0.1:8000 in a browser
```

Næste: [Trin 3: Om-side](Step-3-About-Page-da).
