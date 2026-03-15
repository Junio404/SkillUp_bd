from __future__ import annotations

from uuid import UUID

from application.dtos.area_ensino_dto import AreaEnsinoResponseDTO
from application.dtos.instituicao_ensino_dto import (
    InstituicaoEnsinoComAreasResponseDTO,
    InstituicaoEnsinoRequestDTO,
    InstituicaoEnsinoResponseDTO,
)
from application.dtos.mapper import (
    entity_to_response,
    to_response_list,
    apply_update,
    build_entity,
)
from domain.entidades.instituicao_ensino import InstituicaoEnsino
from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService:
    def __init__(self, repository: InstituicaoEnsinoRepository) -> None:
        self._repository = repository

    def create(self, payload: InstituicaoEnsinoRequestDTO) -> InstituicaoEnsinoResponseDTO:
        existente_registro = self._repository.get_by_registro_educacional(payload.registro_educacional)
        if existente_registro is not None:
            raise ValueError("Ja existe instituicao com esse registro educacional")

        if payload.cnpj is not None:
            existente_cnpj = self._repository.get_by_cnpj(payload.cnpj)
            if existente_cnpj is not None:
                raise ValueError("Ja existe instituicao com esse CNPJ")

        entity = build_entity(entity_cls=InstituicaoEnsino, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, InstituicaoEnsinoResponseDTO)

    def get_by_id(self, instituicao_ensino_id: UUID) -> InstituicaoEnsinoResponseDTO | None:
        entity = self._repository.get_by_id(instituicao_ensino_id)
        if entity is None:
            return None
        return entity_to_response(entity, InstituicaoEnsinoResponseDTO)

    def list_all(self) -> list[InstituicaoEnsinoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, InstituicaoEnsinoResponseDTO)

    def update(self, instituicao_ensino_id: UUID, payload: InstituicaoEnsinoRequestDTO) -> InstituicaoEnsinoResponseDTO | None:
        entity = self._repository.get_by_id(instituicao_ensino_id)
        if entity is None:
            raise ValueError("Instituicao de ensino nao encontrada")

        existente_registro = self._repository.get_by_registro_educacional(payload.registro_educacional)
        if existente_registro is not None and existente_registro.id != instituicao_ensino_id:
            raise ValueError("Ja existe outra instituicao com esse registro educacional")

        if payload.cnpj is not None:
            existente_cnpj = self._repository.get_by_cnpj(payload.cnpj)
            if existente_cnpj is not None and existente_cnpj.id != instituicao_ensino_id:
                raise ValueError("Ja existe outra instituicao com esse CNPJ")

        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, InstituicaoEnsinoResponseDTO)

    def delete(self, instituicao_ensino_id: UUID) -> None:
        if not self._repository.exists(instituicao_ensino_id):
            raise ValueError("Instituicao de ensino nao encontrada")
        self._repository.remove(instituicao_ensino_id)

    def get_by_registro_educacional(self, registro: str) -> InstituicaoEnsinoResponseDTO | None:
        entity = self._repository.get_by_registro_educacional(registro)
        if entity is None:
            return None
        return entity_to_response(entity, InstituicaoEnsinoResponseDTO)

    def get_by_cnpj(self, cnpj: str) -> InstituicaoEnsinoResponseDTO | None:
        entity = self._repository.get_by_cnpj(cnpj)
        if entity is None:
            return None
        return entity_to_response(entity, InstituicaoEnsinoResponseDTO)

    def get_with_areas_ensino(self, instituicao_id: UUID) -> InstituicaoEnsinoComAreasResponseDTO | None:
        instituicao = self._repository.get_with_areas_ensino(instituicao_id)
        if instituicao is None:
            return None

        base = entity_to_response(instituicao, InstituicaoEnsinoResponseDTO)
        areas = to_response_list(instituicao.areas_ensino, AreaEnsinoResponseDTO)

        return InstituicaoEnsinoComAreasResponseDTO(
            id=base.id,
            razao_social=base.razao_social,
            registro_educacional=base.registro_educacional,
            nome_fantasia=base.nome_fantasia,
            cnpj=base.cnpj,
            tipo=base.tipo,
            areas_ensino=areas,
        )
