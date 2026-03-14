from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.enums import StatusInscricao
from domain.entidades.inscricao_curso import InscricaoCurso
from domain.interfaces.inscricao_curso_repository import InscricaoCursoRepository


class InscricaoCursoRepositorySql(InscricaoCursoRepository):

    def _to_entity(self, row) -> InscricaoCurso:
        entity = InscricaoCurso(
            _data_inscricao=row["dataInscricao"],
            _status=StatusInscricao(row["status"]),
            _candidato_id=UUID(str(row["candidato_id"])),
            _curso_id=UUID(str(row["curso_id"])),
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: InscricaoCurso) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO inscricao_curso (id, dataInscricao, status, "
                    "candidato_id, curso_id) "
                    "VALUES (:id, :data_inscricao, :status, :candidato_id, :curso_id)"
                ),
                {
                    "id": str(entity.id),
                    "data_inscricao": entity.data_inscricao,
                    "status": entity.status.value,
                    "candidato_id": str(entity.candidato_id),
                    "curso_id": str(entity.curso_id),
                },
            )

    def get_by_id(self, entity_id: UUID) -> InscricaoCurso | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM inscricao_curso WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[InscricaoCurso]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM inscricao_curso"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: InscricaoCurso) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("UPDATE inscricao_curso SET status = :status WHERE id = :id"),
                {
                    "id": str(entity.id),
                    "status": entity.status.value,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM inscricao_curso WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM inscricao_curso WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def list_by_candidato(self, candidato_id: UUID) -> Sequence[InscricaoCurso]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM inscricao_curso WHERE candidato_id = :candidato_id"),
                {"candidato_id": str(candidato_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]

    def get_by_candidato_e_curso(self, candidato_id: UUID, curso_id: UUID) -> InscricaoCurso | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM inscricao_curso "
                    "WHERE candidato_id = :candidato_id AND curso_id = :curso_id"
                ),
                {"candidato_id": str(candidato_id), "curso_id": str(curso_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
