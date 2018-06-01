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

quelle = "e:\\filme\\schnitt"
ziel = "y:\\video"

def findeDatei(datei):
    x = None
    for root, dirs, files in os.walk(ziel):
        if datei in files:
            x = os.path.join(root, datei)
            break
    return x

if __name__ == "__main__":
    log = logger.openlog(TimeStamp=True, printout=True, replace=True)

    i = 0
    hit = 0     # nur name stimmt
    nl_hit = 0  # nur name & Datum stimmen
    nd_hit = 0  # nur name & Länge stimmen
    nld_hit = 0 # name, länge und Datum stimmen
    niete = 0
    for entry in os.scandir(quelle):
        if entry.is_file():
            i += 1
            qdatei = os.path.join(quelle, entry.name)
            qlen = os.stat(qdatei).st_size
            qdat = os.stat(qdatei).st_ctime
            log.log("Bearbeite: {0:2}: {1}:".format(i, qdatei))
            zdatei = findeDatei(entry.name)
            if zdatei is None:
                log.log("--- nicht gefunden\n")
                niete += 1
            else:
                # hier noch weitere tests
                zlen = os.stat(zdatei).st_size
                zdat = os.stat(zdatei).st_ctime
                if (qlen == zlen):
                    if (qdat == zdat):
                        log.log("--- gefunden: {0} (Voller Treffer)".format(zdatei))
                        nld_hit += 1
                    else:
                        log.log("--- gefunden: {0} (Nur Name und Länge stimmen)".format(zdatei))
                        nl_hit += 1
                else:
                    if (qdat == zdat):
                        log.log("--- gefunden: {0} (Nur Name und Datum stimmen)".format(zdatei))
                        nd_hit += 1
                    else:
                        log.log("--- gefunden: {0} (Nur Name stimmt)".format(zdatei))
                        hit += 1
    log.log("Name gefunden: {0}; Name nicht gefunden: {1}".format(hit + nld_hit + nd_hit + nl_hit, niete))
    log.log("Name, Länge & Datum: \t{0}".format(nld_hit))
    log.log("Name & Länge gefunden: \t{0}".format(nl_hit))
    log.log("Name & Datum gefunden: \t{0}".format(nd_hit))
    log.log("Nur Name gefunden: \t{0}".format(hit))
    log.log("Ende!")
    log.close()
