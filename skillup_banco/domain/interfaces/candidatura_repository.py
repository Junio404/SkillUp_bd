from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from domain.entidades.candidatura import Candidatura
from domain.interfaces.base_repository import BaseRepository


class CandidaturaRepository(BaseRepository[Candidatura], ABC):
    @abstractmethod
    def list_by_candidato(self, candidato_id: UUID) -> Sequence[Candidatura]:
        pass

    @abstractmethod
    def get_by_candidato_e_vaga(self, candidato_id: UUID, vaga_id: UUID) -> Candidatura | None:
        pass
