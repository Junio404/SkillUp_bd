from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.enums import Nivel
from domain.entidades.requisito_vaga import RequisitoVaga
from domain.interfaces.requisito_vaga_repository import RequisitoVagaRepository


class RequisitoVagaRepositorySql(RequisitoVagaRepository):

    def _to_entity(self, row) -> RequisitoVaga:
        entity = RequisitoVaga(
            _nivel=Nivel(row["nivel"]),
            _vaga_id=UUID(str(row["vaga_id"])),
            _competencia_id=UUID(str(row["competencia_id"])),
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: RequisitoVaga) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO requisito_vaga (id, nivel, vaga_id, competencia_id) "
                    "VALUES (:id, :nivel, :vaga_id, :competencia_id)"
                ),
                {
                    "id": str(entity.id),
                    "nivel": entity.nivel.value,
                    "vaga_id": str(entity.vaga_id),
                    "competencia_id": str(entity.competencia_id),
                },
            )

    def get_by_id(self, requisito_vaga_id: UUID) -> RequisitoVaga | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM requisito_vaga WHERE id = :id"),
                {"id": str(requisito_vaga_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[RequisitoVaga]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM requisito_vaga"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: RequisitoVaga) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("UPDATE requisito_vaga SET nivel = :nivel WHERE id = :id"),
                {
                    "id": str(entity.id),
                    "nivel": entity.nivel.value,
                },
            )

    def remove(self, requisito_vaga_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM requisito_vaga WHERE id = :id"),
                {"id": str(requisito_vaga_id)},
            )

    def exists(self, requisito_vaga_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM requisito_vaga WHERE id = :id"),
                {"id": str(requisito_vaga_id)},
            )
            return result.first() is not None

    def list_by_vaga(self, vaga_id: UUID) -> Sequence[RequisitoVaga]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM requisito_vaga WHERE vaga_id = :vaga_id"),
                {"vaga_id": str(vaga_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]
