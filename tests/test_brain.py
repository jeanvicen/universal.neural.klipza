
import pytest
from unittest.mock import MagicMock, patch
from core.brain import KlipzaBrain

def test_initialization_openai():
    with patch('core.brain.OpenAI') as mock_openai:
        brain = KlipzaBrain(api_key="fake_key", ai_type="openai")
        assert brain.ai_type == "openai"
        mock_openai.assert_called_once_with(api_key="fake_key")

def test_initialization_gemini():
    with patch('core.brain.genai.Client') as mock_client_class:
        brain = KlipzaBrain(api_key="fake_key", ai_type="gemini")
        assert brain.ai_type == "gemini"
        mock_client_class.assert_called_once_with(api_key="fake_key")

def test_initialization_claude():
    with patch('core.brain.anthropic.Anthropic') as mock_anthropic:
        brain = KlipzaBrain(api_key="fake_key", ai_type="claude")
        assert brain.ai_type == "claude"
        mock_anthropic.assert_called_once_with(api_key="fake_key")

def test_initialization_invalid_type():
    with pytest.raises(ValueError, match="Tipo de IA inválido"):
        KlipzaBrain(api_key="fake_key", ai_type="invalid")

def test_think_openai():
    with patch('core.brain.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Resposta OpenAI"
        
        brain = KlipzaBrain(api_key="fake_key", ai_type="openai")
        response = brain.think("Olá")
        assert response == "Resposta OpenAI"

def test_think_gemini():
    with patch('core.brain.genai.Client') as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.models.generate_content.return_value.text = "Resposta Gemini"
        
        brain = KlipzaBrain(api_key="fake_key", ai_type="gemini")
        response = brain.think("Olá")
        assert response == "Resposta Gemini"

def test_think_claude():
    with patch('core.brain.anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = "Resposta Claude"
        
        brain = KlipzaBrain(api_key="fake_key", ai_type="claude")
        response = brain.think("Olá")
        assert response == "Resposta Claude"
