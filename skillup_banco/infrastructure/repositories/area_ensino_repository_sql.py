from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.area_ensino import AreaEnsino
from domain.interfaces.area_ensino_repository import AreaEnsinoRepository


class AreaEnsinoRepositorySql(AreaEnsinoRepository):

    def _to_entity(self, row) -> AreaEnsino:
        entity = AreaEnsino(_nome=row["nome"])
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: AreaEnsino) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("INSERT INTO area_ensino (id, nome) VALUES (:id, :nome)"),
                {"id": str(entity.id), "nome": entity.nome},
            )

    def get_by_id(self, entity_id: UUID) -> AreaEnsino | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM area_ensino WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[AreaEnsino]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM area_ensino"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: AreaEnsino) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("UPDATE area_ensino SET nome = :nome WHERE id = :id"),
                {"id": str(entity.id), "nome": entity.nome},
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM area_ensino WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM area_ensino WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def get_by_nome(self, nome: str) -> AreaEnsino | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM area_ensino WHERE nome = :nome"),
                {"nome": nome},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
