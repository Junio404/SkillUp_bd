import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class Candidato:
    nome: str
    cpf: str
    email: str
    senha_hash: str
    area_interesse: Optional[str] = None
    nivel_formacao: Optional[str] = None
    curriculo_url: Optional[str] = None
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def criar_conta(self) -> None:
        raise NotImplementedError

    def fazer_login(self) -> None:
        raise NotImplementedError

    def atualizar_perfil(self) -> None:
        raise NotImplementedError

    def buscar_vagas(self) -> None:
        raise NotImplementedError

    def buscar_cursos(self) -> None:
        raise NotImplementedError

    def receber_recomendacoes(self) -> None:
        raise NotImplementedError
