from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.candidato import Candidato
from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidato_repository import CandidatoRepository


class CandidatoRepositorySql(CandidatoRepository):

    def _to_entity(self, row) -> Candidato:
        entity = Candidato(
            _nome=row["nome"],
            _cpf=row["cpf"],
            _email=row["email"],
            _senha_hash=row["senha_hash"],
            _area_interesse=row["areaInteresse"],
            _nivel_formacao=row["nivelFormacao"],
            _curriculo_url=row["curriculo_url"],
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def _to_candidatura_from_join(self, row) -> Candidatura | None:
        if row["candidatura_id"] is None:
            return None

        candidatura = Candidatura(
            _status=StatusCandidatura(row["status"]),
            _candidato_id=UUID(str(row["candidato_id"])),
            _vaga_id=UUID(str(row["vaga_id"])),
            _data_candidatura=row["dataCandidatura"],
        )
        candidatura._id = UUID(str(row["candidatura_id"]))
        return candidatura

    def add(self, entity: Candidato) -> None:
        if not entity.senha_hash:
            raise ValueError("Senha hash obrigatoria para criar candidato")

        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO candidato (id, nome, cpf, email, senha_hash, areaInteresse, "
                    "nivelFormacao, curriculo_url) "
                    "VALUES (:id, :nome, :cpf, :email, :senha_hash, :area_interesse, "
                    ":nivel_formacao, :curriculo_url)"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "cpf": entity.cpf,
                    "email": entity.email,
                    "senha_hash": entity.senha_hash,
                    "area_interesse": entity.area_interesse,
                    "nivel_formacao": entity.nivel_formacao,
                    "curriculo_url": entity.curriculo_url,
                },
            )

    def get_by_id(self, candidato_id: UUID) -> Candidato | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM candidato WHERE id = :id"),
                {"id": str(candidato_id)},
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
                    "senha_hash = :senha_hash, "
                    "areaInteresse = :area_interesse, nivelFormacao = :nivel_formacao, "
                    "curriculo_url = :curriculo_url WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "email": entity.email,
                    "senha_hash": entity.senha_hash,
                    "area_interesse": entity.area_interesse,
                    "nivel_formacao": entity.nivel_formacao,
                    "curriculo_url": entity.curriculo_url,
                },
            )

    def remove(self, candidato_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM candidato WHERE id = :id"),
                {"id": str(candidato_id)},
            )

    def exists(self, candidato_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM candidato WHERE id = :id"),
                {"id": str(candidato_id)},
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

    def get_with_candidaturas(self, candidato_id: UUID) -> Candidato | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT
                        c.id,
                        c.nome,
                        c.cpf,
                        c.email,
                        c.senha_hash,
                        c.areaInteresse,
                        c.nivelFormacao,
                        c.curriculo_url,
                        cd.id AS candidatura_id,
                        cd.dataCandidatura,
                        cd.status,
                        cd.candidato_id,
                        cd.vaga_id
                    FROM candidato c
                    LEFT JOIN candidatura cd
                        ON cd.candidato_id = c.id
                    WHERE c.id = :candidato_id
                    ORDER BY cd.dataCandidatura DESC
                    """
                ),
                {"candidato_id": str(candidato_id)},
            )

            rows = result.mappings().all()

            if not rows:
                return None

            candidato = self._to_entity(rows[0])

            candidaturas: list[Candidatura] = []
            for row in rows:
                candidatura = self._to_candidatura_from_join(row)
                if candidatura is not None:
                    candidaturas.append(candidatura)

            candidato.definir_candidaturas(candidaturas)
            return candidato
