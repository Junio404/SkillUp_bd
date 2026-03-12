from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.curso_competencia import CursoCompetencia
from domain.entidades.enums import Nivel
from domain.interfaces.curso_competencia_repository import CursoCompetenciaRepository


class CursoCompetenciaRepositorySql(CursoCompetenciaRepository):

    def _to_entity(self, row) -> CursoCompetencia:
        entity = CursoCompetencia(
            _nivel=Nivel(row["nivel"]),
            _curso_id=UUID(str(row["curso_id"])),
            _competencia_id=UUID(str(row["competencia_id"])),
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: CursoCompetencia) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO curso_competencia (id, nivel, curso_id, competencia_id) "
                    "VALUES (:id, :nivel, :curso_id, :competencia_id)"
                ),
                {
                    "id": str(entity.id),
                    "nivel": entity.nivel.value,
                    "curso_id": str(entity.curso_id),
                    "competencia_id": str(entity.competencia_id),
                },
            )

    def get_by_id(self, entity_id: UUID) -> CursoCompetencia | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM curso_competencia WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[CursoCompetencia]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM curso_competencia"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: CursoCompetencia) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("UPDATE curso_competencia SET nivel = :nivel WHERE id = :id"),
                {
                    "id": str(entity.id),
                    "nivel": entity.nivel.value,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM curso_competencia WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM curso_competencia WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def list_by_curso(self, curso_id: UUID) -> Sequence[CursoCompetencia]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM curso_competencia WHERE curso_id = :curso_id"),
                {"curso_id": str(curso_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]
