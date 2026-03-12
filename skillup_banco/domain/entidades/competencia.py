import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class Competencia:
    _nome: str
    _descricao: Optional[str] = None
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._nome:
            raise ValueError("Nome não pode ser vazio")

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
    def descricao(self) -> Optional[str]:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: Optional[str]):
        self._descricao = valor
