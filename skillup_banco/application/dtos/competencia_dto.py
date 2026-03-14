from __future__ import annotations

from typing import Optional
from uuid import UUID

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CompetenciaRequestDTO(BaseRequestDTO):
    nome: str
    descricao: Optional[str] = None


class CompetenciaResponseDTO(BaseResponseDTO):
    id: UUID
    nome: str
    descricao: Optional[str] = None


