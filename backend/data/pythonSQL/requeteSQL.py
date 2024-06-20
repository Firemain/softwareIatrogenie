# Ce fichier regroupe l'ensemble des fonctions qui permettent d'agir et de retourner des résultats depuis la base de données
from flask import Flask, request, jsonify, render_template
import sqlite3
import os

def execute_query(query, params=None):
    """
    Exécute une requête SQL sur la base de données.

    Args:
        query (str): La requête SQL à exécuter.
        params (tuple): Les paramètres à utiliser dans la requête (par défaut None).

    Returns:
        list: Résultat de la requête.
    """
    # Obtenez le chemin absolu du répertoire courant
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Remontez d'un cran dans l'arborescence pour obtenir le répertoire parent
    parent_directory = os.path.dirname(current_directory)

    # Remontez d'un cran supplémentaire pour atteindre le répertoire contenant la base de données
    database_directory = os.path.join(parent_directory, 'data')

    # Construisez le chemin complet vers la base de données
    db_path = os.path.join(database_directory, 'iatroDataBase.db')
    print("Chemin de la base de données :", db_path)

    # Utilisez une chaîne brute pour éviter les échappements Unicode
    db_path = r"C:\Users\87fug\Documents\Lille\iatrogenie\logiciel_iatrogenie_v6\logiciel_iatrogenie\backend\data\iatroDataBase.db"
    connection = sqlite3.connect(db_path)    
    cursor = connection.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        connection.commit()
        return result
    finally:
        cursor.close()
        connection.close()

def getAllPatient():
    """
    Récupère toutes les données des patients avec le nombre de traitements dans la base de données.

    Returns:
        list: Liste des patients avec le nombre de traitements.
    """
    query = """
        SELECT patients.id_patient, patients.nom, patients.prenom, patients.sexe, patients.age, patients.date_admission, COUNT(traitements.id_traitement) as nombre_traitements
        FROM patients
        LEFT JOIN traitements ON patients.id_patient = traitements.id_patient
        GROUP BY patients.id_patient, patients.nom, patients.prenom, patients.sexe, patients.age, patients.date_admission
        ORDER BY patients.id_patient;
    """
    return execute_query(query)
    
def getStringPatient(part_name):
    """
    Récupère les patients dont le nom commence par part_name.

    Args:
        part_name (str): Le nom du patient.

    Returns:
        list: Résultat de la requête pour les patients correspondants.
    """
    query = "SELECT * FROM realpatient WHERE Nom LIKE ?"
    params = (f'{part_name}%',)
    return execute_query(query, params)

def getAllRules():
    """
    Récupère toutes les règles dans la base de données.

    Returns:
        list: Liste des règles.
    """
    query = "SELECT * FROM rules"
    return execute_query(query)

def getMedecinsSQL():
    """
    Récupère toutes les alertes dans la base de données.

    Returns:
        list: Liste des alertes.
    """
    query = "SELECT * FROM medecin"
    return execute_query(query)

def getAllAlertes():
    """
    Récupère toutes les alertes dans la base de données.

    Returns:
        list: Liste des alertes.
    """
    query = "SELECT * FROM alertes"
    return execute_query(query)

def addNewRule(ruleSet):
    """
    Ajoute une nouvelle règle dans la base de données.

    Args:
        ruleSet (dict): Dictionnaire contenant les détails de la règle.

    Returns:
        dict: Message indiquant le succès de l'ajout de la règle.
    """
    nom_table = "rules"

    principeActif1 = ruleSet['principeActif1']
    codeATC1 = ruleSet['codeATC1']
    principeActif2 = ruleSet['principeActif2']
    codeATC2 = ruleSet['codeATC2']
    niveauRisque = ruleSet['niveauRisque']

    requete_insertion = f"INSERT INTO {nom_table} (principe1, codeATC1, principe2, codeATC2, risque) VALUES (?, ?, ?, ?, ?)"

    execute_query(requete_insertion, (principeActif1, codeATC1, principeActif2, codeATC2, niveauRisque))

    return {'message': 'Règle ajoutée avec succès'}

def addNewPatient(PatientSet):
    """
    Ajoute une nouvelle règle dans la base de données.

    Args:
        PatientSet (dict): Dictionnaire contenant les détails du patient.

    Returns:
        dict: Message indiquant le succès de l'ajout de la règle.
    """
    nom_table = "patients"

    nom = PatientSet['nom']
    prenom = PatientSet['prenom']
    sexe = PatientSet['sexe']
    age = PatientSet['age']
    date_admission = PatientSet['date_admission']

    

    requete_insertion = f"INSERT INTO {nom_table} ( nom, prenom, sexe, age, date_admission) VALUES (?, ?, ?, ?, ?)"

    execute_query(requete_insertion, (nom, prenom, sexe, age, date_admission ))

    return {'message': 'Patient ajouté avec succès'}

def addNewTraitement(TraitementSet):
    """
    Ajoute une nouvelle règle dans la base de données.

    Args:
        TraitementSet (dict): Dictionnaire contenant les détails du patient.

    Returns:
        dict: Message indiquant le succès de l'ajout de la règle.
    """
    nom_table = "traitements"

    id_patient = TraitementSet.get('id_patient', None)
    code_traitement = TraitementSet.get('code_traitement', None)
    dose = TraitementSet.get('dose', None)
    date_debut = TraitementSet.get('date_debut', None)
    date_fin = TraitementSet.get('date_fin', None)


    requete_insertion = f"INSERT INTO {nom_table} (id_patient, code_traitement, dose, date_debut, date_fin) VALUES (?, ?, ?, ?, ?)"

    execute_query(requete_insertion, (id_patient, code_traitement, dose, date_debut, date_fin))

    return {'message': 'Traitement ajouté avec succès'}

def addNewAlerte(AlerteSet, iatroData):
    """
    Ajoute une nouvelle alerte dans la base de données.

    Args:
        AlerteSet (dict): Dictionnaire contenant les détails de l'alerte.
        iatroData (dict): Dictionnaire contenant les données de l'alerte.

    Returns:
        dict: Message indiquant le succès de l'ajout de l'alerte.
    """
    nom_table = "alertes"


    id_patient = AlerteSet.get('id_patient', None)
    nom_patient = AlerteSet.get('nom_patient', None)
    age_patient = AlerteSet.get('age_patient', None)
    sexe_patient = AlerteSet.get('sexe_patient', None)
    code_iatrogenique = AlerteSet.get('code_iatrogenique', None)
    date = AlerteSet.get('date', None)
    gestion = AlerteSet.get('gestion', None)

    # Insérer l'alerte dans la table "alertes"
    requete_insertion = f"INSERT INTO {nom_table} (id_patient, nom_patient, age_patient, sexe_patient, code_iatrogenique, date, gestion) VALUES (?, ?, ?, ?, ?, ?, ?)"
    execute_query(requete_insertion, (id_patient, nom_patient, age_patient, sexe_patient, code_iatrogenique, date, gestion))

    return {'message': 'Alerte ajoutée avec succès'}

def getTraitementsByIdPatient(id_patient):
    """
    Récupère l'ensemble des traitements d'un patient.

    Args:
        id_patient (int): ID du patient pour lequel récupérer les traitements.

    Returns:
        list: Liste des traitements du patient.
    """
    nom_table = "traitements"

    requete_selection = f"SELECT * FROM {nom_table} WHERE id_patient = ?"
    resultats = execute_query(requete_selection, (id_patient,))

    traitements = []
    for row in resultats:
        traitement = {
            "id_traitement": row[0],
            "id_patient": row[1],
            "code_traitement": row[2],
            "dose": row[3],
            "date_debut": row[4],
            "date_fin": row[5],
        }
        traitements.append(traitement)

    return traitements