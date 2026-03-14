from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from domain.entidades.requisito_vaga import RequisitoVaga
from domain.interfaces.base_repository import BaseRepository


class RequisitoVagaRepository(BaseRepository[RequisitoVaga], ABC):
    @abstractmethod
    def list_by_vaga(self, vaga_id: UUID) -> Sequence[RequisitoVaga]:
        pass
