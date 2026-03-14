from __future__ import annotations

from typing import Any
from typing import Sequence
from uuid import UUID

from application.dtos.candidato_dto import (
    CandidatoComCandidaturasResponseDTO,
    CandidatoRequestDTO,
    CandidatoResponseDTO,
)
from application.dtos.candidatura_dto import CandidaturaResponseDTO
from application.dtos.mapper import entity_to_response, to_response_list
from domain.entidades.candidato import Candidato
from domain.interfaces.candidato_repository import CandidatoRepository


class CandidatoService:
    def __init__(self, repository: CandidatoRepository) -> None:
        self._repository = repository

    def create(self, payload: CandidatoRequestDTO) -> Candidato:
        if self._repository.get_by_cpf(payload.cpf) is not None:
            raise ValueError("CPF ja cadastrado")
        if self._repository.get_by_email(payload.email) is not None:
            raise ValueError("Email ja cadastrado")

        candidato = Candidato(
            _nome=payload.nome,
            _cpf=payload.cpf,
            _email=payload.email,
            _area_interesse=payload.area_interesse,
            _nivel_formacao=payload.nivel_formacao,
            _curriculo_url=payload.curriculo_url,
        )
        self._repository.add(candidato)
        return candidato

    def get_by_id(self, entity_id: UUID) -> Candidato | None:
        return self._repository.get_by_id(entity_id)

    def list_all(self) -> Sequence[Candidato]:
        return self._repository.list_all()

    def update(self, entity_id: UUID, payload: CandidatoRequestDTO) -> Candidato | None:
        candidato = self._repository.get_by_id(entity_id)
        if candidato is None:
            return None

        if payload.cpf != candidato.cpf:
            raise ValueError("CPF nao pode ser alterado")

        candidato_com_email = self._repository.get_by_email(payload.email)
        if candidato_com_email is not None and candidato_com_email.id != entity_id:
            raise ValueError("Email ja cadastrado")

        candidato.nome = payload.nome
        candidato.email = payload.email
        candidato.area_interesse = payload.area_interesse
        candidato.nivel_formacao = payload.nivel_formacao
        candidato.curriculo_url = payload.curriculo_url

        self._repository.update(candidato)
        return candidato

    def delete(self, entity_id: UUID) -> None:
        if not self._repository.exists(entity_id):
            raise ValueError("Candidato nao encontrado")

        self._repository.remove(entity_id)

    def get_by_cpf(self, cpf: str) -> Candidato | None:
        return self._repository.get_by_cpf(cpf)

    def get_by_email(self, email: str) -> Candidato | None:
        return self._repository.get_by_email(email)

    def list_resumo_candidaturas(self) -> Sequence[dict[str, Any]]:
        return self._repository.list_resumo_candidaturas()

    def get_historico_candidaturas(self, candidato_id: UUID) -> Sequence[dict[str, Any]]:
        return self._repository.get_historico_candidaturas(candidato_id)

    def get_with_candidaturas(self, candidato_id: UUID) -> CandidatoComCandidaturasResponseDTO | None:
        candidato = self._repository.get_with_candidaturas(candidato_id)
        if candidato is None:
            return None

        candidato_base = entity_to_response(candidato, CandidatoResponseDTO)
        candidaturas = to_response_list(candidato.candidaturas, CandidaturaResponseDTO)

        return CandidatoComCandidaturasResponseDTO(
            id=candidato_base.id,
            nome=candidato_base.nome,
            cpf=candidato_base.cpf,
            email=candidato_base.email,
            area_interesse=candidato_base.area_interesse,
            nivel_formacao=candidato_base.nivel_formacao,
            curriculo_url=candidato_base.curriculo_url,
            candidaturas=candidaturas,
        )
