import uuid
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from domain.entidades.enums import StatusCandidatura


@dataclass
class Candidatura:
    data_candidatura: date
    status: StatusCandidatura
    candidato_id: UUID
    vaga_id: UUID
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def atualizar_status(self) -> None:
        raise NotImplementedError
