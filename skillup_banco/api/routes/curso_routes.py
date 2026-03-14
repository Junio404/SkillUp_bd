from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_curso_service
from application.services.curso.curso_service import CursoService
from application.dtos.curso_dto import CursoRequestDTO, CursoResponseDTO


router = APIRouter(prefix="/cursos", tags=["Curso"])

@router.get("/by-instituicao/{instituicao_id}", response_model=list[CursoResponseDTO])
def list_by_instituicao_curso(instituicao_id: UUID, service: CursoService = Depends(get_curso_service)):
    try:
        return service.list_by_instituicao(instituicao_id=instituicao_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_instituicao: {exc}") from exc
@router.get("/by-empresa/{empresa_id}", response_model=list[CursoResponseDTO])
def list_by_empresa_curso(empresa_id: UUID, service: CursoService = Depends(get_curso_service)):
    try:
        return service.list_by_empresa(empresa_id=empresa_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_empresa: {exc}") from exc

@router.get("/", response_model=list[CursoResponseDTO])
def list_curso(service: CursoService = Depends(get_curso_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar curso: {exc}") from exc


@router.get("/{entity_id}", response_model=CursoResponseDTO)
def get_curso(entity_id: UUID, service: CursoService = Depends(get_curso_service)):
    try:
        result = service.get_by_id(entity_id=entity_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Registro nao encontrado")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar curso por id: {exc}") from exc


@router.post("/", response_model=CursoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_curso(payload: CursoRequestDTO, service: CursoService = Depends(get_curso_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar curso: {exc}") from exc


@router.put("/{entity_id}", response_model=CursoResponseDTO)
def update_curso(entity_id: UUID, payload: CursoRequestDTO, service: CursoService = Depends(get_curso_service)):
    try:
        result = service.update(entity_id=entity_id, payload=payload)
        if result is None:
            raise HTTPException(status_code=404, detail="Registro nao encontrado")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar curso: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_curso(entity_id: UUID, service: CursoService = Depends(get_curso_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover curso: {exc}") from exc



