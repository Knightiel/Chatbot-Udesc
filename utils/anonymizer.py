"""
Anonimização de identificadores de usuários.

O chatbot pode ser usado por qualquer pessoa, de forma anônima e sem
cadastro. O número de telefone (WhatsApp) e o chat ID (Telegram) nunca
são armazenados nem registrados em log: cada identificador é convertido
em um hash SHA-256 truncado, determinístico (a mesma pessoa mantém a
mesma sessão) e irreversível (não é possível recuperar o telefone).
"""

import hashlib


def anonymize_user_id(raw_id: str) -> str:
    """Converte um identificador real (telefone/chat ID) em um ID anônimo."""
    digest = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:12]
    return f"anon-{digest}"
