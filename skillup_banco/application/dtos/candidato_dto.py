from __future__ import annotations

from typing import Optional
from uuid import UUID
from collections.abc import Sequence

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO
from application.dtos.candidatura_dto import CandidaturaResponseDTO


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


class CandidatoComCandidaturasResponseDTO(BaseResponseDTO):
    id: UUID
    nome: str
    cpf: str
    email: str
    area_interesse: str | None = None
    nivel_formacao: str | None = None
    curriculo_url: str | None = None
    candidaturas: Sequence[CandidaturaResponseDTO]
