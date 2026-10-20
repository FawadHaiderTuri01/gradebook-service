import pytest
from errors import ValidationError
from rules import ensure_weight_fits

def test_ensure_weight_fits_empty() -> None:
    ensure_weight_fits([], 50)

def test_ensure_weight_fits_rejects_over_100() -> None:
    with pytest.raises(ValidationError, match="100"):
        ensure_weight_fits([60], 50)

def test_ensure_weight_fits_exactly_100() -> None:
    ensure_weight_fits([60], 40)

def test_ensure_weight_fits_float_tolerance() -> None:
    ensure_weight_fits([9.3, 27.3, 33.7], 29.7)