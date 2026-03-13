from __future__ import annotations

from uuid import UUID

from domain.entidades.candidatura import Candidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class ObterCandidaturaPorIdService:
    def __init__(self, candidatura_repository: CandidaturaRepository) -> None:
        self._candidatura_repository = candidatura_repository

    def execute(self, candidatura_id: UUID) -> Candidatura | None:
        return self._candidatura_repository.get_by_id(candidatura_id)
