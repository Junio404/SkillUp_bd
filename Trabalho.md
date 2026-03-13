# Especificação do Trabalho Prático 2: Disciplina de Banco de Dados

## 1. Objetivo Geral
Conduzir os estudantes, em grupos, pela etapa de implementação e consolidação de um projeto de banco de dados previamente modelado. O foco é implementar o esquema em SQL a partir de um modelo relacional na 3ª Forma Normal (3FN) e integrá-lo a uma aplicação desenvolvida em Python.

---

## 2. Requisitos Educacionais Obrigatórios
* **SGBDs Permitidos:** MySQL, PostgreSQL, Oracle ou Microsoft SQL Server.
* **Implementação SQL:**
    * Definição de tipos de dados, chaves primárias (PK), chaves estrangeiras (FK) e restrições de integridade (NOT NULL, UNIQUE, CHECK).
    * O banco deve ser funcional por meio de um **script único** de criação.
* **Integração com Python:**
    * A aplicação deve executar operações de CRUD usando **SQL puro**.
    * **Proibido:** o uso de bibliotecas de ORM (como SQLAlchemy ou Django ORM).
* **Operações do Sistema mínimas para tirar um 7:**
    * **Inserção:** em pelo menos 3 tabelas (sendo 1 obrigatoriamente associativa N:N).
    * **Consulta:** no mínimo 6 consultas distintas (3 parametrizáveis e 1 com múltiplos parâmetros).
    * **Atualização:** em pelo menos 1 tabela.
* **Interface:** livre escol    ha (CLI, Desktop, Web ou Mobile). Se for via linha de comando, deve possuir menus estruturados e navegáveis.

---

## 3. Formação dos Grupos e Repositório
* **Tamanho do Grupo:** entre 5 e 6 estudantes.
* **Fusão:** preferencialmente formados pela fusão de 2 grupos da etapa anterior, escolhendo um tema único entre eles.
* **GitLab:** os scripts, códigos e instruções devem ser adicionados ao repositório público utilizado no trabalho anterior.

---

## 4. Entrega e Apresentação
* **Formato:** presencial em sala de aula.
* **Tempo:** entre 12 e 15 minutos por grupo.
* **Conteúdo da Apresentação:**
    * Ajustes realizados no modelo anterior para adequação às regras de negócio.
    * Demonstração do SGBD com tabelas criadas e povoamento com tuplas de teste.
    * Explicação técnica da conexão entre a aplicação Python e o banco de dados.
    * Evidência (vídeo ou ao vivo) das operações de inserção, consulta e atualização.

---

## 5. Critérios de Avaliação
* Aprofundamento teórico e técnico.
* Corretude e robustez do sistema.
* Uso adequado dos recursos obrigatórios.
* Organização do repositório Git.