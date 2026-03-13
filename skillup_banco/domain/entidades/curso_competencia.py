import uuid
from dataclasses import dataclass, field
from uuid import UUID

from domain.entidades.enums import Nivel


@dataclass
class CursoCompetencia:
    _nivel: Nivel
    _curso_id: UUID
    _competencia_id: UUID
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._curso_id:
            raise ValueError("Curso é obrigatório")

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
    def curso_id(self) -> UUID:
        return self._curso_id

    @property
    def competencia_id(self) -> UUID:
        return self._competencia_id
