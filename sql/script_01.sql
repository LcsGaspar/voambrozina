create table usuarios(
	id INT AUTO_INCREMENT,
	email VARCHAR(50),
	senha VARCHAR(300),
	criado DATETIME,
	PRIMARY KEY(id)
);

INSERT INTO usuarios (email, senha) VALUES ('admin@admin.com.br', '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435f5');

CREATE table inscricoes(
    id_inscricao INT NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(200),
	email VARCHAR(60),
	telefone VARCHAR(15),
	data_nascimento DATE,
	cep VARCHAR(9),
	rua VARCHAR(200),
	numero INTEGER,
    bairro varchar(100),
	cidade VARCHAR(200),
	estado VARCHAR(2),
	oficina INTEGER,
	mensagem TEXT,
	criado DATETIME,
	PRIMARY KEY (id_inscricao)
);

create table oficinas(
	id_oficina INT NOT NULL AUTO_INCREMENT,
	nome_oficina varchar(100),
	PRIMARY KEY(id_oficina)
);

INSERT INTO oficinas (id_oficina, nome_oficina) values (1, 'Informática'), (2, 'Clubinho de Inglês'), (3, 'Educação Ambiental'), (4, 'Inclusão Digital'), (5, 'Pequeninos'), (6, 'Mundo Digital'), (7, 'Projeto de vida')