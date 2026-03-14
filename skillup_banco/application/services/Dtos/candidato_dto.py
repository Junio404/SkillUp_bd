from __future__ import annotations

from typing import Optional
from uuid import UUID

from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CandidatoRequestDTO(BaseRequestDTO):
    nome: str
    cpf: str
    email: str
    area_interesse: Optional[str] = None
    nivel_formacao: Optional[str] = None
    curriculo_url: Optional[str] = None


class CandidatoResponseDTO(BaseResponseDTO):
    id: UUID
    nome: str
    cpf: str
    email: str
    area_interesse: Optional[str] = None
    nivel_formacao: Optional[str] = None
    curriculo_url: Optional[str] = None

