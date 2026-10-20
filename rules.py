from errors import ValidationError

MAX_TOTAL_WEIGHT: float = 100.0
TOLERANCE: float = 1e-9


def ensure_weight_fits(existing_weights: list[float], new_weight: float) -> None:
    """Ensure that total assessment weight including new_weight does not exceed MAX_TOTAL_WEIGHT."""
    if sum(existing_weights) + new_weight > MAX_TOTAL_WEIGHT + TOLERANCE:
        raise ValidationError("Total weight exceeds 100")