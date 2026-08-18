"""Task storage backends for the Task Manager CLI.

Provides a ``TaskStorage`` protocol along with two implementations:

* ``LocalStorage`` -- persists tasks to a local JSON file (the original
  behaviour of the app).
* ``AzureTableStorage`` -- persists tasks to Azure Table Storage, so data
  survives across machines and can be shared.

``get_storage()`` picks the right backend based on whether the
``AZURE_STORAGE_CONNECTION_STRING`` environment variable is set (loaded from
a local ``.env`` file via python-dotenv when present).
"""

import json
import os
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv

PARTITION_KEY = "tasks"
DEFAULT_TABLE_NAME = "tasks"


class StorageConnectionError(Exception):
    """Raised when a storage backend cannot be reached or configured."""


class TaskStorage(Protocol):
    """Protocol that all task storage backends must implement."""

    def load(self) -> list[dict]:
        """Load and return all tasks.

        Returns:
            A list of task dictionaries.
        """
        ...

    def save(self, tasks: list[dict]) -> None:
        """Persist the full list of tasks, replacing any existing data.

        Args:
            tasks: The list of task dictionaries to save.
        """
        ...


class LocalStorage:
    """Task storage backed by a local JSON file."""

    def __init__(self, path: Path) -> None:
        """Create a LocalStorage backend.

        Args:
            path: The JSON file used to persist tasks.
        """
        self.path = path

    def load(self) -> list[dict]:
        """Load tasks from the JSON file.

        Returns:
            A list of task dictionaries. Returns an empty list if the file
            does not exist or cannot be parsed.
        """
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("tasks file must contain a JSON array")
            return data
        except (json.JSONDecodeError, OSError, ValueError):
            return []

    def save(self, tasks: list[dict]) -> None:
        """Write tasks to the JSON file.

        Args:
            tasks: The list of task dictionaries to save.
        """
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)


class AzureTableStorage:
    """Task storage backed by Azure Table Storage.

    Each task is stored as a single entity with ``PartitionKey = "tasks"``
    and ``RowKey = str(task["id"])``. The full task is serialised to JSON
    and stored in a ``data`` property, which sidesteps the limited set of
    native property types supported by Azure Table Storage (e.g. lists are
    not natively supported).
    """

    def __init__(self, connection_string: str, table_name: str = DEFAULT_TABLE_NAME) -> None:
        """Create an AzureTableStorage backend and ensure the table exists.

        Args:
            connection_string: The Azure Storage account connection string.
            table_name: The name of the table used to store tasks.

        Raises:
            StorageConnectionError: If the table service cannot be reached
                or the table cannot be created/accessed.
        """
        from azure.core.exceptions import AzureError
        from azure.data.tables import TableServiceClient

        try:
            service_client = TableServiceClient.from_connection_string(connection_string)
            service_client.create_table_if_not_exists(table_name)
            self._table_client = service_client.get_table_client(table_name)
        except (AzureError, ValueError) as exc:
            raise StorageConnectionError(
                f"Could not connect to Azure Table Storage: {exc}"
            ) from exc

    def load(self) -> list[dict]:
        """Load all tasks from the Azure table.

        Returns:
            A list of task dictionaries.

        Raises:
            StorageConnectionError: If the tasks cannot be retrieved.
        """
        from azure.core.exceptions import AzureError

        try:
            entities = self._table_client.query_entities(f"PartitionKey eq '{PARTITION_KEY}'")
            return [json.loads(entity["data"]) for entity in entities]
        except AzureError as exc:
            raise StorageConnectionError(
                f"Could not load tasks from Azure Table Storage: {exc}"
            ) from exc

    def save(self, tasks: list[dict]) -> None:
        """Replace all tasks in the Azure table with the given list.

        Args:
            tasks: The list of task dictionaries to save.

        Raises:
            StorageConnectionError: If the tasks cannot be saved.
        """
        from azure.core.exceptions import AzureError

        try:
            existing = list(self._table_client.query_entities(f"PartitionKey eq '{PARTITION_KEY}'"))
            for entity in existing:
                self._table_client.delete_entity(
                    partition_key=entity["PartitionKey"], row_key=entity["RowKey"]
                )
            for task in tasks:
                entity = {
                    "PartitionKey": PARTITION_KEY,
                    "RowKey": str(task["id"]),
                    "data": json.dumps(task),
                }
                self._table_client.upsert_entity(entity)
        except AzureError as exc:
            raise StorageConnectionError(
                f"Could not save tasks to Azure Table Storage: {exc}"
            ) from exc


def get_storage(local_path: Path) -> TaskStorage:
    """Select the task storage backend based on environment configuration.

    Loads environment variables from a local ``.env`` file (if present) via
    python-dotenv, then returns an ``AzureTableStorage`` backend when
    ``AZURE_STORAGE_CONNECTION_STRING`` is set, otherwise falls back to
    ``LocalStorage`` using ``local_path``.

    Args:
        local_path: The JSON file path to use for the local fallback.

    Returns:
        A TaskStorage implementation.

    Raises:
        StorageConnectionError: If Azure is configured but cannot be reached.
    """
    load_dotenv()
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if connection_string:
        return AzureTableStorage(connection_string)
    return LocalStorage(local_path)
