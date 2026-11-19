**English** · [Dansk](Step-6-Tests-da) · [Bahasa Malaysia](Step-6-Tests-ms)

# Step 6: Tests

## What this step builds

`pytest` runs unit tests for the entities and use cases, integration tests for the SQLite repositories, Flask test-client tests for every route and header, and end-to-end tests that start the real server and read its answers. `lint-imports` checks that the layers only depend inward, `ruff` checks style and `mypy --strict` checks the types.

![A test run](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-06-tests.png)

## What we gained

- Tests at three levels: small and fast at the bottom, a few that prove the whole site at the top.
- Because the use cases depend on ports, they are tested with simple in-memory stand-ins, with no files and no browser.
- A rule that is checked by a tool (the layer contracts) stays true when the code grows.

## Try it

```text
python -m pytest
python -m ruff check .
python -m mypy
lint-imports
```

Next: [Step 7: Flip cards and profile](Step-7-Flip-Cards-and-Profile).
