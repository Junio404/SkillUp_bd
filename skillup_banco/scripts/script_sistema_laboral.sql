-- ------------------------------------------------------------
-- 1. CRIAR E SELECIONAR O BANCO
-- ------------------------------------------------------------
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'SkillUp')
BEGIN
    CREATE DATABASE SkillUp
    COLLATE Latin1_General_CI_AI;
END
GO

USE SkillUp;
GO

-- ============================================================
-- 2. TABELAS INDEPENDENTES (sem FK)
-- ============================================================

-- ------------------------------------------------------------
-- COMPETENCIA
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.COMPETENCIA', 'U') IS NULL
CREATE TABLE dbo.COMPETENCIA (
    id            UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    nome          VARCHAR(150)     NOT NULL,
    descricao     VARCHAR(MAX)     NULL,

    CONSTRAINT PK_COMPETENCIA PRIMARY KEY (id),
    CONSTRAINT UQ_COMPETENCIA_nome UNIQUE (nome)
);
GO

-- ------------------------------------------------------------
-- AREA_ENSINO
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.AREA_ENSINO', 'U') IS NULL
CREATE TABLE dbo.AREA_ENSINO (
    id    UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    nome  VARCHAR(150)     NOT NULL,

    CONSTRAINT PK_AREA_ENSINO PRIMARY KEY (id),
    CONSTRAINT UQ_AREA_ENSINO_nome UNIQUE (nome)
);
GO

-- ------------------------------------------------------------
-- EMPRESA
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.EMPRESA', 'U') IS NULL
CREATE TABLE dbo.EMPRESA (
    id           UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    razaoSocial  VARCHAR(200)     NOT NULL,
    nomeFantasia VARCHAR(150)     NULL,
    cnpj         CHAR(14)         NOT NULL,

    CONSTRAINT PK_EMPRESA PRIMARY KEY (id),
    CONSTRAINT UQ_EMPRESA_cnpj UNIQUE (cnpj)
);
GO

-- ------------------------------------------------------------
-- CANDIDATO
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.CANDIDATO', 'U') IS NULL
CREATE TABLE dbo.CANDIDATO (
    id             UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    nome           VARCHAR(150)     NOT NULL,
    cpf            CHAR(11)         NOT NULL,
    email          VARCHAR(150)     NOT NULL,
    areaInteresse  VARCHAR(100)     NULL,
    nivelFormacao  VARCHAR(100)     NULL,
    curriculo_url  VARCHAR(300)     NULL,

    CONSTRAINT PK_CANDIDATO PRIMARY KEY (id),
    CONSTRAINT UQ_CANDIDATO_cpf   UNIQUE (cpf),
    CONSTRAINT UQ_CANDIDATO_email UNIQUE (email)
);
GO

-- ------------------------------------------------------------
-- INSTITUICAO_ENSINO
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.INSTITUICAO_ENSINO', 'U') IS NULL
CREATE TABLE dbo.INSTITUICAO_ENSINO (
    id                   UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    razaoSocial          VARCHAR(200)     NOT NULL,
    nomeFantasia         VARCHAR(150)     NULL,
    cnpj                 VARCHAR(14)      NULL,
    registroEducacional  VARCHAR(100)     NOT NULL,
    tipo                 VARCHAR(50)      NULL,

    CONSTRAINT PK_INSTITUICAO_ENSINO PRIMARY KEY (id),
    CONSTRAINT UQ_IE_cnpj UNIQUE (cnpj),
    CONSTRAINT UQ_IE_registroEducacional UNIQUE (registroEducacional),
    CONSTRAINT CK_IE_cnpj_len CHECK (cnpj IS NULL OR LEN(cnpj) = 14)
);
GO

-- ============================================================
-- 3. TABELAS COM FK SIMPLES
-- ============================================================

-- ------------------------------------------------------------
-- CURSO  (sempre vinculado a uma INSTITUICAO_ENSINO; empresa � opcional)
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.CURSO', 'U') IS NULL
CREATE TABLE dbo.CURSO (
    id                UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    nome              VARCHAR(200)     NOT NULL,
    area              VARCHAR(100)     NULL,
    cargaHoraria      INT              NULL,
    -- 0 = presencial | 1 = remoto | 2 = h�brido
    modalidade        TINYINT          NOT NULL,
    capacidade        INT              NULL,
    prazoInscricao    DATE             NULL,
    instituicao_id    UNIQUEIDENTIFIER NOT NULL,
    empresa_id        UNIQUEIDENTIFIER NULL,

    CONSTRAINT PK_CURSO PRIMARY KEY (id),
    CONSTRAINT FK_CURSO_instituicao FOREIGN KEY (instituicao_id)
        REFERENCES dbo.INSTITUICAO_ENSINO(id),
    CONSTRAINT FK_CURSO_empresa FOREIGN KEY (empresa_id)
        REFERENCES dbo.EMPRESA(id),
    CONSTRAINT CK_CURSO_modalidade CHECK (modalidade IN (0, 1, 2)),
    CONSTRAINT CK_CURSO_capacidade CHECK (capacidade IS NULL OR capacidade > 0)
);
GO

-- ------------------------------------------------------------
-- VAGA  (depende de EMPRESA)
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.VAGA', 'U') IS NULL
CREATE TABLE dbo.VAGA (
    id             UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    titulo         VARCHAR(200)     NOT NULL,
    descricao      VARCHAR(MAX)     NULL,
    localidade     VARCHAR(150)     NULL,
    -- 0 = presencial | 1 = remoto | 2 = h�brido
    modalidade     TINYINT          NOT NULL,
    -- 0 = Emprego | 1 = Est�gio | 2 = Trainee
    tipo           TINYINT          NOT NULL,
    jornada        VARCHAR(100)     NULL,
    prazoInscricao DATE             NOT NULL,
    empresa_id     UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_VAGA PRIMARY KEY (id),
    CONSTRAINT FK_VAGA_empresa FOREIGN KEY (empresa_id)
        REFERENCES dbo.EMPRESA(id),
    CONSTRAINT CK_VAGA_modalidade CHECK (modalidade IN (0, 1, 2)),
    CONSTRAINT CK_VAGA_tipo       CHECK (tipo IN (0, 1, 2))
);
GO

-- ============================================================
-- 4. TABELAS ASSOCIATIVAS
-- ============================================================

-- ------------------------------------------------------------
-- INSTITUICAO_AREA_ENSINO  (N:N entre INSTITUICAO_ENSINO e AREA_ENSINO)
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.INSTITUICAO_AREA_ENSINO', 'U') IS NULL
CREATE TABLE dbo.INSTITUICAO_AREA_ENSINO (
    instituicao_id  UNIQUEIDENTIFIER NOT NULL,
    area_ensino_id  UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_IAE PRIMARY KEY (instituicao_id, area_ensino_id),
    CONSTRAINT FK_IAE_instituicao FOREIGN KEY (instituicao_id)
        REFERENCES dbo.INSTITUICAO_ENSINO(id),
    CONSTRAINT FK_IAE_area FOREIGN KEY (area_ensino_id)
        REFERENCES dbo.AREA_ENSINO(id)
);
GO

-- ------------------------------------------------------------
-- COMPETENCIA_CANDIDATO
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.COMPETENCIA_CANDIDATO', 'U') IS NULL
CREATE TABLE dbo.COMPETENCIA_CANDIDATO (
    id              UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    -- 0 = Baixa | 1 = Media | 2 = Alta
    nivel           TINYINT          NOT NULL,
    candidato_id    UNIQUEIDENTIFIER NOT NULL,
    competencia_id  UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_COMPETENCIA_CANDIDATO PRIMARY KEY (id),
    CONSTRAINT FK_CC_candidato   FOREIGN KEY (candidato_id)
        REFERENCES dbo.CANDIDATO(id),
    CONSTRAINT FK_CC_competencia FOREIGN KEY (competencia_id)
        REFERENCES dbo.COMPETENCIA(id),
    -- Regra: candidato n�o pode ter a mesma compet�ncia duas vezes
    CONSTRAINT UQ_CC_candidato_competencia UNIQUE (candidato_id, competencia_id),
    CONSTRAINT CK_CC_nivel CHECK (nivel IN (0, 1, 2))
);
GO

-- ------------------------------------------------------------
-- REQUISITO_VAGA
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.REQUISITO_VAGA', 'U') IS NULL
CREATE TABLE dbo.REQUISITO_VAGA (
    id              UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    nivel           TINYINT          NOT NULL,
    competencia_id  UNIQUEIDENTIFIER NOT NULL,
    vaga_id         UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_REQUISITO_VAGA PRIMARY KEY (id),
    CONSTRAINT FK_RV_competencia FOREIGN KEY (competencia_id)
        REFERENCES dbo.COMPETENCIA(id),
    CONSTRAINT FK_RV_vaga FOREIGN KEY (vaga_id)
        REFERENCES dbo.VAGA(id),
    -- Regra: mesma compet�ncia n�o pode aparecer duas vezes na mesma vaga
    CONSTRAINT UQ_RV_vaga_competencia UNIQUE (vaga_id, competencia_id),
    CONSTRAINT CK_RV_nivel CHECK (nivel IN (0, 1, 2))
);
GO

-- ------------------------------------------------------------
-- CURSO_COMPETENCIA
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.CURSO_COMPETENCIA', 'U') IS NULL
CREATE TABLE dbo.CURSO_COMPETENCIA (
    id              UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    nivel           TINYINT          NOT NULL,
    curso_id        UNIQUEIDENTIFIER NOT NULL,
    competencia_id  UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT PK_CURSO_COMPETENCIA PRIMARY KEY (id),
    CONSTRAINT FK_CComp_curso FOREIGN KEY (curso_id)
        REFERENCES dbo.CURSO(id),
    CONSTRAINT FK_CComp_competencia FOREIGN KEY (competencia_id)
        REFERENCES dbo.COMPETENCIA(id),
    CONSTRAINT UQ_CComp_curso_competencia UNIQUE (curso_id, competencia_id),
    CONSTRAINT CK_CComp_nivel CHECK (nivel IN (0, 1, 2))
);
GO

-- ------------------------------------------------------------
-- CANDIDATURA
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.CANDIDATURA', 'U') IS NULL
CREATE TABLE dbo.CANDIDATURA (
    id               UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    dataCandidatura  DATETIME         NOT NULL DEFAULT GETDATE(),
    candidato_id     UNIQUEIDENTIFIER NOT NULL,
    vaga_id          UNIQUEIDENTIFIER NOT NULL,
    -- 0=enviado | 1=em an�lise | 2=aceita | 3=recusada | 4=cancelada
    status           TINYINT          NOT NULL DEFAULT 0,

    CONSTRAINT PK_CANDIDATURA PRIMARY KEY (id),
    CONSTRAINT FK_CAND_candidato FOREIGN KEY (candidato_id)
        REFERENCES dbo.CANDIDATO(id),
    CONSTRAINT FK_CAND_vaga FOREIGN KEY (vaga_id)
        REFERENCES dbo.VAGA(id),
    -- Regra: candidato n�o pode se candidatar duas vezes � mesma vaga
    -- (a unicidade abrange candidaturas ativas; reinscric�o � tratada no app)
    CONSTRAINT UQ_CAND_candidato_vaga UNIQUE (candidato_id, vaga_id),
    CONSTRAINT CK_CAND_status CHECK (status IN (0, 1, 2, 3, 4))
);
GO

-- ------------------------------------------------------------
-- INSCRICAO_CURSO
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.INSCRICAO_CURSO', 'U') IS NULL
CREATE TABLE dbo.INSCRICAO_CURSO (
    id             UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    dataInscricao  DATETIME         NOT NULL DEFAULT GETDATE(),
    candidato_id   UNIQUEIDENTIFIER NOT NULL,
    curso_id       UNIQUEIDENTIFIER NOT NULL,
    status         TINYINT          NOT NULL DEFAULT 0,

    CONSTRAINT PK_INSCRICAO_CURSO PRIMARY KEY (id),
    CONSTRAINT FK_IC_candidato FOREIGN KEY (candidato_id)
        REFERENCES dbo.CANDIDATO(id),
    CONSTRAINT FK_IC_curso FOREIGN KEY (curso_id)
        REFERENCES dbo.CURSO(id),
    -- Regra: candidato n�o pode se inscrever duas vezes no mesmo curso
    CONSTRAINT UQ_IC_candidato_curso UNIQUE (candidato_id, curso_id),
    CONSTRAINT CK_IC_status CHECK (status IN (0, 1))
);
GO

-- ============================================================
-- 5. �NDICES DE DESEMPENHO (al�m dos criados pelas constraints)
-- ============================================================

-- Buscas frequentes: vagas por empresa
CREATE INDEX IX_VAGA_empresa_id       ON dbo.VAGA (empresa_id);
CREATE INDEX IX_VAGA_prazoInscricao   ON dbo.VAGA (prazoInscricao);

-- Buscas frequentes: cursos por institui��o / por empresa
CREATE INDEX IX_CURSO_instituicao_id  ON dbo.CURSO (instituicao_id);
CREATE INDEX IX_CURSO_empresa_id      ON dbo.CURSO (empresa_id);
CREATE INDEX IX_CURSO_prazoInscricao  ON dbo.CURSO (prazoInscricao);

-- Candidaturas por candidato e por vaga (listagens)
CREATE INDEX IX_CANDIDATURA_candidato ON dbo.CANDIDATURA (candidato_id);
CREATE INDEX IX_CANDIDATURA_vaga      ON dbo.CANDIDATURA (vaga_id);
CREATE INDEX IX_CANDIDATURA_status    ON dbo.CANDIDATURA (status);

-- Inscri��es por candidato e por curso
CREATE INDEX IX_IC_candidato          ON dbo.INSCRICAO_CURSO (candidato_id);
CREATE INDEX IX_IC_curso              ON dbo.INSCRICAO_CURSO (curso_id);

-- Compet�ncias por candidato (perfil)
CREATE INDEX IX_CC_candidato          ON dbo.COMPETENCIA_CANDIDATO (candidato_id);

-- Requisitos por vaga (matching de vagas)
CREATE INDEX IX_RV_vaga               ON dbo.REQUISITO_VAGA (vaga_id);

-- Pesquisa por nome de compet�ncia
CREATE INDEX IX_COMPETENCIA_nome      ON dbo.COMPETENCIA (nome);
GO

GO

PRINT 'Banco SkillUp criado com sucesso!';
GO