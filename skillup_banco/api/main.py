from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api.routes.area_ensino_routes import router as area_ensino_router
from api.routes.candidato_routes import router as candidato_router
from api.routes.candidatura_routes import router as candidatura_router
from api.routes.competencia_routes import router as competencia_router
from api.routes.competencia_candidato_routes import router as competencia_candidato_router
from api.routes.curso_routes import router as curso_router
from api.routes.curso_competencia_routes import router as curso_competencia_router
from api.routes.empresa_routes import router as empresa_router
from api.routes.inscricao_curso_routes import router as inscricao_curso_router
from api.routes.instituicao_area_ensino_routes import router as instituicao_area_ensino_router
from api.routes.instituicao_ensino_routes import router as instituicao_ensino_router
from api.routes.requisito_vaga_routes import router as requisito_vaga_router
from api.routes.vaga_routes import router as vaga_router

app = FastAPI(title="SkillUp Banco API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(area_ensino_router)
app.include_router(candidato_router)
app.include_router(candidatura_router)
app.include_router(competencia_router)
app.include_router(competencia_candidato_router)
app.include_router(curso_router)
app.include_router(curso_competencia_router)
app.include_router(empresa_router)
app.include_router(inscricao_curso_router)
app.include_router(instituicao_area_ensino_router)
app.include_router(instituicao_ensino_router)
app.include_router(requisito_vaga_router)
app.include_router(vaga_router)

# Servir arquivos estáticos do front-end
# O uvicorn é iniciado na pasta 'skillup_banco', onde estão index.html, scripts.js e style.css
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(current_dir, "index.html"))

# Mapeia o restante dos arquivos (js, css, diagrams)
app.mount("/", StaticFiles(directory=current_dir), name="static")
