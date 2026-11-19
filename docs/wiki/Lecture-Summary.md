**English** · [Dansk](Lecture-Summary-da) · [Bahasa Malaysia](Lecture-Summary-ms)

# Lecture summary

This is a short summary of the Day 83 lecture, in my own words. The lecture gives no step-by-step help on purpose.

## The assignment

Build a website that shows who you are as a developer: a home page with the projects you have made, and an about page with a few words about yourself and your skills. Each project has a name, a kind, a description, a picture and a link to its source code.

## The idea behind it

After 82 days of small exercises the course asks you to plan and build something on your own. The lecture suggests a web application with a small database, but the point is the practice of breaking a goal into steps, finding out what you do not know and solving it yourself.

## The functions the assignment names

The assignment names three functions: `home` (the page with the projects), `about` (the page about you) and `load_from_json` (reads the projects from a file). This project keeps those names.

## How this project answers it

The project reaches the same goal with Flask for the web pages and SQLite, through Python's own `sqlite3` module, for the data. The pages are rendered from the database on every request, so a change shows at once. The reasoning is written down in the decision record [ADR-0003](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/src/branch/main/docs/adr/adr-0003-flask-and-jinja-on-sqlite.md). Each step is explained on its own page, starting with [Step 1](Step-1-Project-Data).
