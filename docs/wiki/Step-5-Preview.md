**English** · [Dansk](Step-5-Preview-da) · [Bahasa Malaysia](Step-5-Preview-ms)

# Step 5: Preview

## What this step builds

Two commands finish the tool. `python -m portfolio build` reads the data and writes `index.html`, `about.html` and `style.css` to a folder. `python -m portfolio serve` shows that folder with the standard library's `http.server` at <http://127.0.0.1:8000>. Both have options (`--data`, `--out`, `--host`, `--port`) and give a one-line message and a non-zero exit code when something is wrong, for example a missing data file.

![The build command and its output](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-build-command.png)

![The site on the local preview server](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-preview-server.png)

## What we gained

- A command line interface with `argparse`, with help text for free.
- The server listens on `127.0.0.1` by default, so only your own computer can reach it.
- The composition root (`__main__.py`) is the one place that connects the layers; the rest of the code does not know the concrete classes.

## Try it

```text
python -m portfolio --help
python -m portfolio build --data data --out build
python -m portfolio serve --out build
```

Next: [Step 6: Tests](Step-6-Tests).
