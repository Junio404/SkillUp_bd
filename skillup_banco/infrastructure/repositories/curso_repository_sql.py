from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text

from domain.entidades.curso import Curso
from domain.entidades.enums import Modalidade
from domain.interfaces.curso_repository import CursoRepository


class CursoRepositorySql(CursoRepository):

    def _to_entity(self, row) -> Curso:
        entity = Curso(
            _nome=row["nome"],
            _modalidade=Modalidade(row["modalidade"]),
            _instituicao_ensino_id=UUID(str(row["instituicao_id"])),
            _area=row["area"],
            _carga_horaria=row["cargaHoraria"],
            _capacidade=row["capacidade"],
            _prazo_inscricao=row["prazoInscricao"],
            _empresa_id=UUID(str(row["empresa_id"])
                             ) if row["empresa_id"] else None,
        )
        entity._id = UUID(str(row["id"]))
        return entity

    def add(self, entity: Curso) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO curso (id, nome, modalidade, instituicao_id, "
                    "area, cargaHoraria, capacidade, prazoInscricao, empresa_id) "
                    "VALUES (:id, :nome, :modalidade, :instituicao_id, "
                    ":area, :carga_horaria, :capacidade, :prazo_inscricao, :empresa_id)"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "modalidade": entity.modalidade.value,
                    "instituicao_id": str(entity.instituicao_ensino_id),
                    "area": entity.area,
                    "carga_horaria": entity.carga_horaria,
                    "capacidade": entity.capacidade,
                    "prazo_inscricao": entity.prazo_inscricao,
                    "empresa_id": str(entity.empresa_id) if entity.empresa_id else None,
                },
            )

    def get_by_id(self, entity_id: UUID) -> Curso | None:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM curso WHERE id = :id"),
                {"id": str(entity_id)},
            )
            row = result.mappings().first()
            return self._to_entity(row) if row else None

    def list_all(self) -> Sequence[Curso]:
        with self._connection.connect() as conn:
            result = conn.execute(text("SELECT * FROM curso"))
            return [self._to_entity(row) for row in result.mappings()]

    def update(self, entity: Curso) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text(
                    "UPDATE curso SET nome = :nome, modalidade = :modalidade, "
                    "area = :area, cargaHoraria = :carga_horaria, "
                    "capacidade = :capacidade, prazoInscricao = :prazo_inscricao, "
                    "empresa_id = :empresa_id WHERE id = :id"
                ),
                {
                    "id": str(entity.id),
                    "nome": entity.nome,
                    "modalidade": entity.modalidade.value,
                    "area": entity.area,
                    "carga_horaria": entity.carga_horaria,
                    "capacidade": entity.capacidade,
                    "prazo_inscricao": entity.prazo_inscricao,
                    "empresa_id": str(entity.empresa_id) if entity.empresa_id else None,
                },
            )

    def remove(self, entity_id: UUID) -> None:
        with self._connection.begin() as conn:
            conn.execute(
                text("DELETE FROM curso WHERE id = :id"),
                {"id": str(entity_id)},
            )

    def exists(self, entity_id: UUID) -> bool:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM curso WHERE id = :id"),
                {"id": str(entity_id)},
            )
            return result.first() is not None

    def list_by_instituicao(self, instituicao_id: UUID) -> Sequence[Curso]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM curso WHERE instituicao_id = :instituicao_id"),
                {"instituicao_id": str(instituicao_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]

    def list_by_empresa(self, empresa_id: UUID) -> Sequence[Curso]:
        with self._connection.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM curso WHERE empresa_id = :empresa_id"),
                {"empresa_id": str(empresa_id)},
            )
            return [self._to_entity(row) for row in result.mappings()]
