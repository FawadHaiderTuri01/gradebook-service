import pytest

from errors import ValidationError
from models import parse_number

@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("15", 15.0, id="numeric-string"),
        pytest.param(15, 15.0, id="int"),
        pytest.param("2.5", 2.5, id="decimal-string"),
    ],
)
def test_good_numbers_are_accepted(raw: object, expected: float) -> None:
    assert parse_number(raw) == expected
 

@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("abc", id="text"),
        pytest.param(True, id="bool"),
        pytest.param(None, id="none"),
        pytest.param([], id="list"),
        pytest.param("nan", id="nan"),
        pytest.param("inf", id="inf"),
    ],
)
def test_bad_numbers_are_rejected(raw: object) -> None:
    with pytest.raises(ValidationError):
        parse_number(raw)