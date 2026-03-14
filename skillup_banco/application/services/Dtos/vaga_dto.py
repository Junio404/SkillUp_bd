from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from domain.entidades.enums import Modalidade, TipoVaga
from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class VagaRequestDTO(BaseRequestDTO):
    titulo: str
    modalidade: Modalidade
    tipo: TipoVaga
    prazo_inscricao: date
    empresa_id: UUID
    descricao: Optional[str] = None
    localidade: Optional[str] = None
    jornada: Optional[str] = None


class VagaResponseDTO(BaseResponseDTO):
    id: UUID
    titulo: str
    modalidade: Modalidade
    tipo: TipoVaga
    prazo_inscricao: date
    empresa_id: UUID
    descricao: Optional[str] = None
    localidade: Optional[str] = None
    jornada: Optional[str] = None

