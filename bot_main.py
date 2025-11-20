import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot_app = Application.builder().token(BOT_TOKEN).build()

async def start_cmd(update, context):
    await update.message.reply_text("Bot aktif!")

bot_app.add_handler(CommandHandler("start", start_cmd))

if __name__ == "__main__":
    bot_app.run_polling()
