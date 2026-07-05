"""
Controller da interface web — aceita mensagens JSON sem cadastro (RF19/RF20).

Qualquer usuário com acesso à URL pode conversar imediatamente.
A sessão é identificada por um UUID gerado no browser (localStorage),
sem login ou registro.
"""

import uuid
from flask import Request, jsonify

from services.bot_service import bot_service
from utils.anonymizer import anonymize_user_id
from utils.logger import get_logger
from utils.network_info import get_network_info

logger = get_logger(__name__)


def handle_web_chat(request: Request):
    """Processa uma mensagem recebida via browser."""
    get_network_info(request)

    data = request.get_json(silent=True) or {}
    session_id: str = data.get("session_id") or str(uuid.uuid4())
    message: str = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Mensagem vazia / Empty message"}), 400

    # Prefixo "web:" garante namespace separado de WhatsApp/Telegram;
    # o UUID do browser também passa pelo anonimizador (uso anônimo)
    user_id = anonymize_user_id(f"web:{session_id}")
    logger.info(f"[WEB] user={user_id} msg={message[:80]!r}")

    reply = bot_service.process_message(user_id, message, "web")

    return jsonify({"reply": reply, "session_id": session_id})
