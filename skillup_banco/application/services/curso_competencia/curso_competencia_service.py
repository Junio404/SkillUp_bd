from __future__ import annotations

from uuid import UUID

from domain.interfaces.curso_competencia_repository import CursoCompetenciaRepository
from application.dtos.curso_competencia_dto import CursoCompetenciaRequestDTO, CursoCompetenciaResponseDTO

from domain.entidades.curso_competencia import CursoCompetencia
from application.dtos.mapper import entity_to_response, to_response_list, apply_update, build_entity

class CursoCompetenciaService:
    def __init__(self, repository: CursoCompetenciaRepository) -> None:
        self._repository = repository

    def create(self, payload: CursoCompetenciaRequestDTO) -> CursoCompetenciaResponseDTO:
        existente = self._repository.get_by_id(None)  # Validate duplicata
        curso_competencias = self._repository.list_by_curso(payload.curso_id)
        
        for cc in curso_competencias:
            if cc.competencia_id == payload.competencia_id:
                raise ValueError("Curso ja possui essa competencia")
        
        entity = build_entity(entity_cls=CursoCompetencia, request=payload)
        self._repository.add(entity)
        return entity_to_response(entity, CursoCompetenciaResponseDTO)

    def get_by_id(self, curso_competencia_id: UUID) -> CursoCompetenciaResponseDTO | None:
        entity = self._repository.get_by_id(curso_competencia_id)
        if entity is None:
            return None
        return entity_to_response(entity, CursoCompetenciaResponseDTO)

    def list_all(self) -> list[CursoCompetenciaResponseDTO]:
        entities = self._repository.list_all()
        return to_response_list(entities, CursoCompetenciaResponseDTO)

    def update(self, curso_competencia_id: UUID, payload: CursoCompetenciaRequestDTO) -> CursoCompetenciaResponseDTO | None:
        entity = self._repository.get_by_id(curso_competencia_id)
        if entity is None:
            raise ValueError("CursoCompetencia nao encontrada")
        
        entity = apply_update(entity, payload)
        self._repository.update(entity)
        return entity_to_response(entity, CursoCompetenciaResponseDTO)

    def delete(self, curso_competencia_id: UUID) -> None:
        if not self._repository.exists(curso_competencia_id):
            raise ValueError("CursoCompetencia nao encontrada")
        
        self._repository.remove(curso_competencia_id)

    def list_by_curso(self, curso_id: UUID) -> list[CursoCompetenciaResponseDTO]:
        entities = self._repository.list_by_curso(curso_id)
        return to_response_list(entities, CursoCompetenciaResponseDTO)