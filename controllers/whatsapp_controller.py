from flask import Request
from twilio.twiml.messaging_response import MessagingResponse

from services.bot_service import bot_service


def handle_whatsapp(request: Request) -> str:
    from_number: str = request.form.get("From", "unknown")
    body: str = request.form.get("Body", "").strip()

    user_id = from_number.replace("whatsapp:", "")
    response_text = bot_service.process_message(user_id, body, "whatsapp")

    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)
