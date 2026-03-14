from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.competencia_candidato import CompetenciaCandidato
from domain.entidades.enums import Nivel
from domain.interfaces.competencia_candidato_repository import CompetenciaCandidatoRepository


class CompetenciaCandidatoRepositorySql(CompetenciaCandidatoRepository):

    def _to_entity(self, row) -> CompetenciaCandidato:
        entity = CompetenciaCandidato(
            _nivel=Nivel(row["nivel"]),
            _candidato_id=UUID(str(row["candidato_id"])),
            _competencia_id=UUID(str(row["competencia_id"])),
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: CompetenciaCandidato) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO competencia_candidato (id, nivel, candidato_id, competencia_id) "
                    "VALUES (:id, :nivel, :candidato_id, :competencia_id)"
                ),
                {
                    "id": str(entity.id),
                    "nivel": entity.nivel.value,
                    "candidato_id": str(entity.candidato_id),
                    "competencia_id": str(entity.competencia_id),
                },
            )

    def get_by_id(self, competencia_candidato_id: UUID) -> CompetenciaCandidato | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM competencia_candidato WHERE id = :id"),
                {"id": str(competencia_candidato_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[CompetenciaCandidato]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM competencia_candidato"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: CompetenciaCandidato) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("UPDATE competencia_candidato SET nivel = :nivel WHERE id = :id"),
                {
                    "id": str(entity.id),
                    "nivel": entity.nivel.value,
                },
            )

    def remove(self, competencia_candidato_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM competencia_candidato WHERE id = :id"),
                {"id": str(competencia_candidato_id)},
            )

    def exists(self, competencia_candidato_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM competencia_candidato WHERE id = :id"),
                {"id": str(competencia_candidato_id)},
            )
            return result.first() is not None

    def list_by_candidato(self, candidato_id: UUID) -> Sequence[CompetenciaCandidato]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM competencia_candidato WHERE candidato_id = :candidato_id"),
                {"candidato_id": str(candidato_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]
