from dataclasses import dataclass
from typing import Optional


@dataclass
class InstituicaoEnsino:
    nome_fantasia: str
    id: Optional[int] = None
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    tipo: Optional[str] = None
    email: Optional[str] = None
