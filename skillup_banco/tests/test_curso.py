from __future__ import annotations

import unittest
from datetime import date
from uuid import UUID, uuid4

from application.services.curso import CursoService
from application.dtos.curso_dto import CursoRequestDTO
from domain.entidades.curso import Curso
from domain.entidades.enums import Modalidade
from domain.interfaces.curso_repository import CursoRepository


class FakeCursoRepository(CursoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, Curso] = {}

    def add(self, entity: Curso) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> Curso | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Curso]:
        return list(self._items.values())

    def update(self, entity: Curso) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_instituicao(self, instituicao_id: UUID) -> list[Curso]:
        return [item for item in self._items.values() if item._instituicao_ensino_id == instituicao_id]

    def list_by_empresa(self, empresa_id: UUID) -> list[Curso]:
        return [item for item in self._items.values() if item._empresa_id == empresa_id]


class TestCursoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCursoRepository()
        self.service = CursoService(self.repo)
        self.instituicao_id = uuid4()
        self.empresa_id = uuid4()

    def _novo_request(self, **overrides) -> CursoRequestDTO:
        defaults = dict(
            nome="Curso Exemplo",
            modalidade=Modalidade.PRESENCIAL,
            instituicao_ensino_id=self.instituicao_id,
            area="TI",
            carga_horaria=120,
            capacidade=30,
            prazo_inscricao=date(2024, 12, 31),
            empresa_id=self.empresa_id,
        )
        defaults.update(overrides)
        return CursoRequestDTO(**defaults)

    def _novo_curso(self, **overrides) -> Curso:
        defaults = dict(
            _nome="Curso Teste",
            _modalidade=Modalidade.REMOTO,
            _instituicao_ensino_id=self.instituicao_id,
            _area="Gestão",
            _carga_horaria=80,
            _capacidade=25,
            _prazo_inscricao=date(2024, 6, 30),
            _empresa_id=self.empresa_id,
        )
        defaults.update(overrides)
        entity = Curso(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_curso_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nome, "Curso Exemplo")
        self.assertIn(resultado.modalidade, [Modalidade.PRESENCIAL, Modalidade.PRESENCIAL.value])
        self.assertEqual(resultado.instituicao_ensino_id, self.instituicao_id)
        self.assertEqual(resultado.area, "TI")
        self.assertEqual(resultado.carga_horaria, 120)
        self.assertEqual(resultado.capacidade, 30)

    def test_criar_curso_sem_nome_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(nome=""))

    def test_criar_curso_sem_instituicao_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(instituicao_ensino_id=None))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        curso = self._novo_curso()

        resultado = self.service.get_by_id(curso.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, curso.id)
        self.assertEqual(resultado.nome, "Curso Teste")

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todos(self) -> None:
        self._novo_curso(_nome="Curso 1")
        self._novo_curso(_nome="Curso 2")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_curso_com_sucesso(self) -> None:
        curso = self._novo_curso()

        atualizado = self.service.update(
            curso.id,
            self._novo_request(
                nome="Curso Atualizado",
                area="Administração",
            ),
        )

        self.assertEqual(atualizado.nome, "Curso Atualizado")
        self.assertEqual(atualizado.area, "Administração")

    def test_atualizar_curso_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_curso_com_sucesso(self) -> None:
        curso = self._novo_curso()

        self.service.delete(curso.id)

        self.assertFalse(self.repo.exists(curso.id))

    def test_deletar_curso_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_listar_por_instituicao(self) -> None:
        instituicao_a = uuid4()
        instituicao_b = uuid4()
        
        self._novo_curso(_nome="Curso A", _instituicao_ensino_id=instituicao_a)
        self._novo_curso(_nome="Curso B", _instituicao_ensino_id=instituicao_a)
        self._novo_curso(_nome="Curso C", _instituicao_ensino_id=instituicao_b)

        resultado = self.service.list_by_instituicao(instituicao_a)

        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(c.instituicao_ensino_id == instituicao_a for c in resultado))

    def test_listar_por_instituicao_inexistente_retorna_lista_vazia(self) -> None:
        resultado = self.service.list_by_instituicao(uuid4())
        self.assertEqual(len(resultado), 0)

    def test_listar_por_empresa(self) -> None:
        empresa_a = uuid4()
        empresa_b = uuid4()
        
        self._novo_curso(_nome="Curso A", _empresa_id=empresa_a)
        self._novo_curso(_nome="Curso B", _empresa_id=empresa_a)
        self._novo_curso(_nome="Curso C", _empresa_id=empresa_b)

        resultado = self.service.list_by_empresa(empresa_a)

        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(c._empresa_id == empresa_a for c in [self.repo.get_by_id(c.id) for c in resultado]))

    def test_listar_por_empresa_inexistente_retorna_lista_vazia(self) -> None:
        resultado = self.service.list_by_empresa(uuid4())
        self.assertEqual(len(resultado), 0)


if __name__ == "__main__":
    unittest.main()
