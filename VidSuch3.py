# -*- coding: utf-8 -*-
'''
Created on 2018-06-01
@author: rg
VidSuch.py mit pyqt5
ermöglicht das Suchen von Videos mit 1 bis 2 Suchbegriffen
'''

# import PyQt5.QtWidgets # Import the PyQt5 module we'll need
from PyQt5.QtWidgets import (QMainWindow, 
                             QLabel,
                             QListWidgetItem,
                             QLineEdit, 
                             QPushButton,
                             QWidget,
                             QHBoxLayout, 
                             QVBoxLayout, 
                             QApplication, 
                             QMessageBox,
                             QInputDialog
)

from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QIcon

import sys
import os
import traceback

# das fenster wurde mit dem qtdesigner entworfen und per pyuic5 konvertiert

import VidSuchUI3

stopFlag = False

vpath = "Y:\\video\\"

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
        such2 = None if such2 == "" else such2
        repl_mode = False   # repl_mode wird nur benötigt, wenn such ein Blank oder "_" enthält
        if " " in such or "_" in such:
            such_ = such.replace(" ", "_")  # such1 = such, aber komplett mit _ statt Blank
            suchb = such.replace("_", " ")  # suchb wie such, aber komplett mit Blank (kein _)
            repl_mode = True
        if such2 is None:
            doSuch2 = False
        else:
            such2 = such2.lower()
            doSuch2 = True
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
                    # self.worker.progress.emit(x)
                    self.progress.emit(x)
        if not stopFlag:
            self.result.emit(lst)
        return
        

# --------------------------------------------------------------------------------
# VidSuchApp class
# --------------------------------------------------------------------------------
class VidSuchApp(QMainWindow, VidSuchUI3.Ui_MainWindow):
    suchAnfrage = pyqtSignal(str, str, str)

    def __init__(self, app):
        super(self.__class__, self).__init__()
        
        self.setupUi(self)  # This is defined in VidSuchUI.py file automatically
                            # It sets up layout and widgets that are defined
        # Instanz-Variablen
        self.vpath   = "Y:\\video\\"
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

        # connects
        self.btnDel.clicked.connect(self.delVideo)
        self.btnRen.clicked.connect(self.renVideo)
        self.btn_suchen.clicked.connect(self.suchen)
        
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
        # self.lst_erg.itemDoubleClicked.connect
        self.lst_erg.itemActivated.connect(self.videoStart)
        self.thread.start()

        # Key-Press-Events auswerten
    def keyPressEvent(self, event):
        w = self.focusWidget()
        if event.key() == Qt.Key_F6:
            if w == self.lst_erg :
                self.renVideo()
        elif event.key() == Qt.Key_Delete:
            if w == self.lst_erg :
                self.delVideo()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.suchen()
        return

    def buttonflip(self, txt):
        self.btn_suchen.setText(txt)

    def suchBtnAktivieren(self):       
        self.btn_suchen.setEnabled(self.le_such1.text().strip() > "")

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
                beepSound()
                return
            suchbegriff2 = self.le_such2.text().strip()
            suchbegriff2 = None if suchbegriff2 == "" else suchbegriff2
            self.buttonflip("&Stop")
            self.statusMeldung("Suche läuft ...")
            self.warten(True)
            self.lst_erg.clear()
            self.suchAnfrage.emit(suchbegriff1, suchbegriff2, vpath)

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
        self.lst_erg.clear()
        self.lst_erg.insertItems(0, liste)
        self.warten(False)
        self.statusMeldung("Suche beendet!")
        self.buttonflip("&Suchen")

    def warten(self, anaus):
        if anaus:
            self.proBar.setRange(0,0)
        else:
            self.proBar.setRange(0,100)

    # Funktionen
    @pyqtSlot(str)
    def statusMeldung(self, meldung):
        self.statusbar.showMessage(meldung)

    @pyqtSlot(QListWidgetItem)
    def videoStart(self, item):
        try:
            os.startfile(item.text())
        except:
            self.statusMeldung("Fehler: Kann das Video [{}] nicht starten!".format(item.text()))
            beepSound(self.app)
        return

    @pyqtSlot()
    def delVideo(self):
        fname = self.lst_erg.currentItem()		# kompletter DateiName
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
        # item = self.lst_erg.currentItem().text()
        # fname = item.text()
        fname = self._getItemText(self.lst_erg.currentItem())
        if fname is None:            
            return
        alterName = fname
        vidName = os.path.basename(fname)
        pfad = os.path.dirname(fname)   
        neuerName, ok = QInputDialog.getText(self, 'Film im Prep-Ordner umbenennen', 'Neuer Name:',
                                        QLineEdit.Normal, vidName)
        if ok:
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


    def _getItemText(self, obj: object):
        # gibt den im Objekt enthaltenen Text zurück oder None
        if obj.type() == "Text":
            return obj.text()
        else:
            print("Type ist: {}".obj.type())
            return None

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
