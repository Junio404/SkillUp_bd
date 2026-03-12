from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entidades.area_ensino import AreaEnsino
from domain.interfaces.base_repository import BaseRepository


class AreaEnsinoRepository(BaseRepository[AreaEnsino], ABC):
    @abstractmethod
    def get_by_nome(self, nome: str) -> AreaEnsino | None:
        pass
