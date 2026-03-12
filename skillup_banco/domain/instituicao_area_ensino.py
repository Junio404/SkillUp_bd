import uuid
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class InstituicaoAreaEnsino:
    instituicao_ensino_id: UUID
    area_ensino_id: UUID
