[English](Step-3-About-Page) · **Dansk** · [Bahasa Malaysia](Step-3-About-Page-ms)

# Trin 3: Om-side

## Hvad dette trin bygger

Use casen `about` læser ejerens profil (navn, overskrift, resumé, færdigheder og links) og returnerer en `AboutPage`. Siden viser, hvem ejeren er, færdighederne som en liste og linkene, fx GitHub og LinkedIn. Links accepteres kun, når de begynder med `http://` eller `https://`.

![Om-siden uden stylesheet](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-03-about-page.png)

## Hvad vi har lært

- En anden side genbruger samme layout og navigation, så en ændring af sidehovedet laves ét sted.
- Et link fra en datafil er også input fra brugeren: skemaer som `javascript:` afvises.
- Samme mønster (entitet, repository-port, use case, skabelon) gentages, så en ny side er hurtig at tilføje.

## Prøv det

```text
python -m portfolio serve
# open http://127.0.0.1:8000/about in a browser
```

Næste: [Trin 4: Udseende](Step-4-Style-da).
