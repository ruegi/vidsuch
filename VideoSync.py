'''
Synchronisiert die DB 'vidarch.db' mit dem Archiv,
bestimmt ggf. die md5-Werte der Filme
rg, 2022-05-29

    # Wenn der Job mit Parameter gestartet wrd, wird nur dieser Ordner geprüft,
    # ansonsten das gesamter VideoArchiv
    # z.B. 'VideoSync __in3' prüft nur den Ordner V:\video\__in3

'''
import vidarchdb
import os 
import sys
import hashlib
from sameLinePrint import sameLinePrint
import datetime
import sqlalchemy.sql.default_comparator

# from typing import List

# Dictionary, um ANSI-Sequenzen in der Ausgabe zu kapseln
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

mitMD5 = False
vidPfad = "v:\\video"
version = "1.1 vom 2022-05-30"
medienTypen = ['.m4v', '.m2v', '.mpg', '.mp2', '.mp3', '.mp4', '.ogg', '.mkv', '.webm']
DBNAME="V:\\video\\vidarch.db"

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
    aktOrdner = ""
    anz = 0
    anzD = 0
    neu = True
        
    for (root, _, files) in os.walk(startOrdner, topdown=True):
        # print(root, dirs, files)
        for datei in files:
            # fullPathName = os.path.join(root, datei)            
            if not root == aktOrdner:
                # Ordnerwechsel
                if aktOrdner:   # meint aktOrdner > ""
                    sameLinePrint(f"    --- {anzD} Medien im Ordner [{aktOrdner}]")
                    print("")
                anzD = 0
                aktOrdner = root
                neu = True                                
            _, ext = os.path.splitext(datei)
            if not ext in medienTypen:
                continue
            # print(f"  >>> {datei}")
            relPath = root[len(vidPfad) +1:]
            # print(f"\r{aktOrdner} : {datei}" + " "*80, end="")
            # print(f"Gefunden: {relPath}  -  {datei}" + " "*80)
            ret = vidarchdb.film_merken(relPath, datei, ext, "", verbose=False )
            sameLinePrint(f"\r{ret}{aktOrdner} : {datei}")

            neu = False
            anz +=1
            anzD +=1
        sameLinePrint(" ")  # Ausgabezeile löschen
        print("")           # neue Zeile
    return anz


if __name__ == "__main__":

    os.system('')   # magic Call to enable ANSi-Seq.
    print("=" * 80)
    print(COLOR["BLUE"] + 'VideoSync.py' + COLOR["ENDC"] + ' by ruegi,')
    print(COLOR["BLUE"] + f'Version: {version}' + COLOR["ENDC"])
    
    print("=" * 80)

    # print(f"DBNAME={DBNAME}")

    vidarchdb.defineDBName(DBNAME)
    if not vidarchdb.dbconnect(mustExist=True, SQLECHO=False):
        print("FEHLER!")
        print(f"kann die DB {DBNAME} nicht verbinden!")
        print("Ende ohne Verarbeitung!")
        exit(0)
    else:
        print(f"Verbundene DB: {vidarchdb.engine.url.database}")

    # Wenn der Job mit Parameter gestartet wrd, wird nur dieser Ordner geprüft,
    # ansonsten das gesamter VideoArchiv
    # z.B. 'VideoSync __in3' prüft nur den Ordner V:\video\__in3
    relPfad = None
    vPfad = vidPfad
    teilSuche = False
    if len(sys.argv) > 1:
        # prüfen, ob es diesen Ordner im VideoArchiv gibt
        startord = os.path.join(vidPfad, sys.argv[1])
        if os.path.exists(startord):
            relPfad = sys.argv[1]
            vPfad = startord  
            teilSuche = True

    print(f'DBSync mit VideoOrdner [{vPfad}]\n')


    # 1. Lauf: alle Filme im Archiv in DB unterbringen
    print(COLOR["GREEN"] + '1. Lauf: Archiv-DurchLauf')
    print("-" * 80)
    print(COLOR["ENDC"])

    anz = syncDBmitArchiv(startOrdner=vPfad)

    # 2. Lauf: alle Filme der DB im Ordner suchen, sonst löschen
    print(COLOR["GREEN"] + '2. Lauf: DB-DurchLauf')
    print("-" * 80)
    print(COLOR["ENDC"])

    ret = vidarchdb.db_scan(Pfad=relPfad)
    if ret:
        print("\n" + COLOR["RED"] + f"DB-Problem: {ret}" + COLOR["ENDC"])

    if teilSuche:
        vidarchdb.set_config("letzterTeilSync", datetime.datetime.now() )
        vidarchdb.set_config("letzterTeilSyncOrdner", relPfad )
    else:
        vidarchdb.set_config("letzterFullSync", datetime.datetime.now() )

    print("\n" + COLOR["GREEN"] + f"Fertig! Es wurden {anz} Medien verarbeitet." + COLOR["ENDC"])



