from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entidades.instituicao_ensino import InstituicaoEnsino
from domain.interfaces.base_repository import BaseRepository


class InstituicaoEnsinoRepository(BaseRepository[InstituicaoEnsino], ABC):
    @abstractmethod
    def get_by_registro_educacional(self, registro: str) -> InstituicaoEnsino | None:
        pass

    @abstractmethod
    def get_by_cnpj(self, cnpj: str) -> InstituicaoEnsino | None:
        pass

    @abstractmethod
    def get_with_areas_ensino(self, instituicao_id: UUID) -> InstituicaoEnsino | None:
        pass
