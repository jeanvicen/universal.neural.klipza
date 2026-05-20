
import os
import logging
from openai import OpenAI
from google import genai
from google.genai import types
import anthropic
from groq import Groq
from connectors.universal_api_layer import UniversalAPILayer

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KlipzaBrain:
    def __init__(self, api_key: str, ai_type: str):
        if not api_key:
            raise ValueError("API Key não pode ser vazia.")
        if ai_type not in ['openai', 'gemini', 'claude', 'groq']:
            raise ValueError("Tipo de IA inválido. Escolha entre 'openai', 'gemini', 'claude', 'groq'.")

        self.api_key = api_key
        self.ai_type = ai_type
        self.client = self._initialize_client()
        self.skills = {}
        self._load_skills()
        self.universal_api_layer = UniversalAPILayer(brain_skills=self.skills) # Passa as skills para a camada universal
        logging.info(f"Cérebro Klipza inicializado com sucesso para {self.ai_type}.")
        self._integrity_check()

    def _initialize_client(self):
        if self.ai_type == 'openai':
            return OpenAI(api_key=self.api_key)
        elif self.ai_type == 'gemini':
            return genai.Client(api_key=self.api_key)
        elif self.ai_type == 'claude':
            return anthropic.Anthropic(api_key=self.api_key)
        elif self.ai_type == 'groq':
            return Groq(api_key=self.api_key)

    def _load_skills(self):
        # Placeholder para carregar skills dinamicamente
        # Por enquanto, carrega a skill de sarcasmo diretamente
        try:
            from skills.sarcasmo_br import SarcasmoBR
            self.skills["sarcasmo_br"] = SarcasmoBR()
            logging.info("Skill 'sarcasmo_br' carregada com sucesso.")
        except ImportError as e:
            logging.warning(f"Não foi possível carregar a skill 'sarcasmo_br': {e}")

    def _integrity_check(self):
        # Verificação básica de integridade
        if self.client is None:
            logging.error("Falha na verificação de integridade: Cliente da IA não inicializado.")
            raise RuntimeError("Cliente da IA não inicializado.")
        logging.info("Verificação de integridade inicial do cérebro Klipza concluída.")

    def think(self, prompt: str) -> str:
        logging.info(f"Cérebro pensando com {self.ai_type} para o prompt: {prompt[:50]}...")
        try:
            # Processa o prompt com as skills antes de enviar para a IA
            processed_prompt = self.universal_api_layer.process_with_skills(prompt)

            if self.ai_type == 'openai':
                return self.universal_api_layer.wrap_openai(
                    client=self.client,
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": processed_prompt}]
                )
            elif self.ai_type == 'gemini':
                return self.universal_api_layer.wrap_gemini(
                    client=self.client,
                    model='gemini-2.0-flash',
                    contents=processed_prompt
                )
            elif self.ai_type == 'claude':
                return self.universal_api_layer.wrap_claude(
                    client=self.client,
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": processed_prompt}]
                )
            elif self.ai_type == 'groq':
                return self.universal_api_layer.wrap_groq(
                    client=self.client,
                    model="llama3-8b-8192", # Exemplo de modelo Groq
                    messages=[{"role": "user", "content": processed_prompt}]
                )
        except Exception as e:
            logging.error(f"Erro ao pensar com {self.ai_type}: {e}")
            return f"Erro: {e}"

    def remember(self, data: dict):
        logging.info(f"Cérebro lembrando dados: {data}")
        # Implementação futura para salvar dados na memória coletiva/cultural
        pass

    def evolve(self):
        logging.info("Cérebro iniciando processo de auto-evolução...")
        # Implementação futura para auto-evolução e criação de skills
        pass
