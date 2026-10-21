import os

import telebot

from calculations import best_max, one_rep_max
from parsing import parse_add, parse_name
from storage import add_entry, get_entries, load_data, save_data

HELP = """Я веду дневник силовых тренировок.

/add жим 100 5 — записать подход
/max жим — расчётный максимум на 1 повтор
/history жим — последние записи
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
    ans = f"Записал: {name} {w} кг × {r}\nРасчётный максимум: {round(rm, 1)} кг"
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
        ans += f"\n{e['weight']} кг × {e['reps']}"
    bot.reply_to(message, ans)


@bot.message_handler(content_types=["text"])
def other(message):
    bot.reply_to(message, "Не понял команду. Список команд — /help")


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
