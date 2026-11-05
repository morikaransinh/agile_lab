# Everyday Market

A small Flask e-commerce product-management demo. The catalog and account pages
are rendered by Flask; product prices include a configurable tax calculation.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The local demo account is `demo` / `demo123`.
These defaults are for coursework only. Set `SECRET_KEY`, `DEMO_USERNAME`, and
`DEMO_PASSWORD` in the environment before using the app beyond a local demo.
