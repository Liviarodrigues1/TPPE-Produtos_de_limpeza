CREATE DATABASE Ecommerce;
USE Ecommerce;

CREATE TABLE Produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    preco FLOAT,
    estoque INT,
    imagem VARCHAR(255),
    categoria VARCHAR(100)
);

CREATE TABLE Cliente (
    id INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE Carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id)
);

CREATE TABLE CarrinhoProduto (
    carrinho_id INT,
    produto_id INT,
    quantidade INT,
    PRIMARY KEY (carrinho_id, produto_id),
    FOREIGN KEY (carrinho_id) REFERENCES Carrinho(id),
    FOREIGN KEY (produto_id) REFERENCES Produto(id)
);

CREATE TABLE Pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    valorTotal FLOAT,
    status VARCHAR(50),
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id)
);

CREATE TABLE PedidoProduto (
    pedido_id INT,
    produto_id INT,
    quantidade INT,
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES Pedido(id),
    FOREIGN KEY (produto_id) REFERENCES Produto(id)
);

CREATE TABLE Pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    metodo VARCHAR(50),
    valor FLOAT,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(id)
);

CREATE TABLE Gestor (
    id INT AUTO_INCREMENT PRIMARY KEY
);