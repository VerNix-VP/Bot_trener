import pytest

from calculations import best_max, make_plan, one_rep_max, round_to_plates


def test_one_rep_max():
    assert one_rep_max(100, 5) == pytest.approx(116.67, abs=0.01)
    assert one_rep_max(60, 10) == pytest.approx(80)


def test_one_rep_max_single_rep():
    assert one_rep_max(150, 1) == 150


def test_round_to_plates():
    assert round_to_plates(101) == 100
    assert round_to_plates(103.9) == 105
    assert round_to_plates(100) == 100


def test_make_plan():
    assert make_plan(200) == [(140, 5), (160, 3), (180, 1)]
    for w, r in make_plan(117):
        assert w % 2.5 == 0


def test_best_max():
    entries = [
        {"weight": 100, "reps": 5},
        {"weight": 120, "reps": 1},
        {"weight": 90, "reps": 3},
    ]
    assert best_max(entries) == 120
    assert best_max([]) == 0
