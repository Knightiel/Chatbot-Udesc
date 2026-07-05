"""
Controller do Telegram — usa python-telegram-bot v20+ com polling (RF20).

Protocolo: HTTPS sobre TCP/443 (polling do servidor Telegram Bot API).
"""

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config.settings import settings
from services.bot_service import bot_service
from utils.anonymizer import anonymize_user_id
from utils.logger import get_logger

logger = get_logger(__name__)


async def _reply(update: Update, text: str) -> None:
    """Envia resposta em Markdown, com fallback em texto puro."""
    try:
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(text)


async def _handle_start(update: Update, context) -> None:
    """Comando /start — inicia ou reinicia a conversa."""
    # Uso anônimo: o chat ID real nunca é armazenado nem logado
    user_id = anonymize_user_id(f"telegram:{update.effective_chat.id}")
    logger.info(f"[TELEGRAM] /start de user={user_id}")
    response = bot_service.process_message(user_id, "start", "telegram")
    await _reply(update, response)


async def _handle_message(update: Update, context) -> None:
    """Processa mensagens de texto recebidas."""
    user_id = anonymize_user_id(f"telegram:{update.effective_chat.id}")
    text = update.message.text or ""
    logger.info(f"[TELEGRAM] user={user_id} | mensagem={text[:80]!r}")
    response = bot_service.process_message(user_id, text, "telegram")
    await _reply(update, response)


def run_telegram_bot() -> None:
    """Inicia o bot Telegram em modo polling (blocante — rodar em thread separada)."""
    if not settings.TELEGRAM_TOKEN:
        logger.warning("[TELEGRAM] Token não configurado. Bot Telegram desativado.")
        return

    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", _handle_start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_message)
    )

    logger.info("[TELEGRAM] Polling iniciado...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
