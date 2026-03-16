from __future__ import annotations

from uuid import UUID

from application.dtos.vaga_dto import VagaRequestDTO, VagaResponseDTO
from application.dtos.mapper import (
    build_entity,
    entity_to_response,
    to_response_list,
    apply_update
)
from domain.entidades.vaga import Vaga
from domain.interfaces.vaga_repository import VagaRepository


class VagaService:
    def __init__(self, repository: VagaRepository) -> None:
        self._repository = repository

    def create(self, payload: VagaRequestDTO) -> VagaResponseDTO:
        entity = build_entity(entity_cls=Vaga, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, VagaResponseDTO)

    def get_by_id(self, vaga_id: UUID) -> VagaResponseDTO | None:
        entity = self._repository.get_by_id(vaga_id)
        if entity is None:
            return None
        return entity_to_response(entity, VagaResponseDTO)

    def list_all(self) -> list[VagaResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, VagaResponseDTO)

    def update(self, vaga_id: UUID, payload: VagaRequestDTO) -> VagaResponseDTO | None:
        entity = self._repository.get_by_id(vaga_id)
        if entity is None:
            raise ValueError("Vaga não encontrada")
        
        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, VagaResponseDTO)

    def delete(self, vaga_id: UUID) -> None:
        if not self._repository.exists(vaga_id):
            raise ValueError("Vaga não encontrada")
        
        self._repository.remove(vaga_id)

    def list_by_empresa(self, empresa_id: UUID) -> list[VagaResponseDTO]:
        entities = self._repository.list_by_empresa(empresa_id)
        return to_response_list(entities, VagaResponseDTO)
