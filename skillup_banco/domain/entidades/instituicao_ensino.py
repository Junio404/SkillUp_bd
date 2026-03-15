from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from domain.entidades.area_ensino import AreaEnsino


@dataclass
class InstituicaoEnsino:
    _razao_social: str
    _registro_educacional: str
    _nome_fantasia: Optional[str] = None
    _cnpj: Optional[str] = None
    _tipo: Optional[str] = None
    _areas_ensino: list[AreaEnsino] = field(default_factory=list)
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._razao_social:
            raise ValueError("Razão social não pode ser vazia")
        
        if not isinstance(self._cnpj, str) or len(self._cnpj) != 14 or not self._cnpj.isdigit():
            raise ValueError("CNPJ inválido.")

        if not self._registro_educacional:
            raise ValueError("Registro educacional não pode ser vazio")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def razao_social(self) -> str:
        return self._razao_social

    @razao_social.setter
    def razao_social(self, valor: str):
        if not valor:
            raise ValueError("Razão social não pode ser vazia")
        self._razao_social = valor

    @property
    def registro_educacional(self) -> str:
        return self._registro_educacional

    @property
    def nome_fantasia(self) -> Optional[str]:
        return self._nome_fantasia

    @nome_fantasia.setter
    def nome_fantasia(self, valor: Optional[str]):
        self._nome_fantasia = valor

    @property
    def cnpj(self) -> Optional[str]:
        return self._cnpj

    @property
    def tipo(self) -> Optional[str]:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: Optional[str]):
        self._tipo = valor

    @property
    def areas_ensino(self) -> Sequence[AreaEnsino]:
        return tuple(self._areas_ensino)

    def definir_areas_ensino(self, areas: list[AreaEnsino]) -> None:
        self._areas_ensino = list(areas)

    def cadastrar_curso(self) -> None:
        raise NotImplementedError
