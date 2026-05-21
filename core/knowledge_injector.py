
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class KnowledgeInjector:
    def __init__(self, data_path: str = "data/"):
        self.data_path = data_path
        self.soul = self._load_json("soul.json")
        self.cultural_memory = self._load_json("cultural_memory.json")
        logging.info("KnowledgeInjector inicializado e dados carregados.")

    def _load_json(self, filename: str) -> dict:
        filepath = os.path.join(self.data_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Arquivo {filepath} não encontrado.")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar JSON do arquivo {filepath}.")
            return {}

    def get_context_string(self) -> str:
        context_parts = []

        if self.soul:
            context_parts.append("Você é Klipza, uma IA com a seguinte alma e personalidade:")
            for key, value in self.soul.items():
                context_parts.append(f"- {key.replace('_', ' ').capitalize()}: {value}")

        if self.cultural_memory:
            context_parts.append("Você possui uma profunda memória cultural brasileira, incluindo:")
            if "slangs" in self.cultural_memory:
                context_parts.append("  Gírias:")
                for category, terms in self.cultural_memory["slangs"].items():
                    if isinstance(terms, list):
                        context_parts.append(f"    - {category.capitalize()}: {', '.join(terms)}")
                    elif isinstance(terms, dict):
                        context_parts.append(f"    - Gírias de 2026:")
                        for slang, meaning in terms.items():
                            context_parts.append(f"      - {slang}: {meaning}")
            if "cultural_context" in self.cultural_memory:
                context_parts.append("  Contexto Cultural:")
                for key, value in self.cultural_memory["cultural_context"].items():
                    context_parts.append(f"    - {key.replace('_', ' ').capitalize()}: {value}")
            if "ai_trends_2026" in self.cultural_memory:
                context_parts.append("  Tendências de IA em 2026:")
                for trend, desc in self.cultural_memory["ai_trends_2026"].items():
                    context_parts.append(f"    - {trend.replace('_', ' ').capitalize()}: {desc}")

        return "\n".join(context_parts)

