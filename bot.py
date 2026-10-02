import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

RESPONSES = {
    "שלום": "אהלן מה קורה יא מלך",
    "עובדים?": "אנחנו עובדים 24/7",
    "עובדים": "אנחנו עובדים 24/7",
}


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()

    if message in RESPONSES:
        await update.message.reply_text(RESPONSES[message])
    else:
        await update.message.reply_text("כמה דקות ואחזור אליכם")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
    )

    print("Ice Doctor is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
