from __future__ import annotations

from uuid import UUID

from domain.interfaces.inscricao_curso_repository import InscricaoCursoRepository
from application.dtos.inscricao_curso_dto import InscricaoCursoRequestDTO, InscricaoCursoResponseDTO


class InscricaoCursoService:
    def __init__(self, repository: InscricaoCursoRepository) -> None:
        self._repository = repository

    def create(self, payload: InscricaoCursoRequestDTO) -> InscricaoCursoResponseDTO:
        pass

    def get_by_id(self, inscricao_curso_id: UUID) -> InscricaoCursoResponseDTO | None:
        pass

    def list_all(self) -> list[InscricaoCursoResponseDTO]:
        pass

    def update(self, inscricao_curso_id: UUID, payload: InscricaoCursoRequestDTO) -> InscricaoCursoResponseDTO | None:
        pass

    def delete(self, inscricao_curso_id: UUID) -> None:
        pass

    def list_by_candidato(self, candidato_id: UUID) -> list[InscricaoCursoResponseDTO]:
        pass

    def get_by_candidato_e_curso(self, candidato_id: UUID, curso_id: UUID) -> InscricaoCursoResponseDTO | None:
        pass
