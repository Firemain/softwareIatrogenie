from python_backend.functions import *
from python_backend.treeBuild import root, t_max, attributes, info_liste


#fonction qui va déterminer si il y a un risque iatrogénique ou pas
#entrée : treatments, liste avec les noms des traitements
#          inputOrdonnance : le nouveaux traitement à ajouter aux patients

#retour : iatroData : contient: 
#nDetectionIatro : nombre de détection iatro
#bestIatroDetected : indice maximum de iatro détecté
#iatroFrame : JSON qui récapitule les mauvaises interactions détectés

def requeteIatro(treatments,inputOrdonnance):
    


    #on transforme ce dictionnaire en dataFrame que l'on va pouvoir utiliser
    patient = getKeyDic(treatments,'nom_traitement')

    #on détecte le nombre de traitement pris par le patient parmi le nombre maximum et on ajuste le frame étudié:
    nbTraitement = len(treatments)
    

    inputOrdonnance=[inputOrdonnance]
    #détection iatrogénique deux à deux avec les médicaments déjà pris et entre les deux médicaments indiqués
    nDetectionIatro = 0
    bestIatroDetected = 0
    iatroDetectedList = []

    for i in range(len(inputOrdonnance)):
        for j in range(len(patient)):

            #on sélectionne les traitements deux à deux
            """ data = [[inputOrdonnance[i],patient["treatment"+str(j+1)]]] """
            data = [[inputOrdonnance[i],patient[j]]]

            df = pd.DataFrame(data=data, columns=attributes)
            
            #détection de la classe iatrogénique

            formulas = getTestFormulas(df, attributes)[0]

            #liste de faits
            factList = []
        
            result = FindFormulasInTree(formulas,root,factList)

            #on stocke les résultats si nécessaire
            if result>0 : 
                nDetectionIatro +=1
                #on ajoute les traitements engendrant le risque iatrogénique et leurs indice de risque à liste pour un dataframe de résultat
                dataIatro = data[0].copy()
                dataIatro.append(result)
                iatroDetectedList.append(dataIatro)

                if result>bestIatroDetected :
                    bestIatroDetected=result

            #présentation des résultats
    iatroFrame = pd.DataFrame(data=iatroDetectedList, columns=info_liste)
    
    #traitement et constituion de données à envoye
    iatroData = {
        'nDetectionIatro':str(nDetectionIatro),
        'bestIatroDetected' : str(bestIatroDetected),
        'iatroFrame': iatroFrame.to_json(orient='records')
    }

    
    return iatroData

dic =[{'nom_traitement':'D05AX52'}]
result = requeteIatro(dic, 'N03AA02')
print("la classe iatrogénique est :", result)

