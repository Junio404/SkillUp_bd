import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID

from domain.enums import Modalidade, TipoVaga


@dataclass
class Vaga:
    _titulo: str
    _modalidade: Modalidade
    _tipo: TipoVaga
    _prazo_inscricao: date
    _empresa_id: UUID
    _descricao: Optional[str] = None
    _localidade: Optional[str] = None
    _jornada: Optional[str] = None
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._titulo:
            raise ValueError("Título não pode ser vazio")

        if not self._prazo_inscricao:
            raise ValueError("Prazo de inscrição é obrigatório")

        if not self._empresa_id:
            raise ValueError("Empresa é obrigatória")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not valor:
            raise ValueError("Título não pode ser vazio")
        self._titulo = valor

    @property
    def modalidade(self) -> Modalidade:
        return self._modalidade

    @modalidade.setter
    def modalidade(self, valor: Modalidade):
        self._modalidade = valor

    @property
    def tipo(self) -> TipoVaga:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: TipoVaga):
        self._tipo = valor

    @property
    def prazo_inscricao(self) -> date:
        return self._prazo_inscricao

    @prazo_inscricao.setter
    def prazo_inscricao(self, valor: date):
        if not valor:
            raise ValueError("Prazo de inscrição é obrigatório")
        self._prazo_inscricao = valor

    @property
    def empresa_id(self) -> UUID:
        return self._empresa_id

    @property
    def descricao(self) -> Optional[str]:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: Optional[str]):
        self._descricao = valor

    @property
    def localidade(self) -> Optional[str]:
        return self._localidade

    @localidade.setter
    def localidade(self, valor: Optional[str]):
        self._localidade = valor

    @property
    def jornada(self) -> Optional[str]:
        return self._jornada

    @jornada.setter
    def jornada(self, valor: Optional[str]):
        self._jornada = valor
