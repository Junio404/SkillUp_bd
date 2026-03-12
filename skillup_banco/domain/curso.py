from dataclasses import dataclass
from typing import Optional

from domain.enums import Modalidade


@dataclass
class Curso:
    nome: str
    instituicao_ensino_id: int
    id: Optional[int] = None
    descricao: Optional[str] = None
    modalidade: Optional[Modalidade] = None
    carga_horaria: Optional[int] = None
    capacidade: Optional[int] = None
