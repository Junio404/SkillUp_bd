from __future__ import annotations

import unittest
from datetime import date
from uuid import UUID, uuid4

from application.services.candidato import CandidatoService
from application.dtos.candidato_dto import CandidatoRequestDTO
from domain.entidades.candidato import Candidato
from domain.interfaces.candidato_repository import CandidatoRepository


class FakeCandidatoRepository(CandidatoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, Candidato] = {}

    def add(self, entity: Candidato) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> Candidato | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Candidato]:
        return list(self._items.values())

    def update(self, entity: Candidato) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def get_by_cpf(self, cpf: str) -> Candidato | None:
        for item in self._items.values():
            if item.cpf == cpf:
                return item
        return None

    def get_by_email(self, email: str) -> Candidato | None:
        for item in self._items.values():
            if item.email == email:
                return item
        return None


class TestCandidatoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCandidatoRepository()
        self.service = CandidatoService(self.repo)

    def _novo_request(self, **overrides) -> CandidatoRequestDTO:
        defaults = dict(
            nome="Candidato Exemplo",
            cpf="12345678901",
            email="candidato@exemplo.com",
            data_nascimento=date(1995, 5, 20),
        )
        defaults.update(overrides)
        return CandidatoRequestDTO(**defaults)

    def _novo_candidato(self, **overrides) -> Candidato:
        defaults = dict(
            _nome="Candidato Teste",
            _cpf="98765432100",
            _email="teste@exemplo.com",
            _data_nascimento=date(1990, 1, 1),
        )
        defaults.update(overrides)
        entity = Candidato(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_candidato_com_sucesso(self) -> None:
        resultado = self.service.create(self._novo_request())

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.nome, "Candidato Exemplo")
        self.assertEqual(resultado.cpf, "12345678901")
        self.assertEqual(resultado.email, "candidato@exemplo.com")

    def test_criar_candidato_cpf_duplicado_dispara_erro(self) -> None:
        self._novo_candidato(_cpf="12345678901")

        with self.assertRaises(ValueError) as context:
            self.service.create(self._novo_request(cpf="12345678901"))
        
        # Opcional: validar a mensagem de erro exata se você tiver mensagens padronizadas
        # self.assertIn("CPF", str(context.exception))

    def test_criar_candidato_email_duplicado_dispara_erro(self) -> None:
        self._novo_candidato(_email="candidato@exemplo.com")

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(email="candidato@exemplo.com"))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        candidato = self._novo_candidato()

        resultado = self.service.get_by_id(candidato.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, candidato.id)
        self.assertEqual(resultado.nome, "Candidato Teste")

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todos(self) -> None:
        self._novo_candidato(_cpf="11111111111", _email="um@exemplo.com")
        self._novo_candidato(_cpf="22222222222", _email="dois@exemplo.com")

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_candidato_com_sucesso(self) -> None:
        candidato = self._novo_candidato()

        atualizado = self.service.update(
            candidato.id,
            self._novo_request(
                nome="Nome Atualizado",
                cpf=candidato.cpf,
                email=candidato.email
            ),
        )

        self.assertEqual(atualizado.nome, "Nome Atualizado")

    def test_atualizar_candidato_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    def test_atualizar_cpf_duplicado_dispara_erro(self) -> None:
        self._novo_candidato(_cpf="11111111111", _email="um@teste.com")
        candidato2 = self._novo_candidato(_cpf="22222222222", _email="dois@teste.com")

        with self.assertRaises(ValueError):
            self.service.update(
                candidato2.id,
                self._novo_request(cpf="11111111111", email="dois@teste.com"),
            )

    def test_atualizar_email_duplicado_dispara_erro(self) -> None:
        self._novo_candidato(_cpf="11111111111", _email="um@teste.com")
        candidato2 = self._novo_candidato(_cpf="22222222222", _email="dois@teste.com")

        with self.assertRaises(ValueError):
            self.service.update(
                candidato2.id,
                self._novo_request(cpf="22222222222", email="um@teste.com"),
            )

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_candidato_com_sucesso(self) -> None:
        candidato = self._novo_candidato()

        self.service.delete(candidato.id)

        self.assertFalse(self.repo.exists(candidato.id))

    def test_deletar_candidato_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_obter_por_cpf(self) -> None:
        candidato = self._novo_candidato(_cpf="12345678900")

        resultado = self.service.get_by_cpf("12345678900")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, candidato.id)

    def test_obter_por_cpf_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_cpf("00000000000")
        self.assertIsNone(resultado)

    def test_obter_por_email(self) -> None:
        candidato = self._novo_candidato(_email="busca@exemplo.com")

        resultado = self.service.get_by_email("busca@exemplo.com")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, candidato.id)

    def test_obter_por_email_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_email("inexistente@exemplo.com")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()