"""
Pytest configuration and fixtures for ROBO Chat tests
"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_api_key():
    """Fixture to provide a mock API key"""
    return "test-api-key-12345"


@pytest.fixture
def mock_mistral_response():
    """Fixture to provide a mock Mistral AI response"""
    mock_response = Mock()
    mock_response.content = "This is a test response from Mistral AI"
    return mock_response


@pytest.fixture
def mock_env_vars(monkeypatch, mock_api_key):
    """Fixture to mock environment variables"""
    monkeypatch.setenv("MISTRAL_API_KEY", mock_api_key)
    return mock_api_key


@pytest.fixture
def mock_chat_model():
    """Fixture to provide a mock ChatMistralAI model"""
    with patch("streamlitUI.ChatMistralAI") as mock:
        model_instance = Mock()
        model_instance.invoke = Mock(return_value=Mock(content="Test response"))
        mock.return_value = model_instance
        yield mock


@pytest.fixture
def sample_messages():
    """Fixture to provide sample chat messages"""
    return [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
        {"role": "user", "content": "What is your name?"},
        {"role": "assistant", "content": "I'm ROBO, your friendly chatbot assistant!"},
    ]


@pytest.fixture
def moods_list():
    """Fixture to provide the list of available moods"""
    return [
        "friendly",
        "professional",
        "sarcastic",
        "funny",
        "romantic",
        "sad",
        "angry",
        "confused",
        "excited",
        "bored",
    ]
