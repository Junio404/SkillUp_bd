import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID

from domain.entidades.enums import Modalidade


@dataclass
class Curso:
    _nome: str
    _modalidade: Modalidade
    _instituicao_ensino_id: UUID
    _area: Optional[str] = None
    _carga_horaria: Optional[int] = None
    _capacidade: Optional[int] = None
    _prazo_inscricao: Optional[date] = None
    _empresa_id: Optional[UUID] = None
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._nome:
            raise ValueError("Nome não pode ser vazio")

        if not self._instituicao_ensino_id:
            raise ValueError("Instituição de ensino é obrigatória")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not valor:
            raise ValueError("Nome não pode ser vazio")
        self._nome = valor

    @property
    def modalidade(self) -> Modalidade:
        return self._modalidade

    @modalidade.setter
    def modalidade(self, valor: Modalidade):
        self._modalidade = valor

    @property
    def instituicao_ensino_id(self) -> UUID:
        return self._instituicao_ensino_id

    @property
    def area(self) -> Optional[str]:
        return self._area

    @area.setter
    def area(self, valor: Optional[str]):
        self._area = valor

    @property
    def carga_horaria(self) -> Optional[int]:
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor: Optional[int]):
        self._carga_horaria = valor

    @property
    def capacidade(self) -> Optional[int]:
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor: Optional[int]):
        self._capacidade = valor

    @property
    def prazo_inscricao(self) -> Optional[date]:
        return self._prazo_inscricao

    @prazo_inscricao.setter
    def prazo_inscricao(self, valor: Optional[date]):
        self._prazo_inscricao = valor

    @property
    def empresa_id(self) -> Optional[UUID]:
        return self._empresa_id
