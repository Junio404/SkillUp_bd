from __future__ import annotations

import unittest
from datetime import datetime
from uuid import UUID, uuid4

from application.services.inscricao_curso import InscricaoCursoService
from application.dtos.inscricao_curso_dto import InscricaoCursoRequestDTO
from domain.entidades.inscricao_curso import InscricaoCurso
from domain.entidades.enums import StatusInscricao
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

    def get_by_candidato_e_curso(self, candidato_id: UUID, curso_id: UUID) -> InscricaoCurso | None:
        for item in self._items.values():
            if item.candidato_id == candidato_id and item.curso_id == curso_id:
                return item
        return None

    def list_by_candidato(self, candidato_id: UUID) -> list[InscricaoCurso]:
        return [item for item in self._items.values() if item.candidato_id == candidato_id]

    def list_by_curso(self, curso_id: UUID) -> list[InscricaoCurso]:
        return [item for item in self._items.values() if item.curso_id == curso_id]


class TestInscricaoCursoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeInscricaoCursoRepository()
        self.service = InscricaoCursoService(self.repo)

    def _novo_request(self, **overrides) -> InscricaoCursoRequestDTO:
        defaults = dict(
            candidato_id=uuid4(),
            curso_id=uuid4(),
            data_inscricao=datetime.now().date(),
            status=StatusInscricao.DEFERIDO,
        )
        defaults.update(overrides)
        return InscricaoCursoRequestDTO(**defaults)

    def _nova_inscricao(self, **overrides) -> InscricaoCurso:
        defaults = dict(
            _candidato_id=uuid4(),
            _curso_id=uuid4(),
            _data_inscricao=datetime.now().date(),
            _status=StatusInscricao.DEFERIDO,
        )
        defaults.update(overrides)
        entity = InscricaoCurso(**defaults)
        self.repo.add(entity)
        return entity

    # CREATE

    def test_criar_inscricao_com_sucesso(self) -> None:
        candidato_alvo = uuid4()
        curso_alvo = uuid4()
        resultado = self.service.create(self._novo_request(candidato_id=candidato_alvo, curso_id=curso_alvo))

        self.assertTrue(self.repo.exists(resultado.id))
        self.assertEqual(resultado.candidato_id, candidato_alvo)
        self.assertEqual(resultado.curso_id, curso_alvo)
        self.assertEqual(resultado.status, StatusInscricao.DEFERIDO.value)

    def test_criar_inscricao_duplicada_dispara_erro(self) -> None:
        candidato_alvo = uuid4()
        curso_alvo = uuid4()
        self._nova_inscricao(_candidato_id=candidato_alvo, _curso_id=curso_alvo)

        with self.assertRaises(ValueError):
            self.service.create(self._novo_request(candidato_id=candidato_alvo, curso_id=curso_alvo))

    # GET BY ID

    def test_obter_por_id_existente(self) -> None:
        inscricao = self._nova_inscricao()
        resultado = self.service.get_by_id(inscricao.id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, inscricao.id)

    def test_obter_por_id_inexistente_retorna_none(self) -> None:
        resultado = self.service.get_by_id(uuid4())
        self.assertIsNone(resultado)

    # LIST ALL

    def test_listar_todas(self) -> None:
        self._nova_inscricao()
        self._nova_inscricao()
        resultado = self.service.list_all()
        self.assertEqual(len(resultado), 2)

    # UPDATE

    def test_atualizar_inscricao_com_sucesso(self) -> None:
        inscricao = self._nova_inscricao(_status=StatusInscricao.DEFERIDO)
        atualizada = self.service.update(
            inscricao.id,
            self._novo_request(
                candidato_id=inscricao.candidato_id,
                curso_id=inscricao.curso_id,
                status=StatusInscricao.INDEFERIDO,
            ),
        )
        self.assertEqual(atualizada.status, StatusInscricao.INDEFERIDO.value)

    def test_atualizar_inscricao_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.update(uuid4(), self._novo_request())

    # DELETE

    def test_deletar_inscricao_com_sucesso(self) -> None:
        inscricao = self._nova_inscricao()
        self.service.delete(inscricao.id)
        self.assertFalse(self.repo.exists(inscricao.id))

    def test_deletar_inscricao_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    # BUSCAS ESPECIFICAS

    def test_listar_inscricoes_por_candidato(self) -> None:
        candidato_alvo = uuid4()
        self._nova_inscricao(_candidato_id=candidato_alvo)
        self._nova_inscricao(_candidato_id=candidato_alvo)
        self._nova_inscricao(_candidato_id=uuid4())

        resultado = self.service.list_by_candidato(candidato_alvo)

        self.assertEqual(len(resultado), 2)
        for i in resultado:
            self.assertEqual(i.candidato_id, candidato_alvo)

    def test_listar_inscricoes_candidato_sem_inscricoes(self) -> None:
        self._nova_inscricao()
        self._nova_inscricao()
        resultado = self.service.list_by_candidato(uuid4())
        self.assertEqual(len(resultado), 0)


if __name__ == "__main__":
    unittest.main()
