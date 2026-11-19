**English** · [Dansk](Step-8-SQLite-and-Flask-da) · [Bahasa Malaysia](Step-8-SQLite-and-Flask-ms)

# Step 8: SQLite and Flask

## What this step builds

The site is dynamic. The data lives in a SQLite database, `data/portfolio.db`, which Python reads with its own `sqlite3` module. `python -m portfolio init` creates the database, and `python -m portfolio import` copies the sample JSON files into it once. After that the database is the only source. You change it with commands: `project list`, `project add`, `project set`, `project remove` and `profile set`. `serve` starts a Flask application that opens the database read-only on every request, runs the `home` or `about` use case and renders a Jinja template. So a project you add with a command shows on the next page load, with no build and no restart.

![Creating the database, importing the sample data and listing the projects](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-08-database-commands.png)

![A project added with a command shows on the next page load](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-08-project-added.png)

## What we gained

- A database separates data from files: one place to read and write, with rules the program can trust.
- Every SQL statement is written in advance and gets its values as parameters, never pasted into the text, so a title such as `'; DROP TABLE project; --` is just a title.
- The web server only reads. It has no route that changes data, no login and no session, so there is little to attack.
- Flask is one pinned dependency. The use cases and the domain do not import it, and a layer check proves that, so the web layer can be replaced without touching the rules.
- The server sends `Content-Security-Policy`, `X-Content-Type-Options` and `Referrer-Policy` headers on every answer.

## Try it

```text
python -m portfolio init
python -m portfolio import
python -m portfolio project list
python -m portfolio project add --title "My new project" --kind Website --description "Added with a command while the server runs." --source-code-url https://example.com/my-new-project --tag Flask --skill SQLite
python -m portfolio serve
```

Reload the home page after the `project add` command and the new card is there.
