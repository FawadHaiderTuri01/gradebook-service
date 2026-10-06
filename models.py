from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class Student:
    id: str
    name: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("id must not be empty")
        if not self.name.strip():
            raise ValidationError("name must not be empty")


@dataclass(frozen=True)
class Assessment:
    id: str
    title: str
    weight: float
    total: float

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("id must not be empty")
        if not self.title.strip():
            raise ValidationError("title must not be empty")
        if not 0 <= self.weight <= 100:
            raise ValidationError("weight must be between 0 and 100")
        if self.total <= 0:
            raise ValidationError("total must be above 0")


@dataclass(frozen=True)
class Mark:
    student: str
    assessment: str
    score: float

    def __post_init__(self) -> None:
        if not self.student.strip():
            raise ValidationError("student must not be empty")
        if not self.assessment.strip():
            raise ValidationError("assessment must not be empty")
        if self.score < 0:
            raise ValidationError("score must not be negative")

def parse_number(value: object) -> float:
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValidationError("invalid number")

    raise ValidationError("invalid number")


def parse_text(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("invalid text")
    return value


def parse_student(data: object) -> Student:
    if not isinstance(data, dict):
        raise ValidationError("invalid student")

    return Student(
        id=parse_text(data.get("id")),
        name=parse_text(data.get("name")),
    )


def parse_assessment(data: object) -> Assessment:
    if not isinstance(data, dict):
        raise ValidationError("invalid assessment")

    return Assessment(
        id=parse_text(data.get("id")),
        title=parse_text(data.get("title")),
        weight=parse_number(data.get("weight")),
        total=parse_number(data.get("total")),
    )


def parse_mark(data: object) -> Mark:
    if not isinstance(data, dict):
        raise ValidationError("invalid mark")

    return Mark(
        student=parse_text(data.get("student")),
        assessment=parse_text(data.get("assessment")),
        score=parse_number(data.get("score")),
    )