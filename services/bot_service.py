"""
Núcleo da lógica conversacional do ChatBot UDESC.

Máquina de estados que processa mensagens independente de plataforma (RT08).
Cada estado tem um handler dedicado; navegação global intercepta comandos
especiais antes do dispatch.
"""

import json
import os
from typing import Any, Dict, Optional

from models.session import Session
from services.keyword_service import KeywordService
from services.session_service import SessionService
from utils.logger import get_logger

logger = get_logger(__name__)

# Comandos de navegação global
_NAV = {
    "exit": {"sair", "exit", "bye", "tchau", "quit", "adeus"},
    "menu": {"menu", "inicio", "início", "home", "main menu", "principal", "0"},
    "back": {"voltar", "back", "anterior", "b", "retornar"},
}

# Mapeamento estado → chave JSON para conteúdo estático
_STATIC_CONTENT: Dict[str, str] = {
    "ID_UDESC": "id_udesc",
    "SOE": "soe",
    "EMERGENCY": "emergency",
}

# Opções do menu principal → (próximo estado, chave estática ou None)
# Numeração espelha a Tabela 1 do trabalho (itens 1 a 8) + extras (9 e 10)
_MAIN_MENU_OPTIONS: Dict[str, tuple] = {
    "1": ("CENTERS_LIST", None),
    "2": ("SYSTEMS_ACCESS_MENU", None),
    "3": ("ID_UDESC", "id_udesc"),
    "4": ("SYSTEMS_MENU", None),
    "5": ("CPF_SELECT", None),
    "6": ("TUTORIA_SELECT", None),
    "7": ("SOE", "soe"),
    "8": ("RESIDENCIA_SELECT", None),
    "9": ("FAQ_MENU", None),
    "10": ("EMERGENCY", "emergency"),
    "0": ("ENDED", None),
}


class BotService:
    def __init__(self) -> None:
        self._session_svc = SessionService()
        self._keyword_svc = KeywordService()
        self._msg: Dict[str, Any] = {}
        self._load_messages()

    # ------------------------------------------------------------------
    # Carregamento de mensagens
    # ------------------------------------------------------------------

    def _load_messages(self) -> None:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        for lang in ("pt", "en"):
            path = os.path.join(data_dir, f"messages_{lang}.json")
            with open(path, "r", encoding="utf-8") as f:
                self._msg[lang] = json.load(f)
        logger.info("[BOT] Mensagens carregadas: pt, en")

    def m(self, lang: str, key: str) -> Any:
        """Acessa valor no JSON por chave com notação de ponto (ex: 'faq.items.ru')."""
        data = self._msg.get(lang, self._msg["pt"])
        for part in key.split("."):
            if isinstance(data, dict):
                data = data.get(part, "")
            else:
                return ""
        return data

    # ------------------------------------------------------------------
    # Ponto de entrada público
    # ------------------------------------------------------------------

    def process_message(self, user_id: str, text: str, platform: str) -> str:
        session = self._session_svc.get_or_create(user_id, platform)
        msg = (text or "").strip()
        lang = session.language or "pt"

        logger.info(
            f"[MSG] plataforma={platform} user={user_id} "
            f"estado={session.state} msg={msg[:60]!r}"
        )

        session.add_to_history("user", msg)

        # Navegação global (não aplica no estado WELCOME)
        if session.state != "WELCOME":
            nav_response = self._check_navigation(user_id, session, msg.lower())
            if nav_response is not None:
                session.add_to_history("bot", nav_response)
                return nav_response

        response = self._dispatch(user_id, session, msg)
        session.add_to_history("bot", response)
        self._session_svc.save(user_id, session)
        return response

    # ------------------------------------------------------------------
    # Navegação global
    # ------------------------------------------------------------------

    def _check_navigation(
        self, user_id: str, session: Session, lower: str
    ) -> Optional[str]:
        if lower in _NAV["exit"] or (lower == "0" and session.state == "MAIN_MENU"):
            return self._end_session(user_id, session.language)

        if lower in _NAV["menu"]:
            session.state = "MAIN_MENU"
            session.context = {}
            self._session_svc.save(user_id, session)
            return self.m(session.language, "main_menu")

        if lower in _NAV["back"] and session.state not in ("MAIN_MENU", "WELCOME"):
            prev = session.previous_state or "MAIN_MENU"
            session.state = prev
            session.previous_state = None
            session.context = {}
            self._session_svc.save(user_id, session)
            return self._dispatch(user_id, session, "")

        return None

    def _end_session(self, user_id: str, lang: str) -> str:
        self._session_svc.delete(user_id)
        return self.m(lang or "pt", "goodbye")

    # ------------------------------------------------------------------
    # Máquina de estados
    # ------------------------------------------------------------------

    def _dispatch(self, user_id: str, session: Session, msg: str) -> str:
        handlers = {
            "WELCOME": self._handle_welcome,
            "MAIN_MENU": self._handle_main_menu,
            "CENTERS_LIST": self._handle_centers_list,
            "CENTER_DETAIL": self._handle_center_detail,
            "SYSTEMS_ACCESS_MENU": self._handle_systems_access_menu,
            "SYSTEMS_ACCESS_DETAIL": self._handle_system_detail,
            "SYSTEMS_MENU": self._handle_systems_menu,
            "SYSTEM_DETAIL": self._handle_system_detail,
            "ID_UDESC": self._handle_static,
            "CPF_SELECT": self._handle_cpf_select,
            "CPF_DETAIL": self._handle_cpf_detail,
            "TUTORIA_SELECT": self._handle_tutoria_select,
            "TUTORIA_DETAIL": self._handle_tutoria_detail,
            "SOE": self._handle_static,
            "RESIDENCIA_SELECT": self._handle_residencia_select,
            "RESIDENCIA_DETAIL": self._handle_residencia_detail,
            "FAQ_MENU": self._handle_faq_menu,
            "FAQ_DETAIL": self._handle_faq_detail,
            "EMERGENCY": self._handle_static,
        }
        handler = handlers.get(session.state, self._handle_main_menu)
        return handler(user_id, session, msg)

    # ------------------------------------------------------------------
    # Handlers individuais
    # ------------------------------------------------------------------

    def _handle_welcome(self, user_id: str, session: Session, msg: str) -> str:
        lower = msg.lower()
        if lower in ("1", "pt", "português", "portugues", "p"):
            session.language = "pt"
            session.state = "MAIN_MENU"
            return self.m("pt", "main_menu")
        if lower in ("2", "en", "english", "inglês", "ingles", "e"):
            session.language = "en"
            session.state = "MAIN_MENU"
            return self.m("en", "main_menu")
        return self.m("pt", "welcome")

    def _handle_main_menu(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"

        if not msg:
            return self.m(lang, "main_menu")

        # Busca por palavras-chave antes de verificar número (RF14)
        kw_option = self._keyword_svc.find_menu_option(msg, lang)
        option = msg.strip() if msg.strip() in _MAIN_MENU_OPTIONS else kw_option

        if not option or option not in _MAIN_MENU_OPTIONS:
            return self.m(lang, "invalid_option") + "\n\n" + self.m(lang, "main_menu")

        if option == "0":
            return self._end_session(user_id, lang)

        new_state, content_key = _MAIN_MENU_OPTIONS[option]
        session.previous_state = "MAIN_MENU"
        session.state = new_state

        if content_key:
            return self.m(lang, content_key) + self.m(lang, "navigation_hint")

        return self._dispatch(user_id, session, "")

    # --- Centros ---

    def _handle_centers_list(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")

        if not msg:
            header = self.m(lang, "centers.list_header")
            items = "\n".join(
                f"{i + 1}️⃣  {c['name']} — {c['city']}" for i, c in enumerate(centers)
            )
            return header + items + self.m(lang, "navigation_hint")

        try:
            idx = int(msg.strip()) - 1
            if 0 <= idx < len(centers):
                center = centers[idx]
                session.previous_state = "CENTERS_LIST"
                session.state = "CENTER_DETAIL"
                session.context = {"center_id": center["id"]}
                return self._format_center(center, lang)
        except ValueError:
            pass

        return (
            self.m(lang, "invalid_option")
            + "\n\n"
            + self._handle_centers_list(user_id, session, "")
        )

    def _handle_center_detail(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")
        cid = session.context.get("center_id")
        center = next((c for c in centers if c["id"] == cid), None)
        if center:
            return self._format_center(center, lang)
        return self._handle_centers_list(user_id, session, "")

    def _format_center(self, c: Dict, lang: str) -> str:
        nav = self.m(lang, "navigation_hint")
        if lang == "pt":
            return (
                f"🏛️ *{c['name']}*\n\n"
                f"📍 *Endereço:* {c['address']}\n"
                f"📞 *Telefone:* {c['phone']}\n"
                f"🌐 *Site:* {c['website']}\n"
                f"🗺️ *Google Maps:* {c['maps']}"
                + nav
            )
        return (
            f"🏛️ *{c['name']}*\n\n"
            f"📍 *Address:* {c['address']}\n"
            f"📞 *Phone:* {c['phone']}\n"
            f"🌐 *Website:* {c['website']}\n"
            f"🗺️ *Google Maps:* {c['maps']}"
            + nav
        )

    # --- Sistemas ---
    # Dois menus distintos (Tabela 1, itens 2 e 4):
    #   systems_access → SIGA/Moodle/SIGAA com requisitos de acesso (item 2)
    #   systems        → todos os sistemas UDESC e sua finalidade (item 4)

    def _handle_systems_access_menu(
        self, user_id: str, session: Session, msg: str
    ) -> str:
        return self._systems_list(
            user_id, session, msg, "systems_access",
            "SYSTEMS_ACCESS_MENU", "SYSTEMS_ACCESS_DETAIL",
        )

    def _handle_systems_menu(self, user_id: str, session: Session, msg: str) -> str:
        return self._systems_list(
            user_id, session, msg, "systems", "SYSTEMS_MENU", "SYSTEM_DETAIL"
        )

    def _systems_list(
        self,
        user_id: str,
        session: Session,
        msg: str,
        json_key: str,
        list_state: str,
        detail_state: str,
    ) -> str:
        lang = session.language or "pt"
        systems = self.m(lang, f"{json_key}.items")

        if not msg:
            header = self.m(lang, f"{json_key}.header")
            items = "\n".join(
                f"{i + 1}️⃣  *{s['name']}* — {s['description']}"
                for i, s in enumerate(systems)
            )
            return header + items + self.m(lang, "navigation_hint")

        try:
            idx = int(msg.strip()) - 1
            if 0 <= idx < len(systems):
                system = systems[idx]
                session.previous_state = list_state
                session.state = detail_state
                session.context = {"system_id": system["id"], "system_key": json_key}
                return system["detail"] + self.m(lang, "navigation_hint")
        except ValueError:
            pass

        return (
            self.m(lang, "invalid_option")
            + "\n\n"
            + self._systems_list(user_id, session, "", json_key, list_state, detail_state)
        )

    def _handle_system_detail(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        json_key = session.context.get("system_key", "systems")
        systems = self.m(lang, f"{json_key}.items")
        sid = session.context.get("system_id")
        system = next((s for s in systems if s["id"] == sid), None)
        if system:
            return system["detail"] + self.m(lang, "navigation_hint")
        return self._handle_systems_menu(user_id, session, "")

    # --- CPF (Tabela 1, item 5) ---
    # Informa como obter o CPF online e, com base no centro escolhido,
    # oferece o endereço da Receita Federal para a validação presencial.

    def _handle_cpf_select(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")

        if not msg:
            header = self.m(lang, "cpf.header")
            items = "\n".join(
                f"{i + 1}️⃣  {c['name']} — {c['city']}" for i, c in enumerate(centers)
            )
            return header + items + self.m(lang, "navigation_hint")

        try:
            idx = int(msg.strip()) - 1
            if 0 <= idx < len(centers):
                center = centers[idx]
                session.previous_state = "CPF_SELECT"
                session.state = "CPF_DETAIL"
                session.context = {"center_id": center["id"]}
                return self._format_cpf(center, lang)
        except ValueError:
            pass

        return (
            self.m(lang, "invalid_option")
            + "\n\n"
            + self._handle_cpf_select(user_id, session, "")
        )

    def _handle_cpf_detail(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")
        cid = session.context.get("center_id")
        center = next((c for c in centers if c["id"] == cid), None)
        if center:
            return self._format_cpf(center, lang)
        return self._handle_cpf_select(user_id, session, "")

    def _format_cpf(self, c: Dict, lang: str) -> str:
        tmpl = self.m(lang, "cpf.detail_template")
        return (
            tmpl.format(
                center=c["name"], city=c["city"], receita=c["receita_federal"]
            )
            + self.m(lang, "navigation_hint")
        )

    # --- Tutoria ---

    def _handle_tutoria_select(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")

        if not msg:
            header = (
                "👩‍🏫 *TUTORIA ACADÊMICA*\n\nSelecione seu centro:\n\n"
                if lang == "pt"
                else "👩‍🏫 *ACADEMIC TUTORING*\n\nSelect your campus:\n\n"
            )
            items = "\n".join(
                f"{i + 1}️⃣  {c['name']}" for i, c in enumerate(centers)
            )
            return header + items + self.m(lang, "navigation_hint")

        try:
            idx = int(msg.strip()) - 1
            if 0 <= idx < len(centers):
                center = centers[idx]
                session.previous_state = "TUTORIA_SELECT"
                session.state = "TUTORIA_DETAIL"
                session.context = {"center_id": center["id"]}
                return self._format_tutoria(center, lang)
        except ValueError:
            pass

        return (
            self.m(lang, "invalid_option")
            + "\n\n"
            + self._handle_tutoria_select(user_id, session, "")
        )

    def _handle_tutoria_detail(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")
        cid = session.context.get("center_id")
        center = next((c for c in centers if c["id"] == cid), None)
        if center:
            return self._format_tutoria(center, lang)
        return self._handle_tutoria_select(user_id, session, "")

    def _format_tutoria(self, c: Dict, lang: str) -> str:
        nav = self.m(lang, "navigation_hint")
        if lang == "pt":
            return (
                f"👩‍🏫 *Tutoria Acadêmica — {c['name']}*\n\n"
                f"📧 E-mail: {c['tutoria_email']}\n"
                f"📞 Telefone: {c['tutoria_phone']}\n"
                f"🌐 Site: {c['tutoria_site']}\n"
                f"🕐 Horário: {c['tutoria_hours']}\n\n"
                "A equipe de tutoria auxilia estudantes estrangeiros na adaptação "
                "acadêmica e cultural à UDESC."
                + nav
            )
        return (
            f"👩‍🏫 *Academic Tutoring — {c['name']}*\n\n"
            f"📧 Email: {c['tutoria_email']}\n"
            f"📞 Phone: {c['tutoria_phone']}\n"
            f"🌐 Website: {c['tutoria_site']}\n"
            f"🕐 Hours: {c['tutoria_hours']}\n\n"
            "The tutoring team helps international students adapt academically "
            "and culturally to UDESC."
            + nav
        )

    # --- Residência ---

    def _handle_residencia_select(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")

        if not msg:
            header = self.m(lang, "residencia.header")
            items = "\n".join(
                f"{i + 1}️⃣  {c['name']}" for i, c in enumerate(centers)
            )
            return header + items + self.m(lang, "navigation_hint")

        try:
            idx = int(msg.strip()) - 1
            if 0 <= idx < len(centers):
                center = centers[idx]
                session.previous_state = "RESIDENCIA_SELECT"
                session.state = "RESIDENCIA_DETAIL"
                session.context = {"center_id": center["id"]}
                return self._format_residencia(center, lang)
        except ValueError:
            pass

        return (
            self.m(lang, "invalid_option")
            + "\n\n"
            + self._handle_residencia_select(user_id, session, "")
        )

    def _handle_residencia_detail(
        self, user_id: str, session: Session, msg: str
    ) -> str:
        lang = session.language or "pt"
        centers = self.m(lang, "centers.items")
        cid = session.context.get("center_id")
        center = next((c for c in centers if c["id"] == cid), None)
        if center:
            return self._format_residencia(center, lang)
        return self._handle_residencia_select(user_id, session, "")

    def _format_residencia(self, c: Dict, lang: str) -> str:
        nav = self.m(lang, "navigation_hint")
        if c.get("has_residencia"):
            tmpl = self.m(lang, "residencia.available_template")
            return (
                tmpl.format(
                    center=c["name"],
                    residencia_info=c.get("residencia_info", ""),
                    tutoria_contact=f"{c['tutoria_email']} | {c['tutoria_phone']}",
                )
                + nav
            )
        tmpl = self.m(lang, "residencia.not_available")
        return tmpl.format(center=c["name"]) + nav

    # --- FAQ ---

    _FAQ_MAP = {
        "1": "ru",
        "2": "transporte",
        "3": "wifi",
        "4": "impressao",
        "5": "bancos",
        "6": "chip",
        "7": "moradia",
    }

    def _handle_faq_menu(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"

        if not msg:
            return self.m(lang, "faq.header") + self.m(lang, "navigation_hint")

        key = self._FAQ_MAP.get(msg.strip())
        if key:
            session.previous_state = "FAQ_MENU"
            session.state = "FAQ_DETAIL"
            session.context = {"faq_key": key}
            return self.m(lang, f"faq.items.{key}") + self.m(lang, "navigation_hint")

        return (
            self.m(lang, "invalid_option")
            + "\n\n"
            + self._handle_faq_menu(user_id, session, "")
        )

    def _handle_faq_detail(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        key = session.context.get("faq_key", "")
        return self.m(lang, f"faq.items.{key}") + self.m(lang, "navigation_hint")

    # --- Conteúdo estático (ID UDESC, CPF, SOE, Emergência) ---

    def _handle_static(self, user_id: str, session: Session, msg: str) -> str:
        lang = session.language or "pt"
        content_key = _STATIC_CONTENT.get(session.state, "")
        return self.m(lang, content_key) + self.m(lang, "navigation_hint")


# Instância singleton usada pelos controllers
bot_service = BotService()
