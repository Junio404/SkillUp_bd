from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_competencia_candidato_service
from application.services.competencia_candidato.competencia_candidato_service import CompetenciaCandidatoService
from application.services.Dtos.competencia_candidato_dto import CompetenciaCandidatoRequestDTO, CompetenciaCandidatoResponseDTO


router = APIRouter(prefix="/competencias-candidato", tags=["CompetenciaCandidato"])

@router.get("/by-candidato/{candidato_id}", response_model=list[CompetenciaCandidatoResponseDTO])
def list_by_candidato_competencia_candidato(candidato_id: UUID, service: CompetenciaCandidatoService = Depends(get_competencia_candidato_service)):
    try:
        return service.list_by_candidato(candidato_id=candidato_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_candidato: {exc}") from exc

@router.get("/", response_model=list[CompetenciaCandidatoResponseDTO])
def list_competencia_candidato(service: CompetenciaCandidatoService = Depends(get_competencia_candidato_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar competencia_candidato: {exc}") from exc


@router.get("/{entity_id}", response_model=CompetenciaCandidatoResponseDTO)
def get_competencia_candidato(entity_id: UUID, service: CompetenciaCandidatoService = Depends(get_competencia_candidato_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar competencia_candidato por id: {exc}") from exc


@router.post("/", response_model=CompetenciaCandidatoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_competencia_candidato(payload: CompetenciaCandidatoRequestDTO, service: CompetenciaCandidatoService = Depends(get_competencia_candidato_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar competencia_candidato: {exc}") from exc


@router.put("/{entity_id}", response_model=CompetenciaCandidatoResponseDTO)
def update_competencia_candidato(entity_id: UUID, payload: CompetenciaCandidatoRequestDTO, service: CompetenciaCandidatoService = Depends(get_competencia_candidato_service)):
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
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar competencia_candidato: {exc}") from exc


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competencia_candidato(entity_id: UUID, service: CompetenciaCandidatoService = Depends(get_competencia_candidato_service)):
    try:
        service.delete(entity_id=entity_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover competencia_candidato: {exc}") from exc


