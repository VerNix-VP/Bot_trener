import os

import telebot

from calculations import best_max, make_plan, one_rep_max
from parsing import fmt_weight, parse_add, parse_name
from storage import add_entry, delete_last, get_entries, load_data, save_data

HELP = """Я веду дневник силовых тренировок.

/add жим 100 5 — записать подход
/max жим — расчётный максимум на 1 повтор
/history жим — последние записи
/plan жим — рабочие веса от максимума
/undo — удалить последнюю запись
/help — список команд"""

token = os.environ.get("BOT_TOKEN")
if not token:
    raise SystemExit("Не задан токен. Выполни: export BOT_TOKEN=\"токен от @BotFather\"")

bot = telebot.TeleBot(token)


def get_text(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return ""
    return parts[1]


@bot.message_handler(commands=["start", "help"])
def cmd_help(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=["add"])
def cmd_add(message):
    try:
        name, w, r = parse_add(get_text(message))
        data = load_data()
        old = best_max(get_entries(data, message.from_user.id, name))
        add_entry(data, message.from_user.id, name, w, r)
        save_data(data)
    except ValueError as e:
        bot.reply_to(message, str(e))
        return

    rm = one_rep_max(w, r)
    ans = f"Записал: {name} {fmt_weight(w)} кг × {r}\nРасчётный максимум: {round(rm, 1)} кг"
    if rm > old:
        ans += "\nНовый рекорд!"
    bot.reply_to(message, ans)


@bot.message_handler(commands=["max"])
def cmd_max(message):
    try:
        name = parse_name(get_text(message))
        entries = get_entries(load_data(), message.from_user.id, name)
    except ValueError as e:
        bot.reply_to(message, str(e))
        return

    if len(entries) == 0:
        bot.reply_to(message, f"По упражнению «{name}» пока нет записей")
        return
    bot.reply_to(message, f"{name}: максимум {round(best_max(entries), 1)} кг")


@bot.message_handler(commands=["history"])
def cmd_history(message):
    try:
        name = parse_name(get_text(message))
        entries = get_entries(load_data(), message.from_user.id, name)
    except ValueError as e:
        bot.reply_to(message, str(e))
        return

    if len(entries) == 0:
        bot.reply_to(message, f"По упражнению «{name}» пока нет записей")
        return
    ans = f"Последние записи — {name}:"
    for e in entries[-10:]:
        ans += f"\n{fmt_weight(e['weight'])} кг × {e['reps']}"
    bot.reply_to(message, ans)


@bot.message_handler(commands=["plan"])
def cmd_plan(message):
    try:
        name = parse_name(get_text(message))
        entries = get_entries(load_data(), message.from_user.id, name)
    except ValueError as e:
        bot.reply_to(message, str(e))
        return

    if len(entries) == 0:
        bot.reply_to(message, f"Сначала запиши подход: /add {name} вес повторы")
        return
    rm = best_max(entries)
    ans = f"План для «{name}» (максимум {round(rm, 1)} кг):"
    for w, r in make_plan(rm):
        ans += f"\n{fmt_weight(w)} кг × {r}"
    bot.reply_to(message, ans)


@bot.message_handler(commands=["undo"])
def cmd_undo(message):
    try:
        data = load_data()
        e = delete_last(data, message.from_user.id)
        save_data(data)
    except ValueError as err:
        bot.reply_to(message, str(err))
        return
    bot.reply_to(message, f"Удалил: {e['exercise']} {fmt_weight(e['weight'])} кг × {e['reps']}")


@bot.message_handler(content_types=["text"])
def other(message):
    bot.reply_to(message, "Не понял команду. Список команд — /help")


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
