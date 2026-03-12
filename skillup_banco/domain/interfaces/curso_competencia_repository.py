from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from domain.entidades.curso_competencia import CursoCompetencia
from domain.interfaces.base_repository import BaseRepository


class CursoCompetenciaRepository(BaseRepository[CursoCompetencia], ABC):
    @abstractmethod
    def list_by_curso(self, curso_id: UUID) -> Sequence[CursoCompetencia]:
        pass
