import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class InstituicaoEnsino:
    razao_social: str
    registro_educacional: str
    senha_hash: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    tipo: Optional[str] = None
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def criar_conta(self) -> None:
        raise NotImplementedError

    def fazer_login(self) -> None:
        raise NotImplementedError

    def cadastrar_curso(self) -> None:
        raise NotImplementedError

    def gerenciar_cursos(self) -> None:
        raise NotImplementedError
