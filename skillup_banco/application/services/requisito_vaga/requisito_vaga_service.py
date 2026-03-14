from __future__ import annotations

from uuid import UUID

from domain.interfaces.requisito_vaga_repository import RequisitoVagaRepository
from application.dtos.requisito_vaga_dto import RequisitoVagaRequestDTO, RequisitoVagaResponseDTO


class RequisitoVagaService:
    def __init__(self, repository: RequisitoVagaRepository) -> None:
        self._repository = repository

    def create(self, payload: RequisitoVagaRequestDTO) -> RequisitoVagaResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> RequisitoVagaResponseDTO | None:
        pass

    def list_all(self) -> list[RequisitoVagaResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: RequisitoVagaRequestDTO) -> RequisitoVagaResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def list_by_vaga(self, vaga_id: UUID) -> list[RequisitoVagaResponseDTO]:
        pass


