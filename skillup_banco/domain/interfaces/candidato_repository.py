from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entidades.candidato import Candidato
from domain.interfaces.base_repository import BaseRepository


class CandidatoRepository(BaseRepository[Candidato], ABC):
    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Candidato | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Candidato | None:
        pass
