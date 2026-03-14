from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence
from uuid import UUID

from domain.entidades.candidato import Candidato
from domain.interfaces.base_repository import BaseRepository


class CandidatoRepository(BaseRepository[Candidato], ABC):
    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Candidato | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Candidato | None:
        pass

    @abstractmethod
    def list_resumo_candidaturas(self) -> Sequence[dict[str, Any]]:
        pass

    @abstractmethod
    def get_historico_candidaturas(self, candidato_id: UUID) -> Sequence[dict[str, Any]]:
        pass

    @abstractmethod
    def get_with_candidaturas(self, candidato_id: UUID) -> Candidato | None:
        pass
