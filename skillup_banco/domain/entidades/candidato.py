from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID
from collections.abc import Sequence

from domain.entidades.candidatura import Candidatura


@dataclass
class Candidato:
    _nome: str
    _cpf: str
    _email: str
    _senha_hash: str | None = None
    _area_interesse: Optional[str] = None
    _nivel_formacao: Optional[str] = None
    _curriculo_url: Optional[str] = None
    _candidaturas: list[Candidatura] = field(default_factory=list)
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._nome:
            raise ValueError("Nome não pode ser vazio")

        if len(self._cpf) != 11:
            raise ValueError("CPF deve conter 11 dígitos")

        if not self._email:
            raise ValueError("Email não pode ser vazio")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not valor:
            raise ValueError("Nome não pode ser vazio")
        self._nome = valor

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not valor:
            raise ValueError("Email não pode ser vazio")
        self._email = valor

    @property
    def senha_hash(self) -> str | None:
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, valor: str | None):
        self._senha_hash = valor

    @property
    def area_interesse(self) -> Optional[str]:
        return self._area_interesse

    @area_interesse.setter
    def area_interesse(self, valor: Optional[str]):
        self._area_interesse = valor

    @property
    def nivel_formacao(self) -> Optional[str]:
        return self._nivel_formacao

    @nivel_formacao.setter
    def nivel_formacao(self, valor: Optional[str]):
        self._nivel_formacao = valor

    @property
    def curriculo_url(self) -> Optional[str]:
        return self._curriculo_url

    @curriculo_url.setter
    def curriculo_url(self, valor: Optional[str]):
        self._curriculo_url = valor

    @property
    def candidaturas(self) -> Sequence[Candidatura]:
        return tuple(self._candidaturas)

    def definir_candidaturas(self, candidaturas: list[Candidatura]) -> None:
        self._candidaturas = list(candidaturas)

    def adicionar_candidatura(self, candidatura: Candidatura) -> None:
        self._candidaturas.append(candidatura)
