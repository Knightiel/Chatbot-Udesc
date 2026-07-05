from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# Mapeia palavras-chave para a opção correspondente do menu principal (RF14)
_KEYWORDS: dict = {
    "pt": {
        "centro": "1", "endereço": "1", "campus": "1", "onde fica": "1",
        "siga": "2", "sigaa": "2", "moodle": "2", "acesso": "2",
        "id udesc": "3", "id": "3", "login": "3", "senha": "3", "primeiro acesso": "3",
        "sistemas": "4", "sas": "4", "office": "4", "office 365": "4",
        "biblioteca": "4", "site udesc": "4", "ppc": "4",
        "cpf": "5", "receita federal": "5", "documento": "5",
        "tutoria": "6", "tutor": "6", "orientação acadêmica": "6",
        "soe": "7", "psicólogo": "7", "apoio": "7", "orientação": "7",
        "residência": "8", "moradia": "8", "morar": "8", "casa": "8",
        "restaurante": "9", "comida": "9", "ru": "9", "almoço": "9",
        "wifi": "9", "wi-fi": "9", "internet": "9",
        "ônibus": "9", "transporte": "9", "uber": "9",
        "banco": "9", "dinheiro": "9", "câmbio": "9",
        "chip": "9", "celular": "9", "sim": "9",
        "emergência": "10", "polícia": "10", "samu": "10",
        "bombeiro": "10", "hospital": "10", "socorro": "10",
    },
    "en": {
        "campus": "1", "center": "1", "address": "1", "where": "1",
        "siga": "2", "sigaa": "2", "moodle": "2", "access": "2",
        "udesc id": "3", "id": "3", "login": "3", "password": "3",
        "systems": "4", "sas": "4", "office": "4", "office 365": "4",
        "library": "4", "udesc website": "4", "curriculum": "4",
        "cpf": "5", "tax id": "5", "document": "5",
        "tutoring": "6", "tutor": "6", "academic support": "6",
        "soe": "7", "counseling": "7", "psychologist": "7",
        "housing": "8", "residence": "8", "accommodation": "8",
        "restaurant": "9", "food": "9", "lunch": "9", "cafeteria": "9",
        "wifi": "9", "wi-fi": "9", "internet": "9",
        "bus": "9", "transport": "9", "uber": "9",
        "bank": "9", "money": "9", "exchange": "9",
        "sim card": "9", "phone": "9", "sim": "9",
        "emergency": "10", "police": "10", "ambulance": "10",
        "fire": "10", "hospital": "10", "help": "10",
    },
}


class KeywordService:
    """Identifica intenção do usuário por palavras-chave (RF14)."""

    def find_menu_option(self, text: str, lang: str) -> Optional[str]:
        lower = text.lower().strip()
        keyword_map = _KEYWORDS.get(lang, _KEYWORDS["pt"])

        # Tenta correspondência de frases primeiro (mais longas têm prioridade)
        for keyword in sorted(keyword_map, key=len, reverse=True):
            if keyword in lower:
                option = keyword_map[keyword]
                logger.info(f"[KEYWORD] Correspondência: '{keyword}' → opção {option}")
                return option

        return None
