
-- Banco de Dados: Gestao de Pedal

-- =============================
-- TABELA: bikers
-- =============================
CREATE TABLE bikers (
    id_biker INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    tipo_bike ENUM('MTB', 'SPEED', 'E-BIKE') NOT NULL,
    pedais_participa SET('3A', '5A') NOT NULL,
    participa_trilha BOOLEAN NOT NULL,
    problema_saude BOOLEAN NOT NULL,
    descricao_problema_saude VARCHAR(255) NULL
);

-- =============================
-- TABELA: contatos_emergencia
-- =============================
CREATE TABLE contatos_emergencia (
    id_contato INT AUTO_INCREMENT PRIMARY KEY,
    id_biker INT NOT NULL,
    nome_contato VARCHAR(150) NOT NULL,
    grau_parentesco VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_biker) REFERENCES bikers(id_biker) ON DELETE CASCADE
);

-- =============================
-- EXEMPLOS DE CADASTROS
-- =============================

-- Inserindo biker
INSERT INTO bikers 
(nome, tipo_bike, pedais_participa, participa_trilha, problema_saude, descricao_problema_saude)
VALUES 
('João Silva', 'MTB', '3A,5A', TRUE, TRUE, 'Asma leve'),
('Carla Mendes', 'SPEED', '5A', FALSE, FALSE, NULL);

-- Inserindo contatos de emergência
INSERT INTO contatos_emergencia (id_biker, nome_contato, grau_parentesco, telefone)
VALUES
(1, 'Maria Silva', 'Esposa', '(11) 99999-9999'),
(2, 'José Mendes', 'Pai', '(11) 98888-8888');
