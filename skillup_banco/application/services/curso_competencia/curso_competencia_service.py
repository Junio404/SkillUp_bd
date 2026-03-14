from __future__ import annotations

from uuid import UUID

from domain.interfaces.curso_competencia_repository import CursoCompetenciaRepository
from application.services.Dtos.curso_competencia_dto import CursoCompetenciaRequestDTO, CursoCompetenciaResponseDTO


class CursoCompetenciaService:
    def __init__(self, repository: CursoCompetenciaRepository) -> None:
        self._repository = repository

    def create(self, payload: CursoCompetenciaRequestDTO) -> CursoCompetenciaResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> CursoCompetenciaResponseDTO | None:
        pass

    def list_all(self) -> list[CursoCompetenciaResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: CursoCompetenciaRequestDTO) -> CursoCompetenciaResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def list_by_curso(self, curso_id: UUID) -> list[CursoCompetenciaResponseDTO]:
        pass

