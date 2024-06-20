-- Configuration générale
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

-- Création de la table rules
CREATE TABLE IF NOT EXISTS `rules` (
  `principe1` text NOT NULL,
  `codeATC1` text NOT NULL,
  `principe2` text NOT NULL,
  `codeATC2` text NOT NULL,
  `risque` text NOT NULL
);


-- Création de la table des patients
CREATE TABLE IF NOT EXISTS `patients` (
  `id_patient` INTEGER PRIMARY KEY,
  `nom` TEXT NOT NULL,
  `prenom` TEXT NOT NULL,
  `sexe` TEXT NOT NULL,
  `age` INTEGER NOT NULL,
  `date_admission` DATE NOT NULL
);


-- Création de la table des traitements
CREATE TABLE IF NOT EXISTS `traitements` (
  `id_traitement` INTEGER PRIMARY KEY,
  `id_patient` INTEGER,
  `code_traitement` TEXT NOT NULL,
  `dose` TEXT NOT NULL,
  `date_debut` DATE NOT NULL,
  `date_fin` DATE NOT NULL,
  FOREIGN KEY (`id_patient`) REFERENCES `patients` (`id_patient`)
);

-- Création de la table alertes
CREATE TABLE IF NOT EXISTS `alertes` (
  `id_alerte` INTEGER PRIMARY KEY,
  `id_patient` INTEGER,
  `nom_patient` TEXT NOT NULL,
  `age_patient` INTEGER NOT NULL,
  `sexe_patient` TEXT NOT NULL,
  `code_iatrogenique` INTEGER CHECK (code_iatrogenique BETWEEN 0 AND 5) NOT NULL,
  `date` DATE NOT NULL,
  `gestion` TEXT, -- Le nom du médecin ou "à gérer"
  FOREIGN KEY (`id_patient`) REFERENCES `patients` (`id_patient`)
);

-- Création de la table medecin
CREATE TABLE IF NOT EXISTS `medecin` (
  `id_medecin` INTEGER PRIMARY KEY,
  `nom` TEXT NOT NULL,
  `prenom` TEXT NOT NULL,
  `specialite` TEXT NOT NULL
);

-- -- Exemples de données pour la table medecin
-- INSERT INTO `medecin` (`nom`, `prenom`, `specialite`) VALUES
--   ('Dupont', 'Jean', 'Cardiologue'),
--   ('Martin', 'Marie', 'Pédiatre'),
--   ('Durand', 'Pierre', 'Chirurgien');


-- --- Insertion des patients
-- INSERT INTO patients (nom, prenom, sexe, age, date_admission) VALUES
--     ('Dupont', 'Franck', 'Homme', 45, '2023-01-01'),
--     ('Durand', 'Elisa', 'Femme', 32, '2023-02-15'),
--     ('Lefevre', 'Claude', 'Homme', 55, '2023-03-10'),
--     ('Martin', 'Gouret', 'Femme', 28, '2023-04-05');

-- -- Ajouter des traitements pour le patient 1
-- INSERT INTO traitements (id_patient, code_traitement, dose, date_debut, date_fin) VALUES
--     (1, 'ABATACEPT', 'Dose1', '2023-01-01', '2023-02-01'),
--     (1, 'ABIRATERONE', 'Dose2', '2023-02-15', '2023-03-15'),
--     (1, 'ACETAZOLAMIDE', 'Dose3', '2023-03-10', '2023-04-10'),
--     (1, 'AMLODIPINE', 'Dose4', '2023-04-05', '2023-05-05'),
--     (1, 'ASPIRIN', 'Dose5', '2023-05-20', '2023-06-20');

-- -- Ajouter des alertes pour le patient 2
-- INSERT INTO alertes (id_patient, nom_patient, age_patient, sexe_patient, code_iatrogenique, date, gestion) VALUES
--     (2, 'Durand Elisa', 32, 'Femme', 4, '2024-01-12', 'Dr. Dupuis');

-- -- Ajouter des alertes pour le patient 3
-- INSERT INTO alertes (id_patient, nom_patient, age_patient, sexe_patient, code_iatrogenique, date, gestion) VALUES
--     (3, 'Lefevre Claude', 55, 'Homme', 0, '2024-01-15', NULL);

-- -- Ajouter des traitements pour le patient 3
-- INSERT INTO traitements (id_patient, code_traitement, dose, date_debut, date_fin) VALUES
--     (3, 'AMLODIPINE', 'Dose1', '2023-01-01', '2023-02-01'),
--     (3, 'APREPITANT', 'Dose2', '2023-02-15', '2023-03-15');

-- -- Ajouter des alertes pour le patient 4
-- INSERT INTO alertes (id_patient, nom_patient, age_patient, sexe_patient, code_iatrogenique, date, gestion) VALUES
--     (4, 'Martin Gouret', 28, 'Femme', 3, '2024-01-20', 'Dr. Dupont');



-- -- Insérer des données dans la table rules
-- INSERT INTO rules (principe1, codeATC1, principe2, codeATC2, risque) VALUES
--   ('ABROCITINIB', 'D11AH08', 'FLUCONAZOLE', 'J02AC01', 'PE'),
--   ('ABROCITINIB', 'D11AH08', 'FLUVOXAMINE', 'N06AB08', 'PE'),
--   ('ACETAZOLAMIDE', 'S01EC01', 'ACIDE ACETYLSALICYLIQUE', 'S01AD03', 'ASDEC'),
--   ('ACETAZOLAMIDE', 'S01EC01', 'CARBAMAZEPINE', 'N03AF01', 'PE'),
--   ('ACETAZOLAMIDE', 'S01EC01', 'LITHIUM', 'N05AN01', 'PE'),
--   ('ACIDE ACETOHYDROXAMIQUE', 'S01AD03', 'FER', 'G01AF12', 'APEC'),
--   ('ACIDE ACETYLSALICYLIQUE', 'S01AD03', 'ACETAZOLAMIDE', 'S01EC01', 'ASDEC'),
--   ('AMLODIPINE', 'C08CA01', 'LOSARTAN', 'C09CA01', 'PE'),
--   ('ATENOLOL', 'C07AB03', 'IBUPROFEN', 'M01AE01', 'ASDEC'),
--   ('CARBAMAZEPINE', 'N03AF01', 'DILTIAZEM', 'C08DB01', 'PE'),
--   ('LEVOTHYROXINE', 'H03AA01', 'METFORMIN', 'A10BA02', 'CI'),
--   ('METHOTREXATE', 'L01BA01', 'RANITIDINE', 'A02BA02', 'ASDEC');


-- Fin de la transaction
COMMIT;
PRAGMA foreign_keys=on;
