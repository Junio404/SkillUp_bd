from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.instituicao_area_ensino import InstituicaoAreaEnsino
from domain.interfaces.instituicao_area_ensino_repository import InstituicaoAreaEnsinoRepository


class InstituicaoAreaEnsinoRepositorySql(InstituicaoAreaEnsinoRepository):

    def _to_entity(self, row) -> InstituicaoAreaEnsino:
        return InstituicaoAreaEnsino(
            _instituicao_ensino_id=UUID(str(row["instituicao_id"])),
            _area_ensino_id=UUID(str(row["area_ensino_id"])),
        )

    def add(self, entity: InstituicaoAreaEnsino) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO instituicao_area_ensino (instituicao_id, area_ensino_id) "
                    "VALUES (:instituicao_id, :area_ensino_id)"
                ),
                {
                    "instituicao_id": str(entity.instituicao_ensino_id),
                    "area_ensino_id": str(entity.area_ensino_id),
                },
            )

    def get_by_id(self, entity_id: UUID) -> InstituicaoAreaEnsino | None:
        raise NotImplementedError("Tabela associativa sem campo id")

    def list_all(self) -> Sequence[InstituicaoAreaEnsino]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM instituicao_area_ensino"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: InstituicaoAreaEnsino) -> None:
        raise NotImplementedError("Tabela associativa sem campos mutáveis")

    def remove(self, entity_id: UUID) -> None:
        raise NotImplementedError(
            "Tabela associativa sem campo id, use remove_by_chave")

    def exists(self, entity_id: UUID) -> bool:
        raise NotImplementedError(
            "Tabela associativa sem campo id, use get_by_chave")

    def list_by_instituicao(self, instituicao_id: UUID) -> Sequence[InstituicaoAreaEnsino]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM instituicao_area_ensino "
                    "WHERE instituicao_id = :instituicao_id"
                ),
                {"instituicao_id": str(instituicao_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]

    def get_by_chave(self, instituicao_id: UUID, area_ensino_id: UUID) -> InstituicaoAreaEnsino | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM instituicao_area_ensino "
                    "WHERE instituicao_id = :instituicao_id "
                    "AND area_ensino_id = :area_ensino_id"
                ),
                {
                    "instituicao_id": str(instituicao_id),
                    "area_ensino_id": str(area_ensino_id),
                },
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
