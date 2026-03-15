from __future__ import annotations

import unittest
from collections.abc import Sequence
from uuid import UUID, uuid4

from application.services.instituicao_area_ensino import InstituicaoAreaEnsinoService
from application.dtos.instituicao_area_ensino_dto import InstituicaoAreaEnsinoRequestDTO
from domain.entidades.instituicao_area_ensino import InstituicaoAreaEnsino
from domain.entidades.instituicao_ensino import InstituicaoEnsino
from domain.entidades.area_ensino import AreaEnsino
from domain.interfaces.instituicao_area_ensino_repository import InstituicaoAreaEnsinoRepository
from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository
from domain.interfaces.area_ensino_repository import AreaEnsinoRepository


# ── Fake Repositories ──────────────────────────────────────


class FakeInstituicaoAreaEnsinoRepository(InstituicaoAreaEnsinoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, InstituicaoAreaEnsino] = {}
        self._counter = 0

    def add(self, entity: InstituicaoAreaEnsino) -> None:
        key = uuid4()
        self._items[key] = entity

    def get_by_id(self, entity_id: UUID) -> InstituicaoAreaEnsino | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[InstituicaoAreaEnsino]:
        return list(self._items.values())

    def update(self, entity: InstituicaoAreaEnsino) -> None:
        for key, item in self._items.items():
            if (
                item.instituicao_ensino_id == entity.instituicao_ensino_id
                and item.area_ensino_id == entity.area_ensino_id
            ):
                self._items[key] = entity
                return

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_instituicao(self, instituicao_id: UUID) -> Sequence[InstituicaoAreaEnsino]:
        return [
            item
            for item in self._items.values()
            if item.instituicao_ensino_id == instituicao_id
        ]

    def get_by_chave(self, instituicao_id: UUID, area_ensino_id: UUID) -> InstituicaoAreaEnsino | None:
        for item in self._items.values():
            if item.instituicao_ensino_id == instituicao_id and item.area_ensino_id == area_ensino_id:
                return item
        return None


class FakeInstituicaoEnsinoRepository(InstituicaoEnsinoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, InstituicaoEnsino] = {}

    def add(self, entity: InstituicaoEnsino) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> InstituicaoEnsino | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[InstituicaoEnsino]:
        return list(self._items.values())

    def update(self, entity: InstituicaoEnsino) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def get_by_registro_educacional(self, registro: str) -> InstituicaoEnsino | None:
        return None

    def get_by_cnpj(self, cnpj: str) -> InstituicaoEnsino | None:
        return None

    def get_with_areas_ensino(self, instituicao_id: UUID) -> InstituicaoEnsino | None:
        return self._items.get(instituicao_id)


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
        return None


# ── Tests ───────────────────────────────────────────────────


class TestInstituicaoAreaEnsinoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeInstituicaoAreaEnsinoRepository()
        self.inst_repo = FakeInstituicaoEnsinoRepository()
        self.area_repo = FakeAreaEnsinoRepository()
        self.service = InstituicaoAreaEnsinoService(
            repository=self.repo,
            instituicao_ensino_repository=self.inst_repo,
            area_ensino_repository=self.area_repo,
        )

    def _criar_instituicao(self) -> InstituicaoEnsino:
        inst = InstituicaoEnsino(
            _razao_social="Universidade Teste",
            _registro_educacional="REG-001",
            _cnpj="12345678901234",
        )
        self.inst_repo.add(inst)
        return inst

    def _criar_area(self, nome: str = "Tecnologia") -> AreaEnsino:
        area = AreaEnsino(_nome=nome)
        self.area_repo.add(area)
        return area

    def _novo_request(self, inst_id: UUID, area_id: UUID) -> InstituicaoAreaEnsinoRequestDTO:
        return InstituicaoAreaEnsinoRequestDTO(
            instituicao_ensino_id=inst_id,
            area_ensino_id=area_id,
        )

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_associacao_com_sucesso(self) -> None:
        inst = self._criar_instituicao()
        area = self._criar_area()

        resultado = self.service.create(self._novo_request(inst.id, area.id))

        self.assertEqual(resultado.instituicao_ensino_id, inst.id)
        self.assertEqual(resultado.area_ensino_id, area.id)

    def test_criar_com_instituicao_inexistente_dispara_erro(self) -> None:
        area = self._criar_area()

        with self.assertRaises(ValueError) as ctx:
            self.service.create(self._novo_request(uuid4(), area.id))

        self.assertIn("Instituicao de ensino nao encontrada", str(ctx.exception))

    def test_criar_com_area_inexistente_dispara_erro(self) -> None:
        inst = self._criar_instituicao()

        with self.assertRaises(ValueError) as ctx:
            self.service.create(self._novo_request(inst.id, uuid4()))

        self.assertIn("Area de ensino nao encontrada", str(ctx.exception))

    def test_criar_associacao_duplicada_dispara_erro(self) -> None:
        inst = self._criar_instituicao()
        area = self._criar_area()
        self.service.create(self._novo_request(inst.id, area.id))

        with self.assertRaises(ValueError) as ctx:
            self.service.create(self._novo_request(inst.id, area.id))

        self.assertIn("ja existe", str(ctx.exception))

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        inst = self._criar_instituicao()
        area1 = self._criar_area("Saude")
        area2 = self._criar_area("Direito")
        self.service.create(self._novo_request(inst.id, area1.id))
        self.service.create(self._novo_request(inst.id, area2.id))

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── LIST BY INSTITUICAO ─────────────────────────────────

    def test_listar_por_instituicao(self) -> None:
        inst1 = self._criar_instituicao()
        inst2 = InstituicaoEnsino(
            _razao_social="Outra Universidade",
            _registro_educacional="REG-002",
            _cnpj="98765432101234",
        )
        self.inst_repo.add(inst2)

        area1 = self._criar_area("Saude")
        area2 = self._criar_area("Direito")

        self.service.create(self._novo_request(inst1.id, area1.id))
        self.service.create(self._novo_request(inst1.id, area2.id))
        self.service.create(self._novo_request(inst2.id, area1.id))

        resultado = self.service.list_by_instituicao(inst1.id)

        self.assertEqual(len(resultado), 2)

    def test_listar_por_instituicao_sem_associacoes(self) -> None:
        resultado = self.service.list_by_instituicao(uuid4())
        self.assertEqual(len(resultado), 0)

    # ── GET BY CHAVE ────────────────────────────────────────

    def test_obter_por_chave(self) -> None:
        inst = self._criar_instituicao()
        area = self._criar_area()
        self.service.create(self._novo_request(inst.id, area.id))

        resultado = self.service.get_by_chave(inst.id, area.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.instituicao_ensino_id, inst.id)
        self.assertEqual(resultado.area_ensino_id, area.id)

    def test_obter_por_chave_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_chave(uuid4(), uuid4())
        self.assertIsNone(resultado)

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())


if __name__ == "__main__":
    unittest.main()
