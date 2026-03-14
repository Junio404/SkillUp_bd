from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_vaga_service
from application.services.vaga.vaga_service import VagaService
from application.services.Dtos.vaga_dto import VagaRequestDTO, VagaResponseDTO


router = APIRouter(prefix="/vagas", tags=["Vaga"])

@router.get("/by-empresa/{empresa_id}", response_model=list[VagaResponseDTO])
def list_by_empresa_vaga(empresa_id: UUID, service: VagaService = Depends(get_vaga_service)):
    try:
        return service.list_by_empresa(empresa_id=empresa_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_empresa: {exc}") from exc

@router.get("/", response_model=list[VagaResponseDTO])
def list_vaga(service: VagaService = Depends(get_vaga_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar vaga: {exc}") from exc


@router.get("/{entity_id}", response_model=VagaResponseDTO)
def get_vaga(entity_id: UUID, service: VagaService = Depends(get_vaga_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar vaga por id: {exc}") from exc


@router.post("/", response_model=VagaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_vaga(payload: VagaRequestDTO, service: VagaService = Depends(get_vaga_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar vaga: {exc}") from exc


@router.put("/{entity_id}", response_model=VagaResponseDTO)
def update_vaga(entity_id: UUID, payload: VagaRequestDTO, service: VagaService = Depends(get_vaga_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar vaga: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vaga(entity_id: UUID, service: VagaService = Depends(get_vaga_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover vaga: {exc}") from exc


