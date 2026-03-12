from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.enums import StatusInscricao


@dataclass
class InscricaoCurso:
    data_inscricao: date
    status: StatusInscricao
    candidato_id: int
    curso_id: int
    id: Optional[int] = None
