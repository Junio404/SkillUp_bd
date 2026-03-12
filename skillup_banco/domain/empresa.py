from dataclasses import dataclass
from typing import Optional


@dataclass
class Empresa:
    cnpj: str
    nome_fantasia: str
    razao_social: str
    email: str
    porte: str
    id: Optional[int] = None