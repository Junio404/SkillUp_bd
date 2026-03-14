from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.instituicao_ensino import InstituicaoEnsino
from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository


class InstituicaoEnsinoRepositorySql(InstituicaoEnsinoRepository):

    def _to_entity(self, row) -> InstituicaoEnsino:
        entity = InstituicaoEnsino(
            _razao_social=row["razaoSocial"],
            _registro_educacional=row["registroEducacional"],
            _nome_fantasia=row["nomeFantasia"],
            _cnpj=row["cnpj"],
            _tipo=row["tipo"],
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: InstituicaoEnsino) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO instituicao_ensino (id, razaoSocial, registroEducacional, "
                    "nomeFantasia, cnpj, tipo) "
                    "VALUES (:id, :razao_social, :registro_educacional, "
                    ":nome_fantasia, :cnpj, :tipo)"
                ),
                {
                    "id": str(entity.id),
                    "razao_social": entity.razao_social,
                    "registro_educacional": entity.registro_educacional,
                    "nome_fantasia": entity.nome_fantasia,
                    "cnpj": entity.cnpj,
                    "tipo": entity.tipo,
                },
            )

    def get_by_id(self, entity_id: UUID) -> InstituicaoEnsino | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM instituicao_ensino WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[InstituicaoEnsino]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM instituicao_ensino"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: InstituicaoEnsino) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "UPDATE instituicao_ensino SET razaoSocial = :razao_social, "
                    "nomeFantasia = :nome_fantasia, tipo = :tipo WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "razao_social": entity.razao_social,
                    "nome_fantasia": entity.nome_fantasia,
                    "tipo": entity.tipo,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM instituicao_ensino WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM instituicao_ensino WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def get_by_registro_educacional(self, registro: str) -> InstituicaoEnsino | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM instituicao_ensino WHERE registroEducacional = :registro"),
                {"registro": registro},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def get_by_cnpj(self, cnpj: str) -> InstituicaoEnsino | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM instituicao_ensino WHERE cnpj = :cnpj"),
                {"cnpj": cnpj},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
