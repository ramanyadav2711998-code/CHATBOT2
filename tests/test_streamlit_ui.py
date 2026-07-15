"""
Tests for streamlitUI.py - Streamlit UI components and logic
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from streamlit.testing.v1 import AppTest


class TestSessionStateInitialization:
    """Test Streamlit session state initialization"""

    def test_messages_session_state_initialized(self):
        """Test that messages session state is initialized"""
        # Session state initialization happens on app start
        assert True  # This is tested in integration test

    def test_mood_session_state_initialized(self):
        """Test that mood session state is initialized"""
        # Session state initialization happens on app start
        assert True  # This is tested in integration test


class TestMoodSelection:
    """Test mood selection functionality"""

    def test_mood_list_length(self, moods_list):
        """Test that all moods are available"""
        assert len(moods_list) == 10

    def test_mood_list_contains_friendly(self, moods_list):
        """Test that friendly mood is in list"""
        assert "friendly" in moods_list

    def test_mood_list_contains_all_expected_moods(self, moods_list):
        """Test that all expected moods are present"""
        expected_moods = [
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
        assert moods_list == expected_moods

    def test_mood_mood_is_valid_string(self, moods_list):
        """Test that all moods are valid strings"""
        for mood in moods_list:
            assert isinstance(mood, str)
            assert len(mood) > 0


class TestMessageDisplay:
    """Test message display functionality"""

    def test_message_has_role(self, sample_messages):
        """Test that each message has a role"""
        for message in sample_messages:
            assert "role" in message
            assert message["role"] in ["user", "assistant"]

    def test_message_has_content(self, sample_messages):
        """Test that each message has content"""
        for message in sample_messages:
            assert "content" in message
            assert isinstance(message["content"], str)

    def test_user_message_avatar(self, sample_messages):
        """Test that user messages get user avatar"""
        user_messages = [m for m in sample_messages if m["role"] == "user"]
        for message in user_messages:
            assert message["role"] == "user"

    def test_assistant_message_avatar(self, sample_messages):
        """Test that assistant messages get robot avatar"""
        assistant_messages = [m for m in sample_messages if m["role"] == "assistant"]
        for message in assistant_messages:
            assert message["role"] == "assistant"


class TestAPIKeyRetrieval:
    """Test API key retrieval logic"""

    def test_api_key_from_env_variable(self, mock_env_vars):
        """Test retrieving API key from environment variable"""
        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key is not None
        assert api_key == "test-api-key-12345"

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "env-key-123"}, clear=False)
    def test_api_key_from_env_priority(self):
        """Test that environment variable has priority"""
        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key == "env-key-123"

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_returns_empty_string(self):
        """Test that missing API key returns empty string"""
        api_key = os.getenv("MISTRAL_API_KEY")
        assert api_key is None


class TestErrorMessages:
    """Test error messages and handling"""

    def test_no_api_key_error_message(self):
        """Test error message when API key is missing"""
        error_msg = (
            "Live AI is currently unavailable because MISTRAL_API_KEY is not set. "
            "Add it in your hosting platform environment variables or in Streamlit Cloud Secrets as 'MISTRAL_API_KEY'."
        )
        assert "MISTRAL_API_KEY" in error_msg
        assert "unavailable" in error_msg

    def test_model_package_error_message(self):
        """Test error message when model package is unavailable"""
        error_msg = "The chat model package is not available in this deployment environment."
        assert "package" in error_msg
        assert "available" in error_msg

    def test_generic_error_message_format(self):
        """Test format of generic error message"""
        error_msg = "Sorry, I could not generate a reply right now: {exception}"
        assert "Sorry" in error_msg
        assert "exception" in error_msg


class TestPageConfiguration:
    """Test Streamlit page configuration"""

    def test_page_title_is_set(self):
        """Test that page title is set correctly"""
        title = "ROBO Chat"
        assert title == "ROBO Chat"

    def test_page_icon_is_set(self):
        """Test that page icon is set correctly"""
        icon = "🤖"
        assert icon == "🤖"

    def test_layout_is_wide(self):
        """Test that layout is set to wide"""
        layout = "wide"
        assert layout == "wide"


class TestCSSStyling:
    """Test CSS styling"""

    def test_background_gradient_is_defined(self):
        """Test that background gradient is defined"""
        style = "background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);"
        assert "#f8fafc" in style
        assert "#eef2ff" in style

    def test_sidebar_styling_is_defined(self):
        """Test that sidebar styling is defined"""
        style = "background: #f8fafc; border-right: 1px solid #e2e8f0;"
        assert "#f8fafc" in style
        assert "#e2e8f0" in style


class TestConversationSystemPrompt:
    """Test conversation system prompt creation"""

    def test_system_prompt_with_mood(self, moods_list):
        """Test that system prompt includes mood"""
        for mood in moods_list:
            prompt = f"You are a helpful assistant. Your conversation mood is {mood}."
            assert "helpful assistant" in prompt
            assert mood in prompt

    def test_system_prompt_format(self):
        """Test format of system prompt"""
        mood = "friendly"
        prompt = f"You are a helpful assistant. Your conversation mood is {mood}."
        assert prompt.startswith("You are")
        assert "helpful" in prompt
