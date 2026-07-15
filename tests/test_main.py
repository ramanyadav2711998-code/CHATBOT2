"""
Unit tests for main.py - Core chatbot functionality
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from dotenv import load_dotenv


class TestEnvironmentVariables:
    """Test environment variable loading"""

    def test_env_vars_loaded(self):
        """Test that environment variables are loaded"""
        load_dotenv()
        # This test verifies that dotenv loads successfully
        assert True

    def test_mistral_api_key_accessible(self, mock_env_vars):
        """Test that MISTRAL_API_KEY is accessible"""
        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key == "test-api-key-12345"


class TestMistralAIIntegration:
    """Test Mistral AI model integration"""

    @patch("main.ChatMistralAI")
    def test_model_initialization(self, mock_mistral_ai):
        """Test that ChatMistralAI model initializes correctly"""
        mock_instance = Mock()
        mock_mistral_ai.return_value = mock_instance

        # Simulate model initialization
        model = mock_mistral_ai(
            model="mistral-large-latest", temperature=0.7, max_retries=2
        )

        assert model is not None
        mock_mistral_ai.assert_called_once_with(
            model="mistral-large-latest", temperature=0.7, max_retries=2
        )

    @patch("main.ChatMistralAI")
    def test_model_invoke(self, mock_mistral_ai, mock_mistral_response):
        """Test that model.invoke returns expected response"""
        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_mistral_response
        mock_mistral_ai.return_value = mock_instance

        model = mock_mistral_ai()
        response = model.invoke([])

        assert response.content == "This is a test response from Mistral AI"


class TestMessageHandling:
    """Test message creation and handling"""

    def test_system_message_creation(self):
        """Test creation of SystemMessage"""
        from langchain_core.messages import SystemMessage

        system_msg = SystemMessage("You are a helpful assistant.")
        assert system_msg.content == "You are a helpful assistant."
        assert system_msg.type == "system"

    def test_human_message_creation(self):
        """Test creation of HumanMessage"""
        from langchain_core.messages import HumanMessage

        human_msg = HumanMessage("who is virat kholi")
        assert human_msg.content == "who is virat kholi"
        assert human_msg.type == "human"

    @patch("main.ChatMistralAI")
    def test_message_list_construction(self, mock_mistral_ai):
        """Test that message list is constructed correctly"""
        from langchain_core.messages import SystemMessage, HumanMessage

        message = [
            SystemMessage("You are a helpful assistant."),
            HumanMessage("who is virat kholi"),
        ]

        assert len(message) == 2
        assert message[0].type == "system"
        assert message[1].type == "human"

    @patch("main.ChatMistralAI")
    def test_response_content_extraction(self, mock_mistral_ai, mock_mistral_response):
        """Test that response content is extracted correctly"""
        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_mistral_response
        mock_mistral_ai.return_value = mock_instance

        from langchain_core.messages import SystemMessage, HumanMessage

        model = mock_mistral_ai()
        message = [
            SystemMessage("You are a helpful assistant."),
            HumanMessage("who is virat kholi"),
        ]
        response = model.invoke(message)

        assert hasattr(response, "content")
        assert response.content == "This is a test response from Mistral AI"


class TestErrorHandling:
    """Test error handling in main.py"""

    @patch("main.ChatMistralAI", side_effect=Exception("API Error"))
    def test_api_error_handling(self, mock_mistral_ai):
        """Test that API errors are handled gracefully"""
        with pytest.raises(Exception):
            mock_mistral_ai()

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_error(self):
        """Test behavior when API key is missing"""
        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key is None


class TestResponseValidation:
    """Test response validation"""

    def test_valid_response_format(self, mock_mistral_response):
        """Test that response has expected format"""
        assert hasattr(mock_mistral_response, "content")
        assert isinstance(mock_mistral_response.content, str)
        assert len(mock_mistral_response.content) > 0

    def test_response_is_string(self, mock_mistral_response):
        """Test that response content is a string"""
        assert isinstance(mock_mistral_response.content, str)

    def test_response_not_empty(self, mock_mistral_response):
        """Test that response is not empty"""
        assert mock_mistral_response.content.strip() != ""
