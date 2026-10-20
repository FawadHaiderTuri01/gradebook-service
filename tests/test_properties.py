from unittest.mock import patch
import pytest
from hypothesis import given, strategies as st
import gradebook


@pytest.mark.xfail(strict=True, reason="duplicate marks are all counted")
@given(
    scores=st.lists(
        st.integers(min_value=0, max_value=20),
        min_size=1,
        max_size=5,
    )
)
def test_pct_does_not_exceed_weight(scores: list[int]) -> None:
    state = {
        "students": {"S1": {"id": "S1", "name": "Ayesha"}},
        "assessments": {
            "A1": {"id": "A1", "title": "Quiz 1", "weight": 10, "total": 20}
        },
        "marks": [],
    }

    for score in scores:
        gradebook.add_mark(
            state,
            gradebook.Mark(student="S1", assessment="A1", score=float(score)),
            now=lambda: "2026-01-01",
            save=lambda s: None,
        )

    with patch.object(gradebook, "STATE", state):
        assert float(gradebook.pct("S1")) <= 10.0