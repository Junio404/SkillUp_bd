from __future__ import annotations

from datetime import datetime
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
    candidatura_id: UUID
    data_candidatura: datetime
    status: int
    vaga_id: UUID
    vaga_titulo: str
    empresa_id: UUID
    empresa_nome_fantasia: str


class EmpresaResumoRecrutamentoResponseDTO(BaseResponseDTO):
    empresa_id: UUID
    empresa_nome_fantasia: str
    total_vagas: int
    total_candidaturas: int
    total_aceitos: int