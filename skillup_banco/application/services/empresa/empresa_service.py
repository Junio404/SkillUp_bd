from __future__ import annotations

from uuid import UUID

from application.dtos.mapper import (
    apply_update,
    build_entity,
    entity_to_response,
    to_response_list,
)
from domain.entidades.empresa import Empresa
from domain.interfaces.empresa_repository import EmpresaRepository
from application.dtos.empresa_dto import EmpresaRequestDTO, EmpresaResponseDTO


class EmpresaService:
    def __init__(self, repository: EmpresaRepository) -> None:
        self._repository = repository

    def create(self, payload: EmpresaRequestDTO) -> EmpresaResponseDTO:
        empresa_por_cnpj = self._repository.get_by_cnpj(payload.cnpj)
        if empresa_por_cnpj is not None:
            raise ValueError("Ja existe empresa com esse CNPJ")

        entity = build_entity(entity_cls=Empresa, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, EmpresaResponseDTO)

    def get_by_id(self, empresa_id: UUID) -> EmpresaResponseDTO | None:
        entity = self._repository.get_by_id(empresa_id)
        if entity is None:
            return None
        return entity_to_response(entity, EmpresaResponseDTO)

    def list_all(self) -> list[EmpresaResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, EmpresaResponseDTO)

    def update(self, empresa_id: UUID, payload: EmpresaRequestDTO) -> EmpresaResponseDTO | None:
        entity = self._repository.get_by_id(empresa_id)
        if entity is None:
            raise ValueError("Empresa nao encontrada")

        empresa_por_cnpj = self._repository.get_by_cnpj(payload.cnpj)
        if empresa_por_cnpj is not None and empresa_por_cnpj.id != empresa_id:
            raise ValueError("Ja existe outra empresa com esse CNPJ")

        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, EmpresaResponseDTO)

    def delete(self, empresa_id: UUID) -> None:
        if not self._repository.exists(empresa_id):
            raise ValueError("Empresa nao encontrada")

        self._repository.remove(empresa_id)

    def get_by_cnpj(self, cnpj: str) -> EmpresaResponseDTO | None:
        entity = self._repository.get_by_cnpj(cnpj=cnpj)
        if entity is None:
            return None
        return entity_to_response(entity, EmpresaResponseDTO)
