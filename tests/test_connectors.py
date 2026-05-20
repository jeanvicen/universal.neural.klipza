
import pytest
from unittest.mock import MagicMock, patch
from connectors.universal_api_layer import UniversalAPILayer
from skills.sarcasmo_br import SarcasmoBR

def test_inject_context():
    layer = UniversalAPILayer()
    prompt = "Como vai?"
    modified = layer._inject_context(prompt)
    assert "alma brasileira" in modified
    assert prompt in modified

def test_process_with_skills():
    mock_sarcasmo_skill = MagicMock(spec=SarcasmoBR)
    mock_sarcasmo_skill.process.return_value = "Ah, entendi o sarcasmo... ou não? 😉 Olá"
    
    layer = UniversalAPILayer(brain_skills={"sarcasmo_br": mock_sarcasmo_skill})
    processed_prompt = layer.process_with_skills("Olá")
    
    mock_sarcasmo_skill.process.assert_called_once_with("Olá")
    assert processed_prompt == "Ah, entendi o sarcasmo... ou não? 😉 Olá"

def test_wrap_openai_interception_with_skills():
    mock_sarcasmo_skill = MagicMock(spec=SarcasmoBR)
    mock_sarcasmo_skill.process.return_value = "Ah, entendi o sarcasmo... ou não? 😉 Olá"

    layer = UniversalAPILayer(brain_skills={"sarcasmo_br": mock_sarcasmo_skill})
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = "Resposta simulada"
    
    messages = [{"role": "user", "content": "Olá"}]
    layer.wrap_openai(mock_client, "gpt-4o-mini", messages)
    
    # Verifica se o conteúdo da mensagem foi modificado antes da chamada
    called_messages = mock_client.chat.completions.create.call_args[1]["messages"]
    assert "alma brasileira" in called_messages[0]["content"]
    assert "Ah, entendi o sarcasmo... ou não? 😉 Olá" in called_messages[0]["content"]
    assert called_messages[0]["content"].startswith("Como um assistente de IA com alma brasileira, humor e contexto cultural, responda: Ah, entendi o sarcasmo... ou não? 😉 Olá")

def test_wrap_gemini_interception_with_skills():
    mock_sarcasmo_skill = MagicMock(spec=SarcasmoBR)
    mock_sarcasmo_skill.process.return_value = "Ah, entendi o sarcasmo... ou não? 😉 Olá"

    layer = UniversalAPILayer(brain_skills={"sarcasmo_br": mock_sarcasmo_skill})
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value.text = "Resposta Gemini"
    
    layer.wrap_gemini(mock_client, "gemini-2.0-flash", "Olá")
    
    called_contents = mock_client.models.generate_content.call_args[1]["contents"]
    assert "alma brasileira" in called_contents
    assert "Ah, entendi o sarcasmo... ou não? 😉 Olá" in called_contents
    assert called_contents.startswith("Como um assistente de IA com alma brasileira, humor e contexto cultural, responda: Ah, entendi o sarcasmo... ou não? 😉 Olá")

def test_wrap_claude_interception_with_skills():
    mock_sarcasmo_skill = MagicMock(spec=SarcasmoBR)
    mock_sarcasmo_skill.process.return_value = "Ah, entendi o sarcasmo... ou não? 😉 Olá"

    layer = UniversalAPILayer(brain_skills={"sarcasmo_br": mock_sarcasmo_skill})
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content[0].text = "Resposta Claude"
    
    messages = [{"role": "user", "content": "Olá"}]
    layer.wrap_claude(mock_client, "claude-3-5-sonnet-20240620", messages)
    
    called_messages = mock_client.messages.create.call_args[1]["messages"]
    assert "alma brasileira" in called_messages[0]["content"]
    assert "Ah, entendi o sarcasmo... ou não? 😉 Olá" in called_messages[0]["content"]
    assert called_messages[0]["content"].startswith("Como um assistente de IA com alma brasileira, humor e contexto cultural, responda: Ah, entendi o sarcasmo... ou não? 😉 Olá")

def test_wrap_groq_interception_with_skills():
    mock_sarcasmo_skill = MagicMock(spec=SarcasmoBR)
    mock_sarcasmo_skill.process.return_value = "Ah, entendi o sarcasmo... ou não? 😉 Teste Groq"

    layer = UniversalAPILayer(brain_skills={"sarcasmo_br": mock_sarcasmo_skill})
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = "Resposta Groq"
    
    messages = [{"role": "user", "content": "Teste Groq"}]
    layer.wrap_groq(mock_client, "llama3-8b-8192", messages)
    
    called_messages = mock_client.chat.completions.create.call_args[1]["messages"]
    assert "alma brasileira" in called_messages[0]["content"]
    assert "Ah, entendi o sarcasmo... ou não? 😉 Teste Groq" in called_messages[0]["content"]
    assert called_messages[0]["content"].startswith("Como um assistente de IA com alma brasileira, humor e contexto cultural, responda: Ah, entendi o sarcasmo... ou não? 😉 Teste Groq")
