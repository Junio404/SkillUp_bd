from __future__ import annotations

from uuid import UUID

from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository
from application.dtos.instituicao_ensino_dto import InstituicaoEnsinoRequestDTO, InstituicaoEnsinoResponseDTO


class InstituicaoEnsinoService:
    def __init__(self, repository: InstituicaoEnsinoRepository) -> None:
        self._repository = repository

    def create(self, payload: InstituicaoEnsinoRequestDTO) -> InstituicaoEnsinoResponseDTO:
        pass

    def get_by_id(self, entity_id: UUID) -> InstituicaoEnsinoResponseDTO | None:
        pass

    def list_all(self) -> list[InstituicaoEnsinoResponseDTO]:
        pass

    def update(self, entity_id: UUID, payload: InstituicaoEnsinoRequestDTO) -> InstituicaoEnsinoResponseDTO | None:
        pass

    def delete(self, entity_id: UUID) -> None:
        pass

    def get_by_registro_educacional(self, registro: str) -> InstituicaoEnsinoResponseDTO | None:
        pass

    def get_by_cnpj(self, cnpj: str) -> InstituicaoEnsinoResponseDTO | None:
        pass


