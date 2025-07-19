DROP DATABASE IF EXISTS ProdutosLimpeza;
CREATE DATABASE IF NOT EXISTS ProdutosLimpeza;
USE ProdutosLimpeza;
CREATE TABLE Produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL
);
CREATE TABLE Cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20)
);
CREATE TABLE Carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT UNIQUE,
    produto_id INT,
    quantidade INT NOT NULL DEFAULT 1,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES Produto(id) ON DELETE CASCADE
);
CREATE TABLE Pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    produto_id INT,
    quantidade INT NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10, 2),
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES Produto(id) ON DELETE CASCADE
);
CREATE TABLE Pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    metodo ENUM('cartao_credito', 'boleto', 'pix'),
    valor DECIMAL(10, 2),
    FOREIGN KEY (pedido_id) REFERENCES Pedido(id) ON DELETE CASCADE
);