def parse_add(text):
    parts = text.split()
    if len(parts) < 3:
        raise ValueError("Формат: /add упражнение вес повторы, например /add жим 100 5")

    name = " ".join(parts[:-2]).lower()

    try:
        w = float(parts[-2].replace(",", "."))
        r = int(parts[-1])
    except ValueError:
        raise ValueError("Вес и повторы должны быть числами, например /add жим 100 5")

    if not 0 < w <= 1000:
        raise ValueError("Вес должен быть от 0 до 1000 кг")
    if not 1 <= r <= 100:
        raise ValueError("Повторов должно быть от 1 до 100")

    return name, w, r


def parse_name(text):
    name = " ".join(text.split()).lower()
    if name == "":
        raise ValueError("Укажи упражнение, например: /max жим")
    return name
