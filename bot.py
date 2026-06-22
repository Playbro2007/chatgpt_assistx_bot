import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ChatGPT Assistant. Напиши вопрос, и я помогу."
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты полезный Telegram-бот. Отвечай подробно, понятно и на русском языке."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception:
        await update.message.reply_text(
            "Ошибка. Проверь BOT_TOKEN и OPENAI_API_KEY в настройках .env."
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY не найден")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    app.run_polling()


if __name__ == "__main__":
    main()
