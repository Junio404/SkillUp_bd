from __future__ import annotations

from typing import Any
from typing import Sequence
from uuid import UUID

from domain.entidades.empresa import Empresa
from domain.interfaces.empresa_repository import EmpresaRepository
from application.dtos.empresa_dto import EmpresaRequestDTO


class EmpresaService:
    def __init__(self, repository: EmpresaRepository) -> None:
        self._repository = repository

    def create(self, payload: EmpresaRequestDTO) -> Empresa:
        if self._repository.get_by_cnpj(payload.cnpj) is not None:
            raise ValueError("CNPJ ja cadastrado")

        empresa = Empresa(
            _razao_social=payload.razao_social,
            _nome_fantasia=payload.nome_fantasia,
            _cnpj=payload.cnpj,
        )
        self._repository.add(empresa)
        return empresa

    def get_by_id(self, entity_id: UUID) -> Empresa | None:
        return self._repository.get_by_id(entity_id)

    def list_all(self) -> Sequence[Empresa]:
        return self._repository.list_all()

    def update(self, entity_id: UUID, payload: EmpresaRequestDTO) -> Empresa | None:
        empresa = self._repository.get_by_id(entity_id)
        if empresa is None:
            return None

        if payload.cnpj != empresa.cnpj:
            raise ValueError("CNPJ nao pode ser alterado")

        empresa.razao_social = payload.razao_social
        empresa.nome_fantasia = payload.nome_fantasia

        self._repository.update(empresa)
        return empresa

    def delete(self, entity_id: UUID) -> None:
        if not self._repository.exists(entity_id):
            raise ValueError("Empresa nao encontrada")

        self._repository.remove(entity_id)

    def get_by_cnpj(self, cnpj: str) -> Empresa | None:
        return self._repository.get_by_cnpj(cnpj)

    def list_resumo_recrutamento(self) -> Sequence[dict[str, Any]]:
        return self._repository.list_resumo_recrutamento()


