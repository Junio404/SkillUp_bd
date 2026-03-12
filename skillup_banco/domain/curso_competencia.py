from dataclasses import dataclass
from typing import Optional

from domain.enums import Nivel


@dataclass
class CursoCompetencia:
    nivel: Nivel
    curso_id: int
    competencia_id: int
    id: Optional[int] = None
