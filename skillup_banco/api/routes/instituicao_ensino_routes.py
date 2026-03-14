from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_instituicao_ensino_service
from application.services.instituicao_ensino.instituicao_ensino_service import InstituicaoEnsinoService
from application.dtos.instituicao_ensino_dto import InstituicaoEnsinoRequestDTO, InstituicaoEnsinoResponseDTO


router = APIRouter(prefix="/instituicoes-ensino", tags=["InstituicaoEnsino"])


@router.get("/by-registro/{registro}", response_model=InstituicaoEnsinoResponseDTO)
def get_by_registro_educacional_instituicao_ensino(registro: str, service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        result = service.get_by_registro_educacional(registro=registro)
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
            status_code=500, detail=f"Erro interno ao executar get_by_registro_educacional: {exc}") from exc


@router.get("/by-cnpj/{cnpj}", response_model=InstituicaoEnsinoResponseDTO)
def get_by_cnpj_instituicao_ensino(cnpj: str, service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        result = service.get_by_cnpj(cnpj=cnpj)
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
            status_code=500, detail=f"Erro interno ao executar get_by_cnpj: {exc}") from exc


@router.get("/", response_model=list[InstituicaoEnsinoResponseDTO])
def list_instituicao_ensino(service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao listar instituicao_ensino: {exc}") from exc


@router.get("/{entity_id}", response_model=InstituicaoEnsinoResponseDTO)
def get_instituicao_ensino(entity_id: UUID, service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        result = service.get_by_id(entity_id=entity_id)
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
            status_code=500, detail=f"Erro interno ao buscar instituicao_ensino por id: {exc}") from exc


@router.post("/", response_model=InstituicaoEnsinoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_instituicao_ensino(payload: InstituicaoEnsinoRequestDTO, service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao criar instituicao_ensino: {exc}") from exc


@router.put("/{entity_id}", response_model=InstituicaoEnsinoResponseDTO)
def update_instituicao_ensino(entity_id: UUID, payload: InstituicaoEnsinoRequestDTO, service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        result = service.update(entity_id=entity_id, payload=payload)
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
            status_code=500, detail=f"Erro interno ao atualizar instituicao_ensino: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instituicao_ensino(entity_id: UUID, service: InstituicaoEnsinoService = Depends(get_instituicao_ensino_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao remover instituicao_ensino: {exc}") from exc

