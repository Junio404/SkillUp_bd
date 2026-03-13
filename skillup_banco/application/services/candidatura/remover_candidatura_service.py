from __future__ import annotations

from uuid import UUID

from domain.interfaces.candidatura_repository import CandidaturaRepository


class RemoverCandidaturaService:
    def __init__(self, candidatura_repository: CandidaturaRepository) -> None:
        self._candidatura_repository = candidatura_repository

    def execute(self, candidatura_id: UUID) -> None:
        if not self._candidatura_repository.exists(candidatura_id):
            raise ValueError("Candidatura nao encontrada")

        self._candidatura_repository.remove(candidatura_id)
