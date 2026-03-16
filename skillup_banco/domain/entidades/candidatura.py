import uuid
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from domain.entidades.enums import StatusCandidatura


@dataclass
class Candidatura:
    _status: StatusCandidatura
    _candidato_id: UUID
    _vaga_id: UUID
    _data_candidatura: datetime = field(default_factory=datetime.now)
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._data_candidatura:
            raise ValueError("Data de candidatura é obrigatória")

        if not self._candidato_id:
            raise ValueError("Candidato é obrigatório")

        if not self._vaga_id:
            raise ValueError("Vaga é obrigatória")
        
        if isinstance(self._status, int):
            self._status = StatusCandidatura(self._status)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def data_candidatura(self) -> datetime:
        return self._data_candidatura

    @property
    def status(self) -> StatusCandidatura:
        return self._status

    @property
    def candidato_id(self) -> UUID:
        return self._candidato_id

    @property
    def vaga_id(self) -> UUID:
        return self._vaga_id

    def atualizar_status(self, novo_status: StatusCandidatura) -> None:
        if not novo_status:
            raise ValueError("Status é obrigatório")
        self._status = novo_status
