from __future__ import annotations

from typing import Sequence
from uuid import UUID

from domain.entidades.candidatura import Candidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class ListarCandidaturasPorCandidatoService:
    def __init__(self, candidatura_repository: CandidaturaRepository) -> None:
        self._candidatura_repository = candidatura_repository

    def execute(self, candidato_id: UUID) -> Sequence[Candidatura]:
        return self._candidatura_repository.list_by_candidato(candidato_id)
