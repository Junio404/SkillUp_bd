from dataclasses import dataclass
from typing import Optional


@dataclass
class Competencia:
    id: Optional[int] = None
    nome: str = ""
    descricao: Optional[str] = None
