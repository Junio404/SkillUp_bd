from __future__ import annotations

from uuid import UUID

from domain.interfaces.competencia_repository import CompetenciaRepository
from application.dtos.competencia_dto import CompetenciaRequestDTO, CompetenciaResponseDTO


class CompetenciaService:
    def __init__(self, repository: CompetenciaRepository) -> None:
        self._repository = repository

    def create(self, payload: CompetenciaRequestDTO) -> CompetenciaResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> CompetenciaResponseDTO | None:
        pass

    def list_all(self) -> list[CompetenciaResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: CompetenciaRequestDTO) -> CompetenciaResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def get_by_nome(self, nome: str) -> CompetenciaResponseDTO | None:
        pass


