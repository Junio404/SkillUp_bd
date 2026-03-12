from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.candidato import Candidato
from domain.interfaces.candidato_repository import CandidatoRepository


class CandidatoRepositorySql(CandidatoRepository):

    def _to_entity(self, row) -> Candidato:
        entity = Candidato(
            _nome=row["nome"],
            _cpf=row["cpf"],
            _email=row["email"],
            _area_interesse=row["areaInteresse"],
            _nivel_formacao=row["nivelFormacao"],
            _curriculo_url=row["curriculo_url"],
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: Candidato) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO candidato (id, nome, cpf, email, areaInteresse, "
                    "nivelFormacao, curriculo_url) "
                    "VALUES (:id, :nome, :cpf, :email, :area_interesse, "
                    ":nivel_formacao, :curriculo_url)"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "cpf": entity.cpf,
                    "email": entity.email,
                    "area_interesse": entity.area_interesse,
                    "nivel_formacao": entity.nivel_formacao,
                    "curriculo_url": entity.curriculo_url,
                },
            )

    def get_by_id(self, entity_id: UUID) -> Candidato | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM candidato WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[Candidato]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM candidato"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: Candidato) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "UPDATE candidato SET nome = :nome, email = :email, "
                    "areaInteresse = :area_interesse, nivelFormacao = :nivel_formacao, "
                    "curriculo_url = :curriculo_url WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "email": entity.email,
                    "area_interesse": entity.area_interesse,
                    "nivel_formacao": entity.nivel_formacao,
                    "curriculo_url": entity.curriculo_url,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM candidato WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM candidato WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def get_by_cpf(self, cpf: str) -> Candidato | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM candidato WHERE cpf = :cpf"),
                {"cpf": cpf},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def get_by_email(self, email: str) -> Candidato | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM candidato WHERE email = :email"),
                {"email": email},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None
