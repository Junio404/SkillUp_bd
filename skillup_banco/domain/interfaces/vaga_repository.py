from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from domain.entidades.vaga import Vaga
from domain.interfaces.base_repository import BaseRepository


class VagaRepository(BaseRepository[Vaga], ABC):
    @abstractmethod
    def list_by_empresa(self, empresa_id: UUID) -> Sequence[Vaga]:
        pass
