from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.enums import Modalidade, TipoVaga
from domain.entidades.vaga import Vaga
from domain.interfaces.vaga_repository import VagaRepository


class VagaRepositorySql(VagaRepository):

    def _to_entity(self, row) -> Vaga:
        entity = Vaga(
            _titulo=row["titulo"],
            _modalidade=Modalidade(row["modalidade"]),
            _tipo=TipoVaga(row["tipo"]),
            _prazo_inscricao=row["prazoInscricao"],
            _empresa_id=UUID(str(row["empresa_id"])),
            _descricao=row["descricao"],
            _localidade=row["localidade"],
            _jornada=row["jornada"],
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: Vaga) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO vaga (id, titulo, modalidade, tipo, prazoInscricao, "
                    "empresa_id, descricao, localidade, jornada) "
                    "VALUES (:id, :titulo, :modalidade, :tipo, :prazo_inscricao, "
                    ":empresa_id, :descricao, :localidade, :jornada)"
                ),
                {
                    "id": str(entity.id),
                    "titulo": entity.titulo,
                    "modalidade": entity.modalidade.value,
                    "tipo": entity.tipo.value,
                    "prazo_inscricao": entity.prazo_inscricao,
                    "empresa_id": str(entity.empresa_id),
                    "descricao": entity.descricao,
                    "localidade": entity.localidade,
                    "jornada": entity.jornada,
                },
            )

    def get_by_id(self, vaga_id: UUID) -> Vaga | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM vaga WHERE id = :id"),
                {"id": str(vaga_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[Vaga]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM vaga"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: Vaga) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "UPDATE vaga SET titulo = :titulo, modalidade = :modalidade, "
                    "tipo = :tipo, prazoInscricao = :prazo_inscricao, "
                    "descricao = :descricao, localidade = :localidade, "
                    "jornada = :jornada WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "titulo": entity.titulo,
                    "modalidade": entity.modalidade.value,
                    "tipo": entity.tipo.value,
                    "prazo_inscricao": entity.prazo_inscricao,
                    "descricao": entity.descricao,
                    "localidade": entity.localidade,
                    "jornada": entity.jornada,
                },
            )

    def remove(self, vaga_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM vaga WHERE id = :id"),
                {"id": str(vaga_id)},
            )

    def exists(self, vaga_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM vaga WHERE id = :id"),
                {"id": str(vaga_id)},
            )
            return result.first() is not None

    def list_by_empresa(self, empresa_id: UUID) -> Sequence[Vaga]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM vaga WHERE empresa_id = :empresa_id"),
                {"empresa_id": str(empresa_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]
