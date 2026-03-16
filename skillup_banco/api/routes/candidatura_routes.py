from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_candidatura_service
from application.services.candidatura.candidatura_service import CandidaturaService
from application.dtos.candidatura_dto import CandidaturaRequestDTO, CandidaturaResponseDTO
from domain.entidades.enums import StatusCandidatura


router = APIRouter(prefix="/candidaturas", tags=["Candidatura"])


@router.get("/candidato/{candidato_id}", response_model=list[CandidaturaResponseDTO])
def list_by_candidato_candidatura(candidato_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        return service.list_by_candidato(candidato_id=candidato_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao executar list_by_candidato: {exc}") from exc


@router.get("/candidato/{candidato_id}/vaga/{vaga_id}", response_model=CandidaturaResponseDTO)
def get_by_candidato_e_vaga_candidatura(candidato_id: UUID, vaga_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        result = service.get_by_candidato_e_vaga(
            candidato_id=candidato_id, vaga_id=vaga_id)
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
            status_code=500, detail=f"Erro interno ao executar get_by_candidato_e_vaga: {exc}") from exc


@router.get("/filtro", response_model=list[CandidaturaResponseDTO])
def list_by_status_e_data_candidatura(
        status: int,
        data_inicio: datetime,
        data_fim: datetime,
        service: CandidaturaService = Depends(get_candidatura_service),
):
    try:
        if status not in {item.value for item in StatusCandidatura}:
            raise HTTPException(
                status_code=400, detail=f"Status invalido: {status}. Use 0, 1, 2, 3 ou 4")

        status_enum = StatusCandidatura(status)
        return service.list_by_status_e_data(
            status=status_enum,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao executar list_by_status_e_data: {exc}") from exc


@router.get("/", response_model=list[CandidaturaResponseDTO])
def list_candidatura(service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao listar candidatura: {exc}") from exc


@router.get("/id/{candidatura_id}", response_model=CandidaturaResponseDTO)
def get_candidatura(candidatura_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        result = service.get_by_id(candidatura_id)
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
            status_code=500, detail=f"Erro interno ao buscar candidatura por id: {exc}") from exc


@router.post("/", response_model=CandidaturaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_candidatura(payload: CandidaturaRequestDTO, service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao criar candidatura: {exc}") from exc


@router.patch("/{candidatura_id}/status", response_model=CandidaturaResponseDTO)
def update_status_candidatura(candidatura_id: UUID, novo_status: int, service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        if novo_status not in {status.value for status in StatusCandidatura}:
            raise HTTPException(
                status_code=400, detail=f"Status invalido: {novo_status}. Use 0, 1, 2, 3 ou 4")
        status_enum = StatusCandidatura(novo_status)
        return service.update_status(candidatura_id=candidatura_id, novo_status=status_enum)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao atualizar status da candidatura: {exc}") from exc


@router.delete("/{candidatura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidatura(candidatura_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
    try:
        service.delete(candidatura_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao remover candidatura: {exc}") from exc
