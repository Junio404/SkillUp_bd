from __future__ import annotations

from uuid import UUID

from application.dtos.competencia_dto import CompetenciaRequestDTO, CompetenciaResponseDTO
from application.dtos.mapper import (
    apply_update,
    build_entity,
    entity_to_response,
    to_response_list,
)
from domain.entidades.competencia import Competencia
from domain.interfaces.competencia_repository import CompetenciaRepository


class CompetenciaService:
    def __init__(self, repository: CompetenciaRepository) -> None:
        self._repository = repository

    def create(self, payload: CompetenciaRequestDTO) -> CompetenciaResponseDTO:
        if self._repository.get_by_nome(payload.nome) is not None:
            raise ValueError("Já existe competência com esse nome")

        entity = build_entity(entity_cls=Competencia, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, CompetenciaResponseDTO)

    def get_by_id(self, competencia_id: UUID) -> CompetenciaResponseDTO | None:
        entity = self._repository.get_by_id(competencia_id)
        if entity is None:
            return None
        return entity_to_response(entity, CompetenciaResponseDTO)

    def list_all(self) -> list[CompetenciaResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, CompetenciaResponseDTO)

    def update(self, competencia_id: UUID, payload: CompetenciaRequestDTO) -> CompetenciaResponseDTO | None:
        entity = self._repository.get_by_id(competencia_id)
        if entity is None:
            raise ValueError("Competência não encontrada")

        existente = self._repository.get_by_nome(payload.nome)
        if existente is not None and existente.id != competencia_id:
            raise ValueError("Já existe outra competência com esse nome")

        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, CompetenciaResponseDTO)

    def delete(self, competencia_id: UUID) -> None:
        if not self._repository.exists(competencia_id):
            raise ValueError("Competência não encontrada")
        self._repository.remove(competencia_id)

    def get_by_nome(self, nome: str) -> CompetenciaResponseDTO | None:
        entity = self._repository.get_by_nome(nome)
        if entity is None:
            return None
        return entity_to_response(entity, CompetenciaResponseDTO)
