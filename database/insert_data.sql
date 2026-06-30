TRUNCATE TABLE medico_especialidade RESTART IDENTITY CASCADE;
TRUNCATE TABLE medico RESTART IDENTITY CASCADE;
TRUNCATE TABLE especialidade RESTART IDENTITY CASCADE;
TRUNCATE TABLE paciente RESTART IDENTITY CASCADE;

INSERT INTO paciente (
    nome_completo,
    cpf,
    data_nascimento,
    email,
    senha
)
VALUES
('Ana Clara Martins', '111.111.111-11', '2000-05-10', 'ana.clara@email.com', '123456'),
('João Pedro Silva', '222.222.222-22', '1998-08-20', 'joao.pedro@email.com', '123456'),
('Mariana Costa Lima', '333.333.333-33', '2002-01-15', 'mariana.costa@email.com', '123456'),
('Carlos Henrique Sousa', '444.444.444-44', '1995-11-03', 'carlos.sousa@email.com', '123456'),
('Fernanda Ribeiro Alves', '555.555.555-55', '2001-03-28', 'fernanda.ribeiro@email.com', '123456'),
('Lucas Gabriel Oliveira', '666.666.666-66', '1999-07-12', 'lucas.oliveira@email.com', '123456'),
('Beatriz Santos Rocha', '777.777.777-77', '2003-09-05', 'beatriz.rocha@email.com', '123456'),
('Rafael Almeida Pereira', '888.888.888-88', '1997-12-19', 'rafael.pereira@email.com', '123456'),
('Camila Ferreira Gomes', '999.999.999-99', '2004-04-22', 'camila.gomes@email.com', '123456'),
('Eduardo Nunes Carvalho', '000.000.000-00', '1996-06-30', 'eduardo.carvalho@email.com', '123456');

INSERT INTO especialidade (nome_especialidade)
VALUES
('Clínico Geral'),
('Cardiologia'),
('Dermatologia'),
('Pediatria'),
('Neurologia'),
('Ortopedia'),
('Ginecologia'),
('Psiquiatria'),
('Endocrinologia'),
('Oftalmologia');

INSERT INTO medico (
    nome_completo,
    crm
)
VALUES
('Dra. Mariana Almeida Costa', 'CRM-CE 10001'),
('Dr. Rafael Henrique Lima', 'CRM-CE 10002'),
('Dra. Camila Ferreira Rocha', 'CRM-CE 10003'),
('Dr. Lucas Martins Oliveira', 'CRM-CE 10004'),
('Dra. Beatriz Santos Nunes', 'CRM-CE 10005'),
('Dr. Carlos Eduardo Pereira', 'CRM-CE 10006'),
('Dra. Fernanda Ribeiro Gomes', 'CRM-CE 10007'),
('Dr. João Pedro Carvalho', 'CRM-CE 10008'),
('Dra. Ana Paula Sousa', 'CRM-CE 10009'),
('Dr. Eduardo Nunes Batista', 'CRM-CE 10010');

INSERT INTO medico_especialidade (
    id_medico,
    id_especialidade
)
VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);