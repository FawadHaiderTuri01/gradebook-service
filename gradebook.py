import datetime
import http.server
import json
import logging
import sys
from typing import Any, Callable

from errors import ConflictError, NotFoundError, ValidationError
from models import Mark, parse_assessment, parse_mark, parse_student

logger = logging.getLogger(__name__)

DATA = "gradebook.json"
STATE: dict[str, Any] = {}


def load() -> None:
    global STATE
    try:
        with open(DATA) as f:
            STATE = json.load(f)
    except FileNotFoundError:
        STATE = {"students": {}, "assessments": {}, "marks": []}


def save() -> None:
    with open(DATA, "w") as f:
        json.dump(STATE, f)


def pct(sid: str) -> str:
    total = 0.0
    got = 0.0
    for m in STATE["marks"]:
        if m["student"] == sid:
            a = STATE["assessments"].get(m["assessment"])
            if a:
                got = got + float(m["score"]) * float(a["weight"]) / float(a["total"])
                total = total + float(a["weight"])
    if total == 0:
        return "0"
    return str(round(got, 2))


def now() -> str:
    return str(datetime.datetime.now(datetime.timezone.utc))


def add_mark(
    state: dict[str, Any],
    mark: Mark,
    now: Callable[[], str],
    save: Callable[[], None],
) -> None:
    """Check a mark against the gradebook, then record it and save."""
    if mark.student not in state["students"]:
        raise NotFoundError(f"no such student: {mark.student}")
    assessment_row = state["assessments"].get(mark.assessment)
    if assessment_row is None:
        raise NotFoundError(f"no such assessment: {mark.assessment}")
    if float(mark.score) > float(assessment_row["total"]):
        raise ValidationError("score exceeds assessment total")
    state["marks"].append(
        {
            "student": mark.student,
            "assessment": mark.assessment,
            "score": mark.score,
            "at": now(),
        }
    )
    save()


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        pass

    def _send(self, code: int, obj: object) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_error(self, error: Exception) -> None:
        if isinstance(error, ValidationError):
            self._send(400, {"error": str(error)})
        elif isinstance(error, NotFoundError):
            self._send(404, {"error": str(error)})
        elif isinstance(error, ConflictError):
            self._send(409, {"error": str(error)})
        else:
            logger.exception("Unexpected error")
            self._send(500, {"error": "internal error"})

    def _get(self) -> tuple[int, object]:
        if self.path == "/students":
            return 200, list(STATE["students"].values())

        if self.path.startswith("/students/"):
            sid = self.path.split("/")[2]

            if sid not in STATE["students"]:
                raise NotFoundError("student not found")

            student = dict(STATE["students"][sid])
            student["percentage"] = pct(sid)
            return 200, student

        if self.path == "/assessments":
            return 200, list(STATE["assessments"].values())

        if self.path == "/report":
            out = []

            for sid in STATE["students"]:
                out.append(
                    {
                        "id": sid,
                        "name": STATE["students"][sid]["name"],
                        "pct": pct(sid),
                    }
                )

            return 200, out

        raise NotFoundError("unknown endpoint")

    def _post(self) -> tuple[int, object]:
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n)

        try:
            d = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValidationError("bad json") from error

        if self.path == "/students":
            student = parse_student(d)

            if student.id in STATE["students"]:
                raise ConflictError("student already exists")

            STATE["students"][student.id] = {
                "id": student.id,
                "name": student.name,
                "joined": now(),
            }

            save()
            return 201, STATE["students"][student.id]

        if self.path == "/assessments":
            assessment = parse_assessment(d)

            if assessment.id in STATE["assessments"]:
                raise ConflictError("assessment already exists")

            STATE["assessments"][assessment.id] = {
                "id": assessment.id,
                "title": assessment.title,
                "weight": assessment.weight,
                "total": assessment.total,
            }

            save()
            return 201, STATE["assessments"][assessment.id]

        if self.path == "/marks":
            mark = parse_mark(d)
            add_mark(STATE, mark, now, save)
            logger.info("recorded mark for %s score %s", mark.student, mark.score)
            return 200, {"ok": True}

        raise NotFoundError("unknown endpoint")

    def do_GET(self) -> None:
        try:
            code, body = self._get()
            self._send(code, body)
        except Exception as error:  # noqa: BLE001
            self._handle_error(error)

    def do_POST(self) -> None:
        try:
            code, body = self._post()
            self._send(code, body)
        except Exception as error:  # noqa: BLE001
            self._handle_error(error)

def main(argv: list[str]) -> None:
    load()
    port = 8000
    if len(argv) > 1:
        if not argv[1].isdigit() or not 1 <= int(argv[1]) <= 65535:
            raise SystemExit("port must be a whole number from 1 to 65535")
        port = int(argv[1])
    logger.info("gradebook on %s", port)
    http.server.HTTPServer(("", port), Handler).serve_forever()


if __name__ == "__main__":
    main(sys.argv)