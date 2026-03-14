from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_competencia_service
from application.services.competencia.competencia_service import CompetenciaService
from application.dtos.competencia_dto import CompetenciaRequestDTO, CompetenciaResponseDTO


router = APIRouter(prefix="/competencias", tags=["Competencia"])

@router.get("/by-nome/{nome}", response_model=CompetenciaResponseDTO)
def get_by_nome_competencia(nome: str, service: CompetenciaService = Depends(get_competencia_service)):
    try:
        result = service.get_by_nome(nome=nome)
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar get_by_nome: {exc}") from exc

@router.get("/", response_model=list[CompetenciaResponseDTO])
def list_competencia(service: CompetenciaService = Depends(get_competencia_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar competencia: {exc}") from exc


@router.get("/{entity_id}", response_model=CompetenciaResponseDTO)
def get_competencia(entity_id: UUID, service: CompetenciaService = Depends(get_competencia_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar competencia por id: {exc}") from exc


@router.post("/", response_model=CompetenciaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_competencia(payload: CompetenciaRequestDTO, service: CompetenciaService = Depends(get_competencia_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar competencia: {exc}") from exc


@router.put("/{entity_id}", response_model=CompetenciaResponseDTO)
def update_competencia(entity_id: UUID, payload: CompetenciaRequestDTO, service: CompetenciaService = Depends(get_competencia_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar competencia: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competencia(entity_id: UUID, service: CompetenciaService = Depends(get_competencia_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover competencia: {exc}") from exc



