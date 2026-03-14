from __future__ import annotations

from typing import Sequence
from uuid import UUID

from application.dtos.candidatura_dto import CandidaturaRequestDTO
from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class CandidaturaService:
    def __init__(self, repository: CandidaturaRepository) -> None:
        self._repository = repository

    def create(self, payload: CandidaturaRequestDTO) -> Candidatura:
        candidatura_existente = self._repository.get_by_candidato_e_vaga(
            payload.candidato_id,
            payload.vaga_id,
        )
        if candidatura_existente is not None:
            raise ValueError("Candidato ja possui candidatura para essa vaga")

        candidatura = Candidatura(
            _data_candidatura=payload.data_candidatura,
            _status=StatusCandidatura(payload.status),
            _candidato_id=payload.candidato_id,
            _vaga_id=payload.vaga_id,
        )
        self._repository.add(candidatura)
        return candidatura

    def get_by_id(self, entity_id: UUID) -> Candidatura | None:
        return self._repository.get_by_id(entity_id)

    def list_all(self) -> Sequence[Candidatura]:
        return self._repository.list_all()

    def delete(self, entity_id: UUID) -> None:
        if not self._repository.exists(entity_id):
            raise ValueError("Candidatura nao encontrada")

        self._repository.remove(entity_id)

    def list_by_candidato(self, candidato_id: UUID) -> Sequence[Candidatura]:
        return self._repository.list_by_candidato(candidato_id)

    def get_by_candidato_e_vaga(self, candidato_id: UUID, vaga_id: UUID) -> Candidatura | None:
        return self._repository.get_by_candidato_e_vaga(candidato_id, vaga_id)

    def list_by_status_e_data(
        self,
        status: StatusCandidatura,
        data_inicio: datetime,
        data_fim: datetime,
    ) -> Sequence[Candidatura]:
        if data_inicio > data_fim:
            raise ValueError("Data inicial nao pode ser maior que data final")

        return self._repository.list_by_status_e_data(
            status=status,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )

    def update_status(self, candidatura_id: UUID, novo_status: StatusCandidatura) -> Candidatura:
        candidatura = self._repository.get_by_id(candidatura_id)
        if candidatura is None:
            raise ValueError("Candidatura nao encontrada")

        candidatura.atualizar_status(novo_status)
        self._repository.update(candidatura)
        return candidatura
