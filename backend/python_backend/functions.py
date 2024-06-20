import numpy as np
import pandas as pd
import sqlite3
from random import randint

from anytree import Node,RenderTree,PreOrderIter,AnyNode
from anytree.exporter import JsonExporter,DotExporter
import json




#Fonctin complémentaire
#Retirer le 1 ou deux du traitement pour éviter de créer un ordre de traitement
def retirerChiffre(string):
    k=list(string)
    i = 0
    while k[i].isdigit()==False:
        i+=1
    k.remove(k[i])
    u=''.join(k)
    return u


#Fonction de création des différents granules
#Granule =[Formule, Regroupement des données associées à la formule]
def getFormulasGranules(column_attr, info_table):
    
    # Granule de base correspondant à une formule F et les éléments du granule G
    basic_granules_table = pd.DataFrame(columns = ['Formula', 'Granule'])
    
    # Index i
    i = 0
    
    for attr in column_attr:
        group = info_table.groupby( by = attr ).groups
        keys = list(group.keys())
        values = list(group.values())

        for key in keys:
            basic_granules_table.loc[i, 'Formula'] = attr + "=" + key
            basic_granules_table.loc[i, 'Granule'] = list(group[key])
            i += 1
        
    return basic_granules_table


# Définition et ajout de la mesure "G : Generality" dans la table des granules
# G = nombres de granules / cardinal de l'univers
def getGenerality(basic_gr_table, info_table):
    for i in range(len(basic_gr_table)):
        # nombres d'éléments dans le granule au rang i
        obj_in_granule =  len(basic_gr_table.loc[i, 'Granule'])
        U = len(info_table)
        #on insère une colonne de "Generality" dans laquelle on renseigne la mesure au rang i
        basic_gr_table.loc[i, 'Generality'] = obj_in_granule / U


#Fonction pour ajouter la mesure de "Confidence"

#pour implémenter cette mesure, nécessaire de déf une fonction qui compte les
# éléments de chaque classe
#adapter en fonction du nombre de classe définies et possibles : peut être créer une variable qui stocke ça

def countClasseGr(objects_Gr, info_table):
    class_0 = 0
    class_1 = 0
    class_2 = 0
    class_3 = 0
    
    for i in objects_Gr:
        if info_table.loc[i, 'iatrogenie'] == 0:
            class_0 += 1
        if info_table.loc[i, 'iatrogenie'] == 1:
            class_1 += 1
        elif info_table.loc[i, 'iatrogenie'] == 2:
            class_2 += 1
        elif info_table.loc[i, 'iatrogenie'] == 3:
            class_3 += 1

    
    return class_0, class_1,class_2,class_3

def getConfidence( basic_gr_table, info_table ):
    
    
    for i in range(len(basic_gr_table)):
        obj_Gr = basic_gr_table.loc[i, 'Granule']
    
        class_0, class_1,class_2, class_3  = countClasseGr(obj_Gr, info_table)
    
        basic_gr_table.loc[i, 'confidence_0']  = class_0 / len(obj_Gr)
        basic_gr_table.loc[i, 'confidence_1']  = class_1 / len(obj_Gr)
        basic_gr_table.loc[i, 'confidence_2']  = class_2 / len(obj_Gr)
        basic_gr_table.loc[i, 'confidence_3']  = class_3 / len(obj_Gr)



# Mesure du coverage
def getCoverage(basic_gr_table, info_table):
    if 0 in info_table[['iatrogenie']].values:
        class_0_count = len(info_table.groupby( by = 'iatrogenie').groups[0])
    else:
        class_0_count = 0

    if 1 in info_table[['iatrogenie']].values:
        class_1_count = len(info_table.groupby( by = 'iatrogenie').groups[1])
    else:
        class_1_count = 0

    if 2 in info_table[['iatrogenie']].values:
        class_2_count = len(info_table.groupby( by = 'iatrogenie').groups[2])
    else:
        class_2_count = 0

    if 3 in info_table[['iatrogenie']].values:
        class_3_count = len(info_table.groupby( by = 'iatrogenie').groups[3])
    else:
        class_3_count = 0

    for i in range(len(basic_gr_table)):
        obj_Gr = basic_gr_table.loc[i, 'Granule']

        class_0, class_1, class_2, class_3 = countClasseGr(obj_Gr, info_table)

        basic_gr_table.loc[i, 'coverage_0']  = (class_0 / class_0_count if class_0_count != 0 else 0)
        basic_gr_table.loc[i, 'coverage_1']  = (class_1 / class_1_count if class_1_count != 0 else 0)
        basic_gr_table.loc[i, 'coverage_2']  = (class_2 / class_2_count if class_2_count != 0 else 0)
        basic_gr_table.loc[i, 'coverage_3']  = (class_3 / class_3_count if class_3_count != 0 else 0)


# We define a function to compute the Entropy

def getEntropy(basic_gr_table, info_table):
    
    res = 0

    for i in range(len(basic_gr_table)):

        for j in range(2):
            p_ = basic_gr_table.loc[i, 'confidence_'+str(j)]
            if p_ == 0:
                res += 0
            else:
                res += -( p_ * np.log2(p_) )

        basic_gr_table.loc[i, 'entropy'] = res
        res = 0


#Fonction complémentaire
def getTestFormulas(test_table, attribut):
    all_formula_test = []
    for i in range(len(test_table)):
        p_i_attribute = []
        for attr in attribut:
            p_i_attribute.append( attr + "=" + test_table.loc[i, attr])
        all_formula_test.append(p_i_attribute)
    return all_formula_test


#Fonction qui crée un règle 

def creationNewRule(fact_list, conclusion, rule_name):
    newRule = {rule_name :{'condition' :fact_list, 'consequence': conclusion } }
    #test = newRule in rules_base.rules #Peut être pas assez rigoureux
    #rules.update(newRule)

    return True


#Fonction de recherche dans l'arbre
def FindFormulasInTree(formula_test, root,fact_list):
    
    X = False  # L'état de la recherche
    copy = formula_test.copy()
    detected_class = -1 #classe abstraite --> aucune classe iatrogénique détectée
    while not X:
        parent = root
        children = list(parent.children)
        for form in copy:
            
            for child in children:
                
                if retirerChiffre(form.strip()) == retirerChiffre(child.name.strip()): #permet d'éviter la prise en compte de l'ordre dans l'entrée des traitement
                    if list(child.children):
                        copy.remove(form)

                        fact_list.append(child.name.strip()) 
                        detected_class = FindFormulasInTree(copy, parent,fact_list)
                        if detected_class != -1:  # Si detected_class est différent de -1, on sort immédiatement
                            return detected_class
                        
                        
                        parent = child
                        detected_class = FindFormulasInTree(copy, parent,fact_list)  # Appel récursif pour mettre à jour detected_class
                        if detected_class != -1:  # Si detected_class est différent de -1, on sort immédiatement
                            return detected_class
                    else:
                        
                        fact_list.append(child.name.strip())
                        X = True
                        detected_class = child.iatro
                        
        if not X:
            return detected_class
    
    return detected_class

#fonction qui transforme un dictionnaire composé de clés:1élement  en dataFrame associé
def fromDicToFrame(treatments):
    columns = []
    for cle in treatments:
        treatments[cle]=[treatments[cle]]
        columns.append(cle)
    
    df = pd.DataFrame(treatments, columns=columns)

    return df

def getKeyDic(dicList, key):
    output = []
    for i in range(len(dicList)):
        actualDic = dicList[i]
        output.append(actualDic[key])
    return output

# Fonction récursive pour recréer l'arbre à partir du JSON
def build_tree(json_node):
    node_name = json_node.get("name")
    if node_name is not None:
        node = Node(node_name)

        # Ajouter l'attribut "iatro" s'il est présent dans le JSON
        iatro_value = json_node.get("iatro")
        if iatro_value is not None:
            setattr(node, "iatro", iatro_value)

        # Appeler la fonction récursivement pour les enfants
        for child_json_node in json_node.get("children", []):
            child_node = build_tree(child_json_node)
            child_node.parent = node

        return node