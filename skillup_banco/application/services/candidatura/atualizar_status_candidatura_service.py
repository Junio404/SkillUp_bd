from __future__ import annotations

from uuid import UUID

from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class AtualizarStatusCandidaturaService:
    def __init__(self, candidatura_repository: CandidaturaRepository) -> None:
        self._candidatura_repository = candidatura_repository

    def execute(self, candidatura_id: UUID, novo_status: StatusCandidatura) -> Candidatura:
        candidatura = self._candidatura_repository.get_by_id(candidatura_id)
        if candidatura is None:
            raise ValueError("Candidatura nao encontrada")

        candidatura.atualizar_status(novo_status)
        self._candidatura_repository.update(candidatura)
        return candidatura
