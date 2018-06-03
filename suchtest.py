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
    :param such:        Suchbegriff 1
    :param such2:       Suchbegriff 2
    :param ausgabefkt:  None oder der Name einer Funktion, um den letzten gefundenen EIntrag zu zeigen
    :return:            Liste mit den vollen Namen der gefundenen Videos
    '''
    such = such.lower()
    if such2 is None:
        doSuch2 = False
    else:
        such2 = such2.lower()
        doSuch2 = True
    lst = []
    lst2 = []
    for root, dirs, files in os.walk(ziel):
        for f in files:
            fl = f.lower()
            if such in fl:
                x = os.path.join(root, f)
                lst.append(x)
    if doSuch2:
        for f in lst:
            fl = f.lower()
            if such2 in fl:
                lst2.append(f)
                if not ausgabefkt is None:
                    ausgabefkt(f)
        return lst2
    else:
        return lst

such = "X-Men"
such2 = None    #"Beyond"

print("Suche...", end=" ")
erg = findewas(such, such2, None)
print("OK")
if erg == []:
    print("Nicht gefunden")
else:
    for f in erg:
        print(f)
