CREATE DATABASE IF NOT EXISTS monitoramento_ambiental
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE monitoramento_ambiental;

CREATE TABLE IF NOT EXISTS dispositivos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(64) NOT NULL UNIQUE,
    localizacao VARCHAR(255),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS leituras_sensores (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    dispositivo_id INT UNSIGNED NOT NULL,
    temperatura DECIMAL(5,2) ,
    umidade DECIMAL(5,2),
    valorAr INT NOT NULL,
    qualidadeArStatus VARCHAR(50) NOT NULL,
	luminosidade INT NOT NULL,
    precipitacao DECIMAL(6,2) NOT NULL,
    pressao DECIMAL(7,2) NOT NULL,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    

    CONSTRAINT fk_leitura_dispositivo
      FOREIGN KEY (dispositivo_id)
      REFERENCES dispositivos(id),

    INDEX idx_data_hora (criado_em),
    INDEX idx_dispositivo_data (dispositivo_id, criado_em)
) ENGINE=InnoDB;

INSERT INTO dispositivos (nome, codigo, localizacao)
VALUES ('Estacao 01', 'ESP32-001', 'UNIP');