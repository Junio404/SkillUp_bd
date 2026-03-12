from dataclasses import dataclass
from typing import Optional

from domain.enums import Modalidade, TipoVaga


@dataclass
class Vaga:
    titulo: str
    descricao: str
    empresa_id: int
    id: Optional[int] = None
    localidade: Optional[str] = None
    modalidade: Optional[Modalidade] = None
    tipo: Optional[TipoVaga] = None
    jornada: Optional[str] = None
