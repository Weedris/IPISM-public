#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:39:15 2020

@author: mathieu
"""
#import time
from copy import deepcopy
import json

"-------------------------------------------------------------"

"""Récupération des informations du document table"""


#.............................................................................
#E         chaine, variable de type '35.967545106(29)'
#Action    Permet d'enlever les parenthèses contenant l'incertitude
#S         La valeur de la chaine en float 35.967545106
def enlever_incertitudes(chaine):
    i = 0
    for caractere in chaine:
        if caractere == "(":
            return float(chaine[:i])
        else:
            i += 1
    return float(chaine)
#.............................................................................

#.............................................................................
#E         v, variable quelconque de type quelconque.
#Action    Permet de vérifier si une variable est un entier.
#S         True si v est un entier, False sinon.
def is_number(v):
    try :
        var = int(v)
        return True
    except :
        return False
#.............................................................................

#.............................................................................
#E         filename,  le nom du fichier contenant les abondances.
#Action    Permet de récupérer les valeurs des abondances isotopiques depuis un fichier texte
#S         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
def upload_abondances(filename = "./../abondances/abondances.txt"):
    table = open(filename, "r")
    tableau = table.read().split("\n")
    abondances = {}

    # On enlève d'abord tous les espaces
    for i in range(len(tableau)):
        ligne = tableau[i].split(" ")
        nouvelle_ligne = []
        for case in ligne:
            if case != '':
                nouvelle_ligne.append(case)
        tableau[i] = nouvelle_ligne
    
    # Puis remplit  le dictionnaire avec les couples masse  abondance
    symbole = ""
    tableau_couples = []
    for i in range(len(tableau)):
        ligne = tableau[i]
        if len(ligne) == 4:  # Il s'agit d'un nouvel élément
            if i != 0: # Si on n'est pas sur la première ligne
                abondances[symbole] = tableau_couples # On ajoute le tableau de l'élément précédent
                tableau_couples = []
            for j in range(len(ligne[1])): # On récupère le symbole
                if not is_number(ligne[1][j]):
                    symbole = ligne[1][j:]
                    break

            masse = enlever_incertitudes(ligne[2])
            abondance = enlever_incertitudes(ligne[3])
            tableau_couples.append([masse,abondance]) # On ajoute la ligne dans le tableau
        elif  len(ligne) == 2: # Il s'agit d'un élément inexistant naturellement
            abondances[ligne[1]] = []          
        else: # Il s'agit d'une nouvelle ligne de l'élément actuel
            masse = enlever_incertitudes(ligne[1])
            abondance = enlever_incertitudes(ligne[2])
            tableau_couples.append([masse,abondance]) # On ajoute la ligne dans le tableau
    
    # On utilise le produit en croix pour avoir les abondances dans le bon format pour le calcul
    for atome in abondances.keys():
        tableau_couples = abondances[atome]
        abondance_max = 0.
        for couple in tableau_couples:
            if couple[1] > abondance_max:
                abondance_max = couple[1]
        for couple in tableau_couples:
            couple[1] = 100*couple[1]/abondance_max
            
    table.close()
    with open('./../abondances/abondances.json', 'w') as fp:
        json.dump(abondances, fp)

    return abondances
#.............................................................................

#.............................................................................
#E         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
#Action    Enregistre le dictionnaire abondances dans un fichier abondances.json
#S         
def save_abondances(abondances):
    with open('./../abondances/abondances.json', 'w') as fp:
        json.dump(abondances, fp)
#.............................................................................

#.............................................................................
#E         
#Action    renvoie abondances qui etait stocke sous un fichier au format json
#S         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
def get_abondances():
    with open('./../abondances/abondances.json', 'r') as fp:
        return json.load(fp)
#.............................................................................

"-------------------------------------------------------------"

"""Fonctions de lecture d'une formule brute"""

#.............................................................................
#E         formeBrute, la formule brute à traiter
#Action    Permet d'analyser la formule brute et de connaître les atomes utilisés ainsi que leurs nombres.
#S         tableau de couples ["Symbole chimique", nombre d'atomes]
def lecture_FB(formeBrute):
    abondances = get_abondances()
    # print(abondances)

    molecule = []
    
    if (formeBrute != ""):
        fb = list(formeBrute)

    i = 0

    while ( i < len(fb) ):

        if is_number(fb[i]):

            temp = 0
            while is_number(fb[ i + temp + 1 ]):
                temp += 1

            if fb[i + temp + 1].isupper():
                
                nombre = formeBrute[i]

                j = temp
                while j != 0:
                    nombre += formeBrute[i + j]
                    j -= 1                

                try:
                    if fb[i + temp + 2].islower():
                    
                        molecule.append( (abondances[ formeBrute[i + temp + 1] + formeBrute[i + temp + 2] ], 
                            int( nombre )) )
                        i += temp + 3
                    else:
                        molecule.append( (abondances[ formeBrute[i + temp + 1] ], 
                            int( nombre )) )
                        i += temp + 2
                except:
                    molecule.append( (abondances[ formeBrute[i + temp + 1] ], 
                        int( nombre )) )
                    i += temp + 2
        
        elif fb[i].isupper():

            try:
                if fb[i + 1].islower():
                    molecule.append( (abondances[ formeBrute[i] + formeBrute[ i + 1] ], 
                        1 ))
                    i += 3
                else:
                    molecule.append( (abondances[ formeBrute[i] ], 
                        1 ))
                    i += 1
            except:
                molecule.append( (abondances[ formeBrute[i] ], 
                        1 ))
                i += 1

    return molecule
#.............................................................................

"-------------------------------------------------------------"

"""Algorithme de tri pour la liste des résultats"""

#.............................................................................
#E         result, la liste de tout les résultats
#          t, la variable qui détermine le tri
#Action    Permet de trier les résultats finaux dans l'ordre décroissant
#S         new_result, la liste triée de tout les résultats
def triInsert(result,t):
    
    new_result = deepcopy(result)
    n = len(result)

    for i in range (1,n):
        x = new_result[i]
        j = i
        while ((j > 0) and new_result[j-1][t] > x[t]):
            new_result[j] = new_result[j-1]
            j = j-1
        new_result[j] = x

    return new_result
#.............................................................................

#.............................................................................
#E         result, la liste de tout les résultats
#Action    Passer d'une liste où la valeur la plus élevée est 100 à une liste où le total est 100
#S         la liste traitée de tout les résultats
def relatif_to_total(result):
    total = 0.
    for ligne in result:
        total += ligne[1]
    for ligne in result:
        ligne[1] = 100*ligne[1]/total
    return result
#.............................................................................

#.............................................................................
#E         result, la liste de tout les résultats
#Action    Passer d'une liste où le total est 100 à une liste où la valeur la plus élevée est 100 
#S         liste traitée de tout les résultats
def total_to_relatif(result):
    maxi = 0.
    for ligne in result:
        if ligne[1] > maxi:
            maxi = ligne[1]
    for ligne in result:
        ligne[1] = 100*ligne[1]/maxi
    return result
#.............................................................................


"-------------------------------------------------------------"

"""Récupération des informations du spectre"""

#.............................................................................
#E         chaine, variable de type '2.911e3'
#Action    Permet de transformer en float en prenant en compte la puissance de 10
#S         La valeur de la chaine en float 2911
def convertir_puissances(chaine):
    i = 0
    for caractere in chaine:
        if caractere == "e":
            return float(chaine[:i])*(10**float(chaine[i+1]))
        else:
            i += 1
    return float(chaine)
#.............................................................................

#.............................................................................
#E         filename,  le nom du fichier contenant le spectre.
#Action    Permet de récupérer les valeurs zommée d'un spectre depuis un fichier texte
#S         abondances,  un dictionnaire dont les indices sont les symboles chimiques des atomes
def upload_spectrum(filename="./../spectrum_list.txt"):
    try:
        with open(filename, encoding='utf-16') as f:
            tableau = f.read()
    except:
        with open(filename, "r") as f:
            tableau = f.read()
    f.close()
    tableau = tableau.split("\n")[3:]

    # On enlève d'abord tous les espaces
    for i in range(len(tableau)):
        ligne = tableau[i].split("\t")
        nouvelle_ligne = []
        for case in ligne:
            if case != '':
                nouvelle_ligne.append(case)
        tableau[i] = [convertir_puissances(x) for x in nouvelle_ligne]

    # Puis on récupère la zone zoomée
    i = 0
    while i < len(tableau):
        if len(tableau[i]) == 4:
            tableau[i] = tableau[i][2:]
            i += 1
        else:
            del tableau[i]
    return tableau
#.............................................................................


#.............................................................................
#E         thing, une string
#Action    met sous un format unique une string particuliere
#S         une string
def normalize(thing):

    # Mise en forme sous tableau de tableau
    # [ Mass, Relative intensity, Number of peaks ]

    tab = thing.split("|")
    # print(tab)
    work = []
    temp = []

    i = 0
    while i < len(tab):
        if tab[i] == " " or tab[i] == " \n" or tab[i] == " \n " or tab[i] == "\n ":
            i += 1
        else:
            temp.append(tab[i])
            if len(temp) == 3:
                work.append(temp)
                temp = []
            i += 1

    # print(work)


    # faisont en sorte qu'il soit de la meme longueure par colone

    for ligne in work:
        
        if len(ligne[0]) < 15:
            for i in range( 15 - len(ligne[0]) ):
                ligne[0] += "."
        
        if len(ligne[1]) < 20:
            for i in range( 20 - len(ligne[1]) ):
                ligne[1] += "."

        if len(ligne[2]) < 2:
            for i in range( 2 - len(ligne[2]) ):
                ligne[2] += "."
    
    # print(work)

    # remise en forme de string

    out = ""

    for ligne in work:
        temp = ""

        for element in ligne:
            temp += element + " | "
        
        out += temp + "\n"

    return out
#.............................................................................