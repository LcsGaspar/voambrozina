CREATE table inscricoes(
    id_inscricao INT NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(200),
	email VARCHAR(60),
	telefone VARCHAR(15),
	data_nascimento DATE,
	cep VARCHAR(9),
	rua VARCHAR(200),
	numero INTEGER,
	cidade VARCHAR(200),
	estado VARCHAR(2),
	oficina INTEGER,
	mensagem TEXT,
	criado DATETIME,
	PRIMARY KEY (id_inscricao)
);

create table usuarios(
	id INT AUTO_INCREMENT,
	email VARCHAR(50),
	senha VARCHAR(300),
	criado DATETIME,
	PRIMARY KEY(id)
);