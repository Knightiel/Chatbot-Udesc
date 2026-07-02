from threading import Lock
from typing import Dict, Optional

from models.session import Session
from utils.logger import get_logger

logger = get_logger(__name__)


class SessionService:
    """Gerencia sessões de usuários em memória (RF18 — histórico da conversa)."""

    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}
        self._lock = Lock()

    def get_or_create(self, user_id: str, platform: str) -> Session:
        with self._lock:
            if user_id not in self._sessions:
                session = Session(user_id=user_id, platform=platform)
                self._sessions[user_id] = session
                logger.info(f"[SESSÃO] Nova sessão: user={user_id} plataforma={platform}")
            return self._sessions[user_id]

    def save(self, user_id: str, session: Session) -> None:
        with self._lock:
            self._sessions[user_id] = session

    def get(self, user_id: str) -> Optional[Session]:
        return self._sessions.get(user_id)

    def delete(self, user_id: str) -> None:
        with self._lock:
            removed = self._sessions.pop(user_id, None)
            if removed:
                logger.info(f"[SESSÃO] Encerrada: user={user_id}")

    def active_count(self) -> int:
        return len(self._sessions)
