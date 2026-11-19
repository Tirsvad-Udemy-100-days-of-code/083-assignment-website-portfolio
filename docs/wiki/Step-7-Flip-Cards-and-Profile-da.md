[English](Step-7-Flip-Cards-and-Profile) · **Dansk** · [Bahasa Malaysia](Step-7-Flip-Cards-and-Profile-ms)

# Trin 7: Vendekort og profil

## Hvad dette trin bygger

Hvert projekt er et vendekort. Forsiden viser projektets billede, navn og beskrivelse. Bagsiden viser linket til kildekoden, tags og de færdigheder, projektet viser. Kortet vender ved hover, ved tastaturfokus og ved et tryk. Om-siden linker til ejerens LinkedIn-profil og viser ejerens profilbillede, eller en rund avatar med initialer, hvis der ikke er sat noget billede. Flask serverer alle billeder fra mappen `images` i datamappen.

![Forsiden af et projektkort](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-flip-card-front.png)

![Bagsiden af et projektkort](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-flip-card-back.png)

![Om-siden med LinkedIn-linket og profilbilledet](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-about-page.png)

## Hvad vi har lært

- Et 3D-vend er ren CSS (`transform-style: preserve-3d` og `backface-visibility: hidden`), ingen JavaScript.
- Tilgængelighed: kortet kan nås med tastaturet, og besøgende, der foretrækker mindre bevægelse, får ingen animation.
- En ny slags fil, binære billeder, krævede en port til at læse filer, og en stikontrol forhindrer en dårlig sti som `../secret` i at slippe ud af billedmappen: den giver 404.
- Eksempelprojekterne er rigtigt arbejde, der viser rigtige færdigheder, ikke kursusøvelser: datafilen er portfolioen.

## Prøv det

Redigér `data/projects.json` for at tilføje `tags` og `skills` til et projekt, læg dit billede i `data/images/` og sæt `"photo"` i `data/profile.json`, og importér igen med `python -m portfolio import --replace`.

Næste: [Trin 8: SQLite og Flask](Step-8-SQLite-and-Flask-da).
