import uuid
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from domain.entidades.enums import StatusInscricao


@dataclass
class InscricaoCurso:
    _data_inscricao: date
    _status: StatusInscricao
    _candidato_id: UUID
    _curso_id: UUID
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._data_inscricao:
            raise ValueError("Data de inscrição é obrigatória")

        if not self._candidato_id:
            raise ValueError("Candidato é obrigatório")

        if not self._curso_id:
            raise ValueError("Curso é obrigatório")
        
        if isinstance(self._status, int):
            self._status = StatusInscricao(self._status)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def data_inscricao(self) -> date:
        return self._data_inscricao

    @property
    def status(self) -> StatusInscricao:
        return self._status

    @property
    def candidato_id(self) -> UUID:
        return self._candidato_id

    @property
    def curso_id(self) -> UUID:
        return self._curso_id

    def atualizar_status_inscricao(self, novo_status: StatusInscricao) -> None:
        if not novo_status:
            raise ValueError("Status é obrigatório")
        self._status = novo_status
