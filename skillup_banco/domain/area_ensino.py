from dataclasses import dataclass
from typing import Optional


@dataclass
class AreaEnsino:
    nome: str
    descricao: Optional[str] = None
