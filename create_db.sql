CREATE DATABASE IF NOT EXISTS db_imoveis 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
    
USE db_imoveis; 

CREATE TABLE tb_imoveis(
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    preco FLOAT(20),
    metragem VARCHAR(10),
    quartos VARCHAR(2),
    suites VARCHAR(2),
    descricao VARCHAR(255),
	link VARCHAR(255)
)
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



    