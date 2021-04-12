#  python3
# -*- coding: utf_8 -*
#
# logger.py
# ----------------
# Exportiert die Prozeduren
#
#
#
#
#  rg, ab 2016-08-23
#
# Änderungen
# ab 2016-10-26 objektorientiert
# 2016-10-27    vereinfachtes Handling; TimeStamp eingeführt
# -----------------------------------------------------------------------------------
from datetime import datetime
import os
from pathlib import Path
import tempfile

class logFile:

#    def __init__(self, lname=os.path.basename(__file__)+".log", TimeStamp=None, printout=True):
    def __init__(self, lname, TimeStamp=None, printout=True):
        self.TimeStamp = False
        self.LogName = lname
        self.printout = printout
        self.TimeStamp = TimeStamp
        _zeit = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        _wid = 109 if TimeStamp == True else 80
        if TimeStamp == True:
            self.TimeStamp = True
        self.logEintrag("{0} : Beginn LOG [{1}]".format(_zeit, self.LogName))
        # self.logEintrag(("Beginn LOG [{0}] um {1}\n" + _wid * "-").format(self.LogName, _zeit))

    def close(self) -> object:
        _zeit = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        _wid = 109 if self.TimeStamp else 80
        # self.TimeStamp = False  # nötig, um den doppelten Timestamp zu verhindern
        self.logEintrag("Ende  LOG [{0}]".format(self.LogName))
        # self.logEintrag(_wid * "-" + "\n>>Ende LOG [{0}] um {1}\n\n".format(self.LogName, _zeit))

    def log(self, logText):
        self.logEintrag(logText)

    def logEintrag(self, logText):
        """
        schreibt den String logText in die Log-Datei und auf den Schirm
        :rtype: nil
        :param lstr: string
        :return: nil
        """
        lg = open(self.LogName, encoding="utf-8", mode='a')
        lt = ""
        if self.TimeStamp:
            # jede Zeile mit einemTimeStamp versehen
            dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            lts = logText.split("\n")
            for st in lts:
                lt = lt + dt + " : " + st + "\n"
        else:
            lt = LogText + "\n"
        lg.writelines(lt)
        lg.close()
        if self.printout:
            print(lt)

# ----Klasse LogFile Ende----------------------------------------------------------------------


def openlog(logName=None, TimeStamp=False, printout=True, replace=True):
    """
    Eröffnet das Logging, indem eine Instanz eines Log-Objekts erzeugt
    und zurückgegeben wird.
    :param  logName:   Name der LogDatei (optional: default = "logger.py_{Datum&Zeit}.log)
                        (die Datum&Zeit-Angabe im Namen wird nur ergänzt, wenn TimeStamp=True ist)
            TimeStamp: boolean  (optional; default = False)
                        bestimmt, ob der DateiNamen und jede Zeile zu Beginn einen Zeitstempel enhält
        :return Referenz auf ein Log-Objekt
    """
    if logName is None:
        logName = os.path.basename(__file__)
    if TimeStamp:
        logName = logName + datetime.now().strftime("__%Y-%m-%d_%H-%M-%S") + ".log"
    else:
        logName = logName + ".log"
    if replace:
        # exfile =
        if Path(logName).exists():
            try:
                open(logName, mode='w')  # alte Datei überschreiben
            except:
                logName = tempfile.mkstemp(suffix=".log", prefix="VidSuch", dir=".\\", text=True)
                print("Kann die alte Log-Datei nicht löschen!\nNehme den temp-FileName {0}!".format(logName))
    return(logFile(logName, TimeStamp, printout))

if __name__ == "__main__":
    log = openlog(TimeStamp=True)
    log.logEintrag("Erster!")
    log.log("Letzter Log-Eintrag")
    log.log("Bye!")
    log.close()


