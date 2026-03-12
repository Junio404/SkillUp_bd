import uuid
from dataclasses import dataclass, field
from uuid import UUID

from domain.enums import Nivel


@dataclass
class CompetenciaCandidato:
    nivel: Nivel
    candidato_id: UUID
    competencia_id: UUID
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def registrar(self) -> None:
        raise NotImplementedError
