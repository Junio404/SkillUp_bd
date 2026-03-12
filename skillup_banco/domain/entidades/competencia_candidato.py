import uuid
from dataclasses import dataclass, field
from uuid import UUID

from domain.entidades.enums import Nivel


@dataclass
class CompetenciaCandidato:
    _nivel: Nivel
    _candidato_id: UUID
    _competencia_id: UUID
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._candidato_id:
            raise ValueError("Candidato é obrigatório")

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
    def candidato_id(self) -> UUID:
        return self._candidato_id

    @property
    def competencia_id(self) -> UUID:
        return self._competencia_id
