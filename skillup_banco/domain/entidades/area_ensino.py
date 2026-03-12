import uuid
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class AreaEnsino:
    nome: str
    id: UUID = field(default_factory=uuid.uuid4, init=False)
