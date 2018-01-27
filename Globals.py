#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 23.06.2017

@author: Mike

Globale Variablen und Konstanten
'''


SPORTARTEN = ["Autofahren", "Klettern", "Laufen", "Mountainbike", "Radfahren", "Schlittschuhlaufen", "Schwimmen"]

###  Globale Variablen

#    Zeitliche Auflösung
#sampletime = 5

autofahren = [50,1000,1000]
klettern = [5,2,2]
laufen = [3,50,50]
mountainbike = [5,100,100]
radfahren = [5,100,100]
raften = [20,50,50]
schlittschuhlaufen = [2,100,100]
schwimmen = [1,10,10]

def parametersatz(sportart):
    if sportart == "Autofahren": return autofahren
    if sportart == "Klettern": return klettern
    if sportart == "Laufen" : return laufen
    if sportart == "Mountainbike": return mountainbike
    if sportart == "Radfahren": return radfahren
    if sportart == "Raften": return raften
    if sportart == "Schlittschuhlaufen": return schlittschuhlaufen
    if sportart == "Schwimmen": return schwimmen
    else: return 0
