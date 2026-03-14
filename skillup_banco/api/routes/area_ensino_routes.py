from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_area_ensino_service
from application.services.area_ensino.area_ensino_service import AreaEnsinoService
from application.services.Dtos.area_ensino_dto import AreaEnsinoRequestDTO, AreaEnsinoResponseDTO


router = APIRouter(prefix="/areas-ensino", tags=["AreaEnsino"])

@router.get("/by-nome/{nome}", response_model=AreaEnsinoResponseDTO)
def get_by_nome_area_ensino(nome: str, service: AreaEnsinoService = Depends(get_area_ensino_service)):
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

@router.get("/", response_model=list[AreaEnsinoResponseDTO])
def list_area_ensino(service: AreaEnsinoService = Depends(get_area_ensino_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar area_ensino: {exc}") from exc


@router.get("/{entity_id}", response_model=AreaEnsinoResponseDTO)
def get_area_ensino(entity_id: UUID, service: AreaEnsinoService = Depends(get_area_ensino_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar area_ensino por id: {exc}") from exc


@router.post("/", response_model=AreaEnsinoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_area_ensino(payload: AreaEnsinoRequestDTO, service: AreaEnsinoService = Depends(get_area_ensino_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar area_ensino: {exc}") from exc


@router.put("/{entity_id}", response_model=AreaEnsinoResponseDTO)
def update_area_ensino(entity_id: UUID, payload: AreaEnsinoRequestDTO, service: AreaEnsinoService = Depends(get_area_ensino_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar area_ensino: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area_ensino(entity_id: UUID, service: AreaEnsinoService = Depends(get_area_ensino_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover area_ensino: {exc}") from exc


