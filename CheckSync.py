'''
Prüft, ob die MD5-Werte aller Filme im übergeben Ordner mit denen in der DB übereinstimmen
Schreibt zum Ende ein Protokoll aller Fehler nach stdout
rg, 2022-06-12
Änderungen:
2022-12-03  Umstellung auf mysql
'''
import vidarchdb
import os 
import sys
import hashlib
from sameLinePrint import sameLinePrint
# import datetime
# import sqlalchemy.sql.default_comparator
from privat import DBZugang

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
version = "1.0 vom 2022-12-03"
medienTypen = ['.m4v', '.m2v', '.mpg', '.mp2', '.mp3', '.mp4', '.ogg', '.mkv', '.webm']

if sys.platform.lower() == "linux":
    ARCHIV = "/archiv/video"
else:
    ARCHIV = "y:/video"
DBNAME=DBZugang.DBNAME
vidPfad = ARCHIV

Fehler = []

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

def checkMD5(startOrdner=vidPfad)->int:
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
            relPath = root[len(vidPfad) +1:]
            ret = vidarchdb.getFilmMD5(relPath, datei)
            if ret == "":
                sameLinePrint(f"{aktOrdner} : {datei}; FEHLER: kein MD5-Wert gefunden")
                sammleFehler(relPath, datei, "MD5-Wert nicht in der DB gefunden!")
                print("")
            else:
                sameLinePrint(f"{aktOrdner} : {datei} Prüfe MD5...")
                fullName = os.path.join(vidPfad, relPath, datei)
                md = vidarchdb.make_md5(fullName, filler=f"{aktOrdner} : {datei} Prüfe MD5 ")
                if md == ret:
                    sameLinePrint(f"{aktOrdner} : {datei} Prüfe MD5...OK!")
                else:
                    fe = f"MD5-FEHLER: DB={ret}; Archiv={md}"
                    sameLinePrint(f"{aktOrdner} : {datei}; {fe}")
                    sammleFehler(relPath, datei, fe)
                print()
            neu = False
            anz +=1
            anzD +=1
        sameLinePrint(" ")  # Ausgabezeile löschen
        print("")           # neue Zeile
    return anz

def sammleFehler(relP, Dat, Err):
    global Fehler
    x = [relP, Dat, Err]
    Fehler.append(x)


if __name__ == "__main__":

    os.system('')   # magic Call to enable ANSi-Seq.
    print("=" * 80)
    print(COLOR["BLUE"] + 'ChecSync.py' + COLOR["ENDC"] + ' by ruegi,')
    print(COLOR["BLUE"] + f'Version: {version}' + COLOR["ENDC"])
    
    print("=" * 80)

    # vidarchdb.defineDBName(DBNAME)
    if not vidarchdb.dbconnect(mustExist=True, SQLECHO=False):
        print("FEHLER!")
        print(f"kann die DB {DBZugang.DBTitel} nicht verbinden!")
        print("Ende ohne Verarbeitung!")
        exit(0)
    else:
        print(f"Verbundene DB: {DBZugang.DBTitel}")

    # Wenn der Job mit Parameter gestartet wrd, wird nur dieser Ordner geprüft,
    # ansonsten das gesamter VideoArchiv
    # z.B. 'CheckSync __in3' prüft nur den Ordner V:\video\__in3
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

    print(f'CheckSync in VideoOrdner [{vPfad}]\n')

    # Ürüfung entlang des Archiv-Ordners...
    anz = checkMD5(vPfad)    
    fanz = len(Fehler)
    if fanz == 0:
        print("\n" + COLOR["GREEN"] + "Keine Fehler gefunden!" + COLOR["ENDC"])
    else:                
        for res in Fehler:
            print(COLOR["RED"] + f"{res[0]}: {res[1]} - {res[2]} "+ COLOR["ENDC"])
        if fanz > 1:
            print(f"--- Das waren {fanz} Fehler")
        else:
            print(f"--- Das war 1 Fehler")
    
    # if teilSuche:
    #     vidarchdb.set_config("letzterTeilSync", datetime.datetime.now() )
    #     vidarchdb.set_config("letzterTeilSyncOrdner", relPfad )
    # else:
    #     vidarchdb.set_config("letzterFullSync", datetime.datetime.now() )

    print("\n" + COLOR["GREEN"] + f"Fertig! Es wurden {anz} Medien verarbeitet." + COLOR["ENDC"])



