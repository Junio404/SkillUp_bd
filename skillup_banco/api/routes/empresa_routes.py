from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_curso_service, get_empresa_service, get_vaga_service
from application.services.curso.curso_service import CursoService
from application.services.empresa.empresa_service import EmpresaService
from application.services.vaga.vaga_service import VagaService
from application.dtos.empresa_dto import (
    EmpresaComCursosResponseDTO,
    EmpresaComVagasResponseDTO,
    EmpresaRequestDTO,
    EmpresaResponseDTO,
)


router = APIRouter(prefix="/empresas", tags=["Empresa"])

@router.get("/cnpj/{cnpj}", response_model=EmpresaResponseDTO)
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


@router.get("/{empresa_id}/vagas", response_model=EmpresaComVagasResponseDTO)
def get_empresa_with_vagas(
    empresa_id: UUID,
    empresa_service: EmpresaService = Depends(get_empresa_service),
    vaga_service: VagaService = Depends(get_vaga_service),
):
    try:
        empresa = empresa_service.get_by_id(empresa_id)
        if empresa is None:
            raise HTTPException(status_code=404, detail="Registro nao encontrado")

        vagas = vaga_service.list_by_empresa(empresa_id)
        return EmpresaComVagasResponseDTO(
            id=empresa.id,
            razao_social=empresa.razao_social,
            nome_fantasia=empresa.nome_fantasia,
            cnpj=empresa.cnpj,
            vagas=vagas,
        )
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar empresa com vagas: {exc}") from exc


@router.get("/{empresa_id}/cursos", response_model=EmpresaComCursosResponseDTO)
def get_empresa_with_cursos(
    empresa_id: UUID,
    empresa_service: EmpresaService = Depends(get_empresa_service),
    curso_service: CursoService = Depends(get_curso_service),
):
    try:
        empresa = empresa_service.get_by_id(empresa_id)
        if empresa is None:
            raise HTTPException(status_code=404, detail="Registro nao encontrado")

        cursos = curso_service.list_by_empresa(empresa_id)
        return EmpresaComCursosResponseDTO(
            id=empresa.id,
            razao_social=empresa.razao_social,
            nome_fantasia=empresa.nome_fantasia,
            cnpj=empresa.cnpj,
            cursos=cursos,
        )
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar empresa com cursos: {exc}") from exc


@router.get("/id/{empresa_id}", response_model=EmpresaResponseDTO)
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


@router.put("/id/{empresa_id}", response_model=EmpresaResponseDTO)
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


@router.delete("/id/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empresa(empresa_id: UUID, service: EmpresaService = Depends(get_empresa_service)):
    try:
        service.delete(empresa_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover empresa: {exc}") from exc





