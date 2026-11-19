[English](Step-6-Tests) · **Dansk** · [Bahasa Malaysia](Step-6-Tests-ms)

# Trin 6: Tests

## Hvad dette trin bygger

`pytest` kører enhedstests af entiteter og use cases, integrationstests af SQLite-repositorierne, Flask-testklient-tests af hver rute og header og end-to-end-tests, der starter den rigtige server og læser dens svar. `lint-imports` kontrollerer, at lagene kun afhænger indad, `ruff` kontrollerer stil, og `mypy --strict` kontrollerer typerne.

![En testkørsel](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-06-tests.png)

## Hvad vi har lært

- Tests på tre niveauer: små og hurtige nederst og nogle få, der beviser hele siden, øverst.
- Fordi use cases afhænger af porte, testes de med enkle stand-ins i hukommelsen, uden filer og uden browser.
- En regel, der kontrolleres af et værktøj (lagkontrakterne), forbliver sand, når koden vokser.

## Prøv det

```text
python -m pytest
python -m ruff check .
python -m mypy
lint-imports
```

Næste: [Trin 7: Vendekort og profil](Step-7-Flip-Cards-and-Profile-da).
