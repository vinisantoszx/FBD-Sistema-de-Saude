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