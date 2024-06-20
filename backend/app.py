from flask import Flask, request, jsonify
from data.pythonSQL.requeteSQL import *

from python_backend.iatroSearch import *




import subprocess
import sqlite3
import os


# Obtenez le chemin absolu du répertoire courant (répertoire de app.py)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin complet vers le fichier SQL
database_sql_path = os.path.join(current_directory, 'data', 'iatroDataBase.sql')

# Connexion à la base de données SQLite
connection = sqlite3.connect(os.path.join(current_directory, 'data', 'iatroDataBase.db'))

# Créer un objet curseur pour exécuter des requêtes SQL
cursor = connection.cursor()

# Lire le contenu du fichier SQL
with open(database_sql_path, 'r') as sql_file:
    sql_script = sql_file.read()

# Exécuter le script SQL
cursor.executescript(sql_script)

# Valider les modifications
connection.commit()

#Créer le serveur flask pour l'api
app = Flask(__name__)


@app.route('/addRule', methods=['POST'])
def addRuleAPI():

    data = request.json.get('interactionDetails', {})

    response=addNewRule(data)

    print(response)

    # Récupérez les données individuelles du formulaire

    return jsonify({"status": response})

@app.route('/getPatient', methods=['POST'])
def getPatientAPI():
    # Récupère les données du corps de la requête
    
    liste_patient=getAllPatient()
    #Utilisation des donnees

    return jsonify({"patients": liste_patient})

@app.route('/getRules', methods=['POST'])
def getRulesAPI():
    # Récupère les données du corps de la requête
    
    liste_regle=getAllRules()
    #Utilisation des donnees

    return jsonify({"regles" :liste_regle})

@app.route('/getAlertes', methods=['POST'])
def getAlertesAPI():
    # Récupère les données du corps de la requête
    
    liste_alertes=getAllAlertes()
    #Utilisation des donnees

    return jsonify({"alertes" :liste_alertes})

@app.route('/addPatient', methods=['POST'])
def addPatientAPI():
    # Récupère les données du corps de la requête
    data = request.json.get('PatientsDetails', {})
    print(data)
    response = addNewPatient(data)
    
    #Utilisation des donnees

    return jsonify({'ajout du patient' : response})

@app.route('/addTraitement', methods=['POST'])
def addTraitementAPI():
    # Récupère les données du corps de la requête
    data = request.json.get('TraitementDetails', {})
    print("bonjour")
    
    traitementAll= getTraitementsByIdPatient(data["id_patient"])

    newTraitement = data["code_traitement"]

    iatroData = requeteIatro(traitementAll, newTraitement)

    # Vérifiez si la valeur de nDetectionIatro est égale à "0"
    if iatroData["nDetectionIatro"] == "0":
        # Appel à la fonction addNewTraitement avec l'objet data
        addNewTraitement(data)
    
    else:

       addNewAlerte(data, iatroData)
    
    #Utilisation des donnees

    return jsonify({'infoIatro' : iatroData})


@app.route('/getTraitements', methods=['POST'])
def getTraitementsAPI():
    # Récupère les données du corps de la requête
    data = request.json.get('TraitementDetails', {})
    
    liste_traitements= getTraitementsByIdPatient(data["id_patient"])

    return jsonify({"alertes" :liste_traitements})

@app.route('/getMedecins', methods=['POST'])
def getMedecinsAPI():
    
    liste_medecins= getMedecinsSQL()

    return jsonify({"medecins" :liste_medecins})








if __name__ == '__main__':
    app.run(port=5000)
