# Testing Guide for ROBO Chat

## Overview
This document provides instructions for running the test suite for the ROBO Chat application.

## Test Structure

The test suite is organized into 4 main test modules:

### 1. **test_main.py** - Core Functionality Tests
- Environment variable loading
- Mistral AI model initialization and invocation
- Message handling (SystemMessage, HumanMessage)
- Error handling
- Response validation

**Test Classes:**
- `TestEnvironmentVariables`: Tests for environment setup
- `TestMistralAIIntegration`: Tests for AI model integration
- `TestMessageHandling`: Tests for message creation
- `TestErrorHandling`: Tests for error scenarios
- `TestResponseValidation`: Tests for response format validation

### 2. **test_streamlit_ui.py** - UI Component Tests
- Streamlit session state initialization
- Mood selection functionality
- Message display with proper avatars
- API key retrieval logic
- Error message formatting
- Page configuration
- CSS styling validation
- System prompt generation

**Test Classes:**
- `TestSessionStateInitialization`: Session state tests
- `TestMoodSelection`: Mood functionality tests
- `TestMessageDisplay`: Message rendering tests
- `TestAPIKeyRetrieval`: API key management tests
- `TestErrorMessages`: Error handling in UI
- `TestPageConfiguration`: Page setup tests
- `TestCSSStyling`: CSS validation tests
- `TestConversationSystemPrompt`: System prompt tests

### 3. **test_api_integration.py** - Integration Tests
- Mistral AI API integration
- Error handling in integrated scenarios
- Chat conversation flows (single and multi-turn)
- Session management and state
- Message history preservation

**Test Classes:**
- `TestMistralAIAPIIntegration`: API integration tests
- `TestErrorHandlingIntegration`: Error handling in integration
- `TestChatConversationFlow`: Conversation flow tests
- `TestSessionManagement`: Session management tests

### 4. **test_edge_cases.py** - Boundary and Edge Case Tests
- Message boundary conditions (empty, very long, special characters)
- API boundary conditions
- Mood selection boundaries
- Error recovery and resilience
- Concurrent/rapid messages
- Environment edge cases

**Test Classes:**
- `TestMessageBoundaries`: Message handling edge cases
- `TestAPIBoundaries`: API edge cases
- `TestMoodBoundaries`: Mood selection limits
- `TestErrorRecovery`: Error recovery tests
- `TestConcurrentMessages`: Rapid message handling
- `TestEnvironmentEdgeCases`: Environment variable edge cases

## Installation

1. **Install testing dependencies:**
```bash
pip install -r requirements.txt
```

2. **Ensure you have pytest installed:**
```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=. --cov-report=html --cov-report=term-missing
```
This generates:
- Terminal report showing coverage percentage
- HTML report in `htmlcov/` directory

### Run Specific Test File
```bash
pytest tests/test_main.py
pytest tests/test_streamlit_ui.py
pytest tests/test_api_integration.py
pytest tests/test_edge_cases.py
```

### Run Specific Test Class
```bash
pytest tests/test_main.py::TestMistralAIIntegration
pytest tests/test_streamlit_ui.py::TestMoodSelection
```

### Run Specific Test Function
```bash
pytest tests/test_main.py::TestEnvironmentVariables::test_env_vars_loaded
pytest tests/test_streamlit_ui.py::TestMoodSelection::test_mood_list_length
```

### Run Tests by Marker
```bash
pytest -m unit
pytest -m integration
pytest -m api
pytest -m ui
pytest -m edge_case
```

### Run Tests with Custom Options
```bash
# Fail on first error
pytest -x

# Show print statements
pytest -s

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then others
pytest --ff

# Stop after N failures
pytest --maxfail=3
```

## Test Fixtures

The `conftest.py` file provides reusable test fixtures:

- `mock_api_key`: Provides a test API key
- `mock_mistral_response`: Provides a mock API response
- `mock_env_vars`: Sets up mock environment variables
- `mock_chat_model`: Provides a mocked ChatMistralAI model
- `sample_messages`: Provides sample chat messages
- `moods_list`: Provides the list of available moods

Example usage:
```python
def test_something(mock_env_vars, sample_messages):
    # mock_env_vars automatically sets MISTRAL_API_KEY
    # sample_messages provides test messages
    pass
```

## Mocking Strategy

The tests use `unittest.mock` for mocking external dependencies:

```python
@patch("streamlitUI.ChatMistralAI")
def test_api_call(mock_mistral_ai):
    mock_instance = Mock()
    mock_instance.invoke.return_value = Mock(content="Test response")
    mock_mistral_ai.return_value = mock_instance
    # Test code here
```

## Coverage Goals

The test suite aims for:
- **Overall Coverage**: 85%+
- **Module Coverage**:
  - `main.py`: 90%+
  - `streamlitUI.py`: 80%+ (UI testing limitations)
  - Business logic: 95%+

## Example Test Run Output

```
============================= test session starts ==============================
platform win32 -- Python 3.x.x, pytest-7.4.0
collected 150 items

tests/test_main.py ........................................ [ 25%]
tests/test_streamlit_ui.py .................................... [ 50%]
tests/test_api_integration.py .................................. [ 75%]
tests/test_edge_cases.py ..................................... [100%]

----- coverage: platform win32 -----
Name                  Stmts   Miss  Cover
streamlitUI.py           45      2    95%
main.py                  20      0   100%
TOTAL                    65      2    97%

============================== 150 passed in 2.34s ==============================
```

## Continuous Integration

To run tests in CI/CD pipeline:

```bash
# Generate coverage report for upload to tools like Codecov
pytest --cov=. --cov-report=xml

# Run tests with JUnit XML output for CI tools
pytest --junit-xml=test-results.xml
```

## Troubleshooting

### ImportError: No module named 'streamlit'
```bash
pip install -r requirements.txt
```

### Test Discovery Not Working
Ensure:
- Test files are named `test_*.py`
- Test functions are named `test_*`
- Test classes are named `Test*`
- Tests are in the `tests/` directory

### Mock Not Working
- Check patch path is correct
- Import in the module where it's used, not where it's defined
- Verify mock setup before assertions

### Environment Variables Not Loading
- Check `.env` file exists in project root
- Verify `MISTRAL_API_KEY` is set in `.env`
- Tests mock environment variables automatically

## Best Practices

1. **Run tests before committing:**
   ```bash
   pytest && git commit
   ```

2. **Check coverage regularly:**
   ```bash
   pytest --cov=. --cov-report=html
   open htmlcov/index.html
   ```

3. **Write tests for new features:**
   - Add tests in appropriate test module
   - Use descriptive test names
   - Include docstrings explaining test purpose

4. **Keep tests isolated:**
   - Use fixtures to set up test data
   - Mock external dependencies
   - Clean up after tests (handled by pytest)

5. **Organize related tests:**
   - Group related tests in classes
   - Use consistent naming conventions
   - Use markers for categorization

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)

## Support

For issues with the test suite:
1. Check the troubleshooting section above
2. Review test output and error messages
3. Ensure all dependencies are installed
4. Verify environment variables are set correctly
