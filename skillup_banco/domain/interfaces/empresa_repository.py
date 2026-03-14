from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from domain.entidades.empresa import Empresa
from domain.interfaces.base_repository import BaseRepository


class EmpresaRepository(BaseRepository[Empresa], ABC):
    @abstractmethod
    def get_by_cnpj(self, cnpj: str) -> Empresa | None:
        pass

    @abstractmethod
    def list_resumo_recrutamento(self) -> Sequence[dict[str, Any]]:
        pass
