from __future__ import annotations

from uuid import UUID

from domain.entidades.enums import Nivel
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CompetenciaCandidatoRequestDTO(BaseRequestDTO):
    nivel: Nivel
    candidato_id: UUID
    competencia_id: UUID


class CompetenciaCandidatoResponseDTO(BaseResponseDTO):
    id: UUID
    nivel: Nivel
    candidato_id: UUID
    competencia_id: UUID

