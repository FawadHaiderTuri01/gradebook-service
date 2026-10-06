import math

import pytest

from errors import ValidationError
from models import parse_assessment, parse_number, parse_student


def test_numeric_string_accepted() -> None:
    assert parse_number("25") == 25.0


def test_text_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number("abc")


def test_bool_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number(True)


def test_nan_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number(math.nan)


def test_zero_total_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_assessment({
            "id": "A1",
            "title": "Test",
            "weight": 50,
            "total": 0,
        })


def test_negative_score_rejected() -> None:
    from models import parse_mark

    with pytest.raises(ValidationError):
        parse_mark({
            "student": "S1",
            "assessment": "A1",
            "score": -5,
        })


def test_missing_field_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_student({"id": "S1"})


def test_non_dict_payload_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_student("student")


def test_valid_assessment() -> None:
    assessment = parse_assessment({
        "id": "A1",
        "title": "Final Exam",
        "weight": 40,
        "total": 100,
    })

    assert assessment.id == "A1"
    assert assessment.title == "Final Exam"
    assert assessment.weight == 40.0
    assert assessment.total == 100.0