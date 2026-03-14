from __future__ import annotations

from typing import Optional
from uuid import UUID

from application.services.Dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class InstituicaoEnsinoRequestDTO(BaseRequestDTO):
    razao_social: str
    registro_educacional: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    tipo: Optional[str] = None


class InstituicaoEnsinoResponseDTO(BaseResponseDTO):
    id: UUID
    razao_social: str
    registro_educacional: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    tipo: Optional[str] = None

