# Setup & Local Development

## 1. Dependencies

From the project root (`quiz_project`), install development and runtime dependencies (which pull in `requirements.txt` via `-r`):

```bash
pip install -r requirements-dev.txt
```

If you only need runtime dependencies without dev/test packages:

```bash
pip install -r requirements.txt
```

If you use a virtual environment on Windows PowerShell, create and activate it first:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## 2. Package & Test Verification

Verify that `webapp.api` imports cleanly and run `pytest` from the project root:

```bash
python -c "import webapp.api; print(webapp.api.app)"
pytest
```

If `webapp` needs `__init__.py` to be treated as a package and does not already have one, create it once rather than on every run:

* **Linux / macOS / Codespaces:** `touch webapp/__init__.py`
* **Windows PowerShell:** `New-Item -ItemType File -Path webapp\__init__.py -Force`

## 3. Running Locally (API on Port `8000` + Frontend on Port `5500`)

Make sure your frontend API base URL points to the local backend (for example, `http://127.0.0.1:8000`).

Start the FastAPI server from the project root:

```bash
python -m uvicorn webapp.api:app --reload --reload-dir . --port 8000
```

In a second terminal (or using Live Server), serve the frontend from `webapp/frontend` on port `5500`:

```bash
cd webapp/frontend
python -m http.server 5500
```