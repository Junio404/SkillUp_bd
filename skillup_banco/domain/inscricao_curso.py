import uuid
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from domain.enums import StatusInscricao


@dataclass
class InscricaoCurso:
    data_inscricao: date
    status: StatusInscricao
    candidato_id: UUID
    curso_id: UUID
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def atualizar_status_inscricao(self) -> None:
        raise NotImplementedError
