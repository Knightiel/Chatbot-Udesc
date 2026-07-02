"""
Controller do WhatsApp — processa webhooks do Twilio (RF19).

Protocolo: HTTPS sobre TCP/443 (Twilio → ngrok → Flask).
"""

from flask import Request
from twilio.twiml.messaging_response import MessagingResponse

from services.bot_service import bot_service
from utils.logger import get_logger
from utils.network_info import get_network_info

logger = get_logger(__name__)


def handle_whatsapp(request: Request) -> str:
    """Recebe mensagem do Twilio, processa e retorna TwiML."""
    get_network_info(request)

    from_number: str = request.form.get("From", "unknown")
    body: str = request.form.get("Body", "").strip()

    logger.info(f"[WHATSAPP] De: {from_number} | Mensagem: {body[:80]!r}")

    response_text = bot_service.process_message(from_number, body, "whatsapp")

    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)
