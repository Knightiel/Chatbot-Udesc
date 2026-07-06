from flask import Blueprint, request

from controllers.whatsapp_controller import handle_whatsapp

whatsapp_bp = Blueprint("whatsapp", __name__)


@whatsapp_bp.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Endpoint chamado pelo Twilio ao receber mensagem no WhatsApp."""
    return handle_whatsapp(request), 200, {"Content-Type": "text/xml"}


@whatsapp_bp.route("/health", methods=["GET"])
def health_check():
    """Verifica se o servidor está ativo."""
    return {"status": "ok", "service": "UDESC ChatBot"}, 200
