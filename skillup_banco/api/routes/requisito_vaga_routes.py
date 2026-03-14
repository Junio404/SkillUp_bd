from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_requisito_vaga_service
from application.services.requisito_vaga.requisito_vaga_service import RequisitoVagaService
from application.dtos.requisito_vaga_dto import RequisitoVagaRequestDTO, RequisitoVagaResponseDTO


router = APIRouter(prefix="/requisitos-vaga", tags=["RequisitoVaga"])

@router.get("/by-vaga/{vaga_id}", response_model=list[RequisitoVagaResponseDTO])
def list_by_vaga_requisito_vaga(vaga_id: UUID, service: RequisitoVagaService = Depends(get_requisito_vaga_service)):
    try:
        return service.list_by_vaga(vaga_id=vaga_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_vaga: {exc}") from exc

@router.get("/", response_model=list[RequisitoVagaResponseDTO])
def list_requisito_vaga(service: RequisitoVagaService = Depends(get_requisito_vaga_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar requisito_vaga: {exc}") from exc


@router.get("/{entity_id}", response_model=RequisitoVagaResponseDTO)
def get_requisito_vaga(entity_id: UUID, service: RequisitoVagaService = Depends(get_requisito_vaga_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar requisito_vaga por id: {exc}") from exc


@router.post("/", response_model=RequisitoVagaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_requisito_vaga(payload: RequisitoVagaRequestDTO, service: RequisitoVagaService = Depends(get_requisito_vaga_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar requisito_vaga: {exc}") from exc


@router.put("/{entity_id}", response_model=RequisitoVagaResponseDTO)
def update_requisito_vaga(entity_id: UUID, payload: RequisitoVagaRequestDTO, service: RequisitoVagaService = Depends(get_requisito_vaga_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar requisito_vaga: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requisito_vaga(entity_id: UUID, service: RequisitoVagaService = Depends(get_requisito_vaga_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover requisito_vaga: {exc}") from exc



