from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.competencia import CompetenciaService
from application.dtos.competencia_dto import CompetenciaRequestDTO
from domain.entidades.competencia import Competencia
from domain.interfaces.competencia_repository import CompetenciaRepository


class FakeCompetenciaRepository(CompetenciaRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, Competencia] = {}

    def add(self, entity: Competencia) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> Competencia | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Competencia]:
        return list(self._items.values())

    def update(self, entity: Competencia) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def get_by_nome(self, nome: str) -> Competencia | None:
        for item in self._items.values():
            if item.nome == nome:
                return item
        return None


class TestCompetenciaService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCompetenciaRepository()
        self.service = CompetenciaService(self.repo)

    def _novo_request(self, **overrides) -> CompetenciaRequestDTO:
        defaults = dict(
            nome="Competência Exemplo",
            descricao="Descrição da competência",
        )
        defaults.update(overrides)
        return CompetenciaRequestDTO(**defaults)

    def _nova_competencia(self, **overrides) -> Competencia:
        defaults = dict(
            _nome="Competência Teste",
            _descricao="Descrição de teste",
        )
        defaults.update(overrides)
        entity = Competencia(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_competencia_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nome, "Competência Exemplo")
        self.assertEqual(resultado.descricao, "Descrição da competência")

    def test_criar_competencia_nome_duplicado_dispara_erro(self) -> None:
        self.service.create(self._novo_request())

        with self.assertRaises(ValueError) as context:
            self.service.create(self._novo_request())
        
        self.assertIn("nome", str(context.exception).lower())

    def test_criar_competencia_sem_nome_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(nome=""))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        competencia = self._nova_competencia()

        resultado = self.service.get_by_id(competencia.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, competencia.id)
        self.assertEqual(resultado.nome, "Competência Teste")

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        self._nova_competencia(_nome="Competência 1")
        self._nova_competencia(_nome="Competência 2")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_competencia_com_sucesso(self) -> None:
        competencia = self._nova_competencia()

        atualizada = self.service.update(
            competencia.id,
            self._novo_request(
                nome="Competência Atualizada",
                descricao="Descrição atualizada",
            ),
        )

        self.assertEqual(atualizada.nome, "Competência Atualizada")
        self.assertEqual(atualizada.descricao, "Descrição atualizada")

    def test_atualizar_competencia_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    def test_atualizar_nome_duplicado_dispara_erro(self) -> None:
        self._nova_competencia(_nome="Competência A")
        competencia_b = self._nova_competencia(_nome="Competência B")

        with self.assertRaises(ValueError) as context:
            self.service.update(
                competencia_b.id,
                self._novo_request(nome="Competência A"),
            )
        
        self.assertIn("nome", str(context.exception).lower())

    def test_atualizar_com_mesmo_nome_nao_dispara_erro(self) -> None:
        competencia = self._nova_competencia(_nome="Mesma Competência")

        atualizada = self.service.update(
            competencia.id,
            self._novo_request(nome="Mesma Competência", descricao="Nova descrição"),
        )

        self.assertEqual(atualizada.nome, "Mesma Competência")
        self.assertEqual(atualizada.descricao, "Nova descrição")

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_competencia_com_sucesso(self) -> None:
        competencia = self._nova_competencia()

        self.service.delete(competencia.id)

        self.assertFalse(self.repo.exists(competencia.id))

    def test_deletar_competencia_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_obter_por_nome(self) -> None:
        competencia = self._nova_competencia(_nome="Liderança")

        resultado = self.service.get_by_nome("Liderança")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, competencia.id)

    def test_obter_por_nome_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_nome("Competência Inexistente")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
