from dataclasses import dataclass
from uuid import UUID


@dataclass
class InstituicaoAreaEnsino:
    _instituicao_ensino_id: UUID
    _area_ensino_id: UUID

    def __post_init__(self):
        if not self._instituicao_ensino_id:
            raise ValueError("Instituição de ensino é obrigatória")

        if not self._area_ensino_id:
            raise ValueError("Área de ensino é obrigatória")

    @property
    def instituicao_ensino_id(self) -> UUID:
        return self._instituicao_ensino_id

    @property
    def area_ensino_id(self) -> UUID:
        return self._area_ensino_id
