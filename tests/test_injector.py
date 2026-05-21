
import pytest
import os
import json
from core.knowledge_injector import KnowledgeInjector

@pytest.fixture
def mock_data(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    soul_content = {
        "personality": "Engraçado e técnico",
        "values": "Transparência e inovação"
    }
    with open(data_dir / "soul.json", "w", encoding="utf-8") as f:
        json.dump(soul_content, f)
        
    cultural_content = {
        "slangs": {
            "legal": ["top", "massa"],
            "modern_2026": {"rizz": "carisma"}
        },
        "cultural_context": {
            "humor": "sarcástico"
        }
    }
    with open(data_dir / "cultural_memory.json", "w", encoding="utf-8") as f:
        json.dump(cultural_content, f)
        
    return str(data_dir)

def test_knowledge_injector_initialization(mock_data):
    injector = KnowledgeInjector(data_path=mock_data)
    assert injector.soul["personality"] == "Engraçado e técnico"
    assert injector.cultural_memory["cultural_context"]["humor"] == "sarcástico"

def test_get_context_string(mock_data):
    injector = KnowledgeInjector(data_path=mock_data)
    context = injector.get_context_string()
    
    assert "Klipza" in context
    assert "Engraçado e técnico" in context
    assert "top, massa" in context
    assert "rizz: carisma" in context
    assert "Humor: sarcástico" in context

def test_missing_files(tmp_path):
    # Testa comportamento com diretório vazio
    injector = KnowledgeInjector(data_path=str(tmp_path))
    context = injector.get_context_string()
    assert context == ""
