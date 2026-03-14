from __future__ import annotations

from uuid import UUID

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class EmpresaRequestDTO(BaseRequestDTO):
    razao_social: str
    nome_fantasia: str
    cnpj: str


class EmpresaResponseDTO(BaseResponseDTO):
    id: UUID
    razao_social: str
    nome_fantasia: str
    cnpj: str


