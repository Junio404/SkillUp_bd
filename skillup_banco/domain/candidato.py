from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Candidato:
    id: Optional[int] = None
    nome: str = ""
    cpf: str = ""
    email: str = ""
    senha: str = ""
    nascimento: Optional[date] = None
    telefone: Optional[str] = None
    nome_fantasia: Optional[str] = None
