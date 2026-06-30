# Sistema de Monitoramento Colaborativo de Saúde

Sistema desenvolvido como projeto da disciplina de **Fundamentos de Banco de Dados**, com o objetivo de aplicar conceitos de modelagem relacional, criação de banco de dados, povoamento de tabelas e desenvolvimento de uma aplicação com operações de CRUD integradas ao PostgreSQL.

O projeto simula um sistema de saúde colaborativo, permitindo o gerenciamento de pacientes, médicos e demais entidades relacionadas ao acompanhamento e atendimento em saúde.

---

## Tecnologias utilizadas

- Python
- Panel
- Pandas
- PostgreSQL
- SQLAlchemy
- psycopg2
- python-dotenv
- Git e GitHub

---

## Funcionalidades implementadas

### Pacientes

A tela de pacientes permite:

- Cadastrar pacientes;
- Listar pacientes cadastrados;
- Carregar dados para edição;
- Atualizar informações do paciente;
- Excluir pacientes do banco de dados.

Campos utilizados:

- ID do paciente;
- Nome completo;
- CPF;
- Data de nascimento;
- E-mail;
- Senha.

### Médicos

A tela de médicos permite:

- Cadastrar médicos;
- Listar médicos cadastrados;
- Associar médicos a especialidades;
- Editar dados de médicos;
- Excluir médicos do banco de dados.

Campos utilizados:

- ID do médico;
- Nome completo;
- CRM;
- Especialidades.

---

## Estrutura do projeto

```text
FBD-Sistema-de-Saude/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── database/
│   ├── create_tables.sql
│   └── insert_data.sql
│
└── src/
    ├── __init__.py
    ├── database.py
    │
    ├── pages/
    │   ├── __init__.py
    │   ├── paciente_page.py
    │   └── medico_page.py
    │
    └── repositories/
        ├── __init__.py
        ├── paciente_repository.py
        └── medico_repository.py
