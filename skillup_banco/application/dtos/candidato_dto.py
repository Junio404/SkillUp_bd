from __future__ import annotations

from typing import Optional
from uuid import UUID
from collections.abc import Sequence

from pydantic import Field, field_validator

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO
from application.dtos.candidatura_dto import CandidaturaResponseDTO


class CandidatoRequestDTO(BaseRequestDTO):
    nome: str = Field(min_length=2, max_length=150)
    cpf: str = Field(min_length=11, max_length=11, pattern=r"^\d{11}$")
    email: str = Field(min_length=5, max_length=150)
    area_interesse: Optional[str] = Field(default=None, max_length=100)
    nivel_formacao: Optional[str] = Field(default=None, max_length=100)
    curriculo_url: Optional[str] = Field(default=None, max_length=300)

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Nome nao pode ser vazio")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned or "@" not in cleaned:
            raise ValueError("Email invalido")
        local, _, domain = cleaned.partition("@")
        if not local or "." not in domain:
            raise ValueError("Email invalido")
        return cleaned

    @field_validator("area_interesse", "nivel_formacao", "curriculo_url")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


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
