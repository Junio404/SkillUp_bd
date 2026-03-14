from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_curso_competencia_service
from application.services.curso_competencia.curso_competencia_service import CursoCompetenciaService
from application.dtos.curso_competencia_dto import CursoCompetenciaRequestDTO, CursoCompetenciaResponseDTO


router = APIRouter(prefix="/cursos-competencia", tags=["CursoCompetencia"])


@router.get("/{curso_id}", response_model=list[CursoCompetenciaResponseDTO])
def list_by_curso_curso_competencia(curso_id: UUID, service: CursoCompetenciaService = Depends(get_curso_competencia_service)):
    try:
        return service.list_by_curso(curso_id=curso_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao executar list_by_curso: {exc}") from exc


@router.get("/", response_model=list[CursoCompetenciaResponseDTO])
def list_curso_competencia(service: CursoCompetenciaService = Depends(get_curso_competencia_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao listar curso_competencia: {exc}") from exc


@router.get("/{curso_competencia_id}", response_model=CursoCompetenciaResponseDTO)
def get_curso_competencia(curso_competencia_id: UUID, service: CursoCompetenciaService = Depends(get_curso_competencia_service)):
    try:
        result = service.get_by_id(curso_competencia_id)
        if result is None:
            raise HTTPException(
                status_code=404, detail="Registro nao encontrado")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao buscar curso_competencia por id: {exc}") from exc


@router.post("/", response_model=CursoCompetenciaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_curso_competencia(payload: CursoCompetenciaRequestDTO, service: CursoCompetenciaService = Depends(get_curso_competencia_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao criar curso_competencia: {exc}") from exc


@router.put("/{curso_competencia_id}", response_model=CursoCompetenciaResponseDTO)
def update_curso_competencia(curso_competencia_id: UUID, payload: CursoCompetenciaRequestDTO, service: CursoCompetenciaService = Depends(get_curso_competencia_service)):
    try:
        result = service.update(curso_competencia_id, payload)
        if result is None:
            raise HTTPException(
                status_code=404, detail="Registro nao encontrado")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao atualizar curso_competencia: {exc}") from exc


@router.delete("/{curso_competencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_curso_competencia(curso_competencia_id: UUID, service: CursoCompetenciaService = Depends(get_curso_competencia_service)):
    try:
        service.delete(curso_competencia_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao remover curso_competencia: {exc}") from exc
