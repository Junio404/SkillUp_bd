from __future__ import annotations

from uuid import UUID

from domain.interfaces.vaga_repository import VagaRepository
from application.dtos.vaga_dto import VagaRequestDTO, VagaResponseDTO


class VagaService:
    def __init__(self, repository: VagaRepository) -> None:
        self._repository = repository

    def create(self, payload: VagaRequestDTO) -> VagaResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> VagaResponseDTO | None:
        pass

    def list_all(self) -> list[VagaResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: VagaRequestDTO) -> VagaResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def list_by_empresa(self, empresa_id: UUID) -> list[VagaResponseDTO]:
        pass


