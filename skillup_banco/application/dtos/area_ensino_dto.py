from __future__ import annotations

from uuid import UUID

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class AreaEnsinoRequestDTO(BaseRequestDTO):
    nome: str


class AreaEnsinoResponseDTO(BaseResponseDTO):
    id: UUID
    nome: str

