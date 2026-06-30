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