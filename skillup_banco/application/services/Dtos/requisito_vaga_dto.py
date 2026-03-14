from __future__ import annotations

from uuid import UUID

from domain.entidades.enums import Nivel
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class RequisitoVagaRequestDTO(BaseRequestDTO):
    nivel: Nivel
    vaga_id: UUID
    competencia_id: UUID


class RequisitoVagaResponseDTO(BaseResponseDTO):
    id: UUID
    nivel: Nivel
    vaga_id: UUID
    competencia_id: UUID

