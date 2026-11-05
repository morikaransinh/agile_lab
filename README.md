# Everyday Market — E-commerce Product Management

A small Flask e-commerce demo with product listing, search and category
filtering, product details, tax-inclusive prices, and a demo login/account page.
The product catalog is in `products.py`; tax calculations are isolated in
`pricing.py`.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Demo credentials are `demo` / `demo123`.
These defaults are for coursework only. Set `SECRET_KEY`, `DEMO_USERNAME`, and
`DEMO_PASSWORD` in your environment before using the app beyond a local demo.
Never commit a real secret or production password.

## Tests and validation

```powershell
python -m scripts.validate_products
python -m pytest -q
```

Pricing tests cover ordinary prices, zero, invalid inputs, tax boundaries, and
rounding. Selenium tests use Chrome in headless mode and explicit waits for both
successful and rejected login. Install Chrome and a compatible ChromeDriver
(Selenium Manager can locate/download a driver) to run those browser tests.
When Chrome is unavailable, the Selenium tests are reported as skipped.

## Docker

Build and run with Docker Compose:

```powershell
docker compose up --build -d
docker compose ps
docker compose logs web
```

Or build and run the image directly:

```powershell
docker build -t everyday-market .
docker run --rm -p 5000:5000 -e SECRET_KEY=replace-me everyday-market
```

Open `http://127.0.0.1:5000`. Set non-demo credentials and a strong secret
through environment variables before exposing the app outside your machine.

## Git workflow

The product search/category filter was implemented on `feature/product-filter`
and merged into `main`. View the commit history with:

```powershell
git --no-pager log --oneline --graph --decorate
```

GitHub Actions runs the catalog validation script and pytest on pushes to
`main` and `feature/**`, and on pull requests targeting `main`.

## Jira

The three Scrum user stories, priorities, and story points are in
[`jira/user_stories.csv`](jira/user_stories.csv); import and board-demo
instructions are in [`jira/README.md`](jira/README.md). Jira requires a signed-in
project member to import the issues.
