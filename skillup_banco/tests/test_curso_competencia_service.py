from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.curso_competencia import CursoCompetenciaService
from application.dtos.curso_competencia_dto import CursoCompetenciaRequestDTO
from domain.entidades.curso_competencia import CursoCompetencia
from domain.entidades.enums import Nivel
from domain.interfaces.curso_competencia_repository import CursoCompetenciaRepository


class FakeCursoCompetenciaRepository(CursoCompetenciaRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, CursoCompetencia] = {}

    def add(self, entity: CursoCompetencia) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> CursoCompetencia | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[CursoCompetencia]:
        return list(self._items.values())

    def update(self, entity: CursoCompetencia) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_curso(self, curso_id: UUID) -> list[CursoCompetencia]:
        return [item for item in self._items.values() if item.curso_id == curso_id]


class TestCursoCompetenciaService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCursoCompetenciaRepository()
        self.service = CursoCompetenciaService(self.repo)
        self.curso_id = uuid4()
        self.competencia_id = uuid4()

    def _novo_request(self, **overrides) -> CursoCompetenciaRequestDTO:
        defaults = dict(
            nivel=Nivel.MEDIA,
            curso_id=self.curso_id,
            competencia_id=self.competencia_id,
        )
        defaults.update(overrides)
        return CursoCompetenciaRequestDTO(**defaults)

    def _nova_curso_competencia(self, **overrides) -> CursoCompetencia:
        defaults = dict(
            _nivel=Nivel.ALTA,
            _curso_id=self.curso_id,
            _competencia_id=self.competencia_id,
        )
        defaults.update(overrides)
        entity = CursoCompetencia(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_curso_competencia_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nivel, Nivel.MEDIA.value)
        self.assertEqual(resultado.curso_id, self.curso_id)
        self.assertEqual(resultado.competencia_id, self.competencia_id)

    def test_criar_curso_competencia_duplicada_dispara_erro(self) -> None:
        self._nova_curso_competencia(_competencia_id=self.competencia_id)

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(competencia_id=self.competencia_id))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        competencia = self._nova_curso_competencia()

        resultado = self.service.get_by_id(competencia.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, competencia.id)
        self.assertEqual(resultado.nivel, Nivel.ALTA.value)

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todos(self) -> None:
        self._nova_curso_competencia(_competencia_id=uuid4())
        self._nova_curso_competencia(_competencia_id=uuid4())

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_curso_competencia_com_sucesso(self) -> None:
        competencia = self._nova_curso_competencia()

        atualizado = self.service.update(
            competencia.id,
            self._novo_request(nivel=Nivel.BAIXA),
        )

        self.assertEqual(atualizado.nivel, Nivel.BAIXA.value)

    def test_atualizar_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_com_sucesso(self) -> None:
        competencia = self._nova_curso_competencia()

        self.service.delete(competencia.id)

        self.assertFalse(self.repo.exists(competencia.id))

    def test_deletar_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_listar_por_curso(self) -> None:
        curso_id = uuid4()
        self._nova_curso_competencia(
            _curso_id=curso_id,
            _competencia_id=uuid4(),
        )
        self._nova_curso_competencia(
            _curso_id=curso_id,
            _competencia_id=uuid4(),
        )
        self._nova_curso_competencia(
            _curso_id=uuid4(),
            _competencia_id=uuid4(),
        )

        resultado = self.service.list_by_curso(curso_id)

        self.assertEqual(len(resultado), 2)
        for item in resultado:
            self.assertEqual(item.curso_id, curso_id)


if __name__ == "__main__":
    unittest.main()
