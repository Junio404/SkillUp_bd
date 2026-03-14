from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_inscricao_curso_service
from application.services.inscricao_curso.inscricao_curso_service import InscricaoCursoService
from application.dtos.inscricao_curso_dto import InscricaoCursoRequestDTO, InscricaoCursoResponseDTO


router = APIRouter(prefix="/inscricoes-curso", tags=["InscricaoCurso"])


@router.get("/{candidato_id}", response_model=list[InscricaoCursoResponseDTO])
def list_by_candidato_inscricao_curso(candidato_id: UUID, service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        return service.list_by_candidato(candidato_id=candidato_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao executar list_by_candidato: {exc}") from exc


@router.get("/{candidato_id}/{curso_id}", response_model=InscricaoCursoResponseDTO)
def get_by_candidato_e_curso_inscricao_curso(candidato_id: UUID, curso_id: UUID, service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        result = service.get_by_candidato_e_curso(
            candidato_id=candidato_id, curso_id=curso_id)
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
            status_code=500, detail=f"Erro interno ao executar get_by_candidato_e_curso: {exc}") from exc


@router.get("/", response_model=list[InscricaoCursoResponseDTO])
def list_inscricao_curso(service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        return service.list_all()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao listar inscricao_curso: {exc}") from exc


@router.get("/{inscricao_curso_id}", response_model=InscricaoCursoResponseDTO)
def get_inscricao_curso(inscricao_curso_id: UUID, service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        result = service.get_by_id(inscricao_curso_id)
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
            status_code=500, detail=f"Erro interno ao buscar inscricao_curso por id: {exc}") from exc


@router.post("/", response_model=InscricaoCursoResponseDTO, status_code=status.HTTP_201_CREATED)
def create_inscricao_curso(payload: InscricaoCursoRequestDTO, service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        return service.create(payload=payload)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao criar inscricao_curso: {exc}") from exc


@router.put("/{inscricao_curso_id}", response_model=InscricaoCursoResponseDTO)
def update_inscricao_curso(inscricao_curso_id: UUID, payload: InscricaoCursoRequestDTO, service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        result = service.update(inscricao_curso_id, payload)
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
            status_code=500, detail=f"Erro interno ao atualizar inscricao_curso: {exc}") from exc


@router.delete("/{inscricao_curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscricao_curso(inscricao_curso_id: UUID, service: InscricaoCursoService = Depends(get_inscricao_curso_service)):
    try:
        service.delete(inscricao_curso_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao remover inscricao_curso: {exc}") from exc
