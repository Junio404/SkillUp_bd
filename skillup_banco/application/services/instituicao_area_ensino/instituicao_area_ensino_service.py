from __future__ import annotations

from uuid import UUID

from application.dtos.instituicao_area_ensino_dto import (
    InstituicaoAreaEnsinoRequestDTO,
    InstituicaoAreaEnsinoResponseDTO,
)
from application.dtos.mapper import (
    entity_to_response,
    to_response_list,
    build_entity,
)
from domain.entidades.instituicao_area_ensino import InstituicaoAreaEnsino
from domain.interfaces.instituicao_area_ensino_repository import InstituicaoAreaEnsinoRepository
from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository
from domain.interfaces.area_ensino_repository import AreaEnsinoRepository


class InstituicaoAreaEnsinoService:
    def __init__(
        self,
        repository: InstituicaoAreaEnsinoRepository,
        instituicao_ensino_repository: InstituicaoEnsinoRepository,
        area_ensino_repository: AreaEnsinoRepository,
    ) -> None:
        self._repository = repository
        self._instituicao_ensino_repository = instituicao_ensino_repository
        self._area_ensino_repository = area_ensino_repository

    def _validar_fks(self, payload: InstituicaoAreaEnsinoRequestDTO) -> None:
        if not self._instituicao_ensino_repository.exists(payload.instituicao_ensino_id):
            raise ValueError("Instituicao de ensino nao encontrada")
        if not self._area_ensino_repository.exists(payload.area_ensino_id):
            raise ValueError("Area de ensino nao encontrada")

    def create(self, payload: InstituicaoAreaEnsinoRequestDTO) -> InstituicaoAreaEnsinoResponseDTO:
        self._validar_fks(payload)

        existente = self._repository.get_by_chave(
            payload.instituicao_ensino_id, payload.area_ensino_id
        )
        if existente is not None:
            raise ValueError("Essa associacao instituicao-area ja existe")

        entity = build_entity(entity_cls=InstituicaoAreaEnsino, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, InstituicaoAreaEnsinoResponseDTO)

    def get_by_id(self, instituicao_area_ensino_id: UUID) -> InstituicaoAreaEnsinoResponseDTO | None:
        entity = self._repository.get_by_id(instituicao_area_ensino_id)
        if entity is None:
            return None
        return entity_to_response(entity, InstituicaoAreaEnsinoResponseDTO)

    def list_all(self) -> list[InstituicaoAreaEnsinoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, InstituicaoAreaEnsinoResponseDTO)

    def update(self, instituicao_area_ensino_id: UUID, payload: InstituicaoAreaEnsinoRequestDTO) -> InstituicaoAreaEnsinoResponseDTO | None:
        entity = self._repository.get_by_id(instituicao_area_ensino_id)
        if entity is None:
            raise ValueError("Associacao instituicao-area nao encontrada")

        self._validar_fks(payload)

        existente = self._repository.get_by_chave(
            payload.instituicao_ensino_id, payload.area_ensino_id
        )
        if existente is not None:
            atual_chave = (entity.instituicao_ensino_id, entity.area_ensino_id)
            nova_chave = (payload.instituicao_ensino_id, payload.area_ensino_id)
            if atual_chave != nova_chave:
                raise ValueError("Essa associacao instituicao-area ja existe")

        entity = build_entity(entity_cls=InstituicaoAreaEnsino, request=payload)
        self._repository.update(entity)
        return entity_to_response(entity, InstituicaoAreaEnsinoResponseDTO)

    def delete(self, instituicao_area_ensino_id: UUID) -> None:
        if not self._repository.exists(instituicao_area_ensino_id):
            raise ValueError("Associacao instituicao-area nao encontrada")
        self._repository.remove(instituicao_area_ensino_id)

    def list_by_instituicao(self, instituicao_id: UUID) -> list[InstituicaoAreaEnsinoResponseDTO]:
        entities = self._repository.list_by_instituicao(instituicao_id)
        return to_response_list(entities, InstituicaoAreaEnsinoResponseDTO)

    def get_by_chave(self, instituicao_id: UUID, area_ensino_id: UUID) -> InstituicaoAreaEnsinoResponseDTO | None:
        entity = self._repository.get_by_chave(instituicao_id, area_ensino_id)
        if entity is None:
            return None
        return entity_to_response(entity, InstituicaoAreaEnsinoResponseDTO)
