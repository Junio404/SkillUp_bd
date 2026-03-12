from enum import Enum


class Modalidade(str, Enum):
    PRESENCIAL = "Presencial"
    REMOTO = "Remoto"
    HIBRIDO = "Hibrido"


class TipoVaga(str, Enum):
    EMPREGO = "Emprego"
    ESTAGIO = "Estágio"
    TRAINEE = "Trainee"


class Nivel(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"


class StatusCandidatura(str, Enum):
    ENVIADO = "Enviado"
    EM_ANALISE = "Em analise"
    ACEITO = "Aceito"
    RECUSADO = "Recusado"
    CANCELADO = "Cancelado"


class StatusInscricao(str, Enum):
    DEFERIDO = "Deferido"
    INDEFERIDO = "Indeferido"
