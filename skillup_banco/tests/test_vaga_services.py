from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.vaga import VagaService
from application.dtos.vaga_dto import VagaRequestDTO
from domain.entidades.vaga import Vaga
from domain.interfaces.vaga_repository import VagaRepository


class FakeVagaRepository(VagaRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, Vaga] = {}

    def add(self, entity: Vaga) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> Vaga | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Vaga]:
        return list(self._items.values())

    def update(self, entity: Vaga) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_empresa(self, empresa_id: UUID) -> list[Vaga]:
        return [item for item in self._items.values() if item.empresa_id == empresa_id]

    def list_ativas(self) -> list[Vaga]:
        return [item for item in self._items.values() if item.ativa]


class TestVagaService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeVagaRepository()
        self.service = VagaService(self.repo)

    def _novo_request(self, **overrides) -> VagaRequestDTO:
        defaults = dict(
            titulo="Desenvolvedor Python Pleno",
            descricao="Vaga para atuar no backend com FastAPI e Clean Architecture.",
            salario=8000.0,
            empresa_id=uuid4(),
            ativa=True,
        )
        defaults.update(overrides)
        return VagaRequestDTO(**defaults)

    def _nova_vaga(self, **overrides) -> Vaga:
        defaults = dict(
            _titulo="Engenheiro de Dados Sênior",
            _descricao="Atuação com AWS, Spark e Airflow.",
            _salario=12000.0,
            _empresa_id=uuid4(),
            _ativa=True,
        )
        defaults.update(overrides)
        entity = Vaga(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_vaga_com_sucesso(self) -> None:
        empresa_alvo = uuid4()
        resultado = self.service.create(self._novo_request(empresa_id=empresa_alvo))

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.titulo, "Desenvolvedor Python Pleno")
        self.assertEqual(resultado.empresa_id, empresa_alvo)
        self.assertTrue(resultado.ativa)

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        vaga = self._nova_vaga()

        resultado = self.service.get_by_id(vaga.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, vaga.id)
        self.assertEqual(resultado.titulo, "Engenheiro de Dados Sênior")

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        self._nova_vaga(_titulo="Vaga 1")
        self._nova_vaga(_titulo="Vaga 2")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_vaga_com_sucesso(self) -> None:
        vaga = self._nova_vaga()

        atualizada = self.service.update(
            vaga.id,
            self._novo_request(
                titulo="Título Atualizado",
                empresa_id=vaga.empresa_id,
                ativa=False # Testando fechamento de vaga
            ),
        )

        self.assertEqual(atualizada.titulo, "Título Atualizado")
        self.assertFalse(atualizada.ativa)

    def test_atualizar_vaga_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_vaga_com_sucesso(self) -> None:
        vaga = self._nova_vaga()

        self.service.delete(vaga.id)

        self.assertFalse(self.repo.exists(vaga.id))

    def test_deletar_vaga_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_listar_vagas_por_empresa(self) -> None:
        empresa_alvo = uuid4()
        self._nova_vaga(_empresa_id=empresa_alvo)
        self._nova_vaga(_empresa_id=empresa_alvo)
        self._nova_vaga(_empresa_id=uuid4()) # Empresa diferente

        resultado = self.service.list_by_empresa(empresa_alvo)

        self.assertEqual(len(resultado), 2)
        for v in resultado:
            self.assertEqual(v.empresa_id, empresa_alvo)

    def test_listar_vagas_ativas(self) -> None:
        self._nova_vaga(_ativa=True)
        self._nova_vaga(_ativa=True)
        self._nova_vaga(_ativa=False) # Vaga fechada

        resultado = self.service.list_ativas()

        self.assertEqual(len(resultado), 2)
        for v in resultado:
            self.assertTrue(v.ativa)


if __name__ == "__main__":
    unittest.main()