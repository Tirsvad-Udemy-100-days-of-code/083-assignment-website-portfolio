**English** · [Dansk](Step-2-Home-Page-da) · [Bahasa Malaysia](Step-2-Home-Page-ms)

# Step 2: Home page

## What this step builds

The use case `home` asks the project repository for all projects and returns a `HomePage` with one card of plain data per project. A Jinja template turns that into HTML. The picture shows the page with its stylesheet removed, so you see the bare structure: a heading, a list of projects and for each one a title, a picture, a description and a link.

![The home page without a stylesheet](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-02-home-page-structure.png)

## What we gained

- A use case holds what the program does; the template only decides how it looks.
- Jinja escapes everything that comes from the data before it reaches the page (autoescape), so a title with `<script>` is shown as text, never run.
- Semantic HTML (headings, lists, links) works without any CSS, and a page can be tested without a browser.

## Try it

```text
python -m portfolio serve
# open http://127.0.0.1:8000 in a browser
```

Next: [Step 3: About page](Step-3-About-Page).
