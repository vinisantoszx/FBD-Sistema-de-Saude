TRUNCATE TABLE exame RESTART IDENTITY CASCADE;
TRUNCATE TABLE medico_especialidade RESTART IDENTITY CASCADE;
TRUNCATE TABLE medico RESTART IDENTITY CASCADE;
TRUNCATE TABLE especialidade RESTART IDENTITY CASCADE;
TRUNCATE TABLE tipo_exame RESTART IDENTITY CASCADE;
TRUNCATE TABLE instituicao_saude RESTART IDENTITY CASCADE;
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

INSERT INTO instituicao_saude (
    cnpj,
    endereco,
    nome_fantasia
)
VALUES
('11.111.111/0001-11', 'Rua das Flores, 100 - Centro', 'Clínica Vida Plena'),
('22.222.222/0001-22', 'Av. Saúde, 250 - Centro', 'Hospital São Lucas'),
('33.333.333/0001-33', 'Rua Esperança, 45 - Bairro Novo', 'Laboratório Diagnóstico Norte'),
('44.444.444/0001-44', 'Av. Brasil, 890 - Centro', 'Clínica Popular Saúde'),
('55.555.555/0001-55', 'Rua São José, 310 - Alto Alegre', 'Centro Médico Bem Estar'),
('66.666.666/0001-66', 'Av. Universitária, 1200 - Planalto', 'Laboratório Imagem Mais'),
('77.777.777/0001-77', 'Rua Padre Cícero, 72 - Centro', 'Hospital Municipal Esperança'),
('88.888.888/0001-88', 'Av. Dom Pedro, 510 - Lagoa Seca', 'Clínica Santa Clara'),
('99.999.999/0001-99', 'Rua do Comércio, 215 - Centro', 'Instituto Saúde Integral'),
('00.000.000/0001-00', 'Av. Central, 999 - Cidade Nova', 'Laboratório Vida Diagnóstica');

INSERT INTO tipo_exame (
    nome_tipo,
    categoria
)
VALUES
('Hemograma Completo', 'Laboratorial'),
('Glicemia em Jejum', 'Laboratorial'),
('Colesterol Total', 'Laboratorial'),
('Raio-X de Tórax', 'Imagem'),
('Ultrassonografia Abdominal', 'Imagem'),
('Eletrocardiograma', 'Cardiológico'),
('Ressonância Magnética', 'Imagem'),
('Tomografia Computadorizada', 'Imagem'),
('Exame de Urina', 'Laboratorial'),
('Teste Ergométrico', 'Cardiológico');

INSERT INTO exame (
    data_realizacao,
    laudo,
    id_paciente,
    id_tipo,
    id_instituicao
)
VALUES
('2026-01-10', 'Resultados dentro dos parâmetros de normalidade.', 1, 1, 1),
('2026-01-15', 'Glicemia levemente alterada. Recomenda-se acompanhamento.', 2, 2, 2),
('2026-02-02', 'Colesterol total acima do valor de referência.', 3, 3, 3),
('2026-02-18', 'Imagem sem alterações pulmonares significativas.', 4, 4, 4),
('2026-03-05', 'Ultrassonografia sem achados relevantes.', 5, 5, 5),
('2026-03-22', 'Ritmo sinusal regular no momento do exame.', 6, 6, 6),
('2026-04-08', 'Exame de imagem sem sinais de lesão aguda.', 7, 7, 7),
('2026-04-25', 'Tomografia sem alterações estruturais relevantes.', 8, 8, 8),
('2026-05-11', 'Exame de urina com parâmetros preservados.', 9, 9, 9),
('2026-05-30', 'Boa resposta ao esforço, sem alterações significativas.', 10, 10, 10);
