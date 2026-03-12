import uuid
from dataclasses import dataclass, field
from uuid import UUID

from domain.enums import Nivel


@dataclass
class RequisitoVaga:
    nivel: Nivel
    vaga_id: UUID
    competencia_id: UUID
    id: UUID = field(default_factory=uuid.uuid4, init=False)
