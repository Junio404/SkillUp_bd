from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.empresa.empresa_service import EmpresaService
from application.dtos.empresa_dto import EmpresaRequestDTO
from domain.entidades.empresa import Empresa
from domain.interfaces.empresa_repository import EmpresaRepository


class FakeEmpresaRepository(EmpresaRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, Empresa] = {}

    def add(self, entity: Empresa) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> Empresa | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Empresa]:
        return list(self._items.values())

    def update(self, entity: Empresa) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def get_by_cnpj(self, cnpj: str) -> Empresa | None:
        for item in self._items.values():
            if item.cnpj == cnpj:
                return item
        return None

    def list_resumo_recrutamento(self) -> list[dict]:
        return [
            {
                "empresa_id": str(item.id),
                "empresa_nome_fantasia": item.nome_fantasia,
                "total_vagas": 0,
                "total_candidaturas": 0,
                "total_aceitos": 0,
            }
            for item in self._items.values()
        ]


class TestEmpresaService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeEmpresaRepository()
        self.service = EmpresaService(self.repo)

    def test_create_com_sucesso(self) -> None:
        empresa = self.service.create(
            EmpresaRequestDTO(
                razao_social="Tech LTDA",
                nome_fantasia="Tech",
                cnpj="12345678000199",
            )
        )

        self.assertTrue(self.repo.exists(empresa.id))
        self.assertEqual(empresa.cnpj, "12345678000199")

    def test_create_com_cnpj_duplicado_dispara_erro(self) -> None:
        self.service.create(
            EmpresaRequestDTO(
                razao_social="Alpha",
                nome_fantasia="Alpha",
                cnpj="00000000000001",
            )
        )

        with self.assertRaises(ValueError):
            self.service.create(
                EmpresaRequestDTO(
                    razao_social="Beta",
                    nome_fantasia="Beta",
                    cnpj="00000000000001",
                )
            )

    def test_update_nao_permite_alterar_cnpj(self) -> None:
        empresa = self.service.create(
            EmpresaRequestDTO(
                razao_social="Gamma",
                nome_fantasia="Gamma",
                cnpj="98765432000100",
            )
        )

        with self.assertRaises(ValueError):
            self.service.update(
                entity_id=empresa.id,
                payload=EmpresaRequestDTO(
                    razao_social="Gamma Nova",
                    nome_fantasia="Gamma Nova",
                    cnpj="11111111000111",
                ),
            )

    def test_delete_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    def test_list_resumo_recrutamento_retorna_dados(self) -> None:
        self.service.create(
            EmpresaRequestDTO(
                razao_social="Delta LTDA",
                nome_fantasia="Delta",
                cnpj="11222333000144",
            )
        )

        resumo = self.service.list_resumo_recrutamento()

        self.assertGreaterEqual(len(resumo), 1)
        self.assertIn("empresa_nome_fantasia", resumo[0])


if __name__ == "__main__":
    unittest.main()
