from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from domain.entidades.instituicao_area_ensino import InstituicaoAreaEnsino
from domain.interfaces.base_repository import BaseRepository


class InstituicaoAreaEnsinoRepository(BaseRepository[InstituicaoAreaEnsino], ABC):
    @abstractmethod
    def list_by_instituicao(self, instituicao_id: UUID) -> Sequence[InstituicaoAreaEnsino]:
        pass

    @abstractmethod
    def get_by_chave(self, instituicao_id: UUID, area_ensino_id: UUID) -> InstituicaoAreaEnsino | None:
        pass
