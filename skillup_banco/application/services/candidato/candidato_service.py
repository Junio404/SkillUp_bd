from __future__ import annotations

from typing import Any
from typing import Sequence
from uuid import UUID

<<<<<<< Updated upstream
from application.dtos.candidato_dto import (
    CandidatoComCandidaturasResponseDTO,
    CandidatoRequestDTO,
    CandidatoResponseDTO,
)
from application.dtos.candidatura_dto import CandidaturaResponseDTO
from application.dtos.mapper import (
    apply_update,
    build_entity,
    entity_to_response,
    to_response_list,
)
from domain.entidades.candidato import Candidato
from domain.interfaces.candidato_repository import CandidatoRepository
=======
from domain.entidades.candidato import Candidato
from domain.interfaces.candidato_repository import CandidatoRepository
<<<<<<< Updated upstream
from application.dtos.candidato_dto import CandidatoRequestDTO, CandidatoResponseDTO
=======
from application.services.Dtos.candidato_dto import CandidatoRequestDTO
>>>>>>> Stashed changes
>>>>>>> Stashed changes


class CandidatoService:
    def __init__(self, repository: CandidatoRepository) -> None:
        self._repository = repository

<<<<<<< Updated upstream
    def create(self, payload: CandidatoRequestDTO) -> CandidatoResponseDTO:
        candidato_por_cpf = self._repository.get_by_cpf(payload.cpf)
        if candidato_por_cpf is not None:
            raise ValueError("Ja existe candidato com esse CPF")

        candidato_por_email = self._repository.get_by_email(payload.email)
        if candidato_por_email is not None:
            raise ValueError("Ja existe candidato com esse email")

        entity = build_entity(entity_cls=Candidato, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, CandidatoResponseDTO)

    def get_by_id(self, entity_id: UUID) -> CandidatoResponseDTO | None:
        entity = self._repository.get_by_id(entity_id)
        if entity is None:
            return None
        return entity_to_response(entity, CandidatoResponseDTO)

    def list_all(self) -> list[CandidatoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, CandidatoResponseDTO)

    def update(self, entity_id: UUID, payload: CandidatoRequestDTO) -> CandidatoResponseDTO | None:
        entity = self._repository.get_by_id(entity_id)
        if entity is None:
            raise ValueError("Candidato nao encontrado")

        candidato_por_cpf = self._repository.get_by_cpf(payload.cpf)
        if candidato_por_cpf is not None and candidato_por_cpf.id != entity_id:
            raise ValueError("Ja existe outro candidato com esse CPF")

        candidato_por_email = self._repository.get_by_email(payload.email)
        if candidato_por_email is not None and candidato_por_email.id != entity_id:
            raise ValueError("Ja existe outro candidato com esse email")

        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, CandidatoResponseDTO)
=======
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
>>>>>>> Stashed changes

    def delete(self, entity_id: UUID) -> None:
        if not self._repository.exists(entity_id):
            raise ValueError("Candidato nao encontrado")
<<<<<<< Updated upstream

        self._repository.remove(entity_id)

    def get_by_cpf(self, cpf: str) -> CandidatoResponseDTO | None:
        entity = self._repository.get_by_cpf(cpf=cpf)
        if entity is None:
            return None
        return entity_to_response(entity, CandidatoResponseDTO)

    def get_by_email(self, email: str) -> CandidatoResponseDTO | None:
        entity = self._repository.get_by_email(email=email)
        if entity is None:
            return None
        return entity_to_response(entity, CandidatoResponseDTO)
=======

        self._repository.remove(entity_id)

    def get_by_cpf(self, cpf: str) -> Candidato | None:
        return self._repository.get_by_cpf(cpf)

    def get_by_email(self, email: str) -> Candidato | None:
        return self._repository.get_by_email(email)

    def list_resumo_candidaturas(self) -> Sequence[dict[str, Any]]:
        return self._repository.list_resumo_candidaturas()

    def get_historico_candidaturas(self, candidato_id: UUID) -> Sequence[dict[str, Any]]:
        return self._repository.get_historico_candidaturas(candidato_id)
>>>>>>> Stashed changes

    def get_with_candidaturas(self, candidato_id: UUID) -> CandidatoComCandidaturasResponseDTO | None:
        entity = self._repository.get_with_candidaturas(
            candidato_id=candidato_id)
        if entity is None:
            return None

        candidato_base = entity_to_response(entity, CandidatoResponseDTO)
        candidaturas_dto = to_response_list(
            entity.candidaturas, CandidaturaResponseDTO)

        return CandidatoComCandidaturasResponseDTO(
            id=candidato_base.id,
            nome=candidato_base.nome,
            cpf=candidato_base.cpf,
            email=candidato_base.email,
            area_interesse=candidato_base.area_interesse,
            nivel_formacao=candidato_base.nivel_formacao,
            curriculo_url=candidato_base.curriculo_url,
            candidaturas=candidaturas_dto,
        )
