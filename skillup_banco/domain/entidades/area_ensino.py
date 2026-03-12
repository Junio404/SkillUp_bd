import uuid
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class AreaEnsino:
    _nome: str
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
