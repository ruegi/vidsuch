"""
genMD5.py
erzeugt für alle im ordner enthaltenen Filme MD5 Werte
und speichert diese im Ordner der Videos unter '._md5List.inf'

rg, ab 2022-02-22
- V2.0 mit os.walk statt scandir

EXPERIMENTELL!
Diese Technik wurde abgelöst durch die DB-Technik
Siehe auch killMD5Files.py, um die erzeugten dateien wieder zu entfernen!
rg, 11.2022
"""

import os 
import hashlib

from typing import List

# Dictionary, um ANSI-Sequenzen in der Ausgabe zu kapseln
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

md5Datei = ".md5List.csv"
# vidPfad = "y:\\video\\Unterhaltung\\Horror"
vidPfad = "/archiv/video"
version = "2.1 vom 2022-02-25"
medienTypen = ['.m4v', '.m2v', '.mpg', '.mp2', '.mp3', '.mp4', '.ogg', '.mkv', '.webm']

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
        chunk = f.read(chunkSize)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunkSize)
            
    md5 = file_hash.hexdigest()
    # print(md5)  # to get a printable str instead of bytes
    return md5


def info_schreiben(ordner, md5, neu=False):    
    infoDatei = os.path.join(ordner, md5Datei)    # die md5Datei im selben ordner nutzen wie das Video
    wMode = "w" if neu else "a"
    with open(infoDatei, wMode) as f:
        print(f'"{datei}","{md5}"', file=f)
    

if __name__ == "__main__":
    
    os.system('')   # magic Call to enable ANSi-Seq.
    print("=" * 80)
    print(COLOR["BLUE"] + 'genMD5.py' + COLOR["ENDC"] + ' by ruegi,')
    print(COLOR["BLUE"] + f'Version: {version}' + COLOR["ENDC"])
    print("=" * 80)

    aktOrdner = ""
    anz = 0
    anzD = None
    neu = True
    # print("Jetzt in .. ", vidPfad)
    for (root,dirs,files) in os.walk(vidPfad, topdown=True):
        for datei in files:
            fullPathName = os.path.join(root, datei)            
            if not root == aktOrdner:
                # Ordnerwechsel
                if not anzD is None:
                    print(f"    --- {anzD} Medien im Ordner {aktOrdner}")
                anzD = 0
                aktOrdner = root
                neu = True
                print("Jetzt in .. ", aktOrdner)
            _, ext = os.path.splitext(datei)
            if not ext in medienTypen:
                continue
            print(f"  >>> {datei}")
            md5 = make_md5(fullPathName)
            info_schreiben(root, md5, neu=neu)
            neu = False
            anz +=1
            anzD +=1

    print(f"    --- {anzD} Medien im Ordner\n")
    print(f"Fertig! Es wurden {anz} Medien verarbeitet.")
