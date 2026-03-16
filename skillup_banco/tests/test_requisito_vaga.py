from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.requisito_vaga import RequisitoVagaService
from application.dtos.requisito_vaga_dto import RequisitoVagaRequestDTO
from domain.entidades.requisito_vaga import RequisitoVaga
from domain.entidades.enums import Nivel
from domain.interfaces.requisito_vaga_repository import RequisitoVagaRepository


class FakeRequisitoVagaRepository(RequisitoVagaRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, RequisitoVaga] = {}

    def add(self, entity: RequisitoVaga) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> RequisitoVaga | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[RequisitoVaga]:
        return list(self._items.values())

    def update(self, entity: RequisitoVaga) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_vaga(self, vaga_id: UUID) -> list[RequisitoVaga]:
        return [item for item in self._items.values() if item.vaga_id == vaga_id]


class TestRequisitoVagaService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeRequisitoVagaRepository()
        self.service = RequisitoVagaService(self.repo)
        self.vaga_id = uuid4()
        self.competencia_id = uuid4()

    def _novo_request(self, **overrides) -> RequisitoVagaRequestDTO:
        defaults = dict(
            nivel=Nivel.MEDIA,
            vaga_id=self.vaga_id,
            competencia_id=self.competencia_id,
        )
        defaults.update(overrides)
        return RequisitoVagaRequestDTO(**defaults)

    def _novo_requisito_vaga(self, **overrides) -> RequisitoVaga:
        defaults = dict(
            _nivel=Nivel.ALTA,
            _vaga_id=self.vaga_id,
            _competencia_id=self.competencia_id,
        )
        defaults.update(overrides)
        entity = RequisitoVaga(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_requisito_vaga_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nivel, Nivel.MEDIA.value)
        self.assertEqual(resultado.vaga_id, self.vaga_id)
        self.assertEqual(resultado.competencia_id, self.competencia_id)

    def test_criar_requisito_vaga_duplicado_dispara_erro(self) -> None:
        self._novo_requisito_vaga(_competencia_id=self.competencia_id)

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(competencia_id=self.competencia_id))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        requisito = self._novo_requisito_vaga()

        resultado = self.service.get_by_id(requisito.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, requisito.id)
        self.assertEqual(resultado.nivel, Nivel.ALTA.value)

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todos(self) -> None:
        self._novo_requisito_vaga(_competencia_id=uuid4())
        self._novo_requisito_vaga(_competencia_id=uuid4())

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_requisito_vaga_com_sucesso(self) -> None:
        requisito = self._novo_requisito_vaga()

        atualizado = self.service.update(
            requisito.id,
            self._novo_request(nivel=Nivel.BAIXA),
        )

        self.assertEqual(atualizado.nivel, Nivel.BAIXA.value)

    def test_atualizar_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_com_sucesso(self) -> None:
        requisito = self._novo_requisito_vaga()

        self.service.delete(requisito.id)

        self.assertFalse(self.repo.exists(requisito.id))

    def test_deletar_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_listar_por_vaga(self) -> None:
        vaga_id = uuid4()
        self._novo_requisito_vaga(
            _vaga_id=vaga_id,
            _competencia_id=uuid4(),
        )
        self._novo_requisito_vaga(
            _vaga_id=vaga_id,
            _competencia_id=uuid4(),
        )
        self._novo_requisito_vaga(
            _vaga_id=uuid4(),
            _competencia_id=uuid4(),
        )

        resultado = self.service.list_by_vaga(vaga_id)

        self.assertEqual(len(resultado), 2)
        for item in resultado:
            self.assertEqual(item.vaga_id, vaga_id)


if __name__ == "__main__":
    unittest.main()
