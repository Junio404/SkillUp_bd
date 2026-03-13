from __future__ import annotations

from datetime import date
from typing import Sequence

from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class FiltrarCandidaturasPorStatusDataService:
    def __init__(self, candidatura_repository: CandidaturaRepository) -> None:
        self._candidatura_repository = candidatura_repository

    def execute(
        self,
        status: StatusCandidatura,
        data_inicio: date,
        data_fim: date,
    ) -> Sequence[Candidatura]:
        if data_inicio > data_fim:
            raise ValueError("Data inicial nao pode ser maior que data final")

        return self._candidatura_repository.list_by_status_e_data(
            status=status,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
