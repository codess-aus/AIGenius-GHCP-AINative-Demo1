"""Unit tests for the storage backends (storage.py)."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import storage
from storage import (
    AzureTableStorage,
    LocalStorage,
    StorageConnectionError,
    get_storage,
)


# ---------------------------------------------------------------------------
# LocalStorage
# ---------------------------------------------------------------------------


class TestLocalStorage:
    def test_load_returns_empty_list_when_file_missing(self, tmp_path: Path) -> None:
        backend = LocalStorage(tmp_path / "tasks.json")
        assert backend.load() == []

    def test_save_and_load_round_trip(self, tmp_path: Path) -> None:
        backend = LocalStorage(tmp_path / "tasks.json")
        tasks = [{"id": 1, "name": "Test", "done": False}]
        backend.save(tasks)
        assert backend.load() == tasks

    def test_load_returns_empty_list_on_corrupt_file(self, tmp_path: Path) -> None:
        path = tmp_path / "tasks.json"
        path.write_text("not-json", encoding="utf-8")
        backend = LocalStorage(path)
        assert backend.load() == []

    def test_load_returns_empty_list_when_file_contains_object(self, tmp_path: Path) -> None:
        path = tmp_path / "tasks.json"
        path.write_text(json.dumps({"key": "value"}), encoding="utf-8")
        backend = LocalStorage(path)
        assert backend.load() == []


# ---------------------------------------------------------------------------
# AzureTableStorage (Azure SDK is fully mocked -- no real API calls)
# ---------------------------------------------------------------------------


class TestAzureTableStorage:
    def test_init_creates_table_and_client(self) -> None:
        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service = MagicMock()
            mock_service_cls.from_connection_string.return_value = mock_service
            mock_table_client = MagicMock()
            mock_service.get_table_client.return_value = mock_table_client

            backend = AzureTableStorage("fake-connection-string")

            mock_service_cls.from_connection_string.assert_called_once_with(
                "fake-connection-string"
            )
            mock_service.create_table_if_not_exists.assert_called_once_with("tasks")
            assert backend._table_client is mock_table_client

    def test_init_raises_storage_connection_error_on_failure(self) -> None:
        from azure.core.exceptions import AzureError

        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service_cls.from_connection_string.side_effect = AzureError("boom")
            with pytest.raises(StorageConnectionError):
                AzureTableStorage("fake-connection-string")

    def test_load_returns_tasks_from_entities(self) -> None:
        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service = MagicMock()
            mock_service_cls.from_connection_string.return_value = mock_service
            mock_table_client = MagicMock()
            mock_service.get_table_client.return_value = mock_table_client

            task = {"id": 1, "name": "Test", "done": False}
            mock_table_client.query_entities.return_value = [
                {"PartitionKey": "tasks", "RowKey": "1", "data": json.dumps(task)}
            ]

            backend = AzureTableStorage("fake-connection-string")
            assert backend.load() == [task]

    def test_load_raises_storage_connection_error_on_failure(self) -> None:
        from azure.core.exceptions import AzureError

        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service = MagicMock()
            mock_service_cls.from_connection_string.return_value = mock_service
            mock_table_client = MagicMock()
            mock_service.get_table_client.return_value = mock_table_client
            mock_table_client.query_entities.side_effect = AzureError("boom")

            backend = AzureTableStorage("fake-connection-string")
            with pytest.raises(StorageConnectionError):
                backend.load()

    def test_save_deletes_existing_and_upserts_new_entities(self) -> None:
        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service = MagicMock()
            mock_service_cls.from_connection_string.return_value = mock_service
            mock_table_client = MagicMock()
            mock_service.get_table_client.return_value = mock_table_client
            mock_table_client.query_entities.return_value = [
                {"PartitionKey": "tasks", "RowKey": "99"}
            ]

            backend = AzureTableStorage("fake-connection-string")
            tasks = [{"id": 1, "name": "Test", "done": False}]
            backend.save(tasks)

            mock_table_client.delete_entity.assert_called_once_with(
                partition_key="tasks", row_key="99"
            )
            mock_table_client.upsert_entity.assert_called_once_with(
                {"PartitionKey": "tasks", "RowKey": "1", "data": json.dumps(tasks[0])}
            )

    def test_save_raises_storage_connection_error_on_failure(self) -> None:
        from azure.core.exceptions import AzureError

        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service = MagicMock()
            mock_service_cls.from_connection_string.return_value = mock_service
            mock_table_client = MagicMock()
            mock_service.get_table_client.return_value = mock_table_client
            mock_table_client.query_entities.side_effect = AzureError("boom")

            backend = AzureTableStorage("fake-connection-string")
            with pytest.raises(StorageConnectionError):
                backend.save([{"id": 1, "name": "Test", "done": False}])


# ---------------------------------------------------------------------------
# get_storage
# ---------------------------------------------------------------------------


class TestGetStorage:
    def test_returns_local_storage_when_env_var_unset(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("AZURE_STORAGE_CONNECTION_STRING", raising=False)
        monkeypatch.setattr(storage, "load_dotenv", lambda: None)
        backend = get_storage(tmp_path / "tasks.json")
        assert isinstance(backend, LocalStorage)

    def test_returns_azure_storage_when_env_var_set(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("AZURE_STORAGE_CONNECTION_STRING", "fake-connection-string")
        monkeypatch.setattr(storage, "load_dotenv", lambda: None)
        with patch("azure.data.tables.TableServiceClient") as mock_service_cls:
            mock_service = MagicMock()
            mock_service_cls.from_connection_string.return_value = mock_service
            backend = get_storage(tmp_path / "tasks.json")
        assert isinstance(backend, AzureTableStorage)
