from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from application.dtos.candidatura_dto import (
    CandidaturaRequestDTO,
    CandidaturaResponseDTO,
)
from application.dtos.mapper import entity_to_response, to_response_list
from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class CandidaturaService:
    def __init__(self, repository: CandidaturaRepository) -> None:
        self._repository = repository

    def create(self, payload: CandidaturaRequestDTO) -> CandidaturaResponseDTO:
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
        return entity_to_response(candidatura, CandidaturaResponseDTO)

    def get_by_id(self, entity_id: UUID) -> CandidaturaResponseDTO | None:
        candidatura = self._repository.get_by_id(entity_id)
        if candidatura is None:
            return None
        return entity_to_response(candidatura, CandidaturaResponseDTO)

    def list_all(self) -> list[CandidaturaResponseDTO]:
        candidaturas = self._repository.list_all()
        return to_response_list(candidaturas, CandidaturaResponseDTO)

    def delete(self, entity_id: UUID) -> None:
        if not self._repository.exists(entity_id):
            raise ValueError("Candidatura nao encontrada")

        self._repository.remove(entity_id)

    def list_by_candidato(self, candidato_id: UUID) -> list[CandidaturaResponseDTO]:
        candidaturas = self._repository.list_by_candidato(candidato_id)
        return to_response_list(candidaturas, CandidaturaResponseDTO)

    def get_by_candidato_e_vaga(
        self,
        candidato_id: UUID,
        vaga_id: UUID,
    ) -> CandidaturaResponseDTO | None:
        candidatura = self._repository.get_by_candidato_e_vaga(
            candidato_id, vaga_id)
        if candidatura is None:
            return None
        return entity_to_response(candidatura, CandidaturaResponseDTO)

    def list_by_status_e_data(
        self,
        status: StatusCandidatura,
        data_inicio: datetime,
        data_fim: datetime,
    ) -> list[CandidaturaResponseDTO]:
        if data_inicio > data_fim:
            raise ValueError("Data inicial nao pode ser maior que data final")

        candidaturas = self._repository.list_by_status_e_data(
            status=status,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
        return to_response_list(candidaturas, CandidaturaResponseDTO)

    def update_status(
        self,
        candidatura_id: UUID,
        novo_status: StatusCandidatura,
    ) -> CandidaturaResponseDTO:
        candidatura = self._repository.get_by_id(candidatura_id)
        if candidatura is None:
            raise ValueError("Candidatura nao encontrada")

        candidatura.atualizar_status(novo_status)
        self._repository.update(candidatura)
        return entity_to_response(candidatura, CandidaturaResponseDTO)
