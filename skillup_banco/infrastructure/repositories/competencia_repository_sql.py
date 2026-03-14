from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.competencia import Competencia
from domain.interfaces.competencia_repository import CompetenciaRepository


class CompetenciaRepositorySql(CompetenciaRepository):

    def _to_entity(self, row) -> Competencia:
        entity = Competencia(
            _nome=row["nome"],
            _descricao=row["descricao"],
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: Competencia) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO competencia (id, nome, descricao) "
                    "VALUES (:id, :nome, :descricao)"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "descricao": entity.descricao,
                },
            )

    def get_by_id(self, competencia_id: UUID) -> Competencia | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM competencia WHERE id = :id"),
                {"id": str(competencia_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[Competencia]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM competencia"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: Competencia) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "UPDATE competencia SET nome = :nome, descricao = :descricao "
                    "WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "descricao": entity.descricao,
                },
            )

    def remove(self, competencia_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM competencia WHERE id = :id"),
                {"id": str(competencia_id)},
            )

    def exists(self, competencia_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM competencia WHERE id = :id"),
                {"id": str(competencia_id)},
            )
            return result.first() is not None

    def get_by_nome(self, nome: str) -> Competencia | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM competencia WHERE nome = :nome"),
                {"nome": nome},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
