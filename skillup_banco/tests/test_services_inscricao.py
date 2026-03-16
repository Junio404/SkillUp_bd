from __future__ import annotations

import unittest
from datetime import datetime
from uuid import UUID, uuid4

from application.services.inscricao_curso import InscricaoCursoService
from application.dtos.inscricao_curso_dto import InscricaoCursoRequestDTO
from domain.entidades.inscricao_curso import InscricaoCurso
from domain.interfaces.inscricao_curso_repository import InscricaoCursoRepository


class FakeInscricaoCursoRepository(InscricaoCursoRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, InscricaoCurso] = {}

    def add(self, entity: InscricaoCurso) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> InscricaoCurso | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[InscricaoCurso]:
        return list(self._items.values())

    def update(self, entity: InscricaoCurso) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def get_by_aluno_e_curso(self, aluno_id: UUID, curso_id: UUID) -> InscricaoCurso | None:
        for item in self._items.values():
            if item.aluno_id == aluno_id and item.curso_id == curso_id:
                return item
        return None

    def list_by_aluno(self, aluno_id: UUID) -> list[InscricaoCurso]:
        return [item for item in self._items.values() if item.aluno_id == aluno_id]

    def list_by_curso(self, curso_id: UUID) -> list[InscricaoCurso]:
        return [item for item in self._items.values() if item.curso_id == curso_id]


class TestInscricaoCursoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeInscricaoCursoRepository()
        self.service = InscricaoCursoService(self.repo)

    def _novo_request(self, **overrides) -> InscricaoCursoRequestDTO:
        defaults = dict(
            aluno_id=uuid4(),
            curso_id=uuid4(),
            data_inscricao=datetime.now(),
            status="ATIVA",
        )
        defaults.update(overrides)
        return InscricaoCursoRequestDTO(**defaults)

    def _nova_inscricao(self, **overrides) -> InscricaoCurso:
        defaults = dict(
            _aluno_id=uuid4(),
            _curso_id=uuid4(),
            _data_inscricao=datetime.now(),
            _status="ATIVA",
        )
        defaults.update(overrides)
        entity = InscricaoCurso(**defaults)
        self.repo.add(entity)
        return entity

    # ── CREATE ──────────────────────────────────────────────

    def test_criar_inscricao_com_sucesso(self) -> None:
        aluno_alvo = uuid4()
        curso_alvo = uuid4()
        resultado = self.service.create(self._novo_request(aluno_id=aluno_alvo, curso_id=curso_alvo))

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.aluno_id, aluno_alvo)
        self.assertEqual(resultado.curso_id, curso_alvo)
        self.assertEqual(resultado.status, "ATIVA")

    def test_criar_inscricao_duplicada_dispara_erro(self) -> None:
        aluno_alvo = uuid4()
        curso_alvo = uuid4()
        
        # Cria a primeira inscrição com sucesso
        self._nova_inscricao(_aluno_id=aluno_alvo, _curso_id=curso_alvo)

        # Tenta criar a segunda inscrição para o mesmo aluno e curso
        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(aluno_id=aluno_alvo, curso_id=curso_alvo))

    # ── GET BY ID ───────────────────────────────────────────

    def test_obter_por_id_existente(self) -> None:
        inscricao = self._nova_inscricao()

        resultado = self.service.get_by_id(inscricao.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, inscricao.id)

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # ── LIST ALL ────────────────────────────────────────────

    def test_listar_todas(self) -> None:
        self._nova_inscricao()
        self._nova_inscricao()

        resultado = self.service.list_all()

        self.assertEqual(len(resultado), 2)

    # ── UPDATE ──────────────────────────────────────────────

    def test_atualizar_inscricao_com_sucesso(self) -> None:
        inscricao = self._nova_inscricao(_status="ATIVA")

        atualizada = self.service.update(
            inscricao.id,
            self._novo_request(
                aluno_id=inscricao.aluno_id,
                curso_id=inscricao.curso_id,
                status="CONCLUIDA"
            ),
        )

        self.assertEqual(atualizada.status, "CONCLUIDA")

    def test_atualizar_inscricao_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    # ── DELETE ──────────────────────────────────────────────

    def test_deletar_inscricao_com_sucesso(self) -> None:
        inscricao = self._nova_inscricao()

        self.service.delete(inscricao.id)

        self.assertFalse(self.repo.exists(inscricao.id))

    def test_deletar_inscricao_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # ── BUSCAS ESPECÍFICAS ──────────────────────────────────

    def test_listar_inscricoes_por_aluno(self) -> None:
        aluno_alvo = uuid4()
        self._nova_inscricao(_aluno_id=aluno_alvo)
        self._nova_inscricao(_aluno_id=aluno_alvo)
        self._nova_inscricao(_aluno_id=uuid4()) # Outro aluno

        resultado = self.service.list_by_aluno(aluno_alvo)

        self.assertEqual(len(resultado), 2)
        for i in resultado:
            self.assertEqual(i.aluno_id, aluno_alvo)

    def test_listar_inscricoes_por_curso(self) -> None:
        curso_alvo = uuid4()
        self._nova_inscricao(_curso_id=curso_alvo)
        self._nova_inscricao(_curso_id=uuid4()) # Outro curso

        resultado = self.service.list_by_curso(curso_alvo)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].curso_id, curso_alvo)


if __name__ == "__main__":
    unittest.main()