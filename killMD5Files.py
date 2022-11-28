"""
killMD5Files.py
löscht alle im Ordner Y:\video geundenen Dateien
mit Namen '._md5List.inf' oder '.md5List.csv'
Diese wurden in einem Vorläufer der VidSuch DB-Lösung ausprobiert, sond aber jetzt
hinfällig

rg, ab 2022-11-22
"""

import os 
import sys

# Dictionary, um ANSI-Sequenzen in der Ausgabe zu kapseln
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

md5Dateien = [".md5List.csv",'._md5List.inf']
if sys.platform == "win32":
    vidPfad = "Y:/video"
else:
    vidPfad = "/archiv/video"

version = "1.0 vom 2022-11-24"

def dateiLoeschen(name: str)->bool:
    try:
        os.remove(name)
        print(COLOR["GREEN"] + f"> gelöscht: {name}" + COLOR["ENDC"] )        
    except OSError as error:
        print(COLOR["RED"] + f"> FEHLER: {name}" + COLOR["ENDC"] )
        print(error)
        return False
    return True

def headline(pgm: str, version: str):
    header = COLOR["BLUE"] + pgm + " "*(80-len(pgm)-8) + "by RUEGI"+ COLOR["ENDC"]
    v = f"Version: {version}"
    scnd   = COLOR["BLUE"] + " "*(80-len(v)) + v + COLOR["ENDC"] 
    print("=" * 80)
    print(header)
    print(scnd)
    print("=" * 80)
    return


if __name__ == "__main__":
    
    os.system('')   # magic Call to enable ANSi-Seq.
    headline("killMD5Files.py", version)
    aktOrdner = ""
    anz = 0
    # print("Jetzt in .. ", vidPfad)
    for (root,dirs,files) in os.walk(vidPfad, topdown=True):
        for md5_file in md5Dateien:
            if md5_file in files:
                fullmd5PathName = os.path.join(root, md5_file)
                if dateiLoeschen(fullmd5PathName):
                    anz +=1

    print(COLOR["BLUE"] + f"Fertig! Es wurden {anz} md5-Dateien entfernt."  + COLOR["ENDC"])

    
