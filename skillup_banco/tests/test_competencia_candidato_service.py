from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.competencia_candidato import CompetenciaCandidatoService
from application.dtos.competencia_candidato_dto import CompetenciaCandidatoRequestDTO
from domain.entidades.competencia_candidato import CompetenciaCandidato
from domain.entidades.enums import Nivel
from domain.interfaces.competencia_candidato_repository import CompetenciaCandidatoRepository


class FakeCompetenciaCandidatoRepository(CompetenciaCandidatoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, CompetenciaCandidato] = {}

    def add(self, entity: CompetenciaCandidato) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> CompetenciaCandidato | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[CompetenciaCandidato]:
        return list(self._items.values())

    def update(self, entity: CompetenciaCandidato) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_candidato(self, candidato_id: UUID) -> list[CompetenciaCandidato]:
        return [item for item in self._items.values() if item.candidato_id == candidato_id]


class TestCompetenciaCandidatoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCompetenciaCandidatoRepository()
        self.service = CompetenciaCandidatoService(self.repo)
        self.candidato_id = uuid4()
        self.competencia_id = uuid4()

    def _novo_request(self, **overrides) -> CompetenciaCandidatoRequestDTO:
        defaults = dict(
            nivel=Nivel.MEDIA,
            candidato_id=self.candidato_id,
            competencia_id=self.competencia_id,
        )
        defaults.update(overrides)
        return CompetenciaCandidatoRequestDTO(**defaults)

    def _nova_competencia_candidato(self, **overrides) -> CompetenciaCandidato:
        defaults = dict(
            _nivel=Nivel.ALTA,
            _candidato_id=self.candidato_id,
            _competencia_id=self.competencia_id,
        )
        defaults.update(overrides)
        entity = CompetenciaCandidato(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_competencia_candidato_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nivel, Nivel.MEDIA.value)
        self.assertEqual(resultado.candidato_id, self.candidato_id)
        self.assertEqual(resultado.competencia_id, self.competencia_id)

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        competencia = self._nova_competencia_candidato()

        resultado = self.service.get_by_id(competencia.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, competencia.id)
        self.assertEqual(resultado.nivel, Nivel.ALTA.value)

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todos(self) -> None:
        self._nova_competencia_candidato(_competencia_id=uuid4())
        self._nova_competencia_candidato(_competencia_id=uuid4())

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_competencia_candidato_com_sucesso(self) -> None:
        competencia = self._nova_competencia_candidato()

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
        competencia = self._nova_competencia_candidato()

        self.service.delete(competencia.id)

        self.assertFalse(self.repo.exists(competencia.id))

    def test_deletar_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_listar_por_candidato(self) -> None:
        candidato_id = uuid4()
        self._nova_competencia_candidato(
            _candidato_id=candidato_id,
            _competencia_id=uuid4(),
        )
        self._nova_competencia_candidato(
            _candidato_id=candidato_id,
            _competencia_id=uuid4(),
        )
        self._nova_competencia_candidato(
            _candidato_id=uuid4(),
            _competencia_id=uuid4(),
        )

        resultado = self.service.list_by_candidato(candidato_id)

        self.assertEqual(len(resultado), 2)
        for item in resultado:
            self.assertEqual(item.candidato_id, candidato_id)


if __name__ == "__main__":
    unittest.main()
