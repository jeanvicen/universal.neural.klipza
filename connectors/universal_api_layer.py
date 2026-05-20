
import os
import logging
from openai import OpenAI
from google import genai
from google.genai import types
import anthropic
from groq import Groq

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class UniversalAPILayer:
    def __init__(self, brain_context: dict = None, brain_skills: dict = None):
        self.brain_context = brain_context if brain_context is not None else {}
        self.brain_skills = brain_skills if brain_skills is not None else {}
        logging.info("UniversalAPILayer inicializada com contexto do cérebro e skills.")

    def _inject_context(self, prompt: str) -> str:
        # Placeholder para injeção de contexto real do cérebro (soul.json, cultural_memory.json)
        # Este prefixo é adicionado APÓS o processamento das skills
        klipza_prefix = "Como um assistente de IA com alma brasileira, humor e contexto cultural, responda: "
        return klipza_prefix + prompt

    def _extract_learnings(self, response_text: str):
        # Placeholder para extração de novos aprendizados da resposta
        logging.info(f"Extraindo aprendizados da resposta: {response_text[:50]}...")
        pass

    def process_with_skills(self, prompt: str) -> str:
        processed_prompt = prompt
        for skill_name, skill_instance in self.brain_skills.items():
            if hasattr(skill_instance, 'process'):
                processed_prompt = skill_instance.process(processed_prompt)
                logging.info(f"Prompt processado pela skill {skill_name}.")
        return processed_prompt

    def wrap_openai(self, client: OpenAI, model: str, messages: list) -> str:
        original_prompt = messages[0]["content"]
        processed_by_skills_prompt = self.process_with_skills(original_prompt)
        modified_prompt = self._inject_context(processed_by_skills_prompt)
        messages[0]["content"] = modified_prompt
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            response_text = response.choices[0].message.content
            self._extract_learnings(response_text)
            return response_text
        except Exception as e:
            logging.error(f"Erro ao usar OpenAI via UniversalAPILayer: {e}")
            raise

    def wrap_gemini(self, client: genai.Client, model: str, contents: str) -> str:
        processed_by_skills_contents = self.process_with_skills(contents)
        modified_contents = self._inject_context(processed_by_skills_contents)
        
        try:
            response = client.models.generate_content(
                model=model,
                contents=modified_contents
            )
            response_text = response.text
            self._extract_learnings(response_text)
            return response_text
        except Exception as e:
            logging.error(f"Erro ao usar Gemini via UniversalAPILayer: {e}")
            raise

    def wrap_claude(self, client: anthropic.Anthropic, model: str, messages: list, max_tokens: int = 1024) -> str:
        original_prompt = messages[0]["content"]
        processed_by_skills_prompt = self.process_with_skills(original_prompt)
        modified_prompt = self._inject_context(processed_by_skills_prompt)
        messages[0]["content"] = modified_prompt

        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages
            )
            response_text = response.content[0].text
            self._extract_learnings(response_text)
            return response_text
        except Exception as e:
            logging.error(f"Erro ao usar Claude via UniversalAPILayer: {e}")
            raise

    def wrap_groq(self, client: Groq, model: str, messages: list) -> str:
        original_prompt = messages[0]["content"]
        processed_by_skills_prompt = self.process_with_skills(original_prompt)
        modified_prompt = self._inject_context(processed_by_skills_prompt)
        messages[0]["content"] = modified_prompt

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            response_text = response.choices[0].message.content
            self._extract_learnings(response_text)
            return response_text
        except Exception as e:
            logging.error(f"Erro ao usar Groq via UniversalAPILayer: {e}")
            raise
