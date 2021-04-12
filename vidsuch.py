
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
            neuer Hotkey Ctrl+M, um eine Zwischenablage einzufügen
            neuer Hotkey Ctrl+s, um einen Text zu splitten
            Menü erzeugt für Doku der Hotkeys & About Dialog

'''

import sys
import os

# das soll die Importe aus dem Ordner FilmDetails mit einschließen...
sys.path.append(r".\FilmDetails")

# import PyQt5.QtWidgets # Import the PyQt5 module we'll need
from PyQt5.QtWidgets import (QMainWindow,
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
                             QInputDialog )

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, Qt
from PyQt5.Qt import  QClipboard
from PyQt5.QtGui import QIcon

from math import log as logarit
from datetime import datetime

import time
# import filmAlyser
import FilmDetails.FilmDetails as FD

# Handle high resolution displays (thx 2 https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution):
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# das fenster wurde mit dem qtdesigner entworfen und per pyuic5 konvertiert
import VidSuchUI
stopFlag = False

class const:
    vpath = "Y:\\video\\"
    version = "6"
    subversion = "2"
    versiondate = "2021-04-11"

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

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def startp(self):
        # print("Thread started")
        pass

    @pyqtSlot(str, str, str)
    def findewas(self, such, such2, vpath):
        '''
        Findet Videos nach Stichworten
        sucht unabhängig von Groß/klein-schreibung
        enthält der erste suchbegriff "such" eine Blank, so wird auch nach "_" an dieser Stelle gesucht
        :param such:        Suchbegriff 1
        :param such2:       Suchbegriff 2
        :param vpath        zu durchsuchender video-Pfad
        :return:            Liste mit den vollen Namen der gefundenen Videos als Signal "result"
        '''
        global stopFlag

        such = such.lower()
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
        for root, dirs, files in os.walk(vpath):
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


# --------------------------------------------------------------------------------
# VidSuchApp class
# --------------------------------------------------------------------------------
class VidSuchApp(QMainWindow, VidSuchUI.Ui_MainWindow):
    suchAnfrage = pyqtSignal(str, str, str)

    def __init__(self, app):
        super(self.__class__, self).__init__()

        self.setupUi(self)  # This is defined in VidSuchUI.py file automatically
                            # It sets up layout and widgets that are defined
        # Instanz-Variablen
        self.vpath   = const.vpath
        self.app = app
        self.worker = None
        self.delBasket = "__del"

        # Icon versorgen
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'VidSuch.ico'))

        self.btn_suchen.setEnabled(False)
        # btn_suchen.setEnabled(True)
        self.le_such1.textChanged.connect(self.suchBtnAktivieren)

        #self.lst_erg.setTextBackgroundColor(QColor("lightyellow"))
        self.lst_erg.setStyleSheet("background-color: lightyellow;")
        self.lst_erg.setHorizontalHeaderLabels(('Video', 'Länge', 'Datum'))
        self.lst_erg.setAlternatingRowColors(True)
        header = self.lst_erg.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.lst_erg.setSelectionMode(QAbstractItemView.NoSelection)
        self.lst_erg.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lst_erg.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lst_erg.setRowCount(0)
        self.lst_erg.setEnabled(False)

        # connects
        self.btn_suchen.clicked.connect(self.suchen)
        self.btnDel.clicked.connect(self.delVideo)
        self.btnRen.clicked.connect(self.renVideo)
        self.btnInfo.clicked.connect(self.videoInfo)
        self.btnPlay.clicked.connect(lambda: self.videoStart(self.lst_erg.currentRow(),0))
        self.btnLeer.clicked.connect(self.suchFeldLeer)
        self.btnLeer2.clicked.connect(self.suchFeldLeer2)
        self.btnEnde.clicked.connect(self.close)

        self.actionEinfuegen.triggered.connect(self.suchFeldLeer2)
        self.actionEnde.triggered.connect(self.close)
        self.actionSplit.triggered.connect(self.suchFeldSplit)
        self.actionAbout.triggered.connect(self.about)

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

        if event.key() == Qt.Key_F6:
            if w == self.lst_erg :
                self.renVideo()
        elif event.key() == Qt.Key_Delete:
            if w == self.lst_erg :
                self.delVideo()
        elif event.key() == Qt.Key_Return:
            w = self.focusWidget()
            if w == self.le_such1 or w == self.le_such2:
                self.suchen()
            else:
                self.videoStart(self.lst_erg.currentRow, 1)
        elif event.key() == Qt.Key_F2:
            self.videoInfo()
        elif event.key() == Qt.Key_F4:  # Split Feld 1
            self.suchFeldSplit()
        elif event.key() == Qt.Key_F5:  # Paste, wie ctrl+m
            self.suchFeldLeer2()
        elif event.key() == Qt.Key_X:
            # modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:
                self.suchFeldLeer()        
        elif event.key() == Qt.Key_M:       # ctrl+m, um die Zwischenablage einzufügen
            if modifiers == Qt.ControlModifier:
                self.suchFeldLeer2()        
        elif event.key() == Qt.Key_S:       # ctrl+s, den Text in dem 1. Suchfeld zu splitten
            if modifiers == Qt.ControlModifier:
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
            self.le_such1.setText(txt)                    
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
        txt = "VidSuch" + "\n" + "-"*50 + f"\nSucht in {const.vpath} nach Dateien" + "\n\n"
        txt += f"Version: {const.version}.{const.subversion} vom {const.versiondate}\n" 
        txt += "Autor: Michael Rüsweg-Gilbert"        
        QMessageBox.about(self, "Über VidSuch", txt)
                                    

    @pyqtSlot()
    def suchen(self):   # slot-Funktion für den suchen button
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
            self.suchAnfrage.emit(suchbegriff1, suchbegriff2, const.vpath)
        return

    def stop_thread_msg(self):
        reply = QMessageBox.warning(self, "Achtung!",
                                    "Laufende Suche abbrechen?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
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
            # weitere dateieigenschaften lesen
            vlen = format_size(os.stat(vid).st_size)
            vdat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(vid).st_ctime))
            # liste aufbauen
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
            self.statusMeldung("Fehler: Kann das Video [{}] nicht starten!".format(item.text()))
            beepSound(self.app)
        return

    # -------------------------------------------------
    # Neu 2020-02-04
    # -------------------------------------------------
    @pyqtSlot()
    def videoInfo(self):
        fname = self._getCurrentVideo()		# kompletter DateiName
        # fname = item.text()
        if fname is None:
            return
        # dialog = QDialog()
        # dialog.ui = FD.mainApp(fname)
        # dialog.exec_()
        # dialog.show()           
        FD.DlgMain(fname)

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
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delVideo = fname
            delTarget = self.vpath + os.sep + self.delBasket + os.sep + vidName
            try:
                os.rename(delVideo, delTarget)
            except OSError as err:
                self.statusMeldung("Fehler! ({})".format(err.strerror))
            finally:
                # SuchErgebnis aktualisieren
                self.suchen()
                self.statusMeldung(
                    "Der Film [{0}] wurde aus dem Archiv nach [{1}] verschoben!".format(fname, delTarget))
        else:
            self.statusMeldung("Löschen abgebrochen!".format(fname))
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
        neuerName, ok = QInputDialog.getText(self, 'Film im Prep-Ordner umbenennen', 'Neuer Name:',
                                        QLineEdit.Normal, vidName)
        if ok and not (neuerName == ''):
            neuerFullName = pfad + os.sep + neuerName
            alterFullName = pfad + os.sep + vidName
            try:
                os.rename(alterFullName, neuerFullName)
            except OSError as err:
                self.statusMeldung("Fehler! ({})".format(err.strerror))
            finally:
                # Anzeige aktualisieren
                self.suchen()
                self.statusbar.showMessage("Video umbenannt in: {}".format(neuerName))
        return

    def _getCurrentVideo(self):
        row = self.lst_erg.currentRow()
        if row > self.lst_erg.rowCount():
            return None
        vid = self.lst_erg.item(row, 0).text()
        return vid
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
            s = '{:{width}.{prec}f} {}'.format(quotient, unit, width=8, prec=num_decimals )
            s = s.replace(".", ",")
            return s
        elif flen == 1:
            return '  1 byte'
        else: # flen == 0
            return ' 0 bytes'

def beepSound(app):
    app.beep()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = VidSuchApp(app)
    form.show()
    app.exec_()
