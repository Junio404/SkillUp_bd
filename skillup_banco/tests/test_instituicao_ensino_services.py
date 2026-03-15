from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from application.services.instituicao_ensino import InstituicaoEnsinoService
from application.dtos.instituicao_ensino_dto import InstituicaoEnsinoRequestDTO
from domain.entidades.area_ensino import AreaEnsino
from domain.entidades.instituicao_ensino import InstituicaoEnsino
from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository


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
        for item in self._items.values():
            if item.registro_educacional == registro:
                return item
        return None

    def get_by_cnpj(self, cnpj: str) -> InstituicaoEnsino | None:
        for item in self._items.values():
            if item.cnpj == cnpj:
                return item
        return None

    def get_with_areas_ensino(self, instituicao_id: UUID) -> InstituicaoEnsino | None:
        return self._items.get(instituicao_id)


class TestInstituicaoEnsinoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeInstituicaoEnsinoRepository()
        self.service = InstituicaoEnsinoService(self.repo)

    def _novo_request(self, **overrides) -> InstituicaoEnsinoRequestDTO:
        defaults = dict(
            razao_social="Universidade Exemplo",
            registro_educacional="REG-001",
            nome_fantasia="UniExemplo",
            cnpj="12345678901234",
            tipo="Universidade",
        )
        defaults.update(overrides)
        return InstituicaoEnsinoRequestDTO(**defaults)

    def _nova_instituicao(self, **overrides) -> InstituicaoEnsino:
        defaults = dict(
            _razao_social="Universidade Teste",
            _registro_educacional="REG-TESTE",
            _nome_fantasia="UniTeste",
            _cnpj="98765432101234",
            _tipo="Faculdade",
        )
        defaults.update(overrides)
        entity = InstituicaoEnsino(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_instituicao_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.razao_social, "Universidade Exemplo")
        self.assertEqual(resultado.registro_educacional, "REG-001")
        self.assertEqual(resultado.cnpj, "12345678901234")

    def test_criar_instituicao_registro_duplicado_dispara_erro(self) -> None:
        self.service.create(self._novo_request())

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(cnpj="11111111111111"))

    def test_criar_instituicao_cnpj_duplicado_dispara_erro(self) -> None:
        self.service.create(self._novo_request())

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(registro_educacional="REG-OUTRO"))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        instituicao = self._nova_instituicao()

        resultado = self.service.get_by_id(instituicao.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, instituicao.id)

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        self._nova_instituicao(_registro_educacional="REG-1", _cnpj="11111111111111")
        self._nova_instituicao(_registro_educacional="REG-2", _cnpj="22222222222222")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_instituicao_com_sucesso(self) -> None:
        instituicao = self._nova_instituicao()

        atualizada = self.service.update(
            instituicao.id,
            self._novo_request(
                razao_social="Universidade Atualizada",
                registro_educacional=instituicao.registro_educacional,
                cnpj=instituicao.cnpj,
            ),
        )

        self.assertEqual(atualizada.razao_social, "Universidade Atualizada")

    def test_atualizar_instituicao_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    def test_atualizar_registro_duplicado_dispara_erro(self) -> None:
        self._nova_instituicao(_registro_educacional="REG-1", _cnpj="11111111111111")
        inst2 = self._nova_instituicao(_registro_educacional="REG-2", _cnpj="22222222222222")

        with self.assertRaises(ValueError):
            self.service.update(
                inst2.id,
                self._novo_request(registro_educacional="REG-1", cnpj="22222222222222"),
            )

    def test_atualizar_cnpj_duplicado_dispara_erro(self) -> None:
        self._nova_instituicao(_registro_educacional="REG-1", _cnpj="11111111111111")
        inst2 = self._nova_instituicao(_registro_educacional="REG-2", _cnpj="22222222222222")

        with self.assertRaises(ValueError):
            self.service.update(
                inst2.id,
                self._novo_request(registro_educacional="REG-2", cnpj="11111111111111"),
            )

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_instituicao_com_sucesso(self) -> None:
        instituicao = self._nova_instituicao()

        self.service.delete(instituicao.id)

        self.assertFalse(self.repo.exists(instituicao.id))

    def test_deletar_instituicao_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── GET BY REGISTRO EDUCACIONAL ─────────────────────────

    def test_obter_por_registro_educacional(self) -> None:
        instituicao = self._nova_instituicao(_registro_educacional="REG-UNICO")

        resultado = self.service.get_by_registro_educacional("REG-UNICO")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, instituicao.id)

    def test_obter_por_registro_educacional_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_registro_educacional("INEXISTENTE")
        self.assertIsNone(resultado)

    # ── GET BY CNPJ ─────────────────────────────────────────

    def test_obter_por_cnpj(self) -> None:
        instituicao = self._nova_instituicao(_cnpj="55555555555555")

        resultado = self.service.get_by_cnpj("55555555555555")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, instituicao.id)

    def test_obter_por_cnpj_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_cnpj("00000000000000")
        self.assertIsNone(resultado)

    # ── GET WITH AREAS ENSINO ───────────────────────────────

    def test_obter_com_areas_ensino(self) -> None:
        instituicao = self._nova_instituicao()

        area1 = AreaEnsino(_nome="Engenharia")
        area2 = AreaEnsino(_nome="Medicina")
        instituicao.definir_areas_ensino([area1, area2])

        resultado = self.service.get_with_areas_ensino(instituicao.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, instituicao.id)
        self.assertEqual(len(resultado.areas_ensino), 2)
        nomes = [a.nome for a in resultado.areas_ensino]
        self.assertIn("Engenharia", nomes)
        self.assertIn("Medicina", nomes)

    def test_obter_com_areas_ensino_sem_areas(self) -> None:
        instituicao = self._nova_instituicao()

        resultado = self.service.get_with_areas_ensino(instituicao.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, instituicao.id)
        self.assertEqual(len(resultado.areas_ensino), 0)

    def test_obter_com_areas_ensino_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_with_areas_ensino(uuid4())
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
