#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:30:49 2020

@author: mathieu
"""
import math

def TriMasse(L):
    for i in range(1,len(L)):
        if L[i][0]<L[0][0]:
            L=[L[i]]+L[0:i]+L[i+1:]
        else:
            j=i-1
            while L[i][0]<L[j][0]:
                j=j-1
            L=L[0:j+1]+[L[i]]+L[j+1:i]+L[i+1:]
    return(L)

def TriProbas(L):
    for i in range(1,len(L)):
        if L[i][1]>L[0][1]:
            L=[L[i]]+L[0:i]+L[i+1:]
        else:
            j=i-1
            while L[i][1]>L[j][1]:
                j=j-1
            L=L[0:j+1]+[L[i]]+L[j+1:i]+L[i+1:]
    return(L)

def regroupementavecmultiplicite(L,M,sensibilite):
#    print(M)
#    print(L)
    seuil=sensibilite*M[0][1]*L[0][1]
    N=[]
    for i in range(len(L)):
        j=0
        while j<len(M) and L[i][1]*M[j][1]>seuil:
            N.append([L[i][0]+M[j][0],L[i][1]*M[j][1],L[i][2]*M[j][2]])
            j=j+1
    return TriProbas(N)

def deresolution1(K,resolution):
#   print('appel de deresolution')
    S=TriMasse(K)
    for z in range(len(S)):
        S[z].append(1)
    Lng=len(S)-1
    for i in range(len(S)-1):
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
    return TriMasse(S)

def deresolution2(K,resolution):
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
            multiplicite=S[indice][2]+S[indice-1][2]
#        et on réduit notre liste:
            S=S[0:indice-1]+[[massemoyenne,probatotale,multiplicite]]+S[indice+1:]
    return TriMasse(S)

def celluleprime(atome,configmere,rang,probamere,sensibilite):
    sortie=[]
    ESSAI=[]
    for indice in range(0,len(configmere)):
        ESSAI.append(configmere[indice][0])
    if rang>=len(atome):
        masse=0
        for i in range(0,len(configmere)):
            masse=masse+atome[i][0]*configmere[i][0]
        sortie.append([masse,probamere])
    else:
        sortie=sortie+celluleprime(atome,configmere,rang+1,probamere,sensibilite)
    if configmere[rang-1][1]:
        for i in range(0,rang-1):
            if configmere[i][2]:
                probafille=probamere*atome[rang-1][1]*configmere[i][0]/(configmere[rang-1][0]+1)/atome[i][1]
                if probafille>sensibilite:
                    configfille=[]
                    for k in range(0,len(configmere)):
                        nombre=configmere[k][0]
                        configfille.append([nombre])
                        if configmere[k][1]:
                            configfille[k].append(True)
                        else:
                            configfille[k].append(False)
                        if configmere[k][2]:
                            configfille[k].append(True)
                        else:
                             configfille[k].append(False)
                    for j in range(0,rang-1):
                        configfille[j][1]=False
                    for j in range(0,i):
                        configfille[j][2]=False
                    configfille[rang-1][0]=configfille[rang-1][0]+1
                    configfille[rang-1][2]=False
                    configfille[i][0]=configfille[i][0]-1
                    if configfille[i][0]==0:
                        configfille[i][2]=False
                    sortie=sortie+celluleprime(atome,configfille,rang,probafille,sensibilite)
    if configmere[rang-1][2]:
        for i in range(0,rang-1):
            if configmere[i][1]:
                probafille=probamere*atome[i][1]*configmere[rang-1][0]/(configmere[i][0]+1)/atome[rang-1][1]
                if probafille>sensibilite:
                    configfille=[]
                    for k in range(0,len(configmere)):
                        nombre=configmere[k][0]
                        configfille.append([nombre])
                        if configmere[k][1]:
                            configfille[k].append(True)
                        else:
                            configfille[k].append(False)
                        if configmere[k][2]:
                            configfille[k].append(True)
                        else:
                             configfille[k].append(False)
                    for j in range(0,rang-1):
                        configfille[j][2]=False
                    for j in range(0,i):
                        configfille[j][1]=False
                    configfille[rang-1][0]=configfille[rang-1][0]-1
                    configfille[rang-1][1]=False
                    configfille[i][0]=configfille[i][0]+1
                    if configfille[rang-1][0]==0:
                        configfille[rang-1][2]=False
                    sortie=sortie+celluleprime(atome,configfille,rang,probafille,sensibilite)
    return sortie

def recherchemax(atome, nombre):
    total=0
    for i in range(0,len(atome)):
        total=total+atome[i][1]
    config=[0]*len(atome)
    somme=0
    for i in range(0,len(atome)):
        config[i]=math.floor(atome[i][1]/total*(nombre+len(atome)/2))
        somme=somme+config[i]
    defaut=somme-nombre
    if defaut<0:
        listajout=[]
        for j in range(0,len(atome)):
            listajout.append([j,atome[j][1]/(config[j]+1)])
        for k in range(0,-defaut/2):
            listajout.append([k,atome[k][1]/(config[k]+2)])
        if defaut==-3:
            listajout.append([0,atome[0][1]/(config[0]+3)])
        listajout=TriProbas(listajout)
        for l in range(0,-defaut):
            config[listajout[l][0]]=config[listajout[l][0]]+1
    if defaut>0:
        listecart=[]
        for j in range(0,len(atome)):
            listecart.append([j,config[j]/atome[j][1]])
        for k in range(0,defaut-1):
            if config[k]>0:
                listecart.append([k,(config[k]-1)/atome[k][1]])
        if defaut>=3 and config[0]>1:
            listecart.append([0,(config[0]-2)/atome[0][1]])
#        if defaut==4 and config[0]>2:
#            listecart.append([0,(config[0]-3)/atome[0][1]])
        listecart=TriProbas(listecart)
        for l in range(0,defaut):
            config[listecart[l][0]]=config[listecart[l][0]]-1
    return(config)

def Base100(liste):
    resultat=TriProbas(liste)
    pivot=100/resultat[0][1]
    for i in range(0,len(resultat)):
        resultat[i][1]=resultat[i][1]*pivot
    return(resultat)

def calculdirect(molecule,resolution,sensibilite):
    spectre=[[0,1,1]]
    for indice in range(0,len(molecule)):
        LISTE=TriProbas(molecule[indice][0])
        configurationdepart=recherchemax(LISTE,molecule[indice][1])
        departcellule=[]
        for j in range(0,len(configurationdepart)):
            departcellule.append([configurationdepart[j],True,True])
            if configurationdepart[j]==0:
                departcellule[-1][2]=False
        seuil=sensibilite
        sortie=celluleprime(molecule[indice][0],departcellule,0,1,sensibilite)
        sortie=deresolution1(sortie,resolution)
        spectre=regroupementavecmultiplicite(spectre,TriProbas(sortie),sensibilite)
        spectre=deresolution2(spectre,resolution)
    return TriMasse(Base100(spectre))

#molecule = [[[[12.0, 100.0], [13.0033548378, 1.0815728292732234]], 13], [[[1.00782503207, 100.0], [2.0141017778, 0.011501322652104991]], 17], [[[15.99491461956, 100.0], [16.9991317, 0.03809256493278667], [17.999161, 0.20549936345319125]], 2]]
#resolution = 0.1
#sensibilite = 0.00001
#print(calculdirect(molecule,resolution,sensibilite))