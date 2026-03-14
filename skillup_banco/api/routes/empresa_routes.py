from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_empresa_service
from application.services.empresa.empresa_service import EmpresaService
from application.dtos.empresa_dto import EmpresaRequestDTO, EmpresaResponseDTO


router = APIRouter(prefix="/empresas", tags=["Empresa"])

@router.get("/{cnpj}", response_model=EmpresaResponseDTO)
def get_by_cnpj_empresa(cnpj: str, service: EmpresaService = Depends(get_empresa_service)):
    try:
        result = service.get_by_cnpj(cnpj=cnpj)
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar get_by_cnpj: {exc}") from exc

@router.get("/", response_model=list[EmpresaResponseDTO])
def list_empresa(service: EmpresaService = Depends(get_empresa_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar empresa: {exc}") from exc


@router.get("/{empresa_id}", response_model=EmpresaResponseDTO)
def get_empresa(empresa_id: UUID, service: EmpresaService = Depends(get_empresa_service)):
    try:
        result = service.get_by_id(empresa_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Registro nao encontrado")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar empresa por id: {exc}") from exc


@router.post("/", response_model=EmpresaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_empresa(payload: EmpresaRequestDTO, service: EmpresaService = Depends(get_empresa_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar empresa: {exc}") from exc


@router.put("/{empresa_id}", response_model=EmpresaResponseDTO)
def update_empresa(empresa_id: UUID, payload: EmpresaRequestDTO, service: EmpresaService = Depends(get_empresa_service)):
    try:
        result = service.update(empresa_id, payload)
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar empresa: {exc}") from exc


@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empresa(empresa_id: UUID, service: EmpresaService = Depends(get_empresa_service)):
    try:
        service.delete(empresa_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover empresa: {exc}") from exc





