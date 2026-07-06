import os
import threading

from dotenv import load_dotenv
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from controllers.telegram_controller import run_telegram_bot
from routes.whatsapp_routes import whatsapp_bp

app = Flask(__name__)
app.register_blueprint(whatsapp_bp)


def _start_telegram_thread() -> None:
    try:
        run_telegram_bot()
    except Exception as exc:
        print(f"Falha ao iniciar bot Telegram: {exc}")


if __name__ == "__main__":

    if os.getenv("TELEGRAM_TOKEN"):
        t = threading.Thread(target=_start_telegram_thread, daemon=True, name="telegram")
        t.start()
    else:
        print("TELEGRAM_TOKEN não definido — bot Telegram desativado.")

    if not os.getenv("TWILIO_ACCOUNT_SID"):
        print("TWILIO_ACCOUNT_SID não definido — webhook WhatsApp desativado.")

    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
