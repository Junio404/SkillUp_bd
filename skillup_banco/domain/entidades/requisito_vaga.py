import uuid
from dataclasses import dataclass, field
from uuid import UUID

from domain.enums import Nivel


@dataclass
class RequisitoVaga:
    _nivel: Nivel
    _vaga_id: UUID
    _competencia_id: UUID
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._vaga_id:
            raise ValueError("Vaga é obrigatória")

        if not self._competencia_id:
            raise ValueError("Competência é obrigatória")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nivel(self) -> Nivel:
        return self._nivel

    @nivel.setter
    def nivel(self, valor: Nivel):
        self._nivel = valor

    @property
    def vaga_id(self) -> UUID:
        return self._vaga_id

    @property
    def competencia_id(self) -> UUID:
        return self._competencia_id
