# 📋 MAPA COMPLETO DE REGRAS DE NEGÓCIO - SkillUp_bd

**Data de Mapeamento:** 18 de Março de 2026  
**Total de Regras:** 46 regras identificadas  
**Dominios:** 10 áreas principais do sistema  
**Padrões Arquiteturais:** 6 padrões recorrentes

---

## 📑 ÍNDICE

1. [Domínio: Candidatos](#1-domínio-candidatos)
2. [Domínio: Vagas e Empresas](#2-domínio-vagas-e-empresas)
3. [Domínio: Candidaturas](#3-domínio-candidaturas)
4. [Domínio: Competências](#4-domínio-competências)
5. [Domínio: Competências do Candidato](#5-domínio-competências-do-candidato)
6. [Domínio: Cursos e Instituições](#6-domínio-cursos-e-instituições)
7. [Domínio: Competências de Curso](#7-domínio-competências-de-curso)
8. [Domínio: Áreas de Ensino](#8-domínio-áreas-de-ensino)
9. [Domínio: Inscrições em Cursos](#9-domínio-inscrições-em-cursos)
10. [Domínio: Requisitos de Vaga](#10-domínio-requisitos-de-vaga)
11. [Padrões Arquiteturais](#padrões-arquiteturais-identificados)

---

## 1. Domínio: Candidatos

### Regra 1.1: Unicidade de CPF
- **Nome:** Candidato com CPF único
- **Descrição:** Cada candidato deve ter um CPF único no sistema. Não é permitido cadastrar dois candidatos com o mesmo CPF.
- **Validação:** CPF deve conter exatamente 11 dígitos
- **Entidades envolvidas:** `Candidato`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/candidato.py](skillup_banco/domain/entidades/candidato.py) - Linha 18
  - 📄 Validação: [skillup_banco/application/services/candidato/candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py) - Linha 19
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/candidato_repository_sql.py](skillup_banco/infrastructure/repositories/candidato_repository_sql.py)
- **Restrições:** Teste na criação e atualização
- **Tipo:** Constraint de Unicidade

---

### Regra 1.2: Unicidade de Email
- **Nome:** Candidato com email único
- **Descrição:** Cada candidato deve ter um email único no sistema. Não é permitido cadastrar dois candidatos com o mesmo email.
- **Validação:** Email não pode ser vazio
- **Entidades envolvidas:** `Candidato`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/candidato.py](skillup_banco/domain/entidades/candidato.py) - Linha 27
  - 📄 Validação: [skillup_banco/application/services/candidato/candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py) - Linha 23
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/candidato_repository_sql.py](skillup_banco/infrastructure/repositories/candidato_repository_sql.py)
- **Restrições:** Teste na criação e atualização
- **Tipo:** Constraint de Unicidade

---

### Regra 1.3: Nome Obrigatório
- **Nome:** Candidato deve ter nome
- **Descrição:** O nome do candidato é obrigatório e não pode ser vazio
- **Validação:** Campo `_nome` deve estar preenchido
- **Entidades envolvidas:** `Candidato`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/candidato.py](skillup_banco/domain/entidades/candidato.py) - Linha 23
  - 📄 Validação: [skillup_banco/domain/entidades/candidato.py](skillup_banco/domain/entidades/candidato.py) - `__post_init__` e setter
- **Restrições:** Validado em construtor
- **Tipo:** Validação de Campo Obrigatório

---

### Regra 1.4: Senha Obrigatória na Criação
- **Nome:** Candidato requer senha no cadastro
- **Descrição:** A senha é obrigatória ao criar um novo candidato. A senha é armazenada como hash BCrypt.
- **Entidades envolvidas:** `Candidato`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/candidato/candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py) - Linha 28
  - 🔐 Hash: [skillup_banco/application/security/password_hasher.py](skillup_banco/application/security/password_hasher.py)
- **Restrictions:** Lançada exceção se senha não for fornecida
- **Tipo:** Security - Senha

---

### Regra 1.5: Campos Opcionais do Candidato
- **Nome:** Campos flexíveis de perfil
- **Descrição:** Um candidato pode opcionalmente especificar: área de interesse, nível de formação, URL do currículo
- **Entidades envolvidas:** `Candidato`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/candidato.py](skillup_banco/domain/entidades/candidato.py) - Linhas 15-17
- **Restrições:** Todos são opcionais (podem ser `None`)
- **Tipo:** Validação Flexível

---

## 2. Domínio: Vagas e Empresas

### Regra 2.1: Empresa com CNPJ Único
- **Nome:** Empresa com CNPJ único
- **Descrição:** Cada empresa deve ter um CNPJ único. Não é permitido cadastrar duas empresas com o mesmo CNPJ.
- **Validação:** CNPJ deve conter exatamente 14 dígitos
- **Entidades envolvidas:** `Empresa`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/empresa.py](skillup_banco/domain/entidades/empresa.py) - Linha 18
  - 📄 Validação: [skillup_banco/application/services/empresa/empresa_service.py](skillup_banco/application/services/empresa/empresa_service.py) - Linha 19
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/empresa_repository_sql.py](skillup_banco/infrastructure/repositories/empresa_repository_sql.py)
- **Restrições:** Teste na criação e atualização
- **Tipo:** Constraint de Unicidade

---

### Regra 2.2: Campos Obrigatórios da Empresa
- **Nome:** Empresa requer identificadores básicos
- **Descrição:** Uma empresa deve ter razão social, nome fantasia e CNPJ válido
- **Validação:** Nenhum desses campos pode ser vazio
- **Entidades envolvidas:** `Empresa`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/empresa.py](skillup_banco/domain/entidades/empresa.py) - Linhas 12-19
- **Restrições:** Validado em construtor
- **Tipo:** Validação de Campo Obrigatório

---

### Regra 2.3: Senha Obrigatória para Empresa
- **Nome:** Empresa requer senha no cadastro
- **Descrição:** A senha é obrigatória ao criar uma nova empresa
- **Entidades envolvidas:** `Empresa`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/empresa/empresa_service.py](skillup_banco/application/services/empresa/empresa_service.py) - Linha 25
  - 🔐 Hash: [skillup_banco/application/security/password_hasher.py](skillup_banco/application/security/password_hasher.py)
- **Restrictions:** Lançada exceção se senha não for fornecida
- **Tipo:** Security - Senha

---

### Regra 2.4: Campos Obrigatórios de Vaga
- **Nome:** Vaga requer informações essenciais
- **Descrição:** Uma vaga deve ter: título, modalidade, tipo, prazo de inscrição e empresa responsável
- **Validação:** Título não pode ser vazio, prazo é obrigatório
- **Entidades envolvidas:** `Vaga`, `Empresa`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/vaga.py](skillup_banco/domain/entidades/vaga.py) - Linhas 15-31
- **Restrições:** Validado em construtor
- **Tipo:** Validação de Campo Obrigatório

---

### Regra 2.5: Modalidades de Vaga
- **Nome:** Tipos de funcionamento de vaga
- **Descrição:** Uma vaga pode ser: PRESENCIAL, REMOTO ou HÍBRIDO
- **Entidades envolvidas:** `Vaga`, `Modalidade`
- **Onde encontrar:**
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 4-7
  - 📄 Vaga: [skillup_banco/domain/entidades/vaga.py](skillup_banco/domain/entidades/vaga.py)
- **Restrições:** Enum com 3 valores possíveis
- **Tipo:** Enumeração

---

### Regra 2.6: Tipos de Vaga
- **Nome:** Categorias de oportunidade
- **Descrição:** Uma vaga pode ser: EMPREGO, ESTÁGIO ou TRAINEE
- **Entidades envolvidas:** `Vaga`, `TipoVaga`
- **Onde encontrar:**
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 10-13
  - 📄 Vaga: [skillup_banco/domain/entidades/vaga.py](skillup_banco/domain/entidades/vaga.py)
- **Restrições:** Enum com 3 valores possíveis
- **Tipo:** Enumeração

---

### Regra 2.7: Dados Opcionais de Vaga
- **Nome:** Campos complementares de vaga
- **Descrição:** Uma vaga pode opcionalmente conter: descrição, localidade, jornada
- **Entidades envolvidas:** `Vaga`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/vaga.py](skillup_banco/domain/entidades/vaga.py) - Linhas 12-14
- **Restrições:** Todos são opcionais (podem ser `None`)
- **Tipo:** Validação Flexível

---

## 3. Domínio: Candidaturas

### Regra 3.1: Candidato Não Pode Candidatar-se Duas Vezes para a Mesma Vaga
- **Nome:** Uma candidatura por vaga por candidato
- **Descrição:** Um candidato só pode se candidatar uma vez para a mesma vaga. Tentar candidatar-se novamente lança exceção.
- **Entidades envolvidas:** `Candidato`, `Vaga`, `Candidatura`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/candidatura/candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py) - Linha 18
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/candidatura_repository_sql.py](skillup_banco/infrastructure/repositories/candidatura_repository_sql.py) - Método `get_by_candidato_e_vaga`
- **Restrições:** Lança exceção ao tentar duplicar
- **Tipo:** Validação de Duplicação em Associação

---

### Regra 3.2: Data de Candidatura Automática
- **Nome:** Data de candidatura preenchida automaticamente
- **Descrição:** Se não fornecida, a data de candidatura é preenchida com a data/hora atual do sistema
- **Entidades envolvidas:** `Candidatura`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/candidatura/candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py) - Linha 24
- **Restrições:** Data deve ser válida
- **Tipo:** Default Value

---

### Regra 3.3: Status de Candidatura
- **Nome:** Ciclo de vida da candidatura
- **Descrição:** Uma candidatura pode ter status: ENVIADO, EM_ANALISE, ACEITO, RECUSADO, CANCELADO
- **Entidades envolvidas:** `Candidatura`, `StatusCandidatura`
- **Onde encontrar:**
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 23-27
- **Restrições:** Enum com 5 valores possíveis
- **Tipo:** State Machine

---

### Regra 3.4: Validação de Intervalo de Datas
- **Nome:** Data inicial menor que data final
- **Descrição:** Ao filtrar candidaturas por data, a data de início deve ser menor ou igual à data final
- **Entidades envolvidas:** `Candidatura`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/candidatura/candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py) - Linha 66
- **Restrições:** Lança exceção se violada
- **Tipo:** Validação de Range

---

## 4. Domínio: Competências

### Regra 4.1: Competência com Nome Único
- **Nome:** Nome de competência único
- **Descrição:** Cada competência deve ter um nome único no sistema. Não é permitido cadastrar duas competências com o mesmo nome.
- **Validação:** Nome não pode ser vazio
- **Entidades envolvidas:** `Competencia`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/competencia.py](skillup_banco/domain/entidades/competencia.py) - Linha 11
  - 📄 Validação: [skillup_banco/application/services/competencia/competencia_service.py](skillup_banco/application/services/competencia/competencia_service.py) - Linha 18
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/competencia_repository_sql.py](skillup_banco/infrastructure/repositories/competencia_repository_sql.py)
- **Restrições:** Teste na criação e atualização
- **Tipo:** Constraint de Unicidade

---

### Regra 4.2: Descrição Opcional de Competência
- **Nome:** Descrição opcional de competência
- **Descrição:** Uma competência pode ter uma descrição opcional que detalha a habilidade
- **Entidades envolvidas:** `Competencia`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/competencia.py](skillup_banco/domain/entidades/competencia.py) - Linha 8
- **Restrições:** Campo opcional (pode ser `None`)
- **Tipo:** Validação Flexível

---

### Regra 4.3: Níveis de Competência
- **Nome:** Classificação de proficiência
- **Descrição:** Uma competência possui um nível de proficiência: BAIXA, MÉDIA, ALTA
- **Entidades envolvidas:** `Competencia`, `CompetenciaCandidato`, `CursoCompetencia`, `RequisitoVaga`
- **Onde encontrar:**
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 16-19
- **Restrições:** Enum com 3 valores possíveis - Usado em múltiplos contextos
- **Tipo:** Enumeração

---

## 5. Domínio: Competências do Candidato

### Regra 5.1: Múltiplas Competências por Candidato
- **Nome:** Candidato pode registrar múltiplas competências
- **Descrição:** Um candidato pode ter múltiplas competências registradas. Não há validação explícita que evite duplicação na criação.
- **Entidades envolvidas:** `Candidato`, `Competencia`, `CompetenciaCandidato`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/competencia_candidato/competencia_candidato_service.py](skillup_banco/application/services/competencia_candidato/competencia_candidato_service.py) - Linha 15
  - 📄 DTO: [skillup_banco/application/dtos/competencia_candidato_dto.py](skillup_banco/application/dtos/competencia_candidato_dto.py)
- **Restrições:** Mínimas validações
- **Tipo:** Relacionamento 1:N

---

### Regra 5.2: Listar Competências por Candidato
- **Nome:** Consulta de competências por candidato
- **Descrição:** É possível listar todas as competências de um candidato específico
- **Entidades envolvidas:** `Candidato`, `CompetenciaCandidato`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/competencia_candidato/competencia_candidato_service.py](skillup_banco/application/services/competencia_candidato/competencia_candidato_service.py) - Linha 49
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/competencia_candidato_repository_sql.py](skillup_banco/infrastructure/repositories/competencia_candidato_repository_sql.py)
- **Restrições:** Requer candidato_id
- **Tipo:** Query

---

## 6. Domínio: Cursos e Instituições

### Regra 6.1: Instituição com Registro Educacional Único
- **Nome:** Registro educacional único
- **Descrição:** Cada instituição de ensino deve ter um registro educacional único. Não é permitido cadastrar duas instituições com o mesmo registro.
- **Validação:** Registro educacional não pode ser vazio
- **Entidades envolvidas:** `InstituicaoEnsino`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/instituicao_ensino.py](skillup_banco/domain/entidades/instituicao_ensino.py) - Linha 22
  - 📄 Validação: [skillup_banco/application/services/instituicao_ensino/instituicao_ensino_service.py](skillup_banco/application/services/instituicao_ensino/instituicao_ensino_service.py) - Linha 18
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/instituicao_ensino_repository_sql.py](skillup_banco/infrastructure/repositories/instituicao_ensino_repository_sql.py)
- **Restrições:** Teste na criação e atualização
- **Tipo:** Constraint de Unicidade

---

### Regra 6.2: CNPJ Único de Instituição (Quando Fornecido)
- **Nome:** CNPJ único quando fornecido
- **Descrição:** Uma instituição de ensino pode ter CNPJ. Se fornecido, deve ser único. CNPJ deve ter exatamente 14 dígitos.
- **Validação:** CNPJ é verificado só se fornecido (não obrigatório)
- **Entidades envolvidas:** `InstituicaoEnsino`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/instituicao_ensino.py](skillup_banco/domain/entidades/instituicao_ensino.py) - Linha 27
  - 📄 Validação: [skillup_banco/application/services/instituicao_ensino/instituicao_ensino_service.py](skillup_banco/application/services/instituicao_ensino/instituicao_ensino_service.py) - Linha 21
- **Restrições:** Validação condicional
- **Tipo:** Constraint Condicional de Unicidade

---

### Regra 6.3: Campos Obrigatórios da Instituição
- **Nome:** Informações essenciais de instituição
- **Descrição:** Uma instituição deve ter razão social e registro educacional obrigatoriamente
- **Entidades envolvidas:** `InstituicaoEnsino`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/instituicao_ensino.py](skillup_banco/domain/entidades/instituicao_ensino.py) - Linhas 16-18
- **Restrições:** Validado em construtor
- **Tipo:** Validação de Campo Obrigatório

---

### Regra 6.4: Curso Obrigatoriamente Ligado a Instituição
- **Nome:** Curso pertence a instituição de ensino
- **Descrição:** Todo curso deve estar ligado a uma instituição de ensino. A instituição é obrigatória.
- **Entidades envolvidas:** `Curso`, `InstituicaoEnsino`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/curso.py](skillup_banco/domain/entidades/curso.py) - Linha 18
- **Restrições:** Validado em construtor
- **Tipo:** Foreign Key Obrigatória

---

### Regra 6.5: Modalidades de Curso
- **Nome:** Tipos de funcionamento do curso
- **Descrição:** Um curso pode ser: PRESENCIAL, REMOTO ou HÍBRIDO
- **Entidades envolvidas:** `Curso`, `Modalidade`
- **Onde encontrar:**
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 4-7
  - 📄 Curso: [skillup_banco/domain/entidades/curso.py](skillup_banco/domain/entidades/curso.py) - Linha 7
- **Restrições:** Enum com 3 valores possíveis
- **Tipo:** Enumeração

---

### Regra 6.6: Curso Opcionalmente Ligado a Empresa
- **Nome:** Curso pode ser oferecido por empresa
- **Descrição:** Um curso pode opcionalmente ser ligado a uma empresa específica (campo opcional)
- **Entidades envolvidas:** `Curso`, `Empresa`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/curso.py](skillup_banco/domain/entidades/curso.py) - Linha 14
- **Restrições:** Campo opcional (pode ser `None`)
- **Tipo:** Foreign Key Opcional

---

### Regra 6.7: Campos Opcionais de Curso
- **Nome:** Informações complementares do curso
- **Descrição:** Um curso pode opcionalmente conter: área, carga horária, capacidade, prazo de inscrição, empresa responsável
- **Entidades envolvidas:** `Curso`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/curso.py](skillup_banco/domain/entidades/curso.py) - Linhas 8-14
- **Restrições:** Todos opcionais (podem ser `None`)
- **Tipo:** Validação Flexível

---

### Regra 6.8: Listar Cursos por Instituição
- **Nome:** Consulta de cursos por instituição
- **Descrição:** É possível listar todos os cursos de uma instituição específica
- **Entidades envolvidas:** `Curso`, `InstituicaoEnsino`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/curso/curso_service.py](skillup_banco/application/services/curso/curso_service.py) - Linha 64
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/curso_repository_sql.py](skillup_banco/infrastructure/repositories/curso_repository_sql.py)
- **Restrições:** Requer instituição_id
- **Tipo:** Query

---

### Regra 6.9: Listar Cursos por Empresa
- **Nome:** Consulta de cursos por empresa
- **Descrição:** É possível listar todos os cursos oferecidos por uma empresa específica
- **Entidades envolvidas:** `Curso`, `Empresa`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/curso/curso_service.py](skillup_banco/application/services/curso/curso_service.py) - Linha 68
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/curso_repository_sql.py](skillup_banco/infrastructure/repositories/curso_repository_sql.py)
- **Restrições:** Requer empresa_id
- **Tipo:** Query

---

## 7. Domínio: Competências de Curso

### Regra 7.1: Cada Competência Aparece Uma Vez por Curso
- **Nome:** Cada competência aparece uma vez por curso
- **Descrição:** Um curso não pode ter a mesma competência registrada duas vezes. Ao adicionar uma competência ao curso, válida-se se já existe.
- **Entidades envolvidas:** `Curso`, `Competencia`, `CursoCompetencia`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/curso_competencia/curso_competencia_service.py](skillup_banco/application/services/curso_competencia/curso_competencia_service.py) - Linha 17
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/curso_competencia_repository_sql.py](skillup_banco/infrastructure/repositories/curso_competencia_repository_sql.py)
- **Restrições:** Lança exceção ao tentar adicionar competência duplicada
- **Tipo:** Validação de Duplicação em Associação

---

### Regra 7.2: Nível de Proficiência em Competências de Curso
- **Nome:** Nível requerido de competência
- **Descrição:** Cada competência de um curso possui um nível: BAIXA, MÉDIA, ALTA
- **Entidades envolvidas:** `CursoCompetencia`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/curso_competencia.py](skillup_banco/domain/entidades/curso_competencia.py) - Linha 9
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 16-19
- **Restrições:** Nível é obrigatório
- **Tipo:** Atributo Obrigatório com Enum

---

### Regra 7.3: Listar Competências por Curso
- **Nome:** Consulta de competências por curso
- **Descrição:** É possível listar todas as competências requeridas por um curso específico
- **Entidades envolvidas:** `Curso`, `CursoCompetencia`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/curso_competencia/curso_competencia_service.py](skillup_banco/application/services/curso_competencia/curso_competencia_service.py) - Linha 64
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/curso_competencia_repository_sql.py](skillup_banco/infrastructure/repositories/curso_competencia_repository_sql.py)
- **Restrições:** Requer curso_id
- **Tipo:** Query

---

## 8. Domínio: Áreas de Ensino

### Regra 8.1: Área de Ensino com Nome Único
- **Nome:** Nome de área único
- **Descrição:** Cada área de ensino deve ter um nome único. Não é permitido cadastrar duas áreas com o mesmo nome.
- **Validação:** Nome não pode ser vazio
- **Entidades envolvidas:** `AreaEnsino`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/area_ensino.py](skillup_banco/domain/entidades/area_ensino.py) - Linha 12
  - 📄 Validação: [skillup_banco/application/services/area_ensino/area_ensino_service.py](skillup_banco/application/services/area_ensino/area_ensino_service.py) - Linha 20
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/area_ensino_repository_sql.py](skillup_banco/infrastructure/repositories/area_ensino_repository_sql.py)
- **Restrições:** Teste na criação e atualização
- **Tipo:** Constraint de Unicidade

---

### Regra 8.2: Instituição Pode ter Múltiplas Áreas
- **Nome:** Associação instituição-área
- **Descrição:** Uma instituição de ensino pode estar associada a múltiplas áreas de ensino
- **Entidades envolvidas:** `InstituicaoEnsino`, `AreaEnsino`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/instituicao_ensino.py](skillup_banco/domain/entidades/instituicao_ensino.py) - Linha 15
- **Restrições:** Associação é 1:N (um para muitos)
- **Tipo:** Relacionamento 1:N

---

### Regra 8.3: Não Permitir Duplicação na Associação Instituição-Área
- **Nome:** Cada instituição-área aparece uma vez
- **Descrição:** Uma instituição não pode estar associada duas vezes com a mesma área de ensino
- **Entidades envolvidas:** `InstituicaoEnsino`, `AreaEnsino`, `InstituicaoAreaEnsino`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py](skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py) - Linha 43
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/instituicao_area_ensino_repository_sql.py](skillup_banco/infrastructure/repositories/instituicao_area_ensino_repository_sql.py)
- **Restrições:** Lança exceção ao tentar adicionar duplicado
- **Tipo:** Validação de Duplicação em Associação

---

### Regra 8.4: Validação de Integridade Referencial
- **Nome:** Validação de FK na associação instituição-área
- **Descrição:** Antes de criar/atualizar uma associação, valida-se se a instituição e a área existem no banco
- **Entidades envolvidas:** `InstituicaoAreaEnsino`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py](skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py) - Linha 27
- **Restrições:** Lança exceção se FK não existir
- **Tipo:** Validação de Foreign Key

---

### Regra 8.5: Listar Áreas por Instituição
- **Nome:** Consulta de áreas por instituição
- **Descrição:** É possível listar todas as áreas de ensino associadas a uma instituição específica
- **Entidades envolvidas:** `InstituicaoAreaEnsino`, `InstituicaoEnsino`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py](skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py) - Linha 84
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/instituicao_area_ensino_repository_sql.py](skillup_banco/infrastructure/repositories/instituicao_area_ensino_repository_sql.py)
- **Restrições:** Requer instituição_id
- **Tipo:** Query

---

## 9. Domínio: Inscrições em Cursos

### Regra 9.1: Uma Inscrição por Curso por Candidato
- **Nome:** Uma inscrição por curso por candidato
- **Descrição:** Um candidato só pode se inscrever uma vez em um curso específico. Tentar inscrever-se novamente lança exceção.
- **Entidades envolvidas:** `Candidato`, `Curso`, `InscricaoCurso`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py) - Linha 16
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/inscricao_curso_repository_sql.py](skillup_banco/infrastructure/repositories/inscricao_curso_repository_sql.py)
- **Restrições:** Validado no método `get_by_candidato_e_curso`
- **Tipo:** Validação de Duplicação em Associação

---

### Regra 9.2: Status de Inscrição em Curso
- **Nome:** Ciclo de vida da inscrição
- **Descrição:** Uma inscrição em curso pode ter status: DEFERIDO, INDEFERIDO
- **Entidades envolvidas:** `InscricaoCurso`, `StatusInscricaoCurso`
- **Onde encontrar:**
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 30-31
  - 📄 Inscrição: [skillup_banco/domain/entidades/inscricao_curso.py](skillup_banco/domain/entidades/inscricao_curso.py)
- **Restrições:** Enum com 2 valores possíveis
- **Tipo:** State Machine

---

### Regra 9.3: Data de Inscrição Obrigatória
- **Nome:** Inscrição possui data
- **Descrição:** Toda inscrição em curso deve ter uma data de inscrição
- **Entidades envolvidas:** `InscricaoCurso`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/inscricao_curso.py](skillup_banco/domain/entidades/inscricao_curso.py) - Linha 7
- **Restrições:** Campo obrigatório
- **Tipo:** Validação de Campo Obrigatório

---

### Regra 9.4: Listar Inscrições por Candidato
- **Nome:** Consulta de inscrições por candidato
- **Descrição:** É possível listar todas as inscrições de um candidato em cursos
- **Entidades envolvidas:** `Candidato`, `InscricaoCurso`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py) - Linha 57
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/inscricao_curso_repository_sql.py](skillup_banco/infrastructure/repositories/inscricao_curso_repository_sql.py)
- **Restrições:** Requer candidato_id
- **Tipo:** Query

---

### Regra 9.5: Verificar Inscrição Específica
- **Nome:** Consulta de inscrição por candidato e curso
- **Descrição:** É possível verificar se um candidato está inscrito em um curso específico
- **Entidades envolvidas:** `Candidato`, `Curso`, `InscricaoCurso`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py) - Linha 61
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/inscricao_curso_repository_sql.py](skillup_banco/infrastructure/repositories/inscricao_curso_repository_sql.py)
- **Restrições:** Requer candidato_id e curso_id
- **Tipo:** Query

---

## 10. Domínio: Requisitos de Vaga

### Regra 10.1: Cada Competência Aparece Uma Vez como Requisito
- **Nome:** Cada competência aparece uma vez como requisito de vaga
- **Descrição:** Uma vaga não pode ter a mesma competência registrada duas vezes como requisito. Ao adicionar um requisito, válida-se se já existe.
- **Entidades envolvidas:** `Vaga`, `Competencia`, `RequisitoVaga`
- **Onde encontrar:**
  - 📄 Validação: [skillup_banco/application/services/requisito_vaga/requisito_vaga_service.py](skillup_banco/application/services/requisito_vaga/requisito_vaga_service.py) - Linha 17
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/requisito_vaga_repository_sql.py](skillup_banco/infrastructure/repositories/requisito_vaga_repository_sql.py)
- **Restrições:** Lança exceção ao tentar adicionar requisito duplicado
- **Tipo:** Validação de Duplicação em Associação

---

### Regra 10.2: Nível de Proficiência em Requisitos
- **Nome:** Nível requerido de competência
- **Descrição:** Cada requisito de vaga possui um nível mínimo: BAIXA, MÉDIA, ALTA
- **Entidades envolvidas:** `RequisitoVaga`
- **Onde encontrar:**
  - 📄 Definição: [skillup_banco/domain/entidades/requisito_vaga.py](skillup_banco/domain/entidades/requisito_vaga.py) - Linha 9
  - 📄 Enum: [skillup_banco/domain/entidades/enums.py](skillup_banco/domain/entidades/enums.py) - Linhas 16-19
- **Restrições:** Nível é obrigatório
- **Tipo:** Atributo Obrigatório com Enum

---

### Regra 10.3: Listar Requisitos por Vaga
- **Nome:** Consulta de requisitos por vaga
- **Descrição:** É possível listar todos os requisitos de competência de uma vaga específica
- **Entidades envolvidas:** `Vaga`, `RequisitoVaga`
- **Onde encontrar:**
  - 📄 Serviço: [skillup_banco/application/services/requisito_vaga/requisito_vaga_service.py](skillup_banco/application/services/requisito_vaga/requisito_vaga_service.py) - Linha 68
  - 🔐 Repository: [skillup_banco/infrastructure/repositories/requisito_vaga_repository_sql.py](skillup_banco/infrastructure/repositories/requisito_vaga_repository_sql.py)
- **Restrições:** Requer vaga_id
- **Tipo:** Query

---

## Padrões Arquiteturais Identificados

### 🔄 Padrão 1: UNICIDADE (6 regras)

Validação de campos únicos em nível de banco de dados:

| Entidade | Campo | Validação | Arquivo |
|----------|-------|-----------|---------|
| **Candidato** | CPF | 11 dígitos | [candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py#L19) |
| **Candidato** | Email | Email válido | [candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py#L23) |
| **Empresa** | CNPJ | 14 dígitos | [empresa_service.py](skillup_banco/application/services/empresa/empresa_service.py#L19) |
| **InstituicaoEnsino** | Registro Educacional | Não vazio | [instituicao_ensino_service.py](skillup_banco/application/services/instituicao_ensino/instituicao_ensino_service.py#L18) |
| **InstituicaoEnsino** | CNPJ | 14 dígitos (opcional) | [instituicao_ensino_service.py](skillup_banco/application/services/instituicao_ensino/instituicao_ensino_service.py#L21) |
| **Competencia** | Nome | Não vazio | [competencia_service.py](skillup_banco/application/services/competencia/competencia_service.py#L18) |
| **AreaEnsino** | Nome | Não vazio | [area_ensino_service.py](skillup_banco/application/services/area_ensino/area_ensino_service.py#L20) |

---

### 🚫 Padrão 2: VALIDAÇÃO DE DUPLICAÇÃO EM ASSOCIAÇÕES (5 regras)

Impede que um mesmo relacionamento seja criado duas vezes:

| Relacionamento | Restrição | Arquivo |
|---|---|---|
| **Candidato + Vaga** | Uma candidatura por vaga por candidato | [candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py#L18) |
| **Candidato + Curso** | Uma inscrição por curso por candidato | [inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py#L16) |
| **Curso + Competencia** | Uma competência por curso | [curso_competencia_service.py](skillup_banco/application/services/curso_competencia/curso_competencia_service.py#L17) |
| **Vaga + Competencia** | Um requisito por vaga | [requisito_vaga_service.py](skillup_banco/application/services/requisito_vaga/requisito_vaga_service.py#L17) |
| **InstituicaoEnsino + AreaEnsino** | Uma associação por instituição-área | [instituicao_area_ensino_service.py](skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py#L43) |

---

### 🔐 Padrão 3: CAMPOS OBRIGATÓRIOS E SEGURANÇA (6 regras)

Validações críticas em criação de entidades principais:

| Entidade | Validação | Tipo | Arquivo |
|---|---|---|---|
| **Candidato** | Nome não vazio | Campo Obrigatório | [candidato.py](skillup_banco/domain/entidades/candidato.py#L23) |
| **Candidato** | Senha na criação | Security | [candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py#L28) |
| **Empresa** | Campos básicos | Campo Obrigatório | [empresa.py](skillup_banco/domain/entidades/empresa.py#L12) |
| **Empresa** | Senha na criação | Security | [empresa_service.py](skillup_banco/application/services/empresa/empresa_service.py#L25) |
| **Vaga** | Título e prazo | Campo Obrigatório | [vaga.py](skillup_banco/domain/entidades/vaga.py#L15) |
| **InstituicaoEnsino** | Razão social e registro | Campo Obrigatório | [instituicao_ensino.py](skillup_banco/domain/entidades/instituicao_ensino.py#L16) |

---

### 📚 Padrão 4: CAMPOS OPCIONAIS (3 categorias)

Campos flexíveis que podem ou não ser fornecidos:

#### Candidato Opcionais:
- Área de interesse: [candidato.py](skillup_banco/domain/entidades/candidato.py#L15)
- Nível de formação: [candidato.py](skillup_banco/domain/entidades/candidato.py#L16)
- URL currículo: [candidato.py](skillup_banco/domain/entidades/candidato.py#L17)

#### Vaga Opcionais:
- Descrição: [vaga.py](skillup_banco/domain/entidades/vaga.py#L12)
- Localidade: [vaga.py](skillup_banco/domain/entidades/vaga.py#L13)
- Jornada: [vaga.py](skillup_banco/domain/entidades/vaga.py#L14)

#### Curso Opcionais:
- Área: [curso.py](skillup_banco/domain/entidades/curso.py#L8)
- Carga horária: [curso.py](skillup_banco/domain/entidades/curso.py#L9)
- Capacidade: [curso.py](skillup_banco/domain/entidades/curso.py#L11)
- Prazo inscrição: [curso.py](skillup_banco/domain/entidades/curso.py#L12)
- Empresa: [curso.py](skillup_banco/domain/entidades/curso.py#L14)

---

### 🎯 Padrão 5: RELACIONAMENTOS COM NÍVEIS DE PROFICIÊNCIA (3 contextos)

Usa sempre o Enum com valores: BAIXA, MÉDIA, ALTA

| Contexto | Entidade | Uso | Arquivo |
|----------|----------|-----|---------|
| **Competência do Candidato** | CompetenciaCandidato | Nível de domínio | [competencia_candidato_dto.py](skillup_banco/application/dtos/competencia_candidato_dto.py) |
| **Competência no Curso** | CursoCompetencia | Nível requerido | [curso_competencia.py](skillup_banco/domain/entidades/curso_competencia.py#L9) |
| **Requisito de Vaga** | RequisitoVaga | Nível mínimo requerido | [requisito_vaga.py](skillup_banco/domain/entidades/requisito_vaga.py#L9) |

Enum definido em: [enums.py](skillup_banco/domain/entidades/enums.py#L16)

---

### 🔄 Padrão 6: STATE MACHINES (2 entidades dinâmicas)

Ciclo de vida de entidades com mudanças de status:

#### **Candidatura**
Estados: ENVIADO → EM_ANALISE → ACEITO/RECUSADO/CANCELADO  
Definição: [enums.py](skillup_banco/domain/entidades/enums.py#L23)  
Serviço: [candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py)

#### **Inscrição em Curso**
Estados: DEFERIDO | INDEFERIDO  
Definição: [enums.py](skillup_banco/domain/entidades/enums.py#L30)  
Serviço: [inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py)

---

## 📊 Resumo Estatístico

### Regras por Domínio
| Domínio | Quantidade | Tipo Principal |
|---------|-----------|------------------|
| Candidatos | 5 | Unicidade + Security |
| Vagas e Empresas | 7 | Unicidade + Enumerações |
| Candidaturas | 4 | State Machine + Validação |
| Competências | 3 | Unicidade + Níveis |
| Competências do Candidato | 2 | Relacionamento 1:N |
| Cursos e Instituições | 9 | Unicidade + Foreign Keys |
| Competências de Curso | 3 | Níveis + Associações |
| Áreas de Ensino | 5 | Unicidade + Associações |
| Inscrições em Cursos | 5 | State Machine + Duplicação |
| Requisitos de Vaga | 3 | Níveis + Associações |
| **TOTAL** | **46** | **Múltiplos** |

### Categorização de Regras
| Tipo | Quantidade | Exemplos |
|------|-----------|----------|
| **Constraint de Unicidade** | 7 | CPF, Email, CNPJ, Nomes |
| **Validação de Duplicação** | 5 | Candidaturas, Inscrições, Competências |
| **Campos Obrigatórios** | 8 | Nome, Senha, Prazo, Data |
| **Foreign Keys** | 4 | Curso→Instituição, Vaga→Empresa |
| **Enumerações** | 6 | Modalidades, Tipos, Status, Níveis |
| **State Machines** | 2 | Candidatura, Inscrição |
| **Queries** | 10 | Listar por ID, Filtros |
| **Relacionamentos 1:N** | 2 | Candidato→Competências, Instituição→Áreas |
| **Validações Condicionais** | 1 | CNPJ de Instituição |

---

## 🏗️ Arquitetura de Validações por Camada

### Domain Layer (Validações Básicas)
**Arquivo:** `skillup_banco/domain/entidades/`

Responsabilidades:
- ✅ Tipos de dados corretos
- ✅ Valores obrigatórios não nulos
- ✅ Formatos básicos (CPF 11 dígitos, CNPJ 14)
- ✅ Ranges válidos

Exemplo: [candidato.py](skillup_banco/domain/entidades/candidato.py)

---

### Application Layer (Regras de Negócio)
**Arquivo:** `skillup_banco/application/services/`

Responsabilidades:
- ✅ Unicidade em banco de dados
- ✅ Validação de duplicação em associações
- ✅ Integridade referencial (FK)
- ✅ Criptografia de senhas
- ✅ Business logic complexa

Exemplo: [candidato_service.py](skillup_banco/application/services/candidato/candidato_service.py)

---

### Infrastructure Layer (Persistência)
**Arquivo:** `skillup_banco/infrastructure/repositories/`

Responsabilidades:
- ✅ Queries especializadas
- ✅ Índices em campos únicos
- ✅ Constraints de foreign key
- ✅ Transações

Exemplo: [candidato_repository_sql.py](skillup_banco/infrastructure/repositories/candidato_repository_sql.py)

---

## 🔒 Dados Sensíveis

### Campos que Requerem Proteção:
1. **Senhas:**
   - 📄 Hasheadas com BCrypt quando criadas
   - 📄 Arquivo: [password_hasher.py](skillup_banco/application/security/password_hasher.py)

2. **Identificadores Pessoais:**
   - 📄 CPF de Candidato - Nunca expor em logs ou APIs
   - 📄 Email de Candidato - Requer consentimento para uso
   - 📄 CNPJ de Empresa - Dados públicos mas sensíveis

3. **URLs e Contatos:**
   - 📄 URL de Currículo - Validar segurança antes de expor
   - 📄 Telefone/Email de Empresa - Controlar acesso

---

## 🔗 Relacionamentos Principais

```
Candidato
├── 1:N → CompetenciaCandidato
├── 1:N → Candidatura
└── 1:N → InscricaoCurso

Empresa
├── 1:N → Vaga
└── 1:N → Curso

Vaga
├── 1:N → Candidatura
└── 1:N → RequisitoVaga
    └── M:1 → Competencia

Curso
├── M:1 → InstituicaoEnsino
├── M:1 → Empresa (opcional)
└── 1:N → InscricaoCurso

InstituicaoEnsino
├── 1:N → Curso
└── 1:N → InstituicaoAreaEnsino
    └── M:1 → AreaEnsino

Competencia
├── 1:N → CompetenciaCandidato
├── 1:N → CursoCompetencia
└── 1:N → RequisitoVaga
```

---

## 📌 Checklist de Desenvolvimento

### Ao Criar Novos Candidatos:
- [ ] Validar CPF (11 dígitos)
- [ ] Validar Email (único)
- [ ] Validar Nome (não vazio)
- [ ] Validar Senha (criação obrigatória)
- [ ] Fazer hash da senha com BCrypt

### Ao Criar Novas Vagas:
- [ ] Validar Título (não vazio)
- [ ] Validar Modalidade (enum)
- [ ] Validar Tipo (enum)
- [ ] Validar Prazo (não vazio)
- [ ] Validar Empresa (FK obrigatória)

### Ao Adicionar Competências a Curso:
- [ ] Validar se competência já existe no curso
- [ ] Validar nível (enum)
- [ ] Lançar exceção se duplicado

### Ao Inscrever Candidato em Curso:
- [ ] Validar se candidato já está inscrito
- [ ] Validar se candidato existe
- [ ] Validar se curso existe
- [ ] Definir data de inscrição
- [ ] Lançar exceção se duplicado

---

**Fim do Documento**

