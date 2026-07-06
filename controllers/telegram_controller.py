import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from services.bot_service import bot_service


async def _reply(update: Update, text: str) -> None:
    """Envia resposta em Markdown, com fallback em texto puro."""
    try:
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(text)


async def _handle_start(update: Update, context) -> None:
    """Comando /start — inicia ou reinicia a conversa."""
    user_id = update.effective_chat.id
    response = bot_service.process_message(user_id, "start", "telegram")
    await _reply(update, response)


async def _handle_message(update: Update, context) -> None:
    """Processa mensagens de texto recebidas."""
    user_id = update.effective_chat.id
    text = update.message.text or ""
    response = bot_service.process_message(user_id, text, "telegram")
    await _reply(update, response)


def run_telegram_bot() -> None:
    """Inicia o bot Telegram em modo polling (blocante — rodar em thread separada)."""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("TELEGRAM_TOKEN não definido — bot Telegram desativado.")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", _handle_start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_message)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
