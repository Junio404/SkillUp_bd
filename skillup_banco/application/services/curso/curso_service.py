from __future__ import annotations

from uuid import UUID

from domain.interfaces.curso_repository import CursoRepository
from application.dtos.curso_dto import CursoRequestDTO, CursoResponseDTO


class CursoService:
    def __init__(self, repository: CursoRepository) -> None:
        self._repository = repository

    def create(self, payload: CursoRequestDTO) -> CursoResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> CursoResponseDTO | None:
        pass

    def list_all(self) -> list[CursoResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: CursoRequestDTO) -> CursoResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def list_by_instituicao(self, instituicao_id: UUID) -> list[CursoResponseDTO]:
        pass

    def list_by_empresa(self, empresa_id: UUID) -> list[CursoResponseDTO]:
        pass


