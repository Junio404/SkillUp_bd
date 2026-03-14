from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_candidato_service
from application.services.candidato.candidato_service import CandidatoService
from application.dtos.candidato_dto import CandidatoRequestDTO, CandidatoResponseDTO


router = APIRouter(prefix="/candidatos", tags=["Candidato"])

@router.get("/by-cpf/{cpf}", response_model=CandidatoResponseDTO)
def get_by_cpf_candidato(cpf: str, service: CandidatoService = Depends(get_candidato_service)):
    try:
        result = service.get_by_cpf(cpf=cpf)
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar get_by_cpf: {exc}") from exc
@router.get("/by-email/{email}", response_model=CandidatoResponseDTO)
def get_by_email_candidato(email: str, service: CandidatoService = Depends(get_candidato_service)):
    try:
        result = service.get_by_email(email=email)
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar get_by_email: {exc}") from exc

@router.get("/", response_model=list[CandidatoResponseDTO])
def list_candidato(service: CandidatoService = Depends(get_candidato_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar candidato: {exc}") from exc


@router.get("/{entity_id}", response_model=CandidatoResponseDTO)
def get_candidato(entity_id: UUID, service: CandidatoService = Depends(get_candidato_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar candidato por id: {exc}") from exc


@router.post("/", response_model=CandidatoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_candidato(payload: CandidatoRequestDTO, service: CandidatoService = Depends(get_candidato_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar candidato: {exc}") from exc


@router.put("/{entity_id}", response_model=CandidatoResponseDTO)
def update_candidato(entity_id: UUID, payload: CandidatoRequestDTO, service: CandidatoService = Depends(get_candidato_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar candidato: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidato(entity_id: UUID, service: CandidatoService = Depends(get_candidato_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover candidato: {exc}") from exc



