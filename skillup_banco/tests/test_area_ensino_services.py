from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.area_ensino import AreaEnsinoService
from application.dtos.area_ensino_dto import AreaEnsinoRequestDTO
from domain.entidades.area_ensino import AreaEnsino
from domain.interfaces.area_ensino_repository import AreaEnsinoRepository


class FakeAreaEnsinoRepository(AreaEnsinoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, AreaEnsino] = {}

    def add(self, entity: AreaEnsino) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> AreaEnsino | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[AreaEnsino]:
        return list(self._items.values())

    def update(self, entity: AreaEnsino) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def get_by_nome(self, nome: str) -> AreaEnsino | None:
        for item in self._items.values():
            if item.nome == nome:
                return item
        return None


class TestAreaEnsinoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeAreaEnsinoRepository()
        self.service = AreaEnsinoService(self.repo)

    def _novo_request(self, **overrides) -> AreaEnsinoRequestDTO:
        defaults = dict(nome="Tecnologia da Informacao")
        defaults.update(overrides)
        return AreaEnsinoRequestDTO(**defaults)

    def _nova_area(self, **overrides) -> AreaEnsino:
        defaults = dict(_nome="Engenharia")
        defaults.update(overrides)
        entity = AreaEnsino(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_area_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nome, "Tecnologia da Informacao")

    def test_criar_area_nome_duplicado_dispara_erro(self) -> None:
        self.service.create(self._novo_request())

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request())

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        area = self._nova_area()

        resultado = self.service.get_by_id(area.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, area.id)
        self.assertEqual(resultado.nome, "Engenharia")

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        self._nova_area(_nome="Saude")
        self._nova_area(_nome="Direito")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_area_com_sucesso(self) -> None:
        area = self._nova_area()

        atualizada = self.service.update(
            area.id,
            self._novo_request(nome="Engenharia Atualizada"),
        )

        self.assertEqual(atualizada.nome, "Engenharia Atualizada")

    def test_atualizar_area_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    def test_atualizar_nome_duplicado_dispara_erro(self) -> None:
        self._nova_area(_nome="Saude")
        area2 = self._nova_area(_nome="Direito")

        with self.assertRaises(ValueError):
            self.service.update(
                area2.id,
                self._novo_request(nome="Saude"),
            )

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_area_com_sucesso(self) -> None:
        area = self._nova_area()

        self.service.delete(area.id)

        self.assertFalse(self.repo.exists(area.id))

    def test_deletar_area_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── GET BY NOME ─────────────────────────────────────────

    def test_obter_por_nome(self) -> None:
        area = self._nova_area(_nome="Ciencias Exatas")

        resultado = self.service.get_by_nome("Ciencias Exatas")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, area.id)

    def test_obter_por_nome_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_nome("Inexistente")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
