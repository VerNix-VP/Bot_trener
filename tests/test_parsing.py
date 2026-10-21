import pytest

from parsing import fmt_weight, parse_add, parse_name


def test_parse_add():
    assert parse_add("жим 100 5") == ("жим", 100, 5)


def test_parse_add_long_name_and_comma():
    assert parse_add("Жим лёжа 102,5 3") == ("жим лёжа", 102.5, 3)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "жим 100",
        "жим сто пять",
        "жим 100 2.5",
        "жим -5 3",
        "жим 0 3",
        "жим 5000 3",
        "жим 100 0",
        "жим inf 3",
        "жим nan 3",
    ],
)
def test_parse_add_errors(text):
    with pytest.raises(ValueError):
        parse_add(text)


def test_parse_name():
    assert parse_name("  Присед ") == "присед"
    assert parse_name("жим   лёжа") == "жим лёжа"
    with pytest.raises(ValueError):
        parse_name("   ")


def test_fmt_weight():
    assert fmt_weight(100.0) == "100"
    assert fmt_weight(102.5) == "102.5"
