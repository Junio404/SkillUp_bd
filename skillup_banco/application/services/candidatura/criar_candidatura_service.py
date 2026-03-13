from __future__ import annotations

from datetime import datetime
from uuid import UUID

from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class CriarCandidaturaService:
    def __init__(self, candidatura_repository: CandidaturaRepository) -> None:
        self._candidatura_repository = candidatura_repository

    def execute(
        self,
        candidato_id: UUID,
        vaga_id: UUID,
        data_candidatura: datetime | None = None,
        status: StatusCandidatura = StatusCandidatura.ENVIADO,
    ) -> Candidatura:
        candidatura_existente = self._candidatura_repository.get_by_candidato_e_vaga(
            candidato_id,
            vaga_id,
        )
        if candidatura_existente is not None:
            raise ValueError("Candidato ja possui candidatura para essa vaga")

        candidatura_kwargs = {
            "_status": status,
            "_candidato_id": candidato_id,
            "_vaga_id": vaga_id,
        }
        if data_candidatura is not None:
            candidatura_kwargs["_data_candidatura"] = data_candidatura

        candidatura = Candidatura(**candidatura_kwargs)
        self._candidatura_repository.add(candidatura)
        return candidatura
