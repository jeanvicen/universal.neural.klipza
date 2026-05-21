
class NegociadorBR:
    def __init__(self):
        self.phrases = [
            "Vou ver o que consigo fazer por você.",
            "Deixa eu dar uma olhada aqui, mas não prometo nada.",
            "Hmm, é um desafio, mas vou tentar.",
            "Vou quebrar um galho pra você, mas é segredo."
        ]

    def process(self, prompt: str) -> str:
        # Simplesmente adiciona uma frase de negociador BR ao prompt
        # Em uma versão mais avançada, poderia analisar o prompt para decidir se aplica ou não
        return f"{prompt} (E, claro, {self.phrases[0].lower()})"
