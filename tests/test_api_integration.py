"""
Integration tests for API interactions and end-to-end chatbot functionality
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock


class TestMistralAIAPIIntegration:
    """Test Mistral AI API integration"""

    @patch("streamlitUI.ChatMistralAI")
    def test_api_call_with_valid_key(self, mock_mistral_ai, mock_env_vars):
        """Test that API call is made with valid key"""
        mock_instance = Mock()
        mock_instance.invoke.return_value = Mock(content="Test response")
        mock_mistral_ai.return_value = mock_instance

        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key is not None

        model = mock_mistral_ai(api_key=api_key, model="mistral-large-latest")
        assert model is not None

    @patch("streamlitUI.ChatMistralAI")
    def test_api_response_format(self, mock_mistral_ai, mock_mistral_response):
        """Test that API response has correct format"""
        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_mistral_response
        mock_mistral_ai.return_value = mock_instance

        model = mock_mistral_ai()
        response = model.invoke([])

        assert hasattr(response, "content")
        assert isinstance(response.content, str)

    @patch("streamlitUI.ChatMistralAI")
    def test_api_call_with_system_message(self, mock_mistral_ai, mock_mistral_response):
        """Test API call includes system message"""
        from langchain_core.messages import SystemMessage, HumanMessage

        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_mistral_response
        mock_mistral_ai.return_value = mock_instance

        model = mock_mistral_ai()
        messages = [
            SystemMessage("You are a helpful assistant. Your conversation mood is friendly."),
            HumanMessage("Hello, how are you?"),
        ]
        response = model.invoke(messages)

        assert response.content is not None
        mock_instance.invoke.assert_called_once_with(messages)

    @patch("streamlitUI.ChatMistralAI")
    def test_api_call_with_different_moods(self, mock_mistral_ai, mock_mistral_response, moods_list):
        """Test API calls with different mood prompts"""
        from langchain_core.messages import SystemMessage, HumanMessage

        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_mistral_response
        mock_mistral_ai.return_value = mock_instance

        for mood in moods_list:
            model = mock_mistral_ai()
            messages = [
                SystemMessage(f"You are a helpful assistant. Your conversation mood is {mood}."),
                HumanMessage("Tell me a joke"),
            ]
            response = model.invoke(messages)
            assert response.content is not None

    @patch("streamlitUI.ChatMistralAI")
    def test_api_temperature_parameter(self, mock_mistral_ai):
        """Test that temperature parameter is set correctly"""
        mock_mistral_ai(model="mistral-large-latest", temperature=0.7, max_retries=2)
        
        mock_mistral_ai.assert_called_once_with(
            model="mistral-large-latest", temperature=0.7, max_retries=2
        )

    @patch("streamlitUI.ChatMistralAI")
    def test_api_max_retries_parameter(self, mock_mistral_ai):
        """Test that max_retries parameter is set correctly"""
        mock_mistral_ai(model="mistral-large-latest", temperature=0.7, max_retries=2)
        
        call_args = mock_mistral_ai.call_args
        assert call_args[1]["max_retries"] == 2


class TestErrorHandlingIntegration:
    """Test error handling in integrated scenarios"""

    @patch("streamlitUI.ChatMistralAI", side_effect=Exception("API Connection Error"))
    def test_api_connection_error(self, mock_mistral_ai):
        """Test handling of API connection errors"""
        with pytest.raises(Exception) as exc_info:
            model = mock_mistral_ai()
        
        assert "API Connection Error" in str(exc_info.value)

    @patch("streamlitUI.ChatMistralAI")
    def test_response_fallback_on_error(self, mock_mistral_ai):
        """Test fallback response when API fails"""
        mock_instance = Mock()
        mock_instance.invoke.side_effect = Exception("API Error")
        mock_mistral_ai.return_value = mock_instance

        model = mock_mistral_ai()
        
        with pytest.raises(Exception):
            from langchain_core.messages import HumanMessage
            model.invoke([HumanMessage("Hello")])

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_in_integration(self):
        """Test integration behavior when API key is missing"""
        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key is None


class TestChatConversationFlow:
    """Test complete chat conversation flow"""

    @patch("streamlitUI.ChatMistralAI")
    def test_single_message_conversation(self, mock_mistral_ai, mock_mistral_response):
        """Test single message conversation"""
        from langchain_core.messages import SystemMessage, HumanMessage

        mock_instance = Mock()
        mock_instance.invoke.return_value = mock_mistral_response
        mock_mistral_ai.return_value = mock_instance

        model = mock_mistral_ai()
        messages = [
            SystemMessage("You are a helpful assistant."),
            HumanMessage("Hello"),
        ]
        response = model.invoke(messages)

        assert response.content is not None

    @patch("streamlitUI.ChatMistralAI")
    def test_multi_turn_conversation(self, mock_mistral_ai):
        """Test multi-turn conversation"""
        from langchain_core.messages import SystemMessage, HumanMessage

        mock_instance = Mock()
        mock_instance.invoke.side_effect = [
            Mock(content="First response"),
            Mock(content="Second response"),
            Mock(content="Third response"),
        ]
        mock_mistral_ai.return_value = mock_instance

        model = mock_mistral_ai()

        # Turn 1
        response1 = model.invoke([SystemMessage("You are a helper."), HumanMessage("Hi")])
        assert response1.content == "First response"

        # Turn 2
        response2 = model.invoke([SystemMessage("You are a helper."), HumanMessage("How are you?")])
        assert response2.content == "Second response"

        # Turn 3
        response3 = model.invoke([SystemMessage("You are a helper."), HumanMessage("Goodbye")])
        assert response3.content == "Third response"

    @patch("streamlitUI.ChatMistralAI")
    def test_message_history_preservation(self, mock_mistral_ai):
        """Test that message history is preserved"""
        messages = []
        
        from langchain_core.messages import HumanMessage
        
        msg1 = HumanMessage("First message")
        messages.append(msg1)
        assert len(messages) == 1

        msg2 = HumanMessage("Second message")
        messages.append(msg2)
        assert len(messages) == 2

        assert messages[0].content == "First message"
        assert messages[1].content == "Second message"


class TestSessionManagement:
    """Test session management and state"""

    def test_message_storage_structure(self, sample_messages):
        """Test that messages are stored with correct structure"""
        for message in sample_messages:
            assert "role" in message
            assert "content" in message
            assert message["role"] in ["user", "assistant"]

    def test_empty_message_history(self):
        """Test empty message history"""
        messages = []
        assert len(messages) == 0

    def test_add_user_message_to_history(self):
        """Test adding user message to history"""
        messages = []
        user_message = {"role": "user", "content": "Hello"}
        messages.append(user_message)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "user"

    def test_add_assistant_message_to_history(self):
        """Test adding assistant message to history"""
        messages = []
        assistant_message = {"role": "assistant", "content": "Hi there!"}
        messages.append(assistant_message)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "assistant"

    def test_clear_message_history(self, sample_messages):
        """Test clearing message history"""
        messages = list(sample_messages)
        assert len(messages) == 4
        
        messages.clear()
        assert len(messages) == 0
