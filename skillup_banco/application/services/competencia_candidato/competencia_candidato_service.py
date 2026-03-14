from __future__ import annotations

from uuid import UUID

from domain.interfaces.competencia_candidato_repository import CompetenciaCandidatoRepository
from application.dtos.competencia_candidato_dto import CompetenciaCandidatoRequestDTO, CompetenciaCandidatoResponseDTO


class CompetenciaCandidatoService:
    def __init__(self, repository: CompetenciaCandidatoRepository) -> None:
        self._repository = repository

    def create(self, payload: CompetenciaCandidatoRequestDTO) -> CompetenciaCandidatoResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> CompetenciaCandidatoResponseDTO | None:
        pass

    def list_all(self) -> list[CompetenciaCandidatoResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: CompetenciaCandidatoRequestDTO) -> CompetenciaCandidatoResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def list_by_candidato(self, candidato_id: UUID) -> list[CompetenciaCandidatoResponseDTO]:
        pass


