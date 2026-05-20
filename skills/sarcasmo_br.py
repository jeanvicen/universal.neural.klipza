
import re

class SarcasmoBR:
    def __init__(self):
        self.keywords = [
            "confia", "claro que sim", "super", "com certeza", "né",
            "imagina", "só que não", "aham", "tipo assim"
        ]
        self.patterns = [
            r"\b(claro que sim|com certeza), (né|né não)?\b",
            r"\b(super|muito) (bom|legal|interessante), (confia|né)?\b",
            r"\b(imagina|aham), (que|se)? (eu|a gente)? (ia|faria)? isso\b"
        ]

    def detect_sarcasm(self, text: str) -> bool:
        text_lower = text.lower()
        for keyword in self.keywords:
            if keyword in text_lower:
                return True
        for pattern in self.patterns:
            if re.search(pattern, text_lower):
                return True
        return False

    def add_sarcastic_flair(self, text: str) -> str:
        if self.detect_sarcasm(text):
            return text + " (sqn)"
        return text

    def process(self, prompt: str) -> str:
        # Lógica para aplicar sarcasmo ou detectar e ajustar a resposta
        # Por enquanto, apenas um placeholder para futura integração com o UniversalAPILayer
        if self.detect_sarcasm(prompt):
            return "Ah, entendi o sarcasmo... ou não? 😉 " + prompt
        return prompt

