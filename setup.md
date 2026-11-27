# Setup & Local Development (`SETUP.md`)

## 1. Dependencies

From the repository root (`C:\Users\mwhit\PycharmProjects\quiz_project`) with `.venv` active:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

`requirements.txt` holds runtime packages for the hosted Render API, while `requirements-dev.txt` layers in local test and desktop packages (`-r requirements.txt`).

## 2. Package Initialization & Import Check

Ensure `webapp` is recognized as a package and verify imports directly before starting Uvicorn:

```powershell
New-Item -ItemType File -Path webapp\__init__.py -Force
python -c "import webapp.api; print(webapp.api.app)"
```

## 3. Running Locally (`8000` API + `5500` Frontend)

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";
```

Start the FastAPI server from the repository root:

```powershell
python -m uvicorn webapp.api:app --reload --reload-dir . --port 8000
```

In a second terminal (or via Live Server), serve the frontend on port `5500`:

```powershell
cd C:\Users\mwhit\PycharmProjects\quiz_project\webapp\frontend
python -m http.server 5500
```