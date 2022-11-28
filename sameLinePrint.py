'''
sameLinePrint.py

'''
import shutil 
anzahlSpalten = shutil.get_terminal_size().columns  


def sameLinePrint(txt: str):    
    '''
    druckt den Text 'txt' in die selbe Zeile, in der aktuell der Cursor steht
    und löscht den Rest der Zeile
    '''
    leer = " " * anzahlSpalten
    print(f"\r{leer}\r" , end="")
    l = len(txt)
    if l > anzahlSpalten:
        txt = txt[-1*anzahlSpalten:]
    else:
        if txt == " ":
            txt = " " * anzahlSpalten
        else:
            txt = txt + " "*(anzahlSpalten-l)
    print(f"\r{txt}\r" , end="")

# only 4 testing
if __name__ == "__main__":
    print("Zeile 1: fds fjds fjkds öfjkldsö kfds fjkdslöa jfkldös ajklföd sjklf d--1")    
    sameLinePrint("Das ist ganz Lang"*10)
    # print("")
    sameLinePrint("Das ist kurz\n")
    # print("")
    print("Zeile 2: fds fjds fjkds öfjkldsö kfds fjkdslöa jfkldös ajklföd")
    sameLinePrint("Das ist kurz")
    sameLinePrint("Zeile 3: fds fjds fjkds öfjkldsö kfds fjkdslöa jfkldös ajklföd--3")
    sameLinePrint("Zeile 4: fds fjds fjkds öfjkldsö kfds fjkdsl--4")
    print("")

