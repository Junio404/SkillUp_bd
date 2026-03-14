from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from domain.entidades.inscricao_curso import InscricaoCurso
from domain.interfaces.base_repository import BaseRepository


class InscricaoCursoRepository(BaseRepository[InscricaoCurso], ABC):
    @abstractmethod
    def list_by_candidato(self, candidato_id: UUID) -> Sequence[InscricaoCurso]:
        pass

    @abstractmethod
    def get_by_candidato_e_curso(self, candidato_id: UUID, curso_id: UUID) -> InscricaoCurso | None:
        pass
