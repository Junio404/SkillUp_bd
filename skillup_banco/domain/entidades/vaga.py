import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID

from domain.enums import Modalidade, TipoVaga


@dataclass
class Vaga:
    titulo: str
    modalidade: Modalidade
    tipo: TipoVaga
    prazo_inscricao: date
    empresa_id: UUID
    descricao: Optional[str] = None
    localidade: Optional[str] = None
    jornada: Optional[str] = None
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def publicar(self) -> None:
        raise NotImplementedError

    def pausar(self) -> None:
        raise NotImplementedError

    def editar(self) -> None:
        raise NotImplementedError
