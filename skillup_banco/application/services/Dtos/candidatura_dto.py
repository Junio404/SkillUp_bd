from __future__ import annotations

from datetime import date
from uuid import UUID

from domain.entidades.enums import StatusCandidatura
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CandidaturaRequestDTO(BaseRequestDTO):
    data_candidatura: date
    status: StatusCandidatura
    candidato_id: UUID
    vaga_id: UUID


class CandidaturaResponseDTO(BaseResponseDTO):
    id: UUID
    data_candidatura: date
    status: StatusCandidatura
    candidato_id: UUID
    vaga_id: UUID

