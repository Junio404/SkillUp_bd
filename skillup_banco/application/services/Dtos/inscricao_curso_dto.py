from __future__ import annotations

from datetime import date
from uuid import UUID

from domain.entidades.enums import StatusInscricao
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class InscricaoCursoRequestDTO(BaseRequestDTO):
    data_inscricao: date
    status: StatusInscricao
    candidato_id: UUID
    curso_id: UUID


class InscricaoCursoResponseDTO(BaseResponseDTO):
    id: UUID
    data_inscricao: date
    status: StatusInscricao
    candidato_id: UUID
    curso_id: UUID

