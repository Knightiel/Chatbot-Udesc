"""
Ponto de entrada da aplicação UDESC ChatBot.

Inicia:
  - Flask (servidor webhook para WhatsApp/Twilio)
  - Bot do Telegram (thread em background, polling)

Arquitetura Cliente-Servidor sobre TCP/IP (RT01, RT02).
"""

import threading

from flask import Flask

from config.settings import settings
from controllers.telegram_controller import run_telegram_bot
from routes.whatsapp_routes import whatsapp_bp
from utils.logger import get_logger
from utils.network_info import print_network_summary

logger = get_logger(__name__)

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.register_blueprint(whatsapp_bp)


def _start_telegram_thread() -> None:
    """Executa o polling do Telegram em thread daemon."""
    try:
        run_telegram_bot()
    except Exception as exc:
        logger.error(f"[TELEGRAM] Erro na thread: {exc}")


if __name__ == "__main__":
    print_network_summary()

    # Telegram em background (polling)
    if settings.TELEGRAM_TOKEN:
        t = threading.Thread(target=_start_telegram_thread, daemon=True, name="telegram")
        t.start()
        logger.info("[APP] Thread do Telegram iniciada.")
    else:
        logger.warning("[APP] TELEGRAM_TOKEN não definido — bot Telegram desativado.")

    if not settings.TWILIO_ACCOUNT_SID:
        logger.warning("[APP] TWILIO_ACCOUNT_SID não definido — webhook WhatsApp inativo.")

    logger.info(f"[APP] Flask iniciando na porta {settings.PORT}...")
    logger.info(f"[APP] Webhook WhatsApp: POST http://0.0.0.0:{settings.PORT}/whatsapp")
    logger.info(f"[APP] Health check:     GET  http://0.0.0.0:{settings.PORT}/health")

    # Flask (webhook para WhatsApp)
    app.run(host="0.0.0.0", port=settings.PORT, debug=False, use_reloader=False)
