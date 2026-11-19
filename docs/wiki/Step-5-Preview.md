**English** · [Dansk](Step-5-Preview-da) · [Bahasa Malaysia](Step-5-Preview-ms)

# Step 5: Preview

## What this step builds

One command shows the site. `python -m portfolio serve` starts a Flask server at <http://127.0.0.1:8000>. It has the options `--db`, `--data`, `--host` and `--port`. Every request reads the database and renders the page with a Jinja template, so there is no build step. When the database is missing, `serve` gives a one-line message that names the commands `init` and `import`, and a non-zero exit code.

![The serve command and a missing database](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-serve-command.png)

![The site on the local preview server](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-preview-server.png)

## What we gained

- A command line interface with `argparse`, with help text for free.
- The server listens on `127.0.0.1` by default, so only your own computer can reach it.
- The composition root (`__main__.py`) is the one place that connects the layers; the rest of the code does not know the concrete classes.

## Try it

```text
python -m portfolio --help
python -m portfolio serve --db data/portfolio.db --data data --port 8000
```

Next: [Step 6: Tests](Step-6-Tests).
