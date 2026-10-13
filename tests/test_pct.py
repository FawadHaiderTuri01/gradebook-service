import gradebook


def test_student_with_no_marks_has_zero_percent(loaded):
    result = gradebook.pct("S1")

    assert result == "0"


def test_mark_of_15_out_of_20_on_weight_10_gives_7_5(loaded):
    loaded["marks"].append({"student": "S1", "assessment": "A1", "score": 15})

    result = gradebook.pct("S1")

    assert result == "7.5"


def test_mark_for_unknown_assessment_is_ignored(loaded):
    loaded["marks"].append({"student": "S1", "assessment": "GHOST", "score": 15})

    result = gradebook.pct("S1")

    assert result == "0"