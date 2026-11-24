from unittest.mock import Mock

import pytest

from errors import ConflictError, ValidationError
from gradebook import add_assessment
from models import Assessment


def test_add_assessment_valid(state) -> None:
    save_mock = Mock()
    assessment = Assessment(id="A3", title="Final Exam", weight=50.0, total=100.0)
    add_assessment(state, assessment, save_mock)
    assert assessment.id in state["assessments"]
    save_mock.assert_called_once()


def test_add_assessment_rejects_over_100(state) -> None:
    save_mock = Mock()
    over_assessment = Assessment(id="A3", title="Final Exam", weight=70.0, total=100.0)
    with pytest.raises(ValidationError):
        add_assessment(state, over_assessment, save_mock)
    save_mock.assert_not_called()


def test_add_assessment_rejects_duplicate_id(state) -> None:
    save_mock = Mock()
    dup_assessment = Assessment(id="A1", title="Duplicate", weight=20.0, total=100.0)
    with pytest.raises(ConflictError):
        add_assessment(state, dup_assessment, save_mock)
    save_mock.assert_not_called()

def test_failed_save_leaves_no_trace(state) -> None:
    def failed_save():
        raise OSError("disk full")

    assessment = Assessment(
        id="A3",
        title="Final Exam",
        weight=10.0,
        total=50.0,
    )

    with pytest.raises(OSError, match="disk full"):
        add_assessment(state, assessment, failed_save)

    assert assessment.id not in state["assessments"]