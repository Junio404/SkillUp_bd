from __future__ import annotations

from uuid import UUID

from domain.entidades.enums import Nivel
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CursoCompetenciaRequestDTO(BaseRequestDTO):
    nivel: Nivel
    curso_id: UUID
    competencia_id: UUID


class CursoCompetenciaResponseDTO(BaseResponseDTO):
    id: UUID
    nivel: Nivel
    curso_id: UUID
    competencia_id: UUID

