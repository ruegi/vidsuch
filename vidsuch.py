# -*- coding: utf-8 -*-
"""
Created on Wed May 29

@author: rg

vidsuich.py mit pyqt5
sucht die Datei einer Quelle (Quell-Dir) im Ziel;
wenn Name, Datei-Datum @ Datei-Länge übereinstimmen
wird das positiv vermerkt, sonst negativ

"""

import logger
import os

quelle = "e:\\filme\\schnittx"
ziel = "y:\\video"

def findeDatei(datei):
    x = None
    for root, dirs, files in os.walk(ziel):
        if datei in files:
            x = os.path.join(root, datei)
            break
    return x

if __name__ == "__main__":
    log = logger.openlog(os.path.basename(__file__)+".log", TimeStamp=True, printout=True)

    i = 0
    hit = 0
    niete = 0
    for entry in os.scandir(quelle):
        if entry.is_file():
            i += 1
            qdatei = os.path.join(quelle, entry.name)
            log.log("Bearbeite: {0:2}: {1}:".format(i, qdatei))
            zdatei = findeDatei(entry.name)
            if zdatei is None:
                log.log("--- nicht gefunden\n")
                niete += 1
            else:
                # hier noch weitere tests

                log.log("--- gefunden: {0}\n".format(zdatei))
                hit +=1
    log.log("Gefunden: {0}; Nicht gefunden: {1}".format(hit, niete))
    log.log("Ende!")
    log.close()
