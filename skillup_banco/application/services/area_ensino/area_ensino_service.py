from __future__ import annotations

from uuid import UUID

from domain.interfaces.area_ensino_repository import AreaEnsinoRepository
from application.dtos.area_ensino_dto import AreaEnsinoRequestDTO, AreaEnsinoResponseDTO


class AreaEnsinoService:
    def __init__(self, repository: AreaEnsinoRepository) -> None:
        self._repository = repository

    def create(self, payload: AreaEnsinoRequestDTO) -> AreaEnsinoResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> AreaEnsinoResponseDTO | None:
        pass

    def list_all(self) -> list[AreaEnsinoResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: AreaEnsinoRequestDTO) -> AreaEnsinoResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def get_by_nome(self, nome: str) -> AreaEnsinoResponseDTO | None:
        pass


