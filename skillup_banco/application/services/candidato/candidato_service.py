from __future__ import annotations

from uuid import UUID

from domain.interfaces.candidato_repository import CandidatoRepository
from application.dtos.candidato_dto import CandidatoRequestDTO, CandidatoResponseDTO


class CandidatoService:
    def __init__(self, repository: CandidatoRepository) -> None:
        self._repository = repository

    def create(self, payload: CandidatoRequestDTO) -> CandidatoResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> CandidatoResponseDTO | None:
        pass

    def list_all(self) -> list[CandidatoResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: CandidatoRequestDTO) -> CandidatoResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def get_by_cpf(self, cpf: str) -> CandidatoResponseDTO | None:
        pass

    def get_by_email(self, email: str) -> CandidatoResponseDTO | None:
        pass


