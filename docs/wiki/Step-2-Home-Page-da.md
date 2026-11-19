[English](Step-2-Home-Page) · **Dansk** · [Bahasa Malaysia](Step-2-Home-Page-ms)

# Trin 2: Forside

## Hvad dette trin bygger

Use casen `home` beder projekt-repositoriet om alle projekter og returnerer en `HomePage` med ét kort af almindelige data pr. projekt. Forside-viewet omsætter det til HTML. Billedet viser siden uden stylesheet, så du ser den nøgne struktur: en overskrift, en liste af projekter og for hvert en titel, et billede, en beskrivelse og et link.

![Forsiden uden stylesheet](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-02-home-page-structure.png)

## Hvad vi har lært

- En use case rummer det, programmet gør; viewet bestemmer kun, hvordan det ser ud.
- Alt, der kommer fra datafilen, escapes med `html.escape`, før det når siden, så en titel med `<script>` vises som tekst og aldrig køres.
- Semantisk HTML (overskrifter, lister, links) virker uden CSS, og en side kan testes uden en browser.

## Prøv det

```text
python -m portfolio build
# open build/index.html in a browser
```

Næste: [Trin 3: Om-side](Step-3-About-Page-da).
