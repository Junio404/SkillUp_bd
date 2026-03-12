from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from domain.entidades.curso import Curso
from domain.interfaces.base_repository import BaseRepository


class CursoRepository(BaseRepository[Curso], ABC):
    @abstractmethod
    def list_by_instituicao(self, instituicao_id: UUID) -> Sequence[Curso]:
        pass

    @abstractmethod
    def list_by_empresa(self, empresa_id: UUID) -> Sequence[Curso]:
        pass
