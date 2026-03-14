from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from application.dtos.base_dto import BaseResponseDTO


class CandidatoResumoCandidaturasResponseDTO(BaseResponseDTO):
    candidato_id: UUID
    candidato_nome: str
    candidato_email: str
    total_candidaturas: int
    enviados: int
    em_analise: int
    aceitos: int
    recusados: int
    cancelados: int


class CandidatoHistoricoCandidaturaResponseDTO(BaseResponseDTO):
    candidatura_id: Optional[UUID] = None
    data_candidatura: Optional[datetime] = None
    status: Optional[int] = None
    vaga_id: Optional[UUID] = None
    vaga_titulo: Optional[str] = None
    empresa_id: Optional[UUID] = None
    empresa_nome_fantasia: Optional[str] = None


class EmpresaResumoRecrutamentoResponseDTO(BaseResponseDTO):
    empresa_id: UUID
    empresa_nome_fantasia: str
    total_vagas: int
    total_candidaturas: int
    total_aceitos: int