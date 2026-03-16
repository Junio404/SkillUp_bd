from __future__ import annotations

from uuid import UUID

from domain.interfaces.competencia_candidato_repository import CompetenciaCandidatoRepository
from application.dtos.competencia_candidato_dto import CompetenciaCandidatoRequestDTO, CompetenciaCandidatoResponseDTO

from domain.entidades.competencia_candidato import CompetenciaCandidato
from application.dtos.mapper import entity_to_response, to_response_list, apply_update, build_entity

class CompetenciaCandidatoService:
    def __init__(self, repository: CompetenciaCandidatoRepository) -> None:
        self._repository = repository

    def create(self, payload: CompetenciaCandidatoRequestDTO) -> CompetenciaCandidatoResponseDTO:
        entity = build_entity(entity_cls=CompetenciaCandidato, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, CompetenciaCandidatoResponseDTO)

    def get_by_id(self, competencia_candidato_id: UUID) -> CompetenciaCandidatoResponseDTO | None:
        entity = self._repository.get_by_id(competencia_candidato_id)
        if entity is None:
            return None
        return entity_to_response(entity, CompetenciaCandidatoResponseDTO)

    def list_all(self) -> list[CompetenciaCandidatoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, CompetenciaCandidatoResponseDTO)

    def update(self, competencia_candidato_id: UUID, payload: CompetenciaCandidatoRequestDTO) -> CompetenciaCandidatoResponseDTO | None:
        entity = self._repository.get_by_id(competencia_candidato_id)
        if entity is None:
            raise ValueError("Competência do candidato não encontrada")
        
        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, CompetenciaCandidatoResponseDTO)

    def delete(self, competencia_candidato_id: UUID) -> None:
        if not self._repository.exists(competencia_candidato_id):
            raise ValueError("Competência do candidato não encontrada.")
        
        self._repository.remove(competencia_candidato_id)

    def list_by_candidato(self, candidato_id: UUID) -> list[CompetenciaCandidatoResponseDTO]:
        entities = self._repository.list_by_candidato(candidato_id)
        return to_response_list(entities, CompetenciaCandidatoResponseDTO)

