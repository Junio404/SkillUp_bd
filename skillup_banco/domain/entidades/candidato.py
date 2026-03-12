import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class Candidato:
    _nome: str
    _cpf: str
    _email: str
    _area_interesse: Optional[str] = None
    _nivel_formacao: Optional[str] = None
    _curriculo_url: Optional[str] = None
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._nome:
            raise ValueError("Nome não pode ser vazio")

        if not self._cpf:
            raise ValueError("CPF inválido")

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
