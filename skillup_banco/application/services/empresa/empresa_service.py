from __future__ import annotations

from uuid import UUID

from domain.interfaces.empresa_repository import EmpresaRepository
from application.dtos.empresa_dto import EmpresaRequestDTO, EmpresaResponseDTO


class EmpresaService:
    def __init__(self, repository: EmpresaRepository) -> None:
        self._repository = repository

    def create(self, payload: EmpresaRequestDTO) -> EmpresaResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> EmpresaResponseDTO | None:
        pass

    def list_all(self) -> list[EmpresaResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: EmpresaRequestDTO) -> EmpresaResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def get_by_cnpj(self, cnpj: str) -> EmpresaResponseDTO | None:
        pass


