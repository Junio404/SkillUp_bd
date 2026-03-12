import uuid
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class Empresa:
    razao_social: str
    nome_fantasia: str
    cnpj: str
    senha_hash: str
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def criar_conta(self) -> None:
        raise NotImplementedError

    def fazer_login(self) -> None:
        raise NotImplementedError

    def publicar_vaga(self) -> None:
        raise NotImplementedError

    def gerenciar_vagas(self) -> None:
        raise NotImplementedError