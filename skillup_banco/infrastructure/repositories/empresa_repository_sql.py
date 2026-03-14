from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.empresa import Empresa
from domain.interfaces.empresa_repository import EmpresaRepository


class EmpresaRepositorySql(EmpresaRepository):

    def _to_entity(self, row) -> Empresa:
        entity = Empresa(
            _razao_social=row["razaoSocial"],
            _nome_fantasia=row["nomeFantasia"],
            _cnpj=row["cnpj"],
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: Empresa) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO empresa (id, razaoSocial, nomeFantasia, cnpj) "
                    "VALUES (:id, :razao_social, :nome_fantasia, :cnpj)"
                ),
                {
                    "id": str(entity.id),
                    "razao_social": entity.razao_social,
                    "nome_fantasia": entity.nome_fantasia,
                    "cnpj": entity.cnpj,
                },
            )

    def get_by_id(self, entity_id: UUID) -> Empresa | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM empresa WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[Empresa]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM empresa"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: Empresa) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "UPDATE empresa SET razaoSocial = :razao_social, "
                    "nomeFantasia = :nome_fantasia WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "razao_social": entity.razao_social,
                    "nome_fantasia": entity.nome_fantasia,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM empresa WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM empresa WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def get_by_cnpj(self, cnpj: str) -> Empresa | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM empresa WHERE cnpj = :cnpj"),
                {"cnpj": cnpj},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
