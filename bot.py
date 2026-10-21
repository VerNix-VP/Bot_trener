import os

import telebot

HELP = """Я веду дневник силовых тренировок.

/help — список команд"""

token = os.environ.get("BOT_TOKEN")
if not token:
    raise SystemExit("Не задан токен. Выполни: export BOT_TOKEN=\"токен от @BotFather\"")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", "help"])
def cmd_help(message):
    bot.reply_to(message, HELP)


@bot.message_handler(content_types=["text"])
def other(message):
    bot.reply_to(message, "Не понял команду. Список команд — /help")


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
