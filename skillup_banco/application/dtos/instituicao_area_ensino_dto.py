from __future__ import annotations

from uuid import UUID

from application.dtos.base_dto import BaseRequestDTO, BaseResponseDTO


class InstituicaoAreaEnsinoRequestDTO(BaseRequestDTO):
    instituicao_ensino_id: UUID
    area_ensino_id: UUID


class InstituicaoAreaEnsinoResponseDTO(BaseResponseDTO):
    instituicao_ensino_id: UUID
    area_ensino_id: UUID


