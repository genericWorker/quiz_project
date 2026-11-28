import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
from urllib import error, parse, request

_ROOT = Path(__file__).resolve().parent
_WEBAPP = _ROOT / "webapp"
for _p in (str(_ROOT), str(_WEBAPP)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi.testclient import TestClient
from quizfactory import QuizFactory
from webapp.api import app

RENDER_API_URL = "https://quiz-api-genericworkerquiz-project.onrender.com"


def _request_json(
    method: str,
    path: str,
    base_url: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    timeout: float = 75.0,
) -> Any:
    if base_url is None:
        client = TestClient(app)
        if method == "GET":
            resp = client.get(path)
        else:
            resp = client.post(path, json=payload)
        resp.raise_for_status()
        return resp.json()

    url = f"{base_url.rstrip('/')}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} from {url}") from exc


def main() -> None:
    titles = list_available_quizzes()
    for title in titles:
        bundle = fetch_quiz_bundle(title)
        selections = {
            str(i): 0 for i in range(len(bundle.get("questions", [])))
        }
        graded = grade_quiz_answers(title, selections)
        print(
            f"{bundle['title']}: {len(bundle['questions'])} questions, "
            f"{graded['score']}/{graded['total_possible_points']} pts ({graded['percentage']}%)"
        )


def list_available_quizzes(base_url: Optional[str] = None) -> List[str]:
    return _request_json("GET", "/api/quizzes", base_url=base_url)


def fetch_quiz_bundle(
    quiz_title: str, base_url: Optional[str] = None
) -> Dict[str, Any]:
    encoded = parse.quote(quiz_title, safe="")
    return _request_json("GET", f"/api/quizzes/{encoded}", base_url=base_url)


def grade_quiz_answers(
    quiz_title: str,
    selections: Dict[str, Optional[int]],
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    return _request_json(
        "POST",
        "/api/grade",
        base_url=base_url,
        payload={"quiz_title": quiz_title, "selections": selections},
    )


if __name__ == "__main__":
    main()