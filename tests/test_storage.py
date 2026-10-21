import pytest

from storage import add_entry, delete_last, get_entries, load_data, save_data


def test_save_and_load(tmp_path):
    path = tmp_path / "data.json"
    data = {}
    add_entry(data, 42, "жим", 100, 5)
    save_data(data, path)
    assert load_data(path) == data


def test_missing_file(tmp_path):
    assert load_data(tmp_path / "nope.json") == {}


@pytest.mark.parametrize("content", ["это не json", "[1, 2, 3]"])
def test_bad_file(tmp_path, content):
    path = tmp_path / "data.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        load_data(path)


def test_get_entries():
    data = {}
    add_entry(data, 1, "жим", 100, 5)
    add_entry(data, 1, "присед", 140, 3)
    add_entry(data, 2, "жим", 80, 5)
    assert get_entries(data, 1, "жим") == [{"exercise": "жим", "weight": 100, "reps": 5}]
    assert get_entries(data, 3, "жим") == []


def test_delete_last():
    data = {}
    add_entry(data, 1, "жим", 100, 5)
    add_entry(data, 1, "присед", 140, 3)
    assert delete_last(data, 1) == {"exercise": "присед", "weight": 140, "reps": 3}
    assert len(data["1"]) == 1


def test_delete_last_empty():
    with pytest.raises(ValueError):
        delete_last({}, 1)
    with pytest.raises(ValueError):
        delete_last({"1": []}, 1)
