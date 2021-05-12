#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:41:57 2020

@author: mathieu
"""
import pylab
import matplotlib.pyplot as plt

"""Exportation en png"""

#.............................................................................
#E         result, la liste de tout les résultats
#          name, le nom du fichier à exporter
#Action    Permet d'exporter les résultats sur un graphes en format png
#S         none
def export_diag(result,name,formule_brute):
      
    fig, ax = plt.subplots()
    
    ax.set_title("Calcul direct de "+formule_brute)

    x = [result[i][0] for i in range (len(result))]
    height = [result[i][1] for i in range (len(result))]
    width = 0.02
    
    columns = plt.bar(x, height, width, color='blue')
    
    plt.xlim(min(x)-1,max(x)+1)
    plt.ylim(0,110)
    
    def autolabel(columns):
        """Attach a text label above each column in *columns*, displaying its height."""
        for column in columns:
            label = str(round(column.get_x(),2))+" ; "+str(round(column.get_height(),0))
            if round(column.get_height(),0) == 0:
                label = round(column.get_x(),2)
            ax.annotate('{}'.format(label),
                        xy=(column.get_x(), column.get_height()),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
            
    autolabel(columns)
    
    try :
        plt.savefig('../'+name)
    except :
        plt.savefig(name)
#.............................................................................