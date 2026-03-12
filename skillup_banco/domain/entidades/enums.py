from enum import Enum


class Modalidade(Enum):
    PRESENCIAL = 0
    REMOTO = 1
    HIBRIDO = 2


class TipoVaga(Enum):
    EMPREGO = 0
    ESTAGIO = 1
    TRAINEE = 2


class Nivel(Enum):
    BAIXA = 0
    MEDIA = 1
    ALTA = 2


class StatusCandidatura(Enum):
    ENVIADO = 0
    EM_ANALISE = 1
    ACEITO = 2
    RECUSADO = 3
    CANCELADO = 4


class StatusInscricao(Enum):
    DEFERIDO = 0
    INDEFERIDO = 1
