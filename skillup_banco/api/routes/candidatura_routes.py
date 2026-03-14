# from __future__ import annotations

# from uuid import UUID

# from fastapi import APIRouter, Depends, HTTPException, Response, status

# from api.dependencies import get_candidatura_service
# from application.services.candidatura.candidatura_service import CandidaturaService
# from application.services.Dtos.candidatura_dto import CandidaturaRequestDTO, CandidaturaResponseDTO


# router = APIRouter(prefix="/candidaturas", tags=["Candidatura"])

# @router.get("/by-candidato/{candidato_id}", response_model=list[CandidaturaResponseDTO])
# def list_by_candidato_candidatura(candidato_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         return service.list_by_candidato(candidato_id=candidato_id)
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except ValueError as exc:
#         raise HTTPException(status_code=400, detail=str(exc)) from exc
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao executar list_by_candidato: {exc}") from exc
# @router.get("/by-candidato-vaga/{candidato_id}/{vaga_id}", response_model=CandidaturaResponseDTO)
# def get_by_candidato_e_vaga_candidatura(candidato_id: UUID, vaga_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         result = service.get_by_candidato_e_vaga(candidato_id=candidato_id, vaga_id=vaga_id)
#         if result is None:
#             raise HTTPException(status_code=404, detail="Registro nao encontrado")
#         return result
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except ValueError as exc:
#         raise HTTPException(status_code=400, detail=str(exc)) from exc
#     except HTTPException:
#         raise
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao executar get_by_candidato_e_vaga: {exc}") from exc

# @router.get("/", response_model=list[CandidaturaResponseDTO])
# def list_candidatura(service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         return service.list_all()
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao listar candidatura: {exc}") from exc


# @router.get("/{entity_id}", response_model=CandidaturaResponseDTO)
# def get_candidatura(entity_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         result = service.get_by_id(entity_id=entity_id)
#         if result is None:
#             raise HTTPException(status_code=404, detail="Registro nao encontrado")
#         return result
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except HTTPException:
#         raise
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao buscar candidatura por id: {exc}") from exc


# @router.post("/", response_model=CandidaturaResponseDTO, status_code=status.HTTP_201_CREATED)
# def create_candidatura(payload: CandidaturaRequestDTO, service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         return service.create(payload=payload)
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except ValueError as exc:
#         raise HTTPException(status_code=400, detail=str(exc)) from exc
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao criar candidatura: {exc}") from exc


# @router.put("/{entity_id}", response_model=CandidaturaResponseDTO)
# def update_candidatura(entity_id: UUID, payload: CandidaturaRequestDTO, service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         result = service.update(entity_id=entity_id, payload=payload)
#         if result is None:
#             raise HTTPException(status_code=404, detail="Registro nao encontrado")
#         return result
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except ValueError as exc:
#         raise HTTPException(status_code=400, detail=str(exc)) from exc
#     except HTTPException:
#         raise
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar candidatura: {exc}") from exc


# @router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_candidatura(entity_id: UUID, service: CandidaturaService = Depends(get_candidatura_service)):
#     try:
#         service.delete(entity_id=entity_id)
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     except NotImplementedError as exc:
#         raise HTTPException(status_code=501, detail=str(exc)) from exc
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Erro interno ao remover candidatura: {exc}") from exc
