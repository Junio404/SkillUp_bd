from __future__ import annotations

import unittest
from datetime import date, timedelta
from uuid import UUID, uuid4

from application.services.candidatura import (
    AtualizarStatusCandidaturaService,
    CriarCandidaturaService,
    FiltrarCandidaturasPorStatusDataService,
    ListarCandidaturasPorCandidatoService,
    ObterCandidaturaPorIdService,
    RemoverCandidaturaService,
)
from domain.entidades.candidatura import Candidatura
from domain.entidades.enums import StatusCandidatura
from domain.interfaces.candidatura_repository import CandidaturaRepository


class FakeCandidaturaRepository(CandidaturaRepository):
    def __init__(self) -> None:
        super().__init__(connection=None)
        self._items: dict[UUID, Candidatura] = {}

    def add(self, entity: Candidatura) -> None:
        self._items[entity.id] = entity

    def get_by_id(self, entity_id: UUID) -> Candidatura | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Candidatura]:
        return list(self._items.values())

    def update(self, entity: Candidatura) -> None:
        self._items[entity.id] = entity

    def remove(self, entity_id: UUID) -> None:
        self._items.pop(entity_id, None)

    def exists(self, entity_id: UUID) -> bool:
        return entity_id in self._items

    def list_by_candidato(self, candidato_id: UUID) -> list[Candidatura]:
        return [item for item in self._items.values() if item.candidato_id == candidato_id]

    def get_by_candidato_e_vaga(self, candidato_id: UUID, vaga_id: UUID) -> Candidatura | None:
        for item in self._items.values():
            if item.candidato_id == candidato_id and item.vaga_id == vaga_id:
                return item
        return None

    def list_by_status_e_data(
        self,
        status: StatusCandidatura,
        data_inicio: date,
        data_fim: date,
    ) -> list[Candidatura]:
        return [
            item
            for item in self._items.values()
            if item.status == status and data_inicio <= item.data_candidatura <= data_fim
        ]


class TestCandidaturaServices(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCandidaturaRepository()
        self.criar_service = CriarCandidaturaService(self.repo)
        self.filtrar_por_status_data_service = FiltrarCandidaturasPorStatusDataService(self.repo)
        self.listar_por_candidato_service = ListarCandidaturasPorCandidatoService(self.repo)
        self.obter_por_id_service = ObterCandidaturaPorIdService(self.repo)
        self.atualizar_status_service = AtualizarStatusCandidaturaService(self.repo)
        self.remover_service = RemoverCandidaturaService(self.repo)

    def _nova_candidatura(self, candidato_id: UUID | None = None) -> Candidatura:
        candidato = candidato_id or uuid4()
        candidatura = Candidatura(
            _data_candidatura=date.today(),
            _status=StatusCandidatura.ENVIADO,
            _candidato_id=candidato,
            _vaga_id=uuid4(),
        )
        self.repo.add(candidatura)
        return candidatura

    def test_criar_candidatura_com_sucesso(self) -> None:
        candidato_id = uuid4()
        vaga_id = uuid4()

        candidatura = self.criar_service.execute(
            candidato_id=candidato_id,
            vaga_id=vaga_id,
        )

        self.assertTrue(self.repo.exists(candidatura.id))
        self.assertEqual(candidatura.status, StatusCandidatura.ENVIADO)
        self.assertEqual(candidatura.data_candidatura, date.today())

    def test_criar_candidatura_duplicada_dispara_erro(self) -> None:
        candidato_id = uuid4()
        vaga_id = uuid4()
        self.criar_service.execute(
            candidato_id=candidato_id,
            vaga_id=vaga_id,
        )

        with self.assertRaises(ValueError):
            self.criar_service.execute(
                candidato_id=candidato_id,
                vaga_id=vaga_id,
            )

    def test_listar_candidaturas_por_candidato(self) -> None:
        candidato_alvo = uuid4()
        self._nova_candidatura(candidato_id=candidato_alvo)
        self._nova_candidatura(candidato_id=candidato_alvo)
        self._nova_candidatura(candidato_id=uuid4())

        resultado = self.listar_por_candidato_service.execute(candidato_alvo)

        self.assertEqual(len(resultado), 2)

    def test_obter_candidatura_por_id(self) -> None:
        candidatura = self._nova_candidatura()

        resultado = self.obter_por_id_service.execute(candidatura.id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, candidatura.id)

    def test_atualizar_status_com_sucesso(self) -> None:
        candidatura = self._nova_candidatura()

        atualizada = self.atualizar_status_service.execute(
            candidatura_id=candidatura.id,
            novo_status=StatusCandidatura.ACEITO,
        )

        self.assertEqual(atualizada.status, StatusCandidatura.ACEITO)

    def test_atualizar_status_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.atualizar_status_service.execute(
                candidatura_id=uuid4(),
                novo_status=StatusCandidatura.RECUSADO,
            )

    def test_remover_candidatura_com_sucesso(self) -> None:
        candidatura = self._nova_candidatura()

        self.remover_service.execute(candidatura.id)

        self.assertFalse(self.repo.exists(candidatura.id))

    def test_remover_candidatura_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.remover_service.execute(uuid4())

    def test_filtrar_por_status_e_data(self) -> None:
        hoje = date.today()
        dentro_janela_1 = Candidatura(
            _data_candidatura=hoje,
            _status=StatusCandidatura.ENVIADO,
            _candidato_id=uuid4(),
            _vaga_id=uuid4(),
        )
        dentro_janela_2 = Candidatura(
            _data_candidatura=hoje - timedelta(days=1),
            _status=StatusCandidatura.ENVIADO,
            _candidato_id=uuid4(),
            _vaga_id=uuid4(),
        )
        status_diferente = Candidatura(
            _data_candidatura=hoje,
            _status=StatusCandidatura.ACEITO,
            _candidato_id=uuid4(),
            _vaga_id=uuid4(),
        )
        fora_janela = Candidatura(
            _data_candidatura=hoje - timedelta(days=20),
            _status=StatusCandidatura.ENVIADO,
            _candidato_id=uuid4(),
            _vaga_id=uuid4(),
        )

        self.repo.add(dentro_janela_1)
        self.repo.add(dentro_janela_2)
        self.repo.add(status_diferente)
        self.repo.add(fora_janela)

        resultado = self.filtrar_por_status_data_service.execute(
            status=StatusCandidatura.ENVIADO,
            data_inicio=hoje - timedelta(days=7),
            data_fim=hoje,
        )

        self.assertEqual(len(resultado), 2)

    def test_filtrar_por_status_e_data_com_intervalo_invalido_dispara_erro(self) -> None:
        hoje = date.today()

        with self.assertRaises(ValueError):
            self.filtrar_por_status_data_service.execute(
                status=StatusCandidatura.ENVIADO,
                data_inicio=hoje,
                data_fim=hoje - timedelta(days=1),
            )


if __name__ == "__main__":
    unittest.main()
