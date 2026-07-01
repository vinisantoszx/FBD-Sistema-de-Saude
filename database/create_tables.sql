CREATE TABLE IF NOT EXISTS paciente (
    id_paciente SERIAL PRIMARY KEY,
    nome_completo VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS medico (
    id_medico SERIAL PRIMARY KEY,
    nome_completo VARCHAR(150) NOT NULL,
    crm VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS especialidade (
    id_especialidade SERIAL PRIMARY KEY,
    nome_especialidade VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS medico_especialidade (
    id_medico INTEGER NOT NULL,
    id_especialidade INTEGER NOT NULL,

    PRIMARY KEY (id_medico, id_especialidade),

    CONSTRAINT fk_medico_especialidade_medico
        FOREIGN KEY (id_medico)
        REFERENCES medico (id_medico)
        ON DELETE CASCADE,

    CONSTRAINT fk_medico_especialidade_especialidade
        FOREIGN KEY (id_especialidade)
        REFERENCES especialidade (id_especialidade)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS instituicao_saude (
    id_instituicao SERIAL PRIMARY KEY,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    endereco VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_exame (
    id_tipo SERIAL PRIMARY KEY,
    nome_tipo VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS exame (
    id_exame SERIAL PRIMARY KEY,
    data_realizacao DATE NOT NULL,
    laudo TEXT,
    id_paciente INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL,
    id_instituicao INTEGER NOT NULL,
    
    CONSTRAINT fk_exame_paciente FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente) ON DELETE CASCADE,
    CONSTRAINT fk_exame_tipo FOREIGN KEY (id_tipo) REFERENCES tipo_exame (id_tipo) ON DELETE CASCADE,
    CONSTRAINT fk_exame_instituicao FOREIGN KEY (id_instituicao) REFERENCES instituicao_saude (id_instituicao) ON DELETE CASCADE
);