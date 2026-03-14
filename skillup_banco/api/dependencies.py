from __future__ import annotations

from fastapi import Depends

from infrastructure.database.engine import engine
from domain.interfaces.area_ensino_repository import AreaEnsinoRepository
from infrastructure.repositories.area_ensino_repository_sql import AreaEnsinoRepositorySql
from application.services.area_ensino.area_ensino_service import AreaEnsinoService
from domain.interfaces.candidato_repository import CandidatoRepository
from infrastructure.repositories.candidato_repository_sql import CandidatoRepositorySql
from application.services.candidato.candidato_service import CandidatoService
from domain.interfaces.candidatura_repository import CandidaturaRepository
from infrastructure.repositories.candidatura_repository_sql import CandidaturaRepositorySql
# from application.services.candidatura.candidatura_service import CandidaturaService
from domain.interfaces.competencia_repository import CompetenciaRepository
from infrastructure.repositories.competencia_repository_sql import CompetenciaRepositorySql
from application.services.competencia.competencia_service import CompetenciaService
from domain.interfaces.competencia_candidato_repository import CompetenciaCandidatoRepository
from infrastructure.repositories.competencia_candidato_repository_sql import CompetenciaCandidatoRepositorySql
from application.services.competencia_candidato.competencia_candidato_service import CompetenciaCandidatoService
from domain.interfaces.curso_repository import CursoRepository
from infrastructure.repositories.curso_repository_sql import CursoRepositorySql
from application.services.curso.curso_service import CursoService
from domain.interfaces.curso_competencia_repository import CursoCompetenciaRepository
from infrastructure.repositories.curso_competencia_repository_sql import CursoCompetenciaRepositorySql
from application.services.curso_competencia.curso_competencia_service import CursoCompetenciaService
from domain.interfaces.empresa_repository import EmpresaRepository
from infrastructure.repositories.empresa_repository_sql import EmpresaRepositorySql
from application.services.empresa.empresa_service import EmpresaService
from domain.interfaces.inscricao_curso_repository import InscricaoCursoRepository
from infrastructure.repositories.inscricao_curso_repository_sql import InscricaoCursoRepositorySql
from application.services.inscricao_curso.inscricao_curso_service import InscricaoCursoService
from domain.interfaces.instituicao_area_ensino_repository import InstituicaoAreaEnsinoRepository
from infrastructure.repositories.instituicao_area_ensino_repository_sql import InstituicaoAreaEnsinoRepositorySql
from application.services.instituicao_area_ensino.instituicao_area_ensino_service import InstituicaoAreaEnsinoService
from domain.interfaces.instituicao_ensino_repository import InstituicaoEnsinoRepository
from infrastructure.repositories.instituicao_ensino_repository_sql import InstituicaoEnsinoRepositorySql
from application.services.instituicao_ensino.instituicao_ensino_service import InstituicaoEnsinoService
from domain.interfaces.requisito_vaga_repository import RequisitoVagaRepository
from infrastructure.repositories.requisito_vaga_repository_sql import RequisitoVagaRepositorySql
from application.services.requisito_vaga.requisito_vaga_service import RequisitoVagaService
from domain.interfaces.vaga_repository import VagaRepository
from infrastructure.repositories.vaga_repository_sql import VagaRepositorySql
from application.services.vaga.vaga_service import VagaService


def get_area_ensino_repository() -> AreaEnsinoRepository:
    return AreaEnsinoRepositorySql(connection=engine)


def get_area_ensino_service(repository: AreaEnsinoRepository = Depends(get_area_ensino_repository)) -> AreaEnsinoService:
    return AreaEnsinoService(repository=repository)


def get_candidato_repository() -> CandidatoRepository:
    return CandidatoRepositorySql(connection=engine)


def get_candidato_service(repository: CandidatoRepository = Depends(get_candidato_repository)) -> CandidatoService:
    return CandidatoService(repository=repository)


def get_candidatura_repository() -> CandidaturaRepository:
    return CandidaturaRepositorySql(connection=engine)


# def get_candidatura_service(repository: CandidaturaRepository = Depends(get_candidatura_repository)) -> CandidaturaService:
#    return CandidaturaService(repository=repository)


def get_competencia_repository() -> CompetenciaRepository:
    return CompetenciaRepositorySql(connection=engine)


def get_competencia_service(repository: CompetenciaRepository = Depends(get_competencia_repository)) -> CompetenciaService:
    return CompetenciaService(repository=repository)


def get_competencia_candidato_repository() -> CompetenciaCandidatoRepository:
    return CompetenciaCandidatoRepositorySql(connection=engine)


def get_competencia_candidato_service(repository: CompetenciaCandidatoRepository = Depends(get_competencia_candidato_repository)) -> CompetenciaCandidatoService:
    return CompetenciaCandidatoService(repository=repository)


def get_curso_repository() -> CursoRepository:
    return CursoRepositorySql(connection=engine)


def get_curso_service(repository: CursoRepository = Depends(get_curso_repository)) -> CursoService:
    return CursoService(repository=repository)


def get_curso_competencia_repository() -> CursoCompetenciaRepository:
    return CursoCompetenciaRepositorySql(connection=engine)


def get_curso_competencia_service(repository: CursoCompetenciaRepository = Depends(get_curso_competencia_repository)) -> CursoCompetenciaService:
    return CursoCompetenciaService(repository=repository)


def get_empresa_repository() -> EmpresaRepository:
    return EmpresaRepositorySql(connection=engine)


def get_empresa_service(repository: EmpresaRepository = Depends(get_empresa_repository)) -> EmpresaService:
    return EmpresaService(repository=repository)


def get_inscricao_curso_repository() -> InscricaoCursoRepository:
    return InscricaoCursoRepositorySql(connection=engine)


def get_inscricao_curso_service(repository: InscricaoCursoRepository = Depends(get_inscricao_curso_repository)) -> InscricaoCursoService:
    return InscricaoCursoService(repository=repository)


def get_instituicao_area_ensino_repository() -> InstituicaoAreaEnsinoRepository:
    return InstituicaoAreaEnsinoRepositorySql(connection=engine)


def get_instituicao_area_ensino_service(repository: InstituicaoAreaEnsinoRepository = Depends(get_instituicao_area_ensino_repository)) -> InstituicaoAreaEnsinoService:
    return InstituicaoAreaEnsinoService(repository=repository)


def get_instituicao_ensino_repository() -> InstituicaoEnsinoRepository:
    return InstituicaoEnsinoRepositorySql(connection=engine)


def get_instituicao_ensino_service(repository: InstituicaoEnsinoRepository = Depends(get_instituicao_ensino_repository)) -> InstituicaoEnsinoService:
    return InstituicaoEnsinoService(repository=repository)


def get_requisito_vaga_repository() -> RequisitoVagaRepository:
    return RequisitoVagaRepositorySql(connection=engine)


def get_requisito_vaga_service(repository: RequisitoVagaRepository = Depends(get_requisito_vaga_repository)) -> RequisitoVagaService:
    return RequisitoVagaService(repository=repository)


def get_vaga_repository() -> VagaRepository:
    return VagaRepositorySql(connection=engine)


def get_vaga_service(repository: VagaRepository = Depends(get_vaga_repository)) -> VagaService:
    return VagaService(repository=repository)
