[English](Getting-Started) · **Dansk** · [Bahasa Malaysia](Getting-Started-ms)

# Kom i gang

Du skal bruge Python 3.13 eller nyere og Git. Projektet har ingen afhængigheder ved kørsel. Docker skal kun bruges til at tage skærmbillederne igen, og Doxygen kun til at bygge API-referencen.

## Opsætning

Windows (PowerShell):

```text
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux og macOS:

```text
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Mappen `.venv` er en privat kopi af Python til dette projekt, så der installeres intet på hele systemet. Kør `deactivate` for at forlade den.

## Kør

```text
python -m portfolio build
python -m portfolio serve
```

Åbn <http://127.0.0.1:8000> i en browser. Tryk `Ctrl+C` for at stoppe serveren.

## Test

```text
python -m pytest
```

Fortsæt med [Opsummering af lektionen](Lecture-Summary-da) eller gå direkte til [Trin 1](Step-1-Project-Data-da).
