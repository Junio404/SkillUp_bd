from __future__ import annotations

from uuid import UUID

from domain.entidades.enums import StatusInscricao
from domain.entidades.inscricao_curso import InscricaoCurso
from domain.interfaces.inscricao_curso_repository import InscricaoCursoRepository
from application.dtos.inscricao_curso_dto import InscricaoCursoRequestDTO, InscricaoCursoResponseDTO
from application.dtos.mapper import build_entity, entity_to_response, to_response_list


class InscricaoCursoService:
    def __init__(self, repository: InscricaoCursoRepository) -> None:
        self._repository = repository

    def create(self, payload: InscricaoCursoRequestDTO) -> InscricaoCursoResponseDTO:
        existing = self._repository.get_by_candidato_e_curso(payload.candidato_id, payload.curso_id)
        if existing:
            raise ValueError("Candidato já inscrito neste curso")
        entity = build_entity(entity_cls=InscricaoCurso, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, InscricaoCursoResponseDTO)

    def get_by_id(self, inscricao_curso_id: UUID) -> InscricaoCursoResponseDTO | None:
        entity = self._repository.get_by_id(inscricao_curso_id)
        if entity is None:
            return None
        return entity_to_response(entity, InscricaoCursoResponseDTO)

    def list_all(self) -> list[InscricaoCursoResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, InscricaoCursoResponseDTO)

    def update(self, inscricao_curso_id: UUID, payload: InscricaoCursoRequestDTO) -> InscricaoCursoResponseDTO | None:
        entity = self._repository.get_by_id(inscricao_curso_id)
        if entity is None:
            raise ValueError("Inscrição não encontrada")

        # Keep update behavior aligned with repository SQL, which persists status only.
        novo_status = StatusInscricao(payload.status)
        entity.atualizar_status_inscricao(novo_status)

        self._repository.update(entity)
        return entity_to_response(entity, InscricaoCursoResponseDTO)

    def delete(self, inscricao_curso_id: UUID) -> None:
        if not self._repository.exists(inscricao_curso_id):
            raise ValueError("Inscrição não encontrada")
        self._repository.remove(inscricao_curso_id)

    def list_by_candidato(self, candidato_id: UUID) -> list[InscricaoCursoResponseDTO]:
        entities = self._repository.list_by_candidato(candidato_id)
        return to_response_list(entities, InscricaoCursoResponseDTO)

    def get_by_candidato_e_curso(self, candidato_id: UUID, curso_id: UUID) -> InscricaoCursoResponseDTO | None:
        entity = self._repository.get_by_candidato_e_curso(candidato_id, curso_id)
        if entity is None:
            return None
        return entity_to_response(entity, InscricaoCursoResponseDTO)
