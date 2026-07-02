from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# Mapeia palavras-chave para a opção correspondente do menu principal (RF14)
_KEYWORDS: dict = {
    "pt": {
        "centro": "1", "endereço": "1", "campus": "1", "onde fica": "1",
        "siga": "2", "sigaa": "2", "moodle": "2", "sas": "2",
        "office": "2", "office 365": "2", "biblioteca": "2",
        "id udesc": "3", "id": "3", "login": "3", "senha": "3", "primeiro acesso": "3",
        "cpf": "4", "receita federal": "4", "documento": "4",
        "tutoria": "5", "tutor": "5", "orientação acadêmica": "5",
        "soe": "6", "psicólogo": "6", "apoio": "6", "orientação": "6",
        "residência": "7", "moradia": "7", "morar": "7", "casa": "7",
        "restaurante": "8", "comida": "8", "ru": "8", "almoço": "8",
        "wifi": "8", "wi-fi": "8", "internet": "8",
        "ônibus": "8", "transporte": "8", "uber": "8",
        "banco": "8", "dinheiro": "8", "câmbio": "8",
        "chip": "8", "celular": "8", "sim": "8",
        "emergência": "9", "polícia": "9", "samu": "9",
        "bombeiro": "9", "hospital": "9", "socorro": "9",
    },
    "en": {
        "campus": "1", "center": "1", "address": "1", "where": "1",
        "siga": "2", "sigaa": "2", "moodle": "2", "sas": "2",
        "office": "2", "office 365": "2", "library": "2",
        "udesc id": "3", "id": "3", "login": "3", "password": "3",
        "cpf": "4", "tax id": "4", "document": "4",
        "tutoring": "5", "tutor": "5", "academic support": "5",
        "soe": "6", "counseling": "6", "psychologist": "6",
        "housing": "7", "residence": "7", "accommodation": "7",
        "restaurant": "8", "food": "8", "lunch": "8", "cafeteria": "8",
        "wifi": "8", "wi-fi": "8", "internet": "8",
        "bus": "8", "transport": "8", "uber": "8",
        "bank": "8", "money": "8", "exchange": "8",
        "sim card": "8", "phone": "8", "sim": "8",
        "emergency": "9", "police": "9", "ambulance": "9",
        "fire": "9", "hospital": "9", "help": "9",
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
