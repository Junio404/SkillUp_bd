import uuid
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class Empresa:
    _razao_social: str
    _nome_fantasia: str
    _cnpj: str
    _id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        if not self._razao_social:
            raise ValueError("Razão social não pode ser vazia")

        if not self._nome_fantasia:
            raise ValueError("Nome fantasia não pode ser vazio")

        if len(self._cnpj) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos")

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def razao_social(self) -> str:
        return self._razao_social

    @razao_social.setter
    def razao_social(self, valor: str):
        if not valor:
            raise ValueError("Razão social não pode ser vazia")
        self._razao_social = valor

    @property
    def nome_fantasia(self) -> str:
        return self._nome_fantasia

    @nome_fantasia.setter
    def nome_fantasia(self, valor: str):
        if not valor:
            raise ValueError("Nome fantasia não pode ser vazio")
        self._nome_fantasia = valor

    @property
    def cnpj(self) -> str:
        return self._cnpj

    def publicar_vaga(self) -> None:
        raise NotImplementedError

    def gerenciar_vagas(self) -> None:
        raise NotImplementedError
