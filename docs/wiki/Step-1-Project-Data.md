**English** · [Dansk](Step-1-Project-Data-da) · [Bahasa Malaysia](Step-1-Project-Data-ms)

# Step 1: Project data

## What this step builds

The projects are not written into the code. They live in `data/projects.json`, one entry each with a `title`, a `type`, a `description`, an `img_url` and a `source_code_url`. The function `load_from_json` reads the file and turns every entry into a `Project`, a small immutable object that is checked when it is made: an empty title or an unsafe link is refused with a message that names the entry.

![The first lines of data/projects.json](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-01-project-data.png)

## What we gained

- Data and code are separate: you change the portfolio by editing a file, not the program.
- JSON maps directly onto Python lists and dictionaries, so the standard library is enough to read it. Step 8 imports these files into SQLite once; after that the database is the source.
- Check data at the border: the rest of the program can trust a `Project`.
- A clear error message (which file, which entry, what is wrong) is part of the design.

## Try it

```text
python -m pytest tests/unit -q
```

Next: [Step 2: Home page](Step-2-Home-Page).
