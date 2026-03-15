from __future__ import annotations

from uuid import UUID

from application.dtos.curso_dto import CursoRequestDTO, CursoResponseDTO
from application.dtos.mapper import (
    build_entity,
    entity_to_response,
    to_response_list,
)
from domain.entidades.curso import Curso
from domain.interfaces.curso_repository import CursoRepository


class CursoService:
    def __init__(self, repository: CursoRepository) -> None:
        self._repository = repository

    def create(self, payload: CursoRequestDTO) -> CursoResponseDTO:
        entity = build_entity(entity_cls=Curso, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, CursoResponseDTO)

    def get_by_id(self, curso_id: UUID) -> CursoResponseDTO | None:
        entity = self._repository.get_by_id(curso_id)
        if entity is None:
            return None
        return entity_to_response(entity, CursoResponseDTO)

    def list_all(self) -> list[CursoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, CursoResponseDTO)

    def update(self, curso_id: UUID, payload: CursoRequestDTO) -> CursoResponseDTO | None:
        entity = self._repository.get_by_id(curso_id)
        if entity is None:
            raise ValueError("Curso não encontrado")

        updated = build_entity(entity_cls=Curso, request=payload)
        updated._id = entity.id

        self._repository.update(updated)
        return entity_to_response(updated, CursoResponseDTO)

    def delete(self, curso_id: UUID) -> None:
        if not self._repository.exists(curso_id):
            raise ValueError("Curso não encontrado")
        self._repository.remove(curso_id)

    def list_by_instituicao(self, instituicao_id: UUID) -> list[CursoResponseDTO]:
        entities = self._repository.list_by_instituicao(instituicao_id)
        return to_response_list(entities, CursoResponseDTO)

    def list_by_empresa(self, empresa_id: UUID) -> list[CursoResponseDTO]:
        entities = self._repository.list_by_empresa(empresa_id)
        return to_response_list(entities, CursoResponseDTO)
