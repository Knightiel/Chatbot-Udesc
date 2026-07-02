import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv(
        "TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886"
    )
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    PORT: int = int(os.getenv("PORT", "5000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/chatbot.log")


settings = Settings()
