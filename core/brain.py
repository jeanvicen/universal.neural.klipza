
import os
import logging
from openai import OpenAI
from google import genai
from google.genai import types
import anthropic

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KlipzaBrain:
    def __init__(self, api_key: str, ai_type: str):
        if not api_key:
            raise ValueError("API Key não pode ser vazia.")
        if ai_type not in ['openai', 'gemini', 'claude']:
            raise ValueError("Tipo de IA inválido. Escolha entre 'openai', 'gemini', 'claude'.")

        self.api_key = api_key
        self.ai_type = ai_type
        self.client = self._initialize_client()
        logging.info(f"Cérebro Klipza inicializado com sucesso para {self.ai_type}.")
        self._integrity_check()

    def _initialize_client(self):
        if self.ai_type == 'openai':
            return OpenAI(api_key=self.api_key)
        elif self.ai_type == 'gemini':
            return genai.Client(api_key=self.api_key)
        elif self.ai_type == 'claude':
            return anthropic.Anthropic(api_key=self.api_key)

    def _integrity_check(self):
        # Verificação básica de integridade
        if self.client is None:
            logging.error("Falha na verificação de integridade: Cliente da IA não inicializado.")
            raise RuntimeError("Cliente da IA não inicializado.")
        logging.info("Verificação de integridade inicial do cérebro Klipza concluída.")

    def think(self, prompt: str) -> str:
        logging.info(f"Cérebro pensando com {self.ai_type} para o prompt: {prompt[:50]}...")
        try:
            if self.ai_type == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini", # Atualizado para um modelo mais moderno
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            elif self.ai_type == 'gemini':
                # Usando o novo SDK google-genai
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=prompt
                )
                return response.text
            elif self.ai_type == 'claude':
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20240620", # Atualizado para Claude 3.5 Sonnet
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
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
