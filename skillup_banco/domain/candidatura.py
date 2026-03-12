from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Candidatura:
    id: Optional[int] = None
    data_candidatura: Optional[date] = None
    status: str = ""  # CHECK constraint
    candidato_id: Optional[int] = None
    vaga_id: Optional[int] = None
