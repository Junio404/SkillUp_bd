from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

TEntity = TypeVar("TEntity")


class BaseRepository(ABC, Generic[TEntity]):
    """Generic contract for persistence operations."""

    def __init__(self, connection: Any) -> None:
        self._connection = connection

    @property
    def connection(self) -> Any:
        return self._connection

    @abstractmethod
    def add(self, entity: TEntity) -> None:
        """Persist a new entity."""

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> TEntity | None:
        """Return an entity by id or None when not found."""

    @abstractmethod
    def list_all(self) -> Sequence[TEntity]:
        """Return all entities for this repository."""

    @abstractmethod
    def update(self, entity: TEntity) -> None:
        """Persist changes for an existing entity."""

    @abstractmethod
    def remove(self, entity_id: UUID) -> None:
        """Delete an entity by id."""

    @abstractmethod
    def exists(self, entity_id: UUID) -> bool:
        """Return True when an entity exists."""
