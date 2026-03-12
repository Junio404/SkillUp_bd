from dataclasses import dataclass
from typing import Optional


@dataclass
class RequisitoVaga:
    obrigatorio: bool
    vaga_id: int
    competencia_id: int
    id: Optional[int] = None
