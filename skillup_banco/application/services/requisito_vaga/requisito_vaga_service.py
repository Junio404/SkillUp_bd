from __future__ import annotations

from uuid import UUID

from application.dtos.requisito_vaga_dto import RequisitoVagaRequestDTO, RequisitoVagaResponseDTO
from application.dtos.mapper import entity_to_response, to_response_list, apply_update, build_entity
from domain.entidades.requisito_vaga import RequisitoVaga
from domain.interfaces.requisito_vaga_repository import RequisitoVagaRepository


class RequisitoVagaService:
    def __init__(self, repository: RequisitoVagaRepository) -> None:
        self._repository = repository

    def create(self, payload: RequisitoVagaRequestDTO) -> RequisitoVagaResponseDTO:
        requisitos = self._repository.list_by_vaga(payload.vaga_id)
        
        for req in requisitos:
            if req.competencia_id == payload.competencia_id:
                raise ValueError("Vaga ja possui esse requisito de competencia")
        
        entity = build_entity(entity_cls=RequisitoVaga, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, RequisitoVagaResponseDTO)

    def get_by_id(self, requisito_vaga_id: UUID) -> RequisitoVagaResponseDTO | None:
        entity = self._repository.get_by_id(requisito_vaga_id)
        if entity is None:
            return None
        return entity_to_response(entity, RequisitoVagaResponseDTO)

    def list_all(self) -> list[RequisitoVagaResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, RequisitoVagaResponseDTO)

    def update(self, requisito_vaga_id: UUID, payload: RequisitoVagaRequestDTO) -> RequisitoVagaResponseDTO | None:
        entity = self._repository.get_by_id(requisito_vaga_id)
        if entity is None:
            raise ValueError("RequisitoVaga nao encontrada")
        
        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, RequisitoVagaResponseDTO)

    def delete(self, requisito_vaga_id: UUID) -> None:
        if not self._repository.exists(requisito_vaga_id):
            raise ValueError("RequisitoVaga nao encontrada")
        
        self._repository.remove(requisito_vaga_id)

    def list_by_vaga(self, vaga_id: UUID) -> list[RequisitoVagaResponseDTO]:
        entities = self._repository.list_by_vaga(vaga_id)
        return to_response_list(entities, RequisitoVagaResponseDTO)