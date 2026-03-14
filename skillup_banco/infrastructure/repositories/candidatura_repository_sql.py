from __future__ import annotations

from datetime import datetime
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class CandidaturaRepositorySql(CandidaturaRepository):

    def _to_entity(self, row) -> Candidatura:
        entity = Candidatura(
            _data_candidatura=row["dataCandidatura"],
            _status=StatusCandidatura(row["status"]),
            _candidato_id=UUID(str(row["candidato_id"])),
            _vaga_id=UUID(str(row["vaga_id"])),
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: Candidatura) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO candidatura (id, dataCandidatura, status, "
                    "candidato_id, vaga_id) "
                    "VALUES (:id, :data_candidatura, :status, :candidato_id, :vaga_id)"
                ),
                {
                    "id": str(entity.id),
                    "data_candidatura": entity.data_candidatura,
                    "status": entity.status.value,
                    "candidato_id": str(entity.candidato_id),
                    "vaga_id": str(entity.vaga_id),
                },
            )

    def get_by_id(self, entity_id: UUID) -> Candidatura | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM candidatura WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[Candidatura]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM candidatura"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: Candidatura) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("UPDATE candidatura SET status = :status WHERE id = :id"),
                {
                    "id": str(entity.id),
                    "status": entity.status.value,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM candidatura WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM candidatura WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def list_by_candidato(self, candidato_id: UUID) -> Sequence[Candidatura]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM candidatura WHERE candidato_id = :candidato_id"),
                {"candidato_id": str(candidato_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]

    def get_by_candidato_e_vaga(self, candidato_id: UUID, vaga_id: UUID) -> Candidatura | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM candidatura "
                    "WHERE candidato_id = :candidato_id AND vaga_id = :vaga_id"
                ),
                {"candidato_id": str(candidato_id), "vaga_id": str(vaga_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_by_status_e_data(
        self,
        status: StatusCandidatura,
        data_inicio: datetime,
        data_fim: datetime,
    ) -> Sequence[Candidatura]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM candidatura "
                    "WHERE status = :status "
                    "AND dataCandidatura BETWEEN :data_inicio AND :data_fim"
                ),
                {
                    "status": status.value,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                },
            )
            return [self._to_entity(row) for row in result.mappings()]
