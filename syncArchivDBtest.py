'''
Testet, ob die DB 'vidarch.db' mit dem Archiv Synchronisiert ist
d.h.    - alle filme in der DB finden sich so auch im Archiv
        - alle Filme im Archiv sind auch so in der DB verzeichnet

rg, 2023-02-13

    # Wenn der Job mit Parameter gestartet wrd, wird nur dieser Ordner geprüft,
    # ansonsten das gesamter VideoArchiv
    # z.B. 'syncArchivDBtest.py __in3' prüft nur den Ordner V:\video\__in3
Änderungen:
2023-02-13  erster Entwurf unter mysql
            
'''
import os 
import sys
import hashlib
from sameLinePrint import sameLinePrint
from datetime import datetime
from privat import DBZugang


# Dictionary, um ANSI-Sequenzen in der Ausgabe zu kapseln
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "YELLOW": "\033[93m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}


version = "1.0 vom 2023-02-13"
medienTypen = ['.m4v', '.m2v', '.mpg', '.mp2', '.mp3', '.mp4', '.ogg', '.mkv', '.webm']

if sys.platform.lower() == "linux":
    ARCHIV = "/archiv/video"
else:
    ARCHIV = "y:/video"

DBNAME=DBZugang.DBNAME
vidPfad = ARCHIV
fehlerListe = []
fehlerAusgabe = "syncArchivTestError.log"
anzMedien_1 = 0
anzMedien_2 = 0

import shutil 
anzahlSpalten = shutil.get_terminal_size().columns  

def fehlerMeldung(fehler):
    fehlerListe.append(fehler)    


# --------------------------------------------------------------------------------------
# DB Init
# --------------------------------------------------------------------------------------
from vidarchdbStruct import *

# from sqlalchemy import create_engine, dialects
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, ForeignKey, UniqueConstraint
# from sqlalchemy.sql.sqltypes import Integer, String, Text
from sqlalchemy import and_
# from sqlalchemy import delete
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import SQLAlchemyError

# SQLECHO = False

# engine = None
# base = declarative_base()
# Session = sessionmaker()
# DBError  = ""   # ggf. für eine Fehlermeldung
# --------------------------------------------------------------------------------------
# DB Init Ende
# --------------------------------------------------------------------------------------

def ausgabe(typ: str, txt: str):
    global anzahlSpalten
    if typ == "ok":
        print("\r"  + " "*anzahlSpalten + "\r" + txt, end="")
    elif typ == "fehler":
        fehlerMeldung(txt)
        print(COLOR["RED"] + "\r"  + " "*anzahlSpalten + "\r" + txt + COLOR["ENDC"], end="")
    else:
        print(COLOR["GREEN"] + "\r"  + " "*anzahlSpalten + "\r"  + txt + COLOR["ENDC"], end="")

def make_md5(DateiName):
    '''
    berechnet die MD5 einer Datei
    Parameter:
        DateiName: voller Dateinam mit Pfad
    Return:
        MD5-Checksum der Datei
    '''
    chunkSize = 8*1024*1024
    with open(DateiName, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(chunkSize):
            file_hash.update(chunk)
            print
    md5 = file_hash.hexdigest()
    # print(md5)  # to get a printable str instead of bytes
    return md5


def syncDBmitArchiv(startOrdner=vidPfad):
    '''
    1. Durchlauf
    prüft, ob alle Medien, die im ARCHIV sind, auch in der DB verzeichnet sind
    und legt sie ggf. an
    '''
    global DB, Session, anzMedien_1
    aktOrdner = ""

    for root, dirs, files in os.walk(startOrdner, topdown=True):
        # print(root, dirs, files)
        # zunächst die pfadId des Ordners bestimmen
        relPfad = root[len(ARCHIV) +1:]

        if relPfad == "":
            continue    # root=vidPfad überspringen
        relPfadId = 0
        relPfad = relPfad.replace("\\", "/")
        with Session() as session:
            try:
                qres = session.query(vapfad).filter(vapfad.relPath == relPfad).first()
                if qres:
                    relPfadId = qres.id
                else:
                    # fehlende Ordner ID's gibst nicht
                    # print(f"{root =}, {relPfad =}, KEINE ID für diesen Ordner!")
                    continue
            except SQLAlchemyError as e:
                DBerror = str(e.orig)
                ausgabe("fehler", "Kann die PfadId von Ordner {relPfad} nich bestimmen!\n" + DBerror)
                break

        for datei in files:
            # fullPathName = os.path.join(root, datei)
            if not root == aktOrdner:
                # Ordnerwechsel
                aktOrdner = root
            _, ext = os.path.splitext(datei)
            if not ext in medienTypen:
                continue

            anzMedien_1 += 1
            if filmIstInDerDB(relPfadId, datei):
                ausgabe("ok", f"OK : {relPfad} ({relPfadId}) : {datei}")
            else:
                ausgabe("fehler", f"Err: {relPfad} ({relPfadId}) : {datei}")
        # end for datei in files...

    # end for (root, ...)

    print(f"\nEnde SyncDB_mit_Archiv!")
    print("")
    return


def filmIstInDerDB(ordnerId, film):
    '''
    prüft, ob ein Film in der DB ist
    Parameter:
        ordnerId:   die PfadeId (int) des Ordners
        film:       Name des Films mit Extension
    Returns:    True oder False
    '''
    global DB, Session

    with Session(bind=DB) as session:
        try:
            exists = session.query(vainhalt.id).filter(and_(vainhalt.relPath == ordnerId, vainhalt.dateiName == film)).first() is not None
        except SQLAlchemyError as e:
            DBerror = str(e.orig)
            ausgabe("fehler", f"Kann die Existenz von OrdnerId: {ordnerId}, Datei: {datei} nicht prüfen\n" + DBerror)
            exists = False
    return exists


def syncArchivmitDB(startOrdner=vidPfad):    
# ----------------------------------------------------------
    # prüft für jeden Film in der DB, ob er auch auf Platte vorhanden ist
    # 2. Durchlauf
    global DB, Session, DBerror, anzMedien_2

    if startOrdner.startswith(ARCHIV):
        relStart = startOrdner[len(ARCHIV)+1:]
    else:
        relStart = startOrdner
    if relStart:
        print(relStart)
    else:
        print("relStart=None")
    with Session(bind=DB) as session:
        try:
            if relStart is None: # .join(vapfad)\
                q = session.query(vapfad.id, vapfad.relPath, vainhalt.id, vainhalt.dateiName)\
                    .join(vainhalt, vapfad.id == vainhalt.relPath )\
                    .group_by(vapfad.id, vainhalt.dateiName)\
                    .all()
            else:
                q = session.query(vapfad.id, vapfad.relPath, vainhalt.id, vainhalt.dateiName)\
                    .filter(vapfad.relPath.startswith(relStart))\
                    .join(vainhalt, vapfad.id == vainhalt.relPath )\
                    .group_by(vapfad.id, vainhalt.dateiName)\
                    .all()

        except SQLAlchemyError as e:            
            DBerror = f"DB-Scan kann nicht laufen! Query meldet Fehler: " + str(e.orig)
            ausgabe("fehler", DBerror + "\n")
            return

        ausgabe("ok", f"Anzahl Medien: {len(q)}")
        for res in q:
            anzMedien_2 +=1
            film = os.path.join(ARCHIV, res.relPath, res.dateiName)
            if os.path.exists(film):
                ausgabe("ok", f"{res.relPath} : {film} gefunden")                
            else:       
                x = f"{res.relPath} : {film} FEHLT im Archiv!"
                ausgabe("fehler", x + "\n")
        # end for ...
    
    # with 'Session = ...'
    #                 
    print(f"\nEnde SyncArchivMitDB!")
    print("")
    return
    

if __name__ == "__main__":

    os.system('')   # magic Call to enable ANSi-Seq.
    print("=" * 80)
    print(COLOR["YELLOW"] + 'SyncArchivDBTest.py' + ' by ruegi,' + COLOR["ENDC"])
    print(COLOR["YELLOW"] + f'Version: {version}' + COLOR["ENDC"])
    
    print("=" * 80)

    # Wenn der Job mit Parameter gestartet wrd, wird nur dieser Ordner geprüft,
    # ansonsten das gesamter VideoArchiv
    # z.B. 'SyncArchivDBTest.py __in3' prüft nur den Ordner V:\video\__in3
    relPfad = None
    vPfad = vidPfad
    teilSuche = False
    if len(sys.argv) > 1:
        # prüfen, ob es diesen Ordner als Ordner existiert
        startord = os.path.join(vidPfad, sys.argv[1])
        if os.path.exists(startord):
            relPfad = sys.argv[1]
            vPfad = startord
            teilSuche = True

    # 1. Lauf: alle Filme im Archiv in der DB vorhanden?
    # -------------------------------------------------
    print(COLOR["GREEN"] + '1. Lauf: Archiv-DurchLauf')
    print("-" * 80)
    print(COLOR["ENDC"])

    syncDBmitArchiv(startOrdner=vPfad)

    # 2. Lauf: alle Filme der DB im Ordner suchen
    print(COLOR["GREEN"] + '2. Lauf: DB-DurchLauf')
    print("-" * 80)
    print(COLOR["ENDC"])

    syncArchivmitDB(startOrdner=vPfad)

    # Ergebnisauswertung
    print("\n" + COLOR["GREEN"] + f"Fertig! Es wurden {anzMedien_1}/{anzMedien_2} Medien verarbeitet." + COLOR["ENDC"])

    if fehlerListe:
        print("\n" + COLOR["RED"] + f":-( Es gab {len(fehlerListe)} Fehler!" + COLOR["ENDC"])    
        print(f"siehe Liste der Fehler in {fehlerAusgabe}!")
        with open(fehlerAusgabe, a) as fa:
            print(f"Fehler der SyncArchiv Testung vom {datetime.now()}", file=fa)
            for zle in fehlerListe:
                print(zle, file=fa)
    else:
        print("\n" + COLOR["GREEN"] + ":-) Alles OK!" + COLOR["ENDC"])
        print()
