import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID

from domain.enums import Modalidade


@dataclass
class Curso:
    nome: str
    modalidade: Modalidade
    instituicao_ensino_id: UUID
    area: Optional[str] = None
    carga_horaria: Optional[int] = None
    capacidade: Optional[int] = None
    prazo_inscricao: Optional[date] = None
    empresa_id: Optional[UUID] = None
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def publicar(self) -> None:
        raise NotImplementedError

    def editar(self) -> None:
        raise NotImplementedError

    def pausar(self) -> None:
        raise NotImplementedError
