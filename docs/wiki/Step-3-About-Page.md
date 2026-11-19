**English** · [Dansk](Step-3-About-Page-da) · [Bahasa Malaysia](Step-3-About-Page-ms)

# Step 3: About page

## What this step builds

The use case `about` reads the owner's profile (name, headline, summary, skills and links) and returns an `AboutPage`. The page shows who the owner is, the skills as a list and the links, such as GitHub and LinkedIn. Links are only accepted when they start with `http://` or `https://`.

![The about page without a stylesheet](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-03-about-page.png)

## What we gained

- A second page reuses the same layout and navigation, so a header change is made once.
- A link from a data file is user input too: schemes such as `javascript:` are refused.
- The same pattern (entity, repository port, use case, template) repeats, which makes a new page quick to add.

## Try it

```text
python -m portfolio serve
# open http://127.0.0.1:8000/about in a browser
```

Next: [Step 4: Style](Step-4-Style).
