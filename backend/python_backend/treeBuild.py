from python_backend.functions import *
import json
from anytree import Node, PreOrderIter

import os


#nombre de traitement maximum à prendre en compte dans le cas de l'entraînement
t_max = 2

# Table de faux patients
#On récupère les données issues du fichier "preparation_donnee.ipynb"
#df = pd.read_csv("implementation_N/data/patientFrame_N.csv")

#colonnes utilisées
info_liste = []
attributes = []

for i in range(t_max):
    info_liste.append("treatment"+str(i+1)) 
    attributes.append("treatment"+str(i+1)) 

info_liste.append('iatrogenie')

#on récupère le data set issu du fichier csv  avec les colonnes souhaitées
# Charger le fichier JSON
# with open("arbre.json", "r") as f:
#     json_data = json.load(f)

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construisez le chemin absolu vers le fichier JSON
json_file_path = os.path.join(script_dir, "arbre.json")


# Lisez le fichier JSON
with open(json_file_path, "r") as f:
    json_data = json.load(f)


# Appeler la fonction pour la racine
root = build_tree(json_data)
""" print(RenderTree(root))
 """# Afficher la structure de l'arbre reconstruit
""" for node in PreOrderIter(root):
    print("Node:", node.name, "Attributs:", node.__dict__) """