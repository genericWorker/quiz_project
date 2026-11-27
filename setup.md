# Setup & Local Development

## 1. Extracting the Project (Codespaces / Zip Archive)

If you are setting up the repository from a downloaded zip archive (`quiz_project-main.zip`) without `git` access:

```bash
mkdir -p quiz_project _extract_tmp
unzip -o quiz_project-main.zip -d _extract_tmp
INNER_DIR=$(find _extract_tmp -mindepth 1 -maxdepth 1 -type d | head -n 1)
mv "$INNER_DIR"/* "$INNER_DIR"/.[!.]* quiz_project/ 2>/dev/null || true
rm -rf _extract_tmp
cd quiz_project
```

## 2. Dependencies

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

## 3. Package & Test Verification

Verify that `webapp.api` imports cleanly and run `pytest` from the project root:

```bash
python -c "import webapp.api; print(webapp.api.app)"
pytest
```

If `webapp` needs `__init__.py` to be treated as a package and does not already have one, create it once rather than on every run:

- **Linux / macOS / Codespaces:** `touch webapp/__init__.py`
- **Windows PowerShell:** `New-Item -ItemType File -Path webapp\__init__.py -Force`

## 4. Running Locally (API on Port `8000` + Frontend on Port `5500`)

Make sure `webapp/frontend/app.js` resolves `API_BASE_URL` for your current host (`http://127.0.0.1:8000` on `127.0.0.1` or `localhost`, the corresponding `-8000.` forwarded host when served from a `-5500.` Codespaces hostname, and your Render URL otherwise).

### Terminal 1 — FastAPI Backend (Port `8000`)

Start the FastAPI server from the project root:

```bash
python -m uvicorn webapp.api:app --reload --reload-dir . --port 8000
```

### Terminal 2 — Static Frontend (Port `5500`)

Stay in the project root (`quiz_project`) and serve `webapp/frontend` on port `5500` using `--directory` so your terminal stays anchored at the root:

```bash
python -m http.server 5500 --directory webapp/frontend
```

## 5. Opening `index.html` in the Browser

- **Local machine:** Open `http://127.0.0.1:5500` (or use Live Server / **Open in Browser** on `webapp/frontend/index.html`).
- **GitHub Codespaces (`cs50.dev`):**
  1. Open the **Ports** tab in the bottom panel of VS Code.
  2. Confirm both port `5500` and port `8000` are listed and forwarded (set port `8000` visibility to **Public** if the browser blocks cross-port requests).
  3. Click **Open in Browser** (globe icon) next to port `5500`.
  4. Avoid opening `index.html` as a `file://` URL or starting Live Server on port `5500` while `python -m http.server 5500` is already running (which triggers `OSError: [Errno 98] Address already in use`).