from unittest.mock import Mock

import pytest

from errors import ValidationError
from gradebook import add_mark
from models import Mark
from rules import ensure_weight_fits


# 1. Assessment weight boundaries for ensure_weight_fits
@pytest.mark.parametrize("weight", [0.0, 100.0])
def test_ensure_weight_fits_accepted(weight: float) -> None:
    ensure_weight_fits([], weight)


@pytest.mark.parametrize("weight", [-0.01, 100.01])
def test_ensure_weight_fits_rejected(weight: float) -> None:
    with pytest.raises(ValidationError):
        ensure_weight_fits([], weight)


# 2. Score boundary tests for add_mark (Assessment total = 20)
@pytest.mark.parametrize("score", [0.0, 20.0])
def test_add_mark_score_accepted(state, score: float) -> None:
    save_mock = Mock()
    mark = Mark(student="S1", assessment="A1", score=score)
    add_mark(state, mark, now=lambda: "2026-01-01", save=save_mock)
    save_mock.assert_called_once()


@pytest.mark.parametrize("score", [-0.01, 20.01])
def test_add_mark_score_rejected(state, score: float) -> None:
    save_mock = Mock()
    initial_marks_count = len(state["marks"])
    with pytest.raises(ValidationError):
        mark = Mark(student="S1", assessment="A1", score=score)
        add_mark(state, mark, now=lambda: "2026-01-01", save=save_mock)
    save_mock.assert_not_called()
    assert len(state["marks"]) == initial_marks_count