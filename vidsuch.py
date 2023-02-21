
# -*- coding: utf-8 -*-
'''
Created on 2018-06-01
@author: rg
VidSuch.py mit pyqt5
ermöglicht das Suchen von Videos mit 1 bis 2 Suchbegriffen
Version 3 : Erweiterung auf Umbenennen und Löschen von Videos
            rg 2018-11-22
Änderungen:
2021-03-09  V6
            neues Untermodul FilmDetails eingefügt
            neuer Hotkey Ctrl+M oder F5, um eine Zwischenablage einzufügen
            neuer Hotkey Ctrl+s oder F4, um einen Text zu splitten
            Menü erzeugt für Doku der Hotkeys & About Dialog
2021-06-01  V6.3
            neues Kontextmeü in der Ergebnisliste
2022-02-11  V6.4
            Änderung der Prozedur 'suchfeldleer2',
            wird ein '\n' oder ':' gefunden. so wird der eingefügte String 
            an dieser Stelle gesplittet und in Suchfeld1 und Suchfeld2 eingefügt
2022-05-28  V7.0
            die Suche wird jetzt über die sqlite-DB VPFAD\vidarch.db geführt
            und damit erheblich beschleunigt.
            Nachteil: die DB muss aktuell gehalten werden!
2022-05-30  V7.1
            Kleine (kosmetische) Korrekturen
2022-05-31  V7.2
            Hinzufügen des Menüpunkts 'Datei/SyncDB" (Funtion Syncdb)
            V7.3
            Die Funktion FilmInfo wird durch einen externen Programmaufruf getätigt
2022-08-01  V7.3.1
            Fehlerbereinigung in vidarchdb.py/findefilm
2022-08-15  V7.4.0
            Strukturbereinigung: vidsuch Sachlogik auf vidarchdb.py (findewas) nach vidsuch.py transportiert
            statt dessen die Funktion getFilmList in vidarchdb.py erzeugt, das eine Menge von Filmnamen zurückliefert
            Die reine Suchlogik mit suchbegriff1/2 ist nur noch in vidsuch.py enthalten
2022-11-29  V7.4.5  
            Umstellung auf PyQt6 und Fehler in findeWas behoben.
2022-12-02  V7.6.0
            DB-Anbindung an MySQL statt sqlite
2023-01-03  Behandlung des Fehlers "(2006, 'MySQL server has gone away')", 
            wenn vidsuch die Nacht über geöffnet war (dann kam es zum harten Absturz)            
            Lösung: siehe im Modul vidarchdb

'''

import sys
import os

# import sqlalchemy
import sqlalchemy.sql.default_comparator        # das braucht pyinstaller zum Finden der Module
import vidarchdb
from privat import DBZugang

# das soll die Importe aus dem Ordner FilmDetails mit einschließen...
sys.path.append(r".\FilmDetails")

# import PyQt5.QtWidgets # Import the PyQt5 module we'll need
from PyQt6.QtWidgets import (QMainWindow,
    	                     QDialog,
                             QLabel,
                             QTableWidgetItem,
                             QAbstractItemView,
                             QHeaderView,
                             QLineEdit,
                             QPushButton,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QApplication,
                             QMessageBox,
                             QInputDialog
                             )
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, Qt
# from QApplication import QClipboard
from PyQt6.QtGui import QIcon, QAction

from math import log as logarit
from datetime import datetime
# from subprocess import Popen, CREATE_NEW_CONSOLE
from subprocess import run as externalRun
from subprocess import Popen

import time

# from FilmDetails import FilmDetails
import VidSuchUI

# Handle high resolution displays (thx 2 https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution):
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

stopFlag = False

class Konstanten:
    ''' Konstanten für den Programmablauf '''
    VPATH = "Y:\\video\\"
    VERSION = "7"
    SUBVERSION = "6.1"
    VERSIONDATE = "2023-01-03"
    DBNAME = DBZugang.DBTitel
    # SYNCDB = ['python.exe', 'c:\\Program Files\\VideoSync\\VideoSync.exe']
    SYNCDB = ['cmd', '/c', 'py', 'VideoSync.py', '_in6']
    FilmInfo = 'c:\\Program Files\\FilmDetails\\FilmDetails.exe'

# --------------------------------------------------------------------------------
# Worker class
# --------------------------------------------------------------------------------
class Worker(QObject):
    '''
    Worker thread
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(list)
    progress = pyqtSignal(str)

    global stopFlag
    stopFlag = False

    # def __init__(self, parent=None):
    #     super().__init__(parent)

    @pyqtSlot()
    def startp(self):
        # print("Thread started")
        pass


    @pyqtSlot(str, str, str)
    def findewas(self, such: str, such2: str, vpath: str):
        ''' 
        Findet Videos nach Stichworten im Archiv-Ordner
        sucht unabhängig von Groß/klein-schreibung
        enthält der erste suchbegriff "such" eine Blank, so wird auch nach "_" an dieser Stelle gesucht
        :param such:        Suchbegriff 1
        :param such2:       Suchbegriff 2
        :param vpath        zu durchsuchender video-Pfad
        :return:            Liste mit den vollen Namen der gefundenen Videos als Signal "result"
        '''
        global stopFlag

        such = such.lower()
        such2 = such2.lower()
        # print(f"in (findewas), Parms: [{such}], [{such2}]")        
        lst = self.findeFilm(such, such2, archiv=Konstanten.VPATH)
        # print(f"nach findefilm, Parms: ({such}), ({such2}]), lst=({lst})")
        if lst is None:     # keine Verbindung zur DB        
            such2 = None if such2 == "" else such2.lower()
            repl_mode = False   # repl_mode wird nur benötigt, wenn such ein Blank oder "_" enthält
            if " " in such or "_" in such:
                such_ = such.replace(" ", "_")  # such1 = such, aber komplett mit _ statt Blank
                suchb = such.replace("_", " ")  # suchb wie such, aber komplett mit Blank (kein _)
                repl_mode = True
            if such2 is None:
                doSuch2 = False
            else:
                doSuch2 = True
                such2_ = such2.replace(" ", "_")  # such2_ = such2, aber komplett mit _ statt Blank
                such2b = such2.replace("_", " ")  # such2b wie such2, aber komplett mit Blank (kein _)
            lst = []
            for root, _, files in os.walk(vpath):
                if stopFlag:
                    break
                for f in files:
                    fl = f.lower()
                    x = None
                    if repl_mode:
                        if suchb in fl or such_ in fl:
                            if doSuch2:
                                if such2 in fl or such2_ in fl or such2b in fl:
                                    x = os.path.join(root, f)
                            else:
                                x = os.path.join(root, f)
                    else:
                        if such in fl:
                            if doSuch2:
                                if such2 in fl or such2_ in fl or such2b in fl:
                                    x = os.path.join(root, f)
                            else:
                                x = os.path.join(root, f)
                    if x is None:
                        continue
                    else:
                        lst.append(x)
                        # self.worker.progress.emit(x)
                        self.progress.emit(x)                
        if not stopFlag:
            self.result.emit(lst)
        return

    def findeFilm(self, suchbegriff1, suchbegriff2, archiv=Konstanten.VPATH):
        '''
        sucht einen Film in der Film-db nach 1-2 Stichworten
        Parms:
        SuchBegriffe 1 und 2,
        benannte Parameter:
            db: Pfad zur sqlite-DB
            archiv: Basis-Pfad zum pyhsischen Archiv / VPATH
        Returns:
            gibt "None" zurück, wenn keine DB verbunden werden kann
            gibt [] zurück, wenn nichts gefunden wurde
        '''
        looking_for = suchbegriff1
        if ' ' in suchbegriff1:
            looking_for = looking_for.replace(' ', '_')
        if  '?' in suchbegriff1:
            looking_for = looking_for.replace('?', '_')
        if  '/' in suchbegriff1:
            looking_for = looking_for.replace('/', '_')
        if  '\\' in suchbegriff1:
            looking_for = looking_for.replace('\\', '_')
        if  '*' in suchbegriff1:
            looking_for = looking_for.replace('*', '%')
        looking_for = '%{0}%'.format(looking_for)

        # print(f"suchbegriff=[{suchbegriff1}], looking_for=[{looking_for}]")   

        if suchbegriff2:
            sb2 = suchbegriff2
            doSuch2 = True
        else:
            doSuch2 = False
            # sb2 = suchbegriff2.replace(" ", "_")
            # sb2 = sb2.replace("_", "[ _]")        
        
        # print(f"Vor query; parms: ({suchbegriff1}), ({looking_for})")

        # den 2. Filterbegriff ggf. auswerten
        lst = []
        anz = 0
        flst = vidarchdb.getFilmListe(looking_for, archiv=archiv)
        if flst is None:            
            flst = self.findeFilm(suchbegriff1, suchbegriff2, archiv)
        for film in flst:
            gefunden = True
            if doSuch2:
                if sb2 not in film.lower():
                    gefunden = False
            if gefunden:
                anz += 1
                lst.append(film)
        
        return lst.sort()

# --------------------------------------------------------------------------------
# VidSuchApp class
# --------------------------------------------------------------------------------
class VidSuchApp(QMainWindow, VidSuchUI.Ui_MainWindow):
    suchAnfrage = pyqtSignal(str, str, str)

    def __init__(self, appN):
        # super(self.__class__, self).__init__()
        QMainWindow.__init__(self)
        VidSuchUI.Ui_MainWindow.__init__(self)

        self.setupUi(self)  # This is defined in VidSuchUI.py file automatically
                            # It sets up layout and widgets that are defined
        # Instanz-Variablen
        self.vpath = Konstanten.VPATH
        self.app = appN
        self.worker = None
        self.delBasket = "__del"
        self.lbl_db.setText("DB: " + Konstanten.DBNAME)

        # Icon versorgen
        scriptDir = str(os.path.dirname(os.path.realpath(__file__)))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'VidSuch.ico'))

        self.btn_suchen.setEnabled(False)
        # btn_suchen.setEnabled(True)
        self.le_such1.textChanged.connect(self.suchBtnAktivieren)
        
        #self.lst_erg.setTextBackgroundColor(QColor("lightyellow"))
        # self.lst_erg.setStyleSheet("background-color: lightyellow;")
        self.lst_erg.setHorizontalHeaderLabels(('Video', 'Länge', 'Datum'))
        self.lst_erg.setAlternatingRowColors(True)
        header = self.lst_erg.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.lst_erg.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.lst_erg.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.lst_erg.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lst_erg.setRowCount(0)
        self.lst_erg.setEnabled(False)

        # connects
        self.btn_suchen.clicked.connect(self.suchen)
        self.btnDel.clicked.connect(self.delVideo)
        self.btnRen.clicked.connect(self.renVideo)
        self.btnInfo.clicked.connect(self.videoInfo)
        self.btnPlay.clicked.connect(lambda: self.videoStart(self.lst_erg.currentRow(), 0))
        self.btnLeer.clicked.connect(self.suchFeldLeer)
        self.btnLeer2.clicked.connect(self.suchFeldLeer2)
        self.btnEnde.clicked.connect(self.close)

        self.actionEinfuegen.triggered.connect(self.suchFeldLeer2)
        self.actionSync.triggered.connect(self.syncDB)
        self.actionEnde.triggered.connect(self.close)
        self.actionSplit.triggered.connect(self.suchFeldSplit)
        self.actionAbout.triggered.connect(self.about)

        # Kontextmenü in der Tabelle lst_erg
        # Actions definieren
        infAct =  QAction('FilmInfo', self.lst_erg, triggered=self.videoInfo)
        separator = QAction(self.lst_erg)
        separator.setSeparator(True)
        zeigAct = QAction('Film zeigen', self.lst_erg, triggered=lambda: self.videoStart(self.lst_erg.currentRow(), 0))
        renAct = QAction('Film umbenennen', self.lst_erg, triggered=self.renVideo)
        delAct =  QAction('Film löschen', self.lst_erg, triggered=self.delVideo)
        # Policy zufügen
        self.lst_erg.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        # Actions zum Kontextmenü zufügen
        self.lst_erg.addAction(infAct)
        self.lst_erg.addAction(separator)
        self.lst_erg.addAction(zeigAct)
        self.lst_erg.addAction(renAct)
        self.lst_erg.addAction(delAct)

        self.statusMeldung("Ready")
        self.warten(False)
        self.proBar.setValue(0)

        #  Thread einrichten, starten und im idle-mode lassen
        self.thread = QThread()
        self.worker = Worker()      # result=self.ergebnis_ausgeben
        self.thread.started.connect(self.worker.startp)
        self.worker.moveToThread(self.thread)
        self.worker.result.connect(self.ergebnis_ausgeben)
        # self.worker.finished.connect(self.thread_complete)
        self.worker.progress.connect(self.statusMeldung)
        self.suchAnfrage.connect(self.worker.findewas)
        self.lst_erg.cellActivated.connect(self.videoStart)
        self.thread.start()

    def buttonflip(self, txt):
        self.btn_suchen.setText(txt)

    def suchBtnAktivieren(self):
        self.btn_suchen.setEnabled(self.le_such1.text().strip() > "")

    # emuliert den default-key
    def keyPressEvent(self, event):
        w = self.focusWidget()
        modifiers = QApplication.keyboardModifiers()

        if event.key() == Qt.Key.Key_F6:
            if w == self.lst_erg:
                self.renVideo()
        elif event.key() == Qt.Key.Key_Delete:
            if w == self.lst_erg:
                self.delVideo()
        elif event.key() == Qt.Key.Key_Return:
            w = self.focusWidget()
            if w == self.le_such1 or w == self.le_such2:
                self.suchen()
            else:
                self.videoStart(self.lst_erg.currentRow, 1)
        elif event.key() == Qt.Key.Key_F2:
            self.videoInfo()
        elif event.key() == Qt.Key.Key_F4:  # Split Feld 1
            self.suchFeldSplit()
        elif event.key() == Qt.Key.Key_F5:  # Paste, wie ctrl+m
            self.suchFeldLeer2()
        elif event.key() == Qt.Key.Key_X:
            # modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.KeyboardModifier.ControlModifier:
                self.suchFeldLeer()
        elif event.key() == Qt.Key.Key_M:       # ctrl+m, um die Zwischenablage einzufügen
            if modifiers == Qt.KeyboardModifier.ControlModifier:
                self.suchFeldLeer2()
        elif event.key() == Qt.Key.Key_S:       # ctrl+s, den Text in dem 1. Suchfeld zu splitten
            if modifiers == Qt.KeyboardModifier.ControlModifier:
                self.suchFeldSplit()

        return

    @pyqtSlot()
    def suchFeldLeer(self):
        self.le_such1.setText("")
        self.le_such2.setText("")
        self.statusMeldung("")
        self.le_such1.setFocus()

    def suchFeldLeer2(self):
        txt = QApplication.clipboard().text().strip()
        if txt > "":
            i = -1
            if ":" in txt:
                sb = ":"
            elif "\n" in txt:
                sb = "\n"
            else:
                sb = None
            if sb is None:
                begr1 = txt
                begr2 = ""    
            else:
                i = txt.find(sb)
                begr1 = txt[:i]
                begr2 = txt[i+1:].strip()
            self.le_such1.setText(begr1)
            self.le_such2.setText(begr2)
        else:
            self.le_such1.setText("")
            self.le_such2.setText("")
        self.statusMeldung("")
        self.le_such1.setFocus()

    
    def suchFeldSplit(self):
        txt = self.le_such1.text()
        # Cursorposition ermittlen
        csrpos = self.le_such1.cursorPosition()
        self.le_such1.setText(txt[0:csrpos])
        self.le_such2.setText(txt[csrpos:])
    
    def about(self):        
        txt = "VidSuch" + "\n" + "-"*50 + f"\nSucht in {Konstanten.VPATH} nach Dateien" + "\n\n"
        txt += f"Version: {Konstanten.VERSION}.{Konstanten.SUBVERSION} vom {Konstanten.VERSIONDATE}\n" 
        txt += f"DB: {Konstanten.DBNAME}\n\n" 
        txt += "Autor: Michael Rüsweg-Gilbert rg@rgilbert.de (github.com/ruegi)"
        QMessageBox.about(self, "Über VidSuch", txt)
                                    

    @pyqtSlot()
    def suchen(self):   # slot-Funktion für den suchen button
        global stopFlag
        if self.btn_suchen.text == "&Stop":
            if self.stop_thread_msg():  # Abbrechen!
                stopFlag = True
                self.buttonflip("&Start")
                self.statusMeldung("Suche abgebrochen!")
        else:
            # starten
            suchbegriff1 = self.le_such1.text().strip()
            if suchbegriff1 == "":
                # beepSound()
                return
            suchbegriff2 = self.le_such2.text().strip()
            suchbegriff2 = None if suchbegriff2 == "" else suchbegriff2
            self.buttonflip("&Stop")
            self.statusMeldung("Suche läuft ...")
            self.warten(True)
            self.lst_erg.clearContents()
            self.lst_erg.setRowCount(0)
            self.lst_erg.setEnabled(False)
            self.suchAnfrage.emit(suchbegriff1, suchbegriff2, Konstanten.VPATH)
        return

    def stop_thread_msg(self):
        reply = QMessageBox.warning(self, "Achtung!",
                                    "Laufende Suche abbrechen?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes.value:
            return True     # Abbrechen!
        else:
            return False    # NICHT Abbrechen!


    @pyqtSlot(list)
    def ergebnis_ausgeben(self, liste):
        self.refreshTable(liste)
        self.warten(False)
        self.statusMeldung("Suche beendet! Es wurden {} Filme gefunden.".format(len(liste)))
        self.buttonflip("&Suchen")

    def refreshTable(self, liste):
        # das Table-widget füllen
        self.lst_erg.clearContents()
        self.lst_erg.setRowCount(0)
        nr = 0
        for vid in liste:
            # weitere Dateieigenschaften lesen
            try:
                oss = os.stat(vid)
                vlen = format_size(oss.st_size)                
                vdat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(oss.st_ctime))
            except:
                vlen = "???"
                vdat = "DB is async!"            
            finally:
                pass

            ''' liste aufbauen ''' 
            self.lst_erg.insertRow(nr)
            self.lst_erg.setItem(nr, 0, QTableWidgetItem(str(vid)))
            self.lst_erg.setItem(nr, 1, QTableWidgetItem(str(vlen)))
            self.lst_erg.setItem(nr, 2, QTableWidgetItem(str(vdat)))
            nr += 1
        self.lst_erg.selectRow(0)
        self.lst_erg.setEnabled(True)

    def warten(self, anaus):
        if anaus:
            self.proBar.setRange(0,0)
        else:
            self.proBar.setRange(0,100)

    # Funktionen
    @pyqtSlot(str)
    def statusMeldung(self, meldung):
        self.statusbar.showMessage(meldung)

    @pyqtSlot(int, int)
    def videoStart(self, row, col):
        if col > 0 or row > self.lst_erg.rowCount():
            return
        vid = self.lst_erg.item(row, col).text()
        try:
            os.startfile(vid)
        except:
            self.statusMeldung("Fehler: Kann das Video [{}] nicht starten!".format(vid))
            # beepSound(self.app)
        return

    # -------------------------------------------------
    # Neu 2020-02-04
    # -------------------------------------------------
    @pyqtSlot()
    def videoInfo(self):
        fname = self._getCurrentVideo()		# kompletter DateiName
        if fname is None:
            return
        self.statusMeldung(f"Lade VideoInfo für {fname} . . .")
        QApplication.processEvents()
        proc = Popen([Konstanten.FilmInfo, fname] )
        proc.wait()
        self.statusMeldung("")

    # def videoInfo_alt(self):
    #     fname = self._getCurrentVideo()		# kompletter DateiName
    #     if fname is None:
    #         return
    #     self.statusMeldung(f"Lade VideoInfo für {fname} . . .")
    #     QApplication.processEvents()        
    #     FilmDetails.DlgMain(fname)
    #     self.statusMeldung("")

    @pyqtSlot()
    def delVideo(self):
        fname = self._getCurrentVideo()		# kompletter DateiName
        # fname = item.text()
        if fname is None:
            return
        vidName = os.path.basename(fname)
        reply = QMessageBox.question(self, "Wirklich?",
                                     "Film [{0}] aus dem Archiv löschen?\n\nKeine Panik!\n".format(fname) +
                                     "Der Film wird nur in dem Mülleimer [{}] verschoben!".format(
                                         self.vpath + os.sep + self.delBasket),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes.value:
            delVideo = fname
            delTarget = os.path.join(self.vpath, self.delBasket, vidName)
            try:                
                os.rename(delVideo, delTarget)
                if not vidarchdb.film_umbenennen(delVideo, delTarget):                 
                    self.statusMeldung("Fehler! Konnte den DB-Namen nicht ändern!")
            except OSError as err:                
                self.statusMeldung("Fehler! ({})".format(err.strerror))                
            else:
                self.statusMeldung(
                    "Der Film [{0}] wurde aus dem Archiv nach [{1}] verschoben!".format(fname, delTarget))
            finally:
                # SuchErgebnis aktualisieren
                self.suchen()
        else:
            self.statusMeldung("Löschen abgebrochen!")
        return

    @pyqtSlot()
    def renVideo(self):
        # startet einen Dialog zur Erfassung des neuen VideoNamens
        #
        # item = self.lst_erg.currentItem().text()
        # fname = item.text()
        # fname = self._getItemText(self.lst_erg.currentItem())
        fname = self._getCurrentVideo()		# kompletter DateiName
        if fname is None:
            return
        alterName = fname
        vidName = os.path.basename(fname)
        pfad = os.path.dirname(fname)
        neuerName = self._runDialog(vidName)
        # neuerName, ok = QInputDialog.getText(self, 'Film im Prep-Ordner umbenennen', 'Neuer Name:',
        #                                      QLineEdit.EcheMode.Normal, vidName)
        if neuerName is None:
            pass
        elif not (neuerName == ''):
            neuerFullName = pfad + os.sep + neuerName
            alterFullName = pfad + os.sep + vidName
            try:
                if vidarchdb.film_umbenennen(alterFullName, neuerFullName):                    
                    os.rename(alterFullName, neuerFullName)
                else:
                    self.statusMeldung("Fehler! Konnte den DB-Namen nicht ändern!")
            except OSError as err:
                self.statusMeldung("Fehler! ({})".format(err.strerror))
            finally:
                # Anzeige aktualisieren
                self.suchen()
                self.statusbar.showMessage("Video umbenannt in: {}".format(neuerName))            
        else:
            pass
        return


    def _runDialog(self, videoName):
        neuerName, ok = QInputDialog.getText(self, 'Film im Prep-Ordner umbenennen', 'Neuer Name:',
                                             QLineEdit.EchoMode.Normal, videoName)
        if not ok:
            return None
        else:
            return neuerName


    def _getCurrentVideo(self):
        row = self.lst_erg.currentRow()
        if row > self.lst_erg.rowCount():
            return None
        vid = self.lst_erg.item(row, 0).text()
        return vid


    def syncDB(self):
        self.statusMeldung(f"Synkronisation von Archiv und {Konstanten.DBNAME} läuft! Pls stand by...")
        # proc = Popen(Konstanten.SYNCDB, creationflags=CREATE_NEW_CONSOLE)
        # proc = Popen(Konstanten.SYNCDB, shell=True, creationflags=CREATE_NEW_CONSOLE)
        proc = externalRun(Konstanten.SYNCDB, shell=True)
        # proc.wait()
        self.statusMeldung(f"Synkronisation von Archiv und {Konstanten.DBNAME} beendet!")


#
#   Allg Funktionen
#
def format_size(flen: int):
    """Human friendly file size"""
    unit_list = list(zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 3, 3, 3, 3, 3]))
    if flen > 1:
        exponent = min(int(logarit(flen, 1024)), len(unit_list) - 1)
        quotient = float(flen) / 1024 ** exponent
        unit, num_decimals = unit_list[exponent]
        s = '{:{width}.{prec}f} {}'.format(quotient, unit, width=8, prec=num_decimals)
        s = s.replace(".", ",")
        return s
    elif flen == 1:
        return '  1 byte'
    else: # flen == 0
        return ' 0 bytes'

def beepSound(app):
    app.beep()

StyleSheet = '''
    QMainWindow {
        background-color: Grey;
    }

    QMenuBar, QMenu, QAction {
        background-color: Grey;
        color: white;
    }
   
    QMenuBar::item {
    padding: 2px 8px;
    background-color: Grey;
    }

    QMenu::item:selected {
        background-color: lightGrey;
        color: Black;
    }

    QPushButton {
        background-color: lightBlue;
        border-style: outset;
        border-width: 1px;
        border-radius: 5px;
        border-color: black;        
        padding: 3px;
    }
    #btnEnde {
        background-color: Grey;
        border-color: Grey;
        border-width: 0px;
    }

    #btn_suchen {
        font 14px;
        color: black;
    }

    QLineEdit {
        background-color: lightGrey;
        color: black;
        font: bold;
    }

    QTableWidget {
        background-color: lightGrey;
        color: black;
    }

    #proBar {
        border-radius: 5px;
        background-color: grey;
    }

    #proBar::chunk {
        background-color: darkGrey;
    }

'''

    # QWidget{
    #         Background: #AA00AA;
    #         color:white;
    #         font:12px bold;
    #         font-weight:bold;
    #         border-radius: 1px;
    #         height: 11px;
    # }

# ürsprüngliches StylSheet des Such-Buttons
# #btn_suchen{
# color: white;
# background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c);
# border-width: 1px;
# border-color: #339;
# border-style: solid;
# border-radius: 7;
# padding: 3 px;
# font-size: 14 px;
# padding-left: 5 px;
# padding-right: 5 px;
# }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    form = VidSuchApp(app)
    form.show()
    app.exec()
