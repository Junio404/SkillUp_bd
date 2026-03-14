from __future__ import annotations

from datetime import datetime
from uuid import UUID

from domain.entidades.enums import StatusCandidatura
from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CandidaturaRequestDTO(BaseRequestDTO):
    data_candidatura: datetime
    status: StatusCandidatura
    candidato_id: UUID
    vaga_id: UUID


class CandidaturaResponseDTO(BaseResponseDTO):
    id: UUID
    data_candidatura: datetime
    status: StatusCandidatura
    candidato_id: UUID
    vaga_id: UUID


