from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from domain.entidades.enums import Modalidade
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class CursoRequestDTO(BaseRequestDTO):
    nome: str
    modalidade: Modalidade
    instituicao_ensino_id: UUID
    area: Optional[str] = None
    carga_horaria: Optional[int] = None
    capacidade: Optional[int] = None
    prazo_inscricao: Optional[date] = None
    empresa_id: Optional[UUID] = None


class CursoResponseDTO(BaseResponseDTO):
    id: UUID
    nome: str
    modalidade: Modalidade
    instituicao_ensino_id: UUID
    area: Optional[str] = None
    carga_horaria: Optional[int] = None
    capacidade: Optional[int] = None
    prazo_inscricao: Optional[date] = None
    empresa_id: Optional[UUID] = None

