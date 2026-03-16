from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from pydantic import Field, field_validator

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO
from application.dtos.curso_dto import CursoResponseDTO
from application.dtos.vaga_dto import VagaResponseDTO


class EmpresaRequestDTO(BaseRequestDTO):
    razao_social: str = Field(min_length=2, max_length=200)
    nome_fantasia: str = Field(min_length=2, max_length=150)
    cnpj: str = Field(min_length=14, max_length=14, pattern=r"^\d{14}$")

    @field_validator("razao_social", "nome_fantasia")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Campo nao pode ser vazio")
        return cleaned


class EmpresaResponseDTO(BaseResponseDTO):
    id: UUID
    razao_social: str
    nome_fantasia: str
    cnpj: str


class EmpresaComVagasResponseDTO(BaseResponseDTO):
    id: UUID
    razao_social: str
    nome_fantasia: str
    cnpj: str
    vagas: Sequence[VagaResponseDTO]


class EmpresaComCursosResponseDTO(BaseResponseDTO):
    id: UUID
    razao_social: str
    nome_fantasia: str
    cnpj: str
    cursos: Sequence[CursoResponseDTO]


