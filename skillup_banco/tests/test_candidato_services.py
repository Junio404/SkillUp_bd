from __future__ import annotations

import unittest
from datetime import datetime
from uuid import UUID, uuid4

from application.services.candidato.candidato_service import CandidatoService
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

    def list_resumo_candidaturas(self) -> list[dict]:
        return [
            {
                "candidato_id": str(item.id),
                "candidato_nome": item.nome,
                "candidato_email": item.email,
                "total_candidaturas": 0,
                "enviados": 0,
                "em_analise": 0,
                "aceitos": 0,
                "recusados": 0,
                "cancelados": 0,
            }
            for item in self._items.values()
        ]

    def get_historico_candidaturas(self, candidato_id: UUID) -> list[dict]:
        return [
            {
                "candidatura_id": str(uuid4()),
                "data_candidatura": datetime.now(),
                "status": 0,
                "vaga_id": str(uuid4()),
                "vaga_titulo": "Vaga Exemplo",
                "empresa_id": str(uuid4()),
                "empresa_nome_fantasia": "Empresa Exemplo",
            }
        ]

    def get_with_candidaturas(self, candidato_id: UUID) -> Candidato | None:
        return self._items.get(candidato_id)


class TestCandidatoService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeCandidatoRepository()
        self.service = CandidatoService(self.repo)

    def test_create_com_sucesso(self) -> None:
        candidato = self.service.create(
            CandidatoRequestDTO(
                nome="Joao",
                cpf="12345678901",
                email="joao@email.com",
                area_interesse="Backend",
                nivel_formacao="Superior",
                curriculo_url="https://cv.exemplo/joao",
            )
        )

        self.assertTrue(self.repo.exists(candidato.id))
        self.assertEqual(candidato.cpf, "12345678901")

    def test_create_com_cpf_duplicado_dispara_erro(self) -> None:
        self.service.create(
            CandidatoRequestDTO(
                nome="Ana",
                cpf="99999999999",
                email="ana@email.com",
            )
        )

        with self.assertRaises(ValueError):
            self.service.create(
                CandidatoRequestDTO(
                    nome="Ana 2",
                    cpf="99999999999",
                    email="ana2@email.com",
                )
            )

    def test_update_nao_permite_alterar_cpf(self) -> None:
        candidato = self.service.create(
            CandidatoRequestDTO(
                nome="Carlos",
                cpf="11111111111",
                email="carlos@email.com",
            )
        )

        with self.assertRaises(ValueError):
            self.service.update(
                entity_id=candidato.id,
                payload=CandidatoRequestDTO(
                    nome="Carlos Silva",
                    cpf="22222222222",
                    email="carlos@email.com",
                ),
            )

    def test_delete_inexistente_dispara_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete(uuid4())

    def test_list_resumo_candidaturas_retorna_dados(self) -> None:
        self.service.create(
            CandidatoRequestDTO(
                nome="Joana",
                cpf="12312312312",
                email="joana@email.com",
            )
        )

        resumo = self.service.list_resumo_candidaturas()

        self.assertGreaterEqual(len(resumo), 1)
        self.assertIn("candidato_nome", resumo[0])


if __name__ == "__main__":
    unittest.main()
