import json
import os

FILE = "data.json"


def load_data(path=FILE):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Файл с данными повреждён")
    if not isinstance(data, dict):
        raise ValueError("Файл с данными имеет неверный формат")
    return data


def save_data(data, path=FILE):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        raise ValueError("Не удалось сохранить данные, попробуй ещё раз")


def add_entry(data, user_id, name, w, r):
    uid = str(user_id)
    if uid not in data:
        data[uid] = []
    data[uid].append({"exercise": name, "weight": w, "reps": r})


def get_entries(data, user_id, name):
    res = []
    for e in data.get(str(user_id), []):
        if e["exercise"] == name:
            res.append(e)
    return res


def delete_last(data, user_id):
    uid = str(user_id)
    if uid not in data or len(data[uid]) == 0:
        raise ValueError("Удалять нечего: записей пока нет")
    return data[uid].pop()


def get_exercises(data, user_id):
    names = set()
    for e in data.get(str(user_id), []):
        names.add(e["exercise"])
    return sorted(names)
