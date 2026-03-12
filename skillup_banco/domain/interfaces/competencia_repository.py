from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entidades.competencia import Competencia
from domain.interfaces.base_repository import BaseRepository


class CompetenciaRepository(BaseRepository[Competencia], ABC):
    @abstractmethod
    def get_by_nome(self, nome: str) -> Competencia | None:
        pass
