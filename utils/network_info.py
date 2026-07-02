"""
Utilitário para capturar e registrar informações de rede (RT03).

Protocolo de transporte: TCP/IP
- WhatsApp (Twilio): HTTPS sobre TCP porta 443
- Telegram Bot API: HTTPS sobre TCP porta 443 (polling)
- Flask Webhook: TCP porta 5000 (exposto via ngrok)
"""

import socket
from typing import Dict, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


def get_network_info(request=None) -> Dict:
    """Extrai IP de origem/destino, portas e protocolo da requisição Flask."""
    info: Dict[str, Optional[str]] = {
        "src_ip": None,
        "dst_ip": None,
        "src_port": None,
        "dst_port": None,
        "protocol": "TCP",
        "transport": "HTTPS (TCP/443)",
    }

    if request:
        forwarded_for = request.headers.get("X-Forwarded-For", "").split(",")
        info["src_ip"] = forwarded_for[0].strip() or request.remote_addr
        info["dst_ip"] = get_local_ip()
        info["dst_port"] = str(request.environ.get("SERVER_PORT", "5000"))
        info["src_port"] = str(request.environ.get("REMOTE_PORT", "desconhecida"))

    logger.info(
        f"[REDE] origem={info['src_ip']}:{info['src_port']} "
        f"destino={info['dst_ip']}:{info['dst_port']} "
        f"protocolo={info['protocol']}"
    )
    return info


def get_local_ip() -> str:
    """Retorna o IP local da máquina."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def print_network_summary() -> None:
    """Imprime no log um resumo das informações de rede ao iniciar o servidor."""
    local_ip = get_local_ip()
    logger.info("=" * 60)
    logger.info(f"[REDE] IP do servidor: {local_ip}")
    logger.info("[REDE] Protocolo de transporte: TCP/IP")
    logger.info("[REDE] WhatsApp: HTTPS via Twilio  → TCP porta 443")
    logger.info("[REDE] Telegram: HTTPS via Bot API  → TCP porta 443 (polling)")
    logger.info("[REDE] Webhook Flask: TCP porta 5000 (túnel ngrok)")
    logger.info("=" * 60)
