'''
testet die suchlogik von vidsuch

'''
import os

quelle = "e:\\filme\\schnitt"
ziel = "Y:\\video"

def ausgabe(text):
    print(text)

def findewas(such, such2, ausgabefkt):
    '''
    Findet Videos nach Stichworten
    sucht unabhängig von Groß/klein-schreibung
    enthält der erste suchbegriff "such" eine Blank, so wird auch nach "_" an dieser Stelle gesucht
    :param such:        Suchbegriff 1
    :param such2:       Suchbegriff 2
    :param ausgabefkt:  None oder der Name einer Funktion, um den letzten gefundenen EIntrag zu zeigen
    :return:            Liste mit den vollen Namen der gefundenen Videos
    '''
    such = such.lower()
    repl_mode = False
    if " " in such or "_" in such:
        such_ = such.replace(" ", "_")      # such1 = such, aber komplett mit _ statt Blank
        suchb = such.replace("_", " ")       # such wie such, aber komplett mit Blank (kein _)
        repl_mode = True
    if such2 is None:
        doSuch2 = False
    else:
        such2 = such2.lower()
        doSuch2 = True
    lst = []
    for root, dirs, files in os.walk(ziel):
        for f in files:
            fl = f.lower()
            x = None
            if repl_mode:
                if suchb in fl or such_ in fl:
                    if doSuch2:
                        if such2 in fl:
                            x = os.path.join(root, f)
                    else:
                        x = os.path.join(root, f)
            else:
                if such in fl:
                    if doSuch2:
                        if such2 in fl:
                            x = os.path.join(root, f)
                    else:
                        x = os.path.join(root, f)
            if x is None:
                continue
            else:
                lst.append(x)
    return lst

such = "Inspector Barnaby"
such2 = "Dame"
# such2 = None
print("Suche...", end=" ")
erg = findewas(such, such2, None)
print("Fertig")

if erg == []:
    print("Nichts gefunden")
else:
    for f in erg:
        print(f)
