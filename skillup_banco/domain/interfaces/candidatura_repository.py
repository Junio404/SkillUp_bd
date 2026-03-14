from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from collections.abc import Sequence
from uuid import UUID

from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.base_repository import BaseRepository


class CandidaturaRepository(BaseRepository[Candidatura], ABC):
    @abstractmethod
    def list_by_candidato(self, candidato_id: UUID) -> Sequence[Candidatura]:
        pass

    @abstractmethod
    def get_by_candidato_e_vaga(self, candidato_id: UUID, vaga_id: UUID) -> Candidatura | None:
        pass

    @abstractmethod
    def list_by_status_e_data(
        self,
        status: StatusCandidatura,
        data_inicio: datetime,
        data_fim: datetime,
    ) -> Sequence[Candidatura]:
        pass
