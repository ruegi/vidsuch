# -*- coding: utf-8 -*-
"""
@author: rg

Kleines, reines Batchprogramm.
Prüft, ob jede Datei der Quelle in einem Unterordner des Ziels vorhanden ist

"""

import logger
import os

#quelle = "c:\\temp\\x"
quelle = "e:\\filme\\schnitt.alt"
ziel = "y:\\video"

def findeDatei(datei):
    x = None
    for root, dirs, files in os.walk(ziel):
        if datei in files:
            x = os.path.join(root, datei)
            break
    return x

if __name__ == "__main__":
    log = logger.openlog(logName="vidvgl", TimeStamp=True, printout=True, replace=True)

    i = 0    
    niete = 0   # name nicht gefunden
    hit = 0     # nur name stimmt
    nl_hit = 0  # nur name & Länge stimmen
    nd_hit = 0  # nur name & Datum stimmen
    nld_hit = 0 # name, länge und Datum stimmen
    lst_niete = []
    lst_n = []
    lst_nl = []
    lst_nd = []
    lst_nld = []
    
    for entry in os.scandir(quelle):
        if entry.is_file():
            i += 1
            filmdatei = entry.name
            qdatei = os.path.join(quelle, filmdatei)
            qlen = os.stat(qdatei).st_size
            qdat = os.stat(qdatei).st_mtime
            log.log("Bearbeite: {0:2}: {1}:".format(i, qdatei))
            zdatei = findeDatei(filmdatei)
            if zdatei is None:
                log.log("--- nicht gefunden\n")
                lst_niete.append(filmdatei)
                niete += 1
            else:
                # hier noch weitere tests
                zlen = os.stat(zdatei).st_size
                zdat = os.stat(zdatei).st_mtime
                if (qlen == zlen):
                    if (qdat == zdat):
                        log.log("--- gefunden: {0} (Voller Treffer)".format(zdatei))
                        nld_hit += 1
                        lst_nld.append(filmdatei)
                    else:
                        log.log("--- gefunden: {0} (Nur Name und Länge stimmen)".format(zdatei))
                        nl_hit += 1
                        lst_nl.append(filmdatei)
                else:
                    if (qdat == zdat):
                        log.log("--- gefunden: {0} (Nur Name und Datum stimmen)".format(zdatei))
                        nd_hit += 1
                        lst_nd.append(filmdatei)
                    else:
                        log.log("--- gefunden: {0} (Nur Name stimmt)".format(zdatei))
                        hit += 1
                        lst_n.append(filmdatei)
    log.log("-" * 80)
    log.log("Name gefunden: {0}; Name nicht gefunden: {1}".format(hit + nld_hit + nd_hit + nl_hit, niete))

    log.log("Name, Länge & Datum: \t{0}".format(nld_hit))
    for name in lst_nld:
        log.log("\t{0}".format(name))

    log.log("Name & Länge gefunden: \t{0}".format(nl_hit))
    for name in lst_nl:
        log.log("\t{0}".format(name))

    log.log("Name & Datum gefunden: \t{0}".format(nd_hit))
    for name in lst_nd:
        log.log("\t{0}".format(name))

    log.log("Nur Name gefunden: \t{0}".format(hit))
    for name in lst_n:
        log.log("\t{0}".format(name))

    log.log("Name nicht gefunden: \t{0}".format(niete))
    for name in lst_niete:
        log.log("\t{0}".format(name))

    log.log("Ende!")
    log.close()
