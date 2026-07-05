"""
Rotas da interface web do ChatBot.

GET  /       → página do chat (sem cadastro)
POST /chat   → endpoint de mensagens (JSON)
"""

from flask import Blueprint, render_template, request

from controllers.web_controller import handle_web_chat

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/chat", methods=["POST"])
def chat():
    return handle_web_chat(request)
