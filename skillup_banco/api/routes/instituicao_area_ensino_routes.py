from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_instituicao_area_ensino_service
from application.services.instituicao_area_ensino.instituicao_area_ensino_service import InstituicaoAreaEnsinoService
from application.services.Dtos.instituicao_area_ensino_dto import InstituicaoAreaEnsinoRequestDTO, InstituicaoAreaEnsinoResponseDTO


router = APIRouter(prefix="/instituicoes-area-ensino", tags=["InstituicaoAreaEnsino"])

@router.get("/by-instituicao/{instituicao_id}", response_model=list[InstituicaoAreaEnsinoResponseDTO])
def list_by_instituicao_instituicao_area_ensino(instituicao_id: UUID, service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
    try:
        return service.list_by_instituicao(instituicao_id=instituicao_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_instituicao: {exc}") from exc
@router.get("/by-chave/{instituicao_id}/{area_ensino_id}", response_model=InstituicaoAreaEnsinoResponseDTO)
def get_by_chave_instituicao_area_ensino(instituicao_id: UUID, area_ensino_id: UUID, service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
    try:
        result = service.get_by_chave(instituicao_id=instituicao_id, area_ensino_id=area_ensino_id)
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar get_by_chave: {exc}") from exc

@router.get("/", response_model=list[InstituicaoAreaEnsinoResponseDTO])
def list_instituicao_area_ensino(service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar instituicao_area_ensino: {exc}") from exc


@router.get("/{entity_id}", response_model=InstituicaoAreaEnsinoResponseDTO)
def get_instituicao_area_ensino(entity_id: UUID, service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar instituicao_area_ensino por id: {exc}") from exc


@router.post("/", response_model=InstituicaoAreaEnsinoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_instituicao_area_ensino(payload: InstituicaoAreaEnsinoRequestDTO, service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar instituicao_area_ensino: {exc}") from exc


@router.put("/{entity_id}", response_model=InstituicaoAreaEnsinoResponseDTO)
def update_instituicao_area_ensino(entity_id: UUID, payload: InstituicaoAreaEnsinoRequestDTO, service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar instituicao_area_ensino: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instituicao_area_ensino(entity_id: UUID, service: InstituicaoAreaEnsinoService = Depends(get_instituicao_area_ensino_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover instituicao_area_ensino: {exc}") from exc


