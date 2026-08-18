"""Shared pytest fixtures for the task manager test suite."""

import json
from pathlib import Path

import pytest

import app


@pytest.fixture(autouse=True)
def isolated_tasks_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point TASKS_FILE at a temporary file for each test.

    Returns:
        The Path to the temporary tasks file.
    """
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr(app, "TASKS_FILE", tasks_file)
    return tasks_file


@pytest.fixture()
def sample_tasks(isolated_tasks_file: Path) -> list[dict]:
    """Seed the tasks file with a small set of sample tasks.

    Returns:
        The list of task dicts written to disk.
    """
    tasks = [
        {
            "id": 1,
            "name": "Buy groceries",
            "description": "",
            "priority": "low",
            "tags": ["personal"],
            "due_date": None,
            "done": False,
            "created_at": "2025-01-01T09:00:00",
        },
        {
            "id": 2,
            "name": "Deploy to production",
            "description": "Run the release pipeline",
            "priority": "high",
            "tags": ["work", "devops"],
            "due_date": "2020-01-01",  # deliberately overdue
            "done": False,
            "created_at": "2025-01-02T10:00:00",
        },
        {
            "id": 3,
            "name": "Write unit tests",
            "description": "",
            "priority": "medium",
            "tags": ["work"],
            "due_date": None,
            "done": True,
            "created_at": "2025-01-03T11:00:00",
        },
    ]
    isolated_tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
    return tasks
