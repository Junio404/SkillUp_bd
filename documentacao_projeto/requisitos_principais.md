# 📋 REGRAS DE CONTEXTO - SkillUp | Sistema de Gerenciamento de Vagas

**Mapeamento:** Regras de Negócio Contextuais  
**Foco:** Lógica e fluxos do sistema de gerenciamento de vagas  
**Data:** 18 de Março de 2026

---

## 🎯 Divisão de Atores

O sistema possui **3 tipos de usuários** com permissões distintas:

### 1. **Candidato**
- Busca e consulta vagas
- Se candidata a vagas
- Entra em Cursos de Capacitação
- Possui competências registradas

### 2. **Empresa**
- Publica vagas de emprego
- Pode oferecer cursos de capacitação
- Recebe candidaturas em suas vagas

### 3. **Instituição de Ensino**
- Oferece cursos de formação
- Registra áreas de ensino
- Cadastra competências exigidas

---

## 🏢 Contexto: Vagas

### Regra 1: Ciclo de Vida da Candidatura
Uma candidatura progride por um fluxo de status definido:

```
ENVIADO → EM_ANALISE → { ACEITO | RECUSADO | CANCELADO }
```

**Entidades Envolvidas:**
- `Candidatura`: conecta Candidato → Vaga
- `StatusCandidatura`: enum com 5 estados

**Localização:**
- Enum: [enums.py](skillup_banco/domain/entidades/enums.py#L23)
- Definição: [candidatura.py](skillup_banco/domain/entidades/candidatura.py)
- Serviço: [candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py)

---

### Regra 2: Unicidade de Candidatura por Vaga
**Um candidato só pode se candidatar UMA VEZ por vaga.**

- Se tentar candidatar novamente → Exceção
- A vaga pode receber múltiplas candidaturas de candidatos diferentes
- Isso previne duplicação indesejada

**Implementação:**
- Validação no serviço: [candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py#L18)
- Query: `get_by_candidato_e_vaga()` em repository

---

### Regra 3: Vaga Como Oportunidade Categórica
Uma vaga define o tipo de oportunidade através de dois atributos:

| Atributo | Valores | Significado |
|----------|---------|-------------|
| **Modalidade** | PRESENCIAL, REMOTO, HÍBRIDO | Onde/como trabalhar |
| **Tipo** | EMPREGO, ESTÁGIO, TRAINEE | Categoria de contratação |

**Exemplo:** Uma vaga pode ser "REMOTO + ESTÁGIO" (estágio remoto)

**Localização:**
- Enum: [enums.py](skillup_banco/domain/entidades/enums.py#L4)
- Vaga: [vaga.py](skillup_banco/domain/entidades/vaga.py)

---

### Regra 4: Requisitos de Competência em Vagas
Uma vaga pode exigir múltiplas competências, cada uma com um nível mínimo:

```
Vaga
└── Requisitos
    ├─ Java (nível MÉDIA)
    ├─ SQL (nível ALTA)
    └─ Git (nível BAIXA)
```

**Lógica:**
- Um candidato só deveria ser compatível com a vaga se tiver todas as competências
- Cada competência tem nível: BAIXA, MÉDIA, ALTA
- Sem duplicação: a mesma competência não pode ser requisito 2x na mesma vaga

**Localização:**
- Definição: [requisito_vaga.py](skillup_banco/domain/entidades/requisito_vaga.py)
- Serviço: [requisito_vaga_service.py](skillup_banco/application/services/requisito_vaga/requisito_vaga_service.py)
- Validação de duplicação: linha 17

---

### Regra 5: Vaga Pertence a uma Empresa
Uma vaga é sempre publicada por uma empresa:

```
Empresa
└── Vagas
    ├─ Vaga 1: "Dev Junior"
    ├─ Vaga 2: "Dev Senior"
    └─ Vaga 3: "Tech Lead"
```

**Implicações:**
- Quando candidato se candidata, a empresa recebe a candidatura
- Empresa é responsável por avaliar e mudar status (ENVIADO → EM_ANALISE → ACEITO/RECUSADO)

**Localização:**
- Vaga: [vaga.py](skillup_banco/domain/entidades/vaga.py#L24)
- Empresa: [empresa.py](skillup_banco/domain/entidades/empresa.py)

---

## 📚 Contexto: Cursos e Capacitação

### Regra 6: Ciclo de Vida da Inscrição em Curso
Uma inscrição em curso tem status binário:

```
InscricaoCurso → { DEFERIDO | INDEFERIDO }
```

**Diferença de Candidatura:**
- Candidatura: tem 5 estados progressivos
- Inscrição: tem 2 estados finais (aceito/rejeitado)

**Localização:**
- Enum: [enums.py](skillup_banco/domain/entidades/enums.py#L30)
- Inscrição: [inscricao_curso.py](skillup_banco/domain/entidades/inscricao_curso.py)

---

### Regra 7: Unicidade de Inscrição por Curso
**Um candidato só pode se inscrever UMA VEZ em um curso específico.**

- Similar à regra de candidatura, mas para cursos
- Previne duplicação de inscrições

**Implementação:**
- Validação: [inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py#L16)

---

### Regra 8: Cursos Podem Ser Oferecidos por Dois Tipos de Instituição

Uma instituição que oferece curso pode ser:

| Tipo | Entidade | Exemplos |
|------|----------|----------|
| **Instituição de Ensino** | `InstituicaoEnsino` | Universidade, Faculdade, Escola Técnica |
| **Empresa** | `Empresa` | Oferecendo treinamento corporativo |

**Lógica:**
- Cursos tem FK obrigatória para `InstituicaoEnsino`
- Cursos tem FK opcional para `Empresa`
- Um curso pode ser oferecido TANTO por instituição quanto empresa, ou apenas instituição

**Implementação:**
- Curso: [curso.py](skillup_banco/domain/entidades/curso.py#L14-L18)

---

### Regra 9: Modalidade de Curso
Como em Vagas, Cursos também têm modalidade:

```
PRESENCIAL | REMOTO | HÍBRIDO
```

**Aplicação:**
- Define como o candidato participará do curso
- Mesmo enum usado em Vagas

**Localização:**
- Curso: [curso.py](skillup_banco/domain/entidades/curso.py#L7)

---

### Regra 10: Competências Requeridas em Cursos
Assim como vagas, cursos exigem competências:

```
Curso "Python Avançado"
└── Competências Requeridas
    ├─ Python (nível MÉDIA)
    ├─ Programação OOP (nível ALTA)
    └─ SQL (nível BAIXA)
```

**Sem duplicação:** mesma competência não pode ser requerida 2x no mesmo curso

**Localização:**
- Definição: [curso_competencia.py](skillup_banco/domain/entidades/curso_competencia.py)
- Serviço: [curso_competencia_service.py](skillup_banco/application/services/curso_competencia/curso_competencia_service.py)

---

## 👤 Contexto: Competências do Candidato

### Regra 11: Candidato Registra Suas Competências
Um candidato pode registrar múltiplas competências que possui:

```
Candidato "João"
└── Competências
    ├─ Java (nível ALTA)
    ├─ Python (nível MÉDIA)
    ├─ Git (nível BAIXA)
    └─ SQL (nível ALTA)
```

**Aplicação:**
- Usado para compatibilidade com vagas (candidato vs requisitos)
- Usado para compatibilidade com cursos (pré-requisitos)

**Localização:**
- Definição: [competencia_candidato.py](skillup_banco/domain/entidades/competencia_candidato.py)
- Serviço: [competencia_candidato_service.py](skillup_banco/application/services/competencia_candidato/competencia_candidato_service.py)

---

## 🏫 Contexto: Organização das Instituições

### Regra 12: Instituição tem Áreas de Ensino
Uma instituição de ensino pode oferecer múltiplas áreas:

```
Universidade X
├── Área: Engenharia
├── Área: Administração
├── Área: Tecnologia
└── Área: Saúde
```

**Sem duplicação:** a mesma área não pode ser associada 2x com a mesma instituição

**Implementação:**
- Tabela de Junção: `InstituicaoAreaEnsino`
- Validação: [instituicao_area_ensino_service.py](skillup_banco/application/services/instituicao_area_ensino/instituicao_area_ensino_service.py#L43)

---

### Regra 13: Áreas de Ensino são Recursos Centralizados
Todas as áreas de ensino são cadastradas uma única vez no sistema:

```
Sistema
└── Áreas de Ensino (Catalog)
    ├─ Engenharia (única)
    ├─ Tecnologia (única)
    ├─ Medicina (única)
    └─ Direito (única)
```

**Cada instituição referencia estas áreas centralizadas** (não cria suas próprias)

**Localização:**
- AreaEnsino: [area_ensino.py](skillup_banco/domain/entidades/area_ensino.py)
- Serviço: [area_ensino_service.py](skillup_banco/application/services/area_ensino/area_ensino_service.py)

---

## 🔗 Fluxos Principais

### Fluxo 1: Candidato se Candidata a uma Vaga

```
1. Candidato acessa lista de Vagas
2. Filtra por Modalidade (PRESENCIAL/REMOTO/etc)
3. Filtra por Tipo (EMPREGO/ESTÁGIO/etc)
4. Visualiza Requisitos de Competência da Vaga
5. Compara com suas Competências
6. CLICA "SE CANDIDATAR"
   └─ Cria Candidatura (status = ENVIADO)
   └─ Registra data atual
   └─ Se já existe comunicação → EXCEÇÃO
7. Empresa recebe candidatura
8. Empresa muda status (ENVIADO → EM_ANALISE → ACEITO/RECUSADO)
```

**Entidades:** Candidato → Candidatura → Vaga → Empresa

---

### Fluxo 2: Candidato se Inscreve em um Curso

```
1. Candidato acessa lista de Cursos
2. Filtra por Modal idade (PRESENCIAL/REMOTO/etc)
3. Visualiza Competências Requeridas do Curso
4. Compara com suas Competências
5. CLICA "SE INSCREVER"
   └─ Cria InscricaoCurso (status = DEFERIDO/INDEFERIDO)
   └─ Registra data atual
   └─ Se já existe comunicação → EXCEÇÃO
6. Instituição/Empresa avalia
7. Atualiza status (DEFERIDO ou INDEFERIDO)
```

**Entidades:** Candidato → InscricaoCurso → Curso → (InstituicaoEnsino ou Empresa)

---

### Fluxo 3: Empresa Publica uma Vaga

```
1. Empresa autenticada acessa admin
2. Preenche dados: Título, Descrição, Modalidade, Tipo, Prazo
3. Adiciona Requisitos (Competências + Níveis)
   └─ Seleciona competência existente
   └─ Define nível (BAIXA/MÉDIA/ALTA)
   └─ Se já existe → EXCEÇÃO
4. Publica vaga
5. Vaga aparece para Candidatos
```

**Entidades:** Empresa → Vaga ⊕ RequisitoVaga + Competencia

---

### Fluxo 4: Instituição Oferece um Curso

```
1. Instituição autenticada acessa admin
2. Preenche dados: Nome, Modalidade, Carga Horária
3. Associa Competências Requeridas
   └─ Seleciona competência
   └─ Define nível (BAIXA/MÉDIA/ALTA)
   └─ Se já existe → EXCEÇÃO
4. (Opcional) Associa Empresa provedora
5. Cria curso
6. Candidatos podem se inscrever
```

**Entidades:** InstituicaoEnsino → Curso ⊕ CursoCompetencia + Competencia + (Empresa?)

---

## 📊 Matriz de Entidades e Relacionamentos

| Entidade Principal | Relacionamentos | Tipo | Cardinalidade |
|---|---|---|---|
| **Candidato** | CompetenciaCandidato | Possui | 1:N |
| **Candidato** | Candidatura | Se candida | 1:N |
| **Candidato** | InscricaoCurso | Se inscreve | 1:N |
| **Vaga** | RequisitoVaga | Exige | 1:N |
| **Vaga** | Candidatura | Recebe | 1:N |
| **Empresa** | Vaga | Publica | 1:N |
| **Empresa** | Curso | Oferece | 1:N (opcional) |
| **Curso** | CursoCompetencia | Exige | 1:N |
| **Curso** | InscricaoCurso | Enrola | 1:N |
| **InstituicaoEnsino** | Curso | Oferece | 1:N |
| **InstituicaoEnsino** | InstituicaoAreaEnsino | Tem | 1:N |
| **AreaEnsino** | InstituicaoAreaEnsino | É Associada | 1:N |
| **Competencia** | CompetenciaCandidato | Possuída | 1:N |
| **Competencia** | RequisitoVaga | Requerida (Vaga) | 1:N |
| **Competencia** | CursoCompetencia | Requerida (Curso) | 1:N |

---

## 🎓 Conceitos Centrais

### Conceito 1: Nível de Proficiência (Ubíquo)
Em 3 contextos diferentes, usamos o MESMO enum de níveis:

```
BAIXA   (conhecimento básico)
MÉDIA   (conhecimento intermediário)
ALTA    (conhecimento avançado)
```

**Contextos:**
1. **CompetenciaCandidato:** nível que o candidato domina
2. **RequisitoVaga:** nível mínimo exigido pela vaga
3. **CursoCompetencia:** nível ensinado/desenvolvido no curso

**Lógica de Compatibilidade:**
- Candidato com "Java MÉDIA" pode preencher vaga que exige "Java BAIXA" ✅
- Candidato com "Java BAIXA" NÃO pode preencher vaga que exige "Java ALTA" ❌

**Localização:** [enums.py](skillup_banco/domain/entidades/enums.py#L16)

---

### Conceito 2: Status Machines

#### **Candidatura (5 estados)**
```
ENVIADO
  ↓
EM_ANALISE
  ↓
├─ ACEITO
├─ RECUSADO
└─ CANCELADO
```

#### **InscricaoCurso (2 estados)**
```
├─ DEFERIDO (aceito)
└─ INDEFERIDO (rejeitado)
```

**Localização:** [enums.py](skillup_banco/domain/entidades/enums.py#L23)

---

### Conceito 3: Modalidade (Compartilhada)
Tanto Vagas quanto Cursos usam:

```
PRESENCIAL  (tudo ao vivo no local)
REMOTO      (tudo online)
HÍBRIDO     (mix presencial + online)
```

**Aplicação:** 
- Filtragem por candidato/estudante
- Planejamento de recursos

**Localização:** [enums.py](skillup_banco/domain/entidades/enums.py#L4)

---

### Conceito 4: Unicidade Transacional
Duas chaves de unicidade impedem duplicação:

1. **Candidato + Vaga = 1 Candidatura**
   - Um candidato não pode se candidatar 2x para mesma vaga

2. **Candidato + Curso = 1 Inscrição**
   - Um candidato não pode se inscrever 2x no mesmo curso

3. **Curso + Competencia = 1 Requisito Competência**
   - Um curso não pode ter a mesma competência 2x como requisito

4. **Vaga + Competencia = 1 Requisito Competência**
   - Uma vaga não pode ter a mesma competência 2x como requisito

5. **InstituicaoEnsino + AreaEnsino = 1 Associação**
   - Uma instituição não pode ter a mesma área 2x

---

## 📝 Sumário de Regras Contextuais

| # | Regra | Tipo | Arquivo Principal |
|---|-------|------|-------------------|
| 1 | Ciclo de vida candidatura (5 estados) | State Machine | [candidatura.py](skillup_banco/domain/entidades/candidatura.py) |
| 2 | Unicidade candidatura por vaga | Constraint | [candidatura_service.py](skillup_banco/application/services/candidatura/candidatura_service.py) |
| 3 | Vaga com modalidade + tipo | Enum | [vaga.py](skillup_banco/domain/entidades/vaga.py) |
| 4 | Requisitos de competência em vagas | Relacionamento | [requisito_vaga.py](skillup_banco/domain/entidades/requisito_vaga.py) |
| 5 | Vaga pertence a empresa | FK | [vaga.py](skillup_banco/domain/entidades/vaga.py) |
| 6 | Ciclo de vida inscrição (2 estados) | State Machine | [inscricao_curso.py](skillup_banco/domain/entidades/inscricao_curso.py) |
| 7 | Unicidade inscrição por curso | Constraint | [inscricao_curso_service.py](skillup_banco/application/services/inscricao_curso/inscricao_curso_service.py) |
| 8 | Curso oferecido por instituição/empresa | FK | [curso.py](skillup_banco/domain/entidades/curso.py) |
| 9 | Curso com modalidade | Enum | [curso.py](skillup_banco/domain/entidades/curso.py) |
| 10 | Competências requeridas em cursos | Relacionamento | [curso_competencia.py](skillup_banco/domain/entidades/curso_competencia.py) |
| 11 | Candidato registra competências | Relacionamento | [competencia_candidato.py](skillup_banco/domain/entidades/competencia_candidato.py) |
| 12 | Instituição tem áreas de ensino | Relacionamento | [instituicao_ensino.py](skillup_banco/domain/entidades/instituicao_ensino.py) |
| 13 | Áreas são recursos centralizados | Pattern | [area_ensino.py](skillup_banco/domain/entidades/area_ensino.py) |

---

## 🚀 Fluxos de Desenvolvimento

### Para Implementar uma Nova Feature:

**Matchmaking Candidato-Vaga:**
- Comparar competências do candidato vs requisitos da vaga
- Usar níveis de proficiência para scoring
- Arquivos: Regra 11 + Regra 4

**Dashboard de Vagas Ativas:**
- Filtrar por modalidade (Regra 3)
- Filtrar por tipo (Regra 3)
- Listar candidatos por vaga (Regra 2)
- Arquivos: Regra 3 + Regra 5

**Gerenciamento de Status:**
- Transição de estados em Candidatura (Regra 1)
- Transição de estados em Inscrição (Regra 6)
- Validações de regra de negócio

---

**Fim do Documento Reduzido**

