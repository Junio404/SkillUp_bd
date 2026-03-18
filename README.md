# SkillUp - Trabalho Prático 2 (Banco de Dados)

![Status](https://img.shields.io/badge/Status-Finalizado-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-green)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-red)
![Docker](https://img.shields.io/badge/Docker-Containerizado-blue)

## Descrição

**SkillUp** é uma plataforma completa de gestão laboral e educacional que conecta **candidatos**, **vagas**, **cursos** e **instituições de ensino**. O projeto foi desenvolvido como trabalho acadêmico da disciplina de Banco de Dados seguindo rigorosos padrões profissionais:

- **Implementação de operações CRUD completas** utilizando SQL puro  
- **Arquitetura em camadas** bem definida (Domain, Application, Infrastructure, API)  
- **API REST robusta** com FastAPI e injeção de dependência  
- **Banco de dados** em 3ª Forma Normal (3FN) com 13 tabelas  
- **Testes unitários** para todas as operações  
- **Interface web** com JavaScript vanilla e monitoramento SQL em tempo real  
- **Containerização** com Docker para execução reproduzível

O sistema utiliza **Microsoft SQL Server** como SGBD e expõe uma **API REST completa** com swagger automático para fácil integração.

---

# Integrantes

- Samuel Wagner
- Pedro Yan
- Diogo Gomes
- Manoel Junio
- Matheus Rennan
- Elder Rayan

---

## Funcionalidades Implementadas

### Operações de Leitura (SELECT)
- Listar todos os candidatos, vagas, cursos, empresas e instituições
- Buscar candidato por CPF ou email (parametrizável)
- Buscar empresa por CNPJ
- Buscar instituição por registro educacional
- Filtrar candidaturas por status e intervalo de datas (múltiplos parâmetros)
- Buscar vagas por empresa, modalidade e tipo

### Operações de Inserção (INSERT)
- **Candidatos**: Nome, CPF, email, senha com hash bcrypt
- **Empresas**: Razão social, CNPJ, nombre fantasia
- **Vagas**: Título, tipo (emprego/estágio/trainee), modalidade (presencial/remoto/híbrido)
- **Cursos**: Nome, carga horária, modalidade, instituição
- **Candidaturas** (N:N): Associação candidato × vaga
- **Competências** (N:N): Associação candidato × competência
- **Inscrições** (N:N): Associação candidato × curso
- **Requisitos de Vaga** (N:N): Associação vaga × competência

### Operações de Atualização (UPDATE)
- **Status de Candidatura**: Enviado → Em análise → Aceito → Recusado → Cancelado
- Monitoramento completo do ciclo de vida de candidaturas

### Operações de Deleção (DELETE)
- Suporte completo para remoção de registros com validação de integridade referencial

---

# Arquitetura do Projeto

O projeto segue uma **arquitetura em camadas profissional** com separação clara de responsabilidades:

```
skillup_banco/
│
├── domain/                           # Camada de Domínio
│   ├── entidades/                    # Modelos de negócio com validações
│   │   ├── candidato.py             # Entidade Candidato
│   │   ├── vaga.py                  # Entidade Vaga
│   │   ├── curso.py                 # Entidade Curso
│   │   └── ...                      # Outras entidades
│   ├── interfaces/                  # Contratos de repositório
│   └── enums.py                     # Enumerações (Modalidade, Status, etc)
│
├── infrastructure/                  # Camada de Infraestrutura
│   ├── database/                    # Configuração de conexão
│   └── repositories/                # 13 repositórios com SQL puro
│       ├── candidato_repository_sql.py
│       ├── vaga_repository_sql.py
│       ├── competencia_candidato_repository_sql.py
│       └── ...
│
├── application/                     # Camada de Aplicação
│   ├── services/                    # Lógica de negócio (13 serviços)
│   ├── dtos/                        # Data Transfer Objects
│   ├── mapper.py                    # Mapeamento entre camadas
│   └── security/                    # Hashing de senhas (bcrypt)
│
├── api/                             # Camada de API
│   ├── main.py                      # FastAPI app com CORS
│   ├── dependencies.py              # Injeção de dependência
│   └── routes/                      # 13 roteadores REST
│       ├── candidato_routes.py
│       ├── vaga_routes.py
│       ├── candidatura_routes.py
│       └── ...
│
├── tests/                           # Testes Unitários
│   ├── test_candidato_services.py
│   ├── test_vaga_services.py
│   ├── test_candidatura_services.py
│   └── ...
│
├── scripts/                         # Scripts SQL
│   └── script_sistema_laboral.sql   # DDL com tabelas, constraints, índices
│
├── index.html                       # Frontend com JavaScript
├── scripts.js                       # Lógica frontend + Monitor SQL
└── style.css                        # Estilização (design system)
```

### Padrões de Design Utilizados

| Padrão | Implementação |
|--------|---------------|
| **Repository Pattern** | `infrastructure/repositories/` - Abstração de dados |
| **Dependency Injection** | `api/dependencies.py` - FastAPI Depends() |
| **Data Transfer Object** | `application/dtos/` - Serialização/Desserialização |
| **Service Locator** | `application/services/` - Lógica centralizada |
| **Factory Pattern** | `application/mapper.py` - Criação de entidades |

---

# Tecnologias Utilizadas

| Camada | Tecnologia | Versão | Propósito |
|--------|-----------|--------|----------|
| **Backend** | Python | 3.11+ | Linguagem principal |
| **API** | FastAPI | 0.135.1 | Framework REST assíncrono |
| **BD** | SQL Server | 2022 | SGBD com SQL puro |
| **Driver** | PyODBC | Latest | Conexão com SQL Server |
| **ORM** | Nenhum | — | SQL puro para máximo controle |
| **Segurança** | Passlib + bcrypt | 1.7.4 | Hash de senhas |
| **Servidor** | Uvicorn | Latest | ASGI server |
| **Containerização** | Docker + Compose | 24+ | Ambiente reproducível |
| **Frontend** | HTML/CSS/JS vanilla | — | Interface web |
| **Testes** | Unittest + Pytest | — | Testes unitários |
| **Env** | python-dotenv | Latest | Variáveis de ambiente |

**Nota:** O projeto **não utiliza ORM** (como SQLAlchemy ORM ou Django ORM), apenas SQLAlchemy para gerenciar a conexão. Todas as queries são **SQL puro** conforme requisito do trabalho.

---

# Banco de Dados

## Modelo Relacional (3FN)

O banco segue a **3ª Forma Normal** com **13 tabelas principais**:

### Tabelas Independentes
- `COMPETENCIA` - Habilidades e tecnologias
- `AREA_ENSINO` - Áreas de conhecimento
- `EMPRESA` - Organizações
- `CANDIDATO` - Pessoas buscando oportunidades
- `INSTITUICAO_ENSINO` - Escolas e universidades

### Tabelas Associativas (N:N)
- `COMPETENCIA_CANDIDATO` - Habilidades do candidato
- `CURSO_COMPETENCIA` - Pré-requisitos do curso
- `REQUISITO_VAGA` - Requisitos da vaga
- `INSTITUICAO_AREA_ENSINO` - Áreas por instituição

### Tabelas Dependentes
- `CURSO` - Cursos oferecidos
- `VAGA` - Posições de emprego/estágio
- `CANDIDATURA` - Aplicações de candidatos
- `INSCRICAO_CURSO` - Matrículas em cursos

## Integridade Referencial

- **Chaves Primárias** (UUID)  
- **Chaves Estrangeiras** com cascade rules  
- **Constraints NOT NULL, UNIQUE, CHECK**  
- **Índices de performance** nas colunas mais consultadas

---

# Como Rodar o Projeto

## Pré-requisitos

| Ferramenta     | Versão mínima | Download                                         |
| -------------- | ------------- | ------------------------------------------------ |
| Docker         | 24+           | [https://www.docker.com](https://www.docker.com) |
| Docker Compose | v2            | incluso no Docker                                |

> **Recomendação:** Use Docker para garantir ambiente idêntico em qualquer máquina. Veja **Executar sem Docker** se necessário.

---

# Rodando com Docker (Recomendado)

## 1. Clonar o repositório

```bash
git clone https://github.com/Junio404/SkillUp_bd.git
cd SkillUp_bd
```

---

## 2. Criar arquivo de variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_USER=sa
DB_PASSWORD=SkillUp2026Db!X
DB_NAME=SistemaLaboral
DB_HOST=db
DB_PORT=1433
DATABASE_URL=mssql+pyodbc://sa:SkillUp2026Db!X@db:1433/SistemaLaboral?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

---

## 3. Subir o ambiente com Docker Compose

Execute na pasta do projeto:

```bash
docker compose up -d --build
```

**O que acontece automaticamente:**
1. Baixa imagem do SQL Server 2022
2. Constrói imagem da API Python
3. Espera banco ficar saudável
4. Inicializa banco com script SQL
5. Inicia a aplicação FastAPI

**Tempo estimado:** 2-3 minutos na primeira vez

---

## 4. Verificar se tudo está rodando

```bash
docker ps
```

Você verá 3 containers:
```
skillup_db      (SQL Server 2022)
skillup_app     (API FastAPI)
(skillup_db_init - completa e para)
```

---

## 5. Acessar a aplicação

| Recurso | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | [http://localhost:8000](http://localhost:8000) | Interface web completa |
| **Swagger/OpenAPI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentação interativa |
| **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Documentação em formato diferente |
| **SQL Server** | `localhost:1433` | BD (user: `sa`, pwd: `SkillUp2026Db!X`) |

### Destaques do Frontend

- **Dashboard de Requisitos**: Verifica conformidade com TP2
- **Monitor SQL em Tempo Real**: Visualiza queries executadas
- **Abas de Perfil**: Candidato, Empresa, Instituição, Dashboard
- **Operações CRUD Completas**: Insert, Read, Update (parcial), Delete
- **Formulários Intuitivos**: Validação no lado do cliente

---

## 6. Parar o ambiente

Manter dados:
```bash
docker compose down
```

Remover tudo incluindo banco:
```bash
docker compose down -v
```

---

## 7. Logs em tempo real

```bash
docker logs -f skillup_app
```

---

## 8. Reconstruir apenas a aplicação

```bash
docker compose up --build app -d
```

---

# Executar sem Docker (Alternativa)

> Requer instalação manual de Python 3.11+ e SQL Server

## Pré-requisitos adicionais

1. **Python 3.11+** - [https://www.python.org](https://www.python.org)
2. **Microsoft ODBC Driver 17 for SQL Server** - [Download](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
3. **SQL Server 2022** - local ou remoto

---

## Passo 1 — Criar ambiente virtual

```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### Linux / macOS
```bash
source .venv/bin/activate
```

---

## Passo 2 — Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Passo 3 — Inicializar banco de dados

Execute o script SQL no seu SQL Server:

```bash
sqlcmd -S seu-servidor -U sa -P sua-senha -i skillup_banco/scripts/script_sistema_laboral.sql
```

---

## Passo 4 — Configurar variáveis de ambiente

### Windows (PowerShell)
```powershell
$env:DATABASE_URL="mssql+pyodbc://sa:SENHA@SERVIDOR:1433/SistemaLaboral?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
```

### Linux/macOS
```bash
export DATABASE_URL="mssql+pyodbc://sa:SENHA@SERVIDOR:1433/SistemaLaboral?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
```

---

## Passo 5 — Iniciar a aplicação

```bash
cd skillup_banco
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

A aplicação estará em [http://localhost:8000](http://localhost:8000)

---

# Executando os Testes

Os testes unitários estão na pasta `tests/` e cobrem todos os serviços.

## Rodar todos os testes

```bash
cd skillup_banco
python -m unittest discover -s tests -p "test_*.py" -v
```

## Rodar teste específico

```bash
python -m unittest tests.test_candidato_services -v
```

## Testes implementados

- `test_candidato_services.py` - Operações de candidato
- `test_vaga_services.py` - Operações de vaga
- `test_candidatura_services.py` - Operações de candidatura
- `test_competencia.py` - Operações de competência
- `test_curso.py` - Operações de curso
- `test_empresa_service.py` - Operações de empresa
- `test_instituicao_ensino_services.py` - Operações de instituição
- E mais 6 outros testes...

---

# Troubleshooting

## Portas já em uso

Se receber erro de porta 8000 ou 1433 em uso:

```bash
# Verificar processos
lsof -i :8000
lsof -i :1433

# Matar processo (Linux/macOS)
kill -9 <PID>

# Ou mudar porta no docker-compose.yml
```

## Banco não inicia

```bash
# Ver logs do banco
docker logs skillup_db

# Remover volume e começar zerado
docker compose down -v
docker compose up -d --build
```

## Erro de conexão com API

```bash
# Verificar se app está rodando
docker ps

# Ver logs
docker logs skillup_app

# Acessar container
docker exec -it skillup_app bash
```

## ODBC Driver não encontrado

Se rodando sem Docker e tiver erro de driver ODBC:

1. Instale o driver correto: [Download](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
2. Verifique qual versão está instalada:
   ```bash
   # Linux
   odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
   
   # macOS
   /usr/local/etc/odbcinst.ini
   ```

---

# API REST - Endpoints

O sistema expõe 13 roteadores com endpoints para operações de CRUD (considerando as rotas base e rotas com `/{id}`):

| Recurso (Base + `/{id}`) | GET | POST | PATCH/PUT | DELETE |
|--------------------------|-----|------|-----------|--------|
| `/candidatos` | Sim | Sim | Sim | Sim |
| `/candidatos/cpf/{cpf}` | Sim | - | - | - |
| `/candidatos/email/{email}` | Sim | - | - | - |
| `/vagas` | Sim | Sim | Sim | Sim |
| `/cursos` | Sim | Sim | Sim | Sim |
| `/empresas` | Sim | Sim | Sim | Sim |
| `/instituicoes-ensino` | Sim | Sim | Sim | Sim |
| `/candidaturas` | Sim | Sim | Sim | Sim |
| `/candidaturas/{id}/status` | - | - | Sim | - |
| `/competencias` | Sim | Sim | Sim | Sim |
| `/competencias-candidato` | Sim | Sim | Não | Sim |
| `/inscricoes-curso` | Sim | Sim | Não | Sim |
| `/area-ensino` | Sim | Sim | Não | Não |
| `/instituicao-area-ensino` | Sim | Sim | Não | Não |
| `/curso-competencia` | Sim | Sim | Não | Sim |
| `/requisito-vaga` | Sim | Sim | Não | Sim |

**Exemplo de uso:**
```bash
# Listar todos os candidatos
curl http://localhost:8000/candidatos/

# Buscar candidato por CPF
curl http://localhost:8000/candidatos/cpf/12345678901

# Criar novo candidato
curl -X POST http://localhost:8000/candidatos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678901",
    "email": "joao@exemplo.com",
    "senha": "senha123"
  }'

# Atualizar status de candidatura
curl -X PATCH "http://localhost:8000/candidaturas/{id}/status?novo_status=2"
```

---

# Conformidade com Requisitos (TP2)

O projeto atende **100% dos requisitos obrigatórios** da disciplina:

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| Modelo em 3FN | OK | 13 tabelas bem normalizadas |
| Inserção ≥3 tabelas | OK | Candidato, Empresa, Vaga, Curso, Instituição |
| Inserção N:N | OK | CompetenciaCandidato, InscrCurso, ReqVaga |
| ≥6 Consultas | OK | 8 consultas implementadas |
| ≥3 Parametrizáveis | OK | CPF, CNPJ, Registro, ID |
| 1 Multi-parâmetro | OK | Filtro Candidatura (status + datas) |
| Atualização | OK | Status de candidatura |
| SQL Puro | OK | Sem ORM (repositórios `.py`) |
| Testes | OK | 10+ testes unitários |
| Interface | OK | Web com Dashboard + Monitor SQL |

---

# Documentação Adicional

- **Especificação Completa**: [Trabalho.md](Trabalho.md)
- **API Interativa**: [Swagger UI](http://localhost:8000/docs)
- **Schema SQL**: [script_sistema_laboral.sql](skillup_banco/scripts/script_sistema_laboral.sql)
- **Análise de Arquitetura**: README (este arquivo)

---

# Contribuindo

Este é um projeto acadêmico finalizado. Para sugestões ou correções:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome`)
3. Commit suas mudanças (`git commit -m 'Add feature'`)
4. Push para a branch (`git push origin feature/nome`)
5. Abra um Pull Request

---

# Licença

Este projeto é de código aberto para fins educacionais.

---

# Contato / Suporte

Para dúvidas sobre o projeto:
- Abra uma issue no GitHub
- Revisite a seção **Troubleshooting**
- Consulte o **Swagger** em `/docs`

---

**Última atualização:** Março 2026  
**Status:** Completo
