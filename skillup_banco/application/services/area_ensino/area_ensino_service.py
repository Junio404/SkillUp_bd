from __future__ import annotations

from uuid import UUID

from application.dtos.area_ensino_dto import (
    AreaEnsinoRequestDTO,
    AreaEnsinoResponseDTO,
)
from application.dtos.mapper import (
    entity_to_response,
    to_response_list,
    apply_update,
    build_entity,
)
from domain.entidades.area_ensino import AreaEnsino
from domain.interfaces.area_ensino_repository import AreaEnsinoRepository


class AreaEnsinoService:
    def __init__(self, repository: AreaEnsinoRepository) -> None:
        self._repository = repository

    def create(self, payload: AreaEnsinoRequestDTO) -> AreaEnsinoResponseDTO:
        existente = self._repository.get_by_nome(payload.nome)
        if existente is not None:
            raise ValueError("Ja existe area de ensino com esse nome")

        entity = build_entity(entity_cls=AreaEnsino, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, AreaEnsinoResponseDTO)

    def get_by_id(self, area_ensino_id: UUID) -> AreaEnsinoResponseDTO | None:
        entity = self._repository.get_by_id(area_ensino_id)
        if entity is None:
            return None
        return entity_to_response(entity, AreaEnsinoResponseDTO)

    def list_all(self) -> list[AreaEnsinoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, AreaEnsinoResponseDTO)

    def update(self, area_ensino_id: UUID, payload: AreaEnsinoRequestDTO) -> AreaEnsinoResponseDTO | None:
        entity = self._repository.get_by_id(area_ensino_id)
        if entity is None:
            raise ValueError("Area de ensino nao encontrada")

        existente = self._repository.get_by_nome(payload.nome)
        if existente is not None and existente.id != area_ensino_id:
            raise ValueError("Ja existe outra area de ensino com esse nome")

        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, AreaEnsinoResponseDTO)

    def delete(self, area_ensino_id: UUID) -> None:
        if not self._repository.exists(area_ensino_id):
            raise ValueError("Area de ensino nao encontrada")
        self._repository.remove(area_ensino_id)

    def get_by_nome(self, nome: str) -> AreaEnsinoResponseDTO | None:
        entity = self._repository.get_by_nome(nome)
        if entity is None:
            return None
        return entity_to_response(entity, AreaEnsinoResponseDTO)
