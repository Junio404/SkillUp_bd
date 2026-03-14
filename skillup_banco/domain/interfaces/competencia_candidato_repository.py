from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from domain.entidades.competencia_candidato import CompetenciaCandidato
from domain.interfaces.base_repository import BaseRepository


class CompetenciaCandidatoRepository(BaseRepository[CompetenciaCandidato], ABC):
    @abstractmethod
    def list_by_candidato(self, candidato_id: UUID) -> Sequence[CompetenciaCandidato]:
        pass
