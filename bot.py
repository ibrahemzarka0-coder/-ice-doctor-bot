import os
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❄️ Welcome to Ice Doctor!\n\n"
        "Send me your question and I’ll try to help."
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = await client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "You are Ice Doctor, a helpful AI assistant. "
                "Answer clearly and concisely. "
                "If the user asks about medical issues, provide general "
                "information and encourage appropriate professional or "
                "emergency medical care when needed."
            ),
            input=user_text,
        )

        await update.message.reply_text(response.output_text)

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again."
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, answer)
    )

    print("Ice Doctor is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
