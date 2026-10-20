from rules import ensure_weight_fits

def test_ensure_weight_fits_empty() -> None:
    ensure_weight_fits([], 50)