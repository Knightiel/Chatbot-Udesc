from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class Session:
    """Representa a sessão de um usuário durante a conversa."""

    user_id: str
    platform: str
    language: Optional[str] = None
    state: str = "WELCOME"
    previous_state: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_to_history(self, role: str, message: str) -> None:
        self.history.append(
            {
                "role": role,
                "message": message[:500],
                "timestamp": datetime.now().isoformat(),
            }
        )
        # Mantém apenas as últimas 50 interações em memória
        if len(self.history) > 50:
            self.history = self.history[-50:]
        self.updated_at = datetime.now().isoformat()
