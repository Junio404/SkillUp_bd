import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class Competencia:
    nome: str
    descricao: Optional[str] = None
    id: UUID = field(default_factory=uuid.uuid4, init=False)
