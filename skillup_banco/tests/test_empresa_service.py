from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.empresa import EmpresaService
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

    def get_by_email(self, email: str) -> Empresa | None:
        for item in self._items.values():
            if item.email == email:
                return item
        return None


class TestEmpresaService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeEmpresaRepository()
        self.service = EmpresaService(self.repo)

    def _novo_request(self, **overrides) -> EmpresaRequestDTO:
        defaults = dict(
            razao_social="Empresa Exemplo LTDA",
            nome_fantasia="Exemplo Tech",
            cnpj="12345678000199",
            email="contato@exemplo.com.br",
        )
        defaults.update(overrides)
        return EmpresaRequestDTO(**defaults)

    def _nova_empresa(self, **overrides) -> Empresa:
        defaults = dict(
            _razao_social="Empresa Teste S.A",
            _nome_fantasia="Teste Corp",
            _cnpj="98765432000188",
            _email="admin@testecorp.com",
        )
        defaults.update(overrides)
        entity = Empresa(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_empresa_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.razao_social, "Empresa Exemplo LTDA")
        self.assertEqual(resultado.cnpj, "12345678000199")
        self.assertEqual(resultado.email, "contato@exemplo.com.br")

    def test_criar_empresa_cnpj_duplicado_dispara_erro(self) -> None:
        self._nova_empresa(_cnpj="12345678000199")

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(cnpj="12345678000199"))

    def test_criar_empresa_email_duplicado_dispara_erro(self) -> None:
        self._nova_empresa(_email="contato@exemplo.com.br")

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(email="contato@exemplo.com.br"))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        empresa = self._nova_empresa()

        resultado = self.service.get_by_id(empresa.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, empresa.id)
        self.assertEqual(resultado.razao_social, "Empresa Teste S.A")

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        self._nova_empresa(_cnpj="11111111000111", _email="um@teste.com")
        self._nova_empresa(_cnpj="22222222000122", _email="dois@teste.com")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_empresa_com_sucesso(self) -> None:
        empresa = self._nova_empresa()

        atualizada = self.service.update(
            empresa.id,
            self._novo_request(
                razao_social="Empresa Teste Atualizada",
                cnpj=empresa.cnpj,
                email=empresa.email
            ),
        )

        self.assertEqual(atualizada.razao_social, "Empresa Teste Atualizada")

    def test_atualizar_empresa_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    def test_atualizar_cnpj_duplicado_dispara_erro(self) -> None:
        self._nova_empresa(_cnpj="11111111000111", _email="um@teste.com")
        empresa2 = self._nova_empresa(_cnpj="22222222000122", _email="dois@teste.com")

        with self.assertRaises(ValueError):
            self.service.update(
                empresa2.id,
                self._novo_request(cnpj="11111111000111", email="dois@teste.com"),
            )

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_empresa_com_sucesso(self) -> None:
        empresa = self._nova_empresa()

        self.service.delete(empresa.id)

        self.assertFalse(self.repo.exists(empresa.id))

    def test_deletar_empresa_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_obter_por_cnpj(self) -> None:
        empresa = self._nova_empresa(_cnpj="55555555000155")

        resultado = self.service.get_by_cnpj("55555555000155")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, empresa.id)

    def test_obter_por_cnpj_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_cnpj("00000000000000")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()