# Copilot Instructions for AIGenius-GHCP-AINative

This is a Python-based workshop project used in the AI Genius Episode 1 session on AI-native coding workflows with GitHub Copilot.

## Project Overview

The `starter-app` is a command-line task manager written in Python. It allows users to add, list, complete, edit, delete, and get stats on tasks. Tasks are stored in a local JSON file and have the following schema:

```json
{
  "id": 1,
  "name": "Deploy to production",
  "description": "Run the release pipeline",
  "priority": "high",
  "tags": ["work", "devops"],
  "due_date": "2025-12-31",
  "done": false,
  "created_at": "2025-01-01T09:00:00"
}
```

## Coding Conventions

- Use Python 3.10+ features and type hints throughout
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Keep functions small and focused on a single responsibility
- Add docstrings to all public functions and classes
- Prefer f-strings for string formatting

## Project Structure

- `starter-app/app.py` -- main application entry point and CLI
- `starter-app/requirements.txt` -- Python dependencies
- `starter-app/tests/` -- pytest test suite

## Dependencies

- `click` -- for building the CLI interface
- `rich` -- for formatted terminal output
- `pytest` -- for the test suite

## Azure Cloud Integration

When adding cloud storage or services, use these libraries and patterns:

### Azure Table Storage (preferred for task persistence)
```python
from azure.data.tables import TableServiceClient, TableClient
from azure.core.credentials import AzureNamedKeyCredential
```
- Use `AZURE_STORAGE_CONNECTION_STRING` environment variable for credentials
- Never hardcode connection strings or account keys
- Use `python-dotenv` to load `.env` files: `from dotenv import load_dotenv`
- Store tasks as entities with `PartitionKey = "tasks"` and `RowKey = str(task_id)`

### Azure OpenAI (for AI features)
```python
from openai import AzureOpenAI
```
- Use environment variables: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`
- Never hardcode API keys in source code
- Use `python-dotenv` to load env vars

### Environment variable pattern
```python
import os
from dotenv import load_dotenv

load_dotenv()
connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
```

## Testing Approach

- Write unit tests using `pytest`
- Place tests in `starter-app/tests/`
- Name test files `test_*.py`
- Use the `isolated_tasks_file` fixture from `conftest.py` to avoid touching real data
- Test edge cases: empty task lists, invalid IDs, invalid dates, missing env vars

## What "Done" Looks Like

A feature is complete when:
- The CLI command works as described in the issue
- Input is validated and errors are handled gracefully
- Secrets are loaded from environment variables, never hardcoded
- The code has docstrings and type hints
- New tests cover the new behaviour

## Style Notes

- Keep CLI output readable and user-friendly using `rich` formatting
- Error messages should be clear and actionable
- Use exit codes: 0 for success, non-zero for errors
- Overdue tasks should be highlighted in red in the task list

