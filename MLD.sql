CREATE TABLE Utilisateur (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    mot_de_passe VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE meteo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    temperature DECIMAL(5,2),
    humidite DECIMAL(5,2),
    pluie_mm DECIMAL(6,2)
);

CREATE TABLE Parcelles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100),
    localisation VARCHAR(255),
    surface_ha DECIMAL(8,2),
    utilisateur_id INT NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
);

CREATE TABLE Cultures (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(100),
    date_semis DATE,
    parcelle_id INT NOT NULL,
    FOREIGN KEY (parcelle_id) REFERENCES Parcelles(id)
);

CREATE TABLE observations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    etat VARCHAR(100),
    commentaire TEXT,
    utilisateur_id INT NOT NULL,
    meteo_id INT NOT NULL,
    parcelle_id INT NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id),
    FOREIGN KEY (meteo_id) REFERENCES meteo(id),
    FOREIGN KEY (parcelle_id) REFERENCES Parcelles(id)
);

CREATE TABLE alertes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    type VARCHAR(100),
    niveau VARCHAR(50),
    parcelle_id INT NOT NULL,
    observation_id INT NULL,
    FOREIGN KEY (parcelle_id) REFERENCES Parcelles(id),
    FOREIGN KEY (observation_id) REFERENCES observations(id)
);