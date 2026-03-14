from __future__ import annotations

from uuid import UUID

from domain.interfaces.instituicao_area_ensino_repository import InstituicaoAreaEnsinoRepository
from application.dtos.instituicao_area_ensino_dto import InstituicaoAreaEnsinoRequestDTO, InstituicaoAreaEnsinoResponseDTO


class InstituicaoAreaEnsinoService:
    def __init__(self, repository: InstituicaoAreaEnsinoRepository) -> None:
        self._repository = repository

    def create(self, payload: InstituicaoAreaEnsinoRequestDTO) -> InstituicaoAreaEnsinoResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> InstituicaoAreaEnsinoResponseDTO | None:
        pass

    def list_all(self) -> list[InstituicaoAreaEnsinoResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: InstituicaoAreaEnsinoRequestDTO) -> InstituicaoAreaEnsinoResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def list_by_instituicao(self, instituicao_id: UUID) -> list[InstituicaoAreaEnsinoResponseDTO]:
        pass

    def get_by_chave(self, instituicao_id: UUID, area_ensino_id: UUID) -> InstituicaoAreaEnsinoResponseDTO | None:
        pass


