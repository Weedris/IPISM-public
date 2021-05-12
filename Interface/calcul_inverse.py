#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:36:14 2020

@author: mathieu
"""
from calcul_direct import *
from copy import deepcopy
import numpy as np

O = [[15.99491461956, 100.0], [16.9991317, 0.03809256493278667], [17.999161, 0.20549936345319125]]
U = [[234.04095,0.006],[235.04393,0.7253],[238.05079,100]]

def deresolution(K,resolution):
#   print('appel de deresolution')
    S=TriMasse(K)
    Lng=len(S)-1
    for i in range(len(S)-1):
        indice=Lng-i
        if S[indice][0]-S[indice-1][0]<resolution:
#        on calcule (en deux étapes!) la masse du couple regroupé
#        (en tenant compte des probabilités respectives)
            masseponderee=(S[indice][1]*S[indice][0]+S[indice-1][1]*S[indice-1][0])
            probatotale=S[indice][1]+S[indice-1][1]
            massemoyenne=masseponderee/probatotale
#        et on réduit notre liste:
            S=S[0:indice-1]+[[massemoyenne,probatotale]]+S[indice+1:]
    return TriMasse(S)

def multimatricialisation(L,k):
    h=len(L)
#    MM=matrix(RDF,k*h,k)
    MM=np.zeros((k*h,k))
#    print(k*h,k)
    for i in range(h):
        for j in range(k):
#            print(k*i+j,j)
#            MM[k*i+j,j]=L[i][1]
            MM[k*i+j][j]=L[i][1]
    return(MM)

"""
def TrisimpleCroissant(L):
    for i in range(1,len(L)):
        if L[i]<L[0]:
            L=[L[i]]+L[0:i]+L[i+1:]
        else:
            j=i-1
            while L[i]<L[j]:
                j=j-1
            L=L[0:j+1]+[L[i]]+L[j+1:i]+L[i+1:]
    return(L)
"""

def calculmasses(L,M):
    N=[]
    Lordonnee=TriMasse(L)
    Mordonnee=TriMasse(M)
    for i in range(len(Lordonnee)):
        for j in range(len(Mordonnee)):
            N.append([Lordonnee[i][0]+Mordonnee[j][0],Lordonnee[i][1],Lordonnee[i][2]*Mordonnee[j][1]])
    return N

def matrix_from_rows(matrice,ordre):
    result = []
    for i in ordre:
        result.append(matrice[i])
    return result

def reordonnancementSuivi(L,MM):
#    P=[0..len(L)-1]
    P=[i for i in range(len(L))]
    for i in range(1,len(L)):
        if L[i]<L[0]:
            L=[L[i]]+L[0:i]+L[i+1:]
            P=[P[i]]+P[0:i]+P[i+1:]
        else:
            j=i-1
            while L[i]<L[j]:
                j=j-1
            L=L[0:j+1]+[L[i]]+L[j+1:i]+L[i+1:]
            P=P[0:j+1]+[P[i]]+P[j+1:i]+P[i+1:]
#    return(L,MM.matrix_from_rows(P))
    return(L,matrix_from_rows(MM,P))

def regroupementmasses(L,MM,resolution):
#    MMM=copy(MM)
    MMM=deepcopy(MM)
    S=L
    Lng=len(S)-1
    for i in range(Lng):
        indice=Lng-i
        if S[indice][0]-S[indice-1][0]<resolution:
#        on calcule (en deux étapes!) la masse du couple regroupé
#        (en tenant compte des probabilités respectives)
            masseponderee=(S[indice][1]*S[indice][0]+S[indice-1][1]*S[indice-1][0])
            probatotale=S[indice][1]+S[indice-1][1]
            massemoyenne=masseponderee/probatotale
            multiplicite=S[indice][2]+S[indice-1][2]
#        et on réduit notre liste:
            S=S[0:indice-1]+[[massemoyenne,probatotale,multiplicite]]+S[indice+1:]
#        et après, on fait suivre les opérations sur les lignes de MMM
            V=MMM[indice]+MMM[indice-1]
#            listeintermediaire=[0..indice-1]+[indice+1..MMM.nrows()]
            listeintermediaire=[i for i in range(indice)]+[i for i in range(indice+1,len(MMM)+1)]
#            MMM=MMM.matrix_from_rows(listeintermediaire[:-1])
            MMM=matrix_from_rows(MMM,listeintermediaire[:-1])
            MMM[indice-1]=V
    return S,MMM

def troncature(RE,bas,haut):
    sortie=TriMasse(RE)
#    print(sortie)
#    print(bas)
#    print(haut)
    i=0
    while i<len(sortie) and sortie[i][0]<bas:
        i=i+1
    j=max(i-1,0)
#    print('OOK')
    while j<len(sortie)-1 and sortie[j][0]<haut:
        j=j+1
#   print('OOOK')
    if j==len(sortie)-1 and sortie[-1][0]<haut:
        j=j+1
#    print('OK')
    sortie=sortie[i:j]
    return sortie

def secondmembre(L,RE,resolution):
    N=deresolution(RE,resolution)
#    print('N=',N)
    S=[0]*len(L)
    for j in range(len(N)):
#        print('j=',j)
        k=len(L)-1
        c=True
        while c and k>=0:
#            print('k=',k)
            if abs(N[j][0]-L[k][0])<resolution:
                S[k]=N[k][1]
                c=False
            k=k-1
        if c:
            print("pic",N[j],"non reconnu")
    return S

def nettoyagespectremesure(L,RE,resolution):
    #print("L :",L,"\n")
    #print("RE :",RE,"\n")
#    On commence par tronquer le spectre observé dans les limites de masse de
#    ce à quoi on s'attend, c'est-à-dire une demie unité de masse atomique en-dessous 
#    et une demie au-dessus des limites de L
#    L est ordonnée par masses croissantes lorsqu'on appellera cette fonction, 
#    donc inutle de réordonner L
    REtronque=troncature(RE,L[0][0]-0.5,L[-1][0]+0.5)
#    Ensuite, on cherche le pic le plus abondant de REtronque indicemax sera à 
#    la fin de la boucle l'indice du pic le plus abondant dans la liste RE
    indicemax=0
    max=REtronque[0][1]
    for i in range(len(REtronque)):
        if REtronque[i][1]>max:
            indicemax=i
            max=REtronque[indicemax][1]
#    Ensuite, on essaie de reconnaître ce pic abondant dans la liste L
    massemax=REtronque[indicemax][0]
    i=0
#    print(L)
#    print(massemax)
    while L[i][0]<massemax:
        i=i+1
#    On arrive à une situation où L[i-1]<massemax<L[i], mais il faut faire 
#    attention que i peut être égal à 0, c'est-à-dire que massemax serait 
#    inférieure à la masse la plus basse de la liste L
#    Il se pourrait également que massemax soit supérieure à la masse maximale 
#    de L, même si c'est peu probable, on va essayer de prendre en compte ce cas-là
    if i>0:
        if i==len(L):
            i=i-1
        if abs(massemax-L[i-1][0])<abs(L[i][0]-massemax):
            i=i-1
#    Cette fois-ci, i désigne l'indice de la masse apparaissant dans L la plus 
#    proche de massemax. On a bien sûr implicitement supposé que la longueur 
#    de L était au moins 2
#    Si la distance du pic le plus abondant à la masse la plus proche de la liste L 
#    est supérieure à la résolution il faut alerter
    if abs(massemax-L[i][0])>resolution:
        print('suspicion de spectre décalé')
#    Dans tous les cas, on calcule le décalage (fut-il petit) qui nous servira 
#    à valider ou invalider les autres pics du spectre
    decalage=massemax-L[i][0]
#    print('decalage=',decalage)
#    Maintenant, il faut pour chaque masse de L, trouver un pic dans REtronque 
#    qui lui correspond, ou lui mettre une abondance 0 (0 signifiant que cela ne sort pas 
#    par rapport au bruit)
#    Il y a là derrière la question de savoir si le bruit est inférieur ou non 
#    à la sensibilité. En principe oui, mais la variation de l'intensité du bruit 
#    quand on se déplace dans le spectre pose question)
#    Pour trouver le pic qui correspond, on tronque entre des bornes qui sont 
#    la demi-distance entre deux masses successivs apparaissant dans L, 
#    puis on cherche dans cette plage de masse le ou les pics qui "sortent" du bruit: 
#    le problème est s'il n'y a pas de bruit... 
#    La procédure ne doit pas planter s'il n'y a par exemple aucun pic dans REtronque 
#    dans la plage sélectionnée. Et il faudrait également de débrouiller d'une situation 
#    où il n'y aurait que du bruit...
#    Du point de vue technique, on construit progressivement le "spectre conservé", 
#    celui où ne resteront que les pics "intéressants" (éventuellement regroupés...)
    Spectreconserve=[]
    secondmembre=[]
    for i in range(len(L)):
        if i==0:
            morceaudespectretronque=troncature(REtronque,L[0][0]-1+decalage,(L[0][0]+L[1][0])/2+decalage)
#            print('on vient d obtenir',morceaudespectretronque)
        else:
            if i==len(L)-1:
                morceaudespectretronque=troncature(REtronque,(L[i-1][0]+L[i][0])/2+decalage,L[i][0]+1+decalage)
            else:
                morceaudespectretronque=troncature(REtronque,(L[i-1][0]+L[i][0])/2+decalage,(L[i][0]+L[i+1][0])/2+decalage)
#        print('massedereference=',L[i][0])
#        print('morceaudespectre correspondant=',morceaudespectretronque)
#    Ce qui précède a pour objectif d'isoler le but de spectre dans lequel 
#    on va chercher les pics "pertinents" concernant la masse d'indice i dans la liste L
#    Maintenant, dans ce bout de spectre, on espère trouver un pic "dominant" 
#    et sortant du bruit qui soit en plus le seul dans la plage et qui soit de masse 
#    assez proche de L[i]...
#    On commence par ordonner notre bout de spectre par probabilités décroissantes
        morceaudespectreordonne=TriProbas(morceaudespectretronque)
#    Puis on élimine tous les pics moins probables que le premier considéré comme du bruit, 
#    c'est-à-dire le premier à être trop loin de la masse cherchée et/ou 
#    le premier qui est trop éloigné en multiplicité pour être crédible
        j=0
        while j<L[i][2] and j<len(morceaudespectreordonne) and abs(L[i][0]-morceaudespectreordonne[j][0])<resolution:
            j=j+1
#    En principe, le j obtenu est le premier indice tel que morceaudespectreordonne[j] 
#    est sûrement du bruit. Il se peut que j soit égal à len(morceaudespectreordonne) 
#    auquel cas aucun pic n'est encore considéré comme du bruit.
#    Mainrenant, on élimine en "remontant" en-desosus de ce j ceux qui ne sortent pas assez du bruit,
#    c'est-à-dire qui ne sont pas au moins 3 fois plus abondants que le suivant
        while (j>0 and j<len(morceaudespectreordonne)) and morceaudespectreordonne[j-1][1]<3*morceaudespectreordonne[j][1]:
            j=j-1
#    Maintenant, notre j est le premier pic considéré comme du bruit dans la liste, 
#    si j vaut 0, c'est qu'il n'y a que du bruit, le pic le plus probable est soit trop loin, 
#    soit pas suffisamment détaché des autres. On va donc maintenant incrémenter 
#    à la fois note second membre et notre spectreconserve
#    Pour le spectreconserve, on regroupe les pics, ceci ne se fait que si j est différent de 0
#    Pour le secondmembre, on met 0 si j=0 et sinon, on met l'abondance observée 
#    après regroupement des spectres
        if j==0:
            secondmembre.append(0)
        else:
            intensitedupicconserve=0
            massedupicconserve=0
            for k in range(j):
                intensitedupicconserve=intensitedupicconserve+morceaudespectreordonne[k][1]
                massedupicconserve=massedupicconserve+morceaudespectreordonne[k][0]*morceaudespectreordonne[k][1]
            massedupicconserve=massedupicconserve/intensitedupicconserve
            secondmembre.append(intensitedupicconserve)
            if j!=len(morceaudespectreordonne):
                Spectreconserve.append([massedupicconserve,intensitedupicconserve,j,morceaudespectreordonne[j][1]])
            else:
                Spectreconserve.append([massedupicconserve,intensitedupicconserve,j,0])
    return Spectreconserve,secondmembre
#    Finalement, cette fonction produit d'une part la partie du spectre qu'on a gardée 
#    (avec des regroupements de pics si nécessaire) et le second membre de notre 
#    système linéaire auquel on va appliquer la technique de Moore-Penrose pour 
#    trouver le massif isotopique des oxygènes cherchés.

def problemeinverse(AU,listedesOx,MES,resolution,sensibilite):
    #D'abord, il faut enlever les oxygènes à chercher de la formule de la molécule totale
    nombre=-1
    somme=0
    for i in range(len(listedesOx)):
        somme=somme+listedesOx[i]
    for j in range(len(AU)):
        if AU[j][0]==O:
            nombre=AU[j][1]
            position=j
    AV=[]
    for i in range(j):
        AV.append(AU[i])
    if nombre>somme:
        AV.append([O,nombre-somme])
    for i in range(j+1,len(U)):
        AV.append(AU[i])
    #etape 1°
    Base=calculdirect(AV, resolution, sensibilite)
    #print('etape1: Base=',Base)
    #etape 2°
    matrice1=multimatricialisation(Base,3)
    #print('etape2OK')
    #etape 3°
    masses=calculdirect([[O,somme]],resolution,0)
    for i in range(len(masses)):
        masses[i]=[masses[i][0],masses[i][2]]
    #on calcule les masses possibles de la réunion des oxygènes, regroupées selon 
    #la résolution cherchée, avec calcul des multiplicité afférent, les intensités 
    #trouvées ne sont pas pertinentes et sont éliminées en fin de calcul
    listemasses1=calculmasses(Base,masses)
    #print('etape3: listemasses1=',listemasses1)
    #etape 4°
    listemasses2,matrice2=reordonnancementSuivi(listemasses1,matrice1)
    #print('etape4: listemasses2=',listemasses2)
    #etape 5°
    listemasses3,matrice3=regroupementmasses(listemasses2,matrice2,resolution)
    #print('etape5: listemasses3:',listemasses3)
    #etape 6°
    spectrenettoye,secondmembre=nettoyagespectremesure(listemasses3,MES,resolution)
#ATTENTION, c'est ici qu'on peut sortir le spectre conservé pour validation par l'utilisateur
#Chaque pic conservé arrive avec sa masse, son intensité, le nombre de pics 
#du spectre mesuré qu'il a regroupés et l'intensité maximale des pics situés dans 
#sa "zone d'influence" qu'il a négligés
    print('partie conservee du spectre =',spectrenettoye)
    #etape 7°,1 On calcule des intensités pour le massif isotopique des oxygènes inconnus
    #print(matrice3)
    #print(secondmembre)
#    transposee=matrice3.transpose()
    transposee=np.array(matrice3).transpose()
#    matricecarree=transposee*matrice3
    matricecarree=np.dot(transposee,matrice3)
#    solution=matricecarree.inverse()*transposee*vector(secondmembre)
    solution=np.dot(np.dot(np.linalg.inv(matricecarree),transposee),np.array(secondmembre).reshape(-1,1))
#    resultat=(100/solution.norm(infinity))*solution
    resultat=(100/max([abs(valeur) for valeur in solution]))*solution
    #print('etape7premiermorceau: resultat=',resultat)
    sortie=[]
    for i in range(len(resultat)):
#        sortie.append([masses[i][0],resultat[i]])
        sortie.append([masses[i][0],float(resultat[i])])
    #print('etape7deuxiemepartie: sortie=',sortie)
    #etape 8° ATTENTION A LA NORMALISATION:BASE100!!!!!
#    imageapprochee1=matrice3*solution
    imageapprochee1=np.dot(matrice3,solution)
#    imageapprochee2=(100/imageapprochee1.norm(infinity))*imageapprochee1
    imageapprochee2=(100/max([abs(valeur) for valeur in imageapprochee1]))*imageapprochee1
    #print('imageapprochee2=',imageapprochee2)
#    imagevecteur=vector(secondmembre)
    imagevecteur=np.array(secondmembre).reshape(-1,1)
    #print('OK1')
#    imagevecteurnormalisee=(100/imagevecteur.norm(infinity))*imagevecteur
    imagevecteurnormalisee=(100/max([abs(valeur) for valeur in imagevecteur]))*imagevecteur
    #print('OK2')
#    estimerreur=(imageapprochee2-imagevecteurnormalisee).norm()
    estimerreur=abs(imageapprochee2-imagevecteurnormalisee)
#    return sortie,estimerreur
    return sortie,[float(valeur) for valeur in estimerreur]

#molecule = [[[[12.0, 100.0], [13.0033548378, 1.0815728292732234]], 13], [[[1.00782503207, 100.0], [2.0141017778, 0.011501322652104991]], 17], [[[15.99491461956, 100.0], [16.9991317, 0.03809256493278667], [17.999161, 0.20549936345319125]], 2]]
#spectre=calculdirect(molecule,resolution,sensibilite)
#Experience1=([[205.13,190578.0,1],[206.14,64809.0],[207.14,51976.0],[208.14,8350.0]])
#sortie,estimerreur = problemeinverse(molecule,[1],Experience1,0.1,0.00001)

#sortie,estimerreur = problemeinverse(molecule,[1],spectre,0.1,0.00001)

#print(sortie)
