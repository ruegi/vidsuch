# -*- coding: utf-8 -*-
"""
Created on 2020-02-14

@author: rg

FilmDetails.py mit pyqt5

Gibt die technischen Daten eines Films in einem Fenster an
technische Basis: c:\ffmpeg\bin\ffprobe.exe

"""
from PyQt5.QtWidgets import (QMainWindow, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton,
                             QFileDialog,
                             QApplication,
                             QMessageBox)
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt

import sys
import os

import FilmDetailsUI # Hauptfenster; mit pyuic aus der UI-Datei konvertiert

from videoFile import videoFile
from formatSize import formatSize
import datetime

# from prettytable import PrettyTable, MARKDOWN
from prettytable import PrettyTable
# einige statische Konstanten
class Konstanten():    
    icon = 'FilmDetails.ico'

class FilmInfo():
    def __init__(self, filmName, filmTyp, Dauer, Groesse):
        self.filmName = filmName
        self.filmTyp = filmTyp
        self.Dauer = Dauer
        self.Groesse = Groesse
        self.videoStreams = []
        self.audioStreams = []
        self.uTitel = []

class vStream():
    def __init__(self, Resolution, frameCnt, BitRate, FrameRate) -> None:
        self.Aufloesung = Resolution
        self.frameCnt = frameCnt
        self.BitRate = BitRate
        self.FrameRate = FrameRate

class aStream():
    def __init__(self, Nr, Sprache, Format, Kanaele, SRate, BitRate) -> None:
        self.Nr = Nr
        self.Sprache = Sprache
        self.Format = Format
        self.Kanaele = Kanaele
        self.SRate = SRate
        self.BitRate = BitRate

class utStream():
    def __init__(self, Nr, Sprache, Format, Lib) -> None:
        self.Nr = Nr
        self.Sprache = Sprache
        self.Format = Format
        self.Lib = Lib
        

fname = None        # Name des zu begutachtenden Films

class mainApp(QMainWindow, FilmDetailsUI.Ui_FilmDetailsDialog):
    def __init__(self, fname):               
        super(self.__class__, self).__init__()
        
        self.setupUi(self)  # This is defined in ...UI.py file automatically
                            # It sets up layout and widgets that are defined
        # Instanz-Variablen
        self.fname = fname
        # Icon versorgen
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + Konstanten.icon))

        # Feintuning der Widgets
        if self.fname is None:
            self.fname = self.openFileNameDialog()
        # gibt es diesen Film tatsächlich?
        if self.fname is None:            
            self.teFilmDetails.setTextColor(QColor('red'))
            self.teFilmDetails.setPlainText('Fatal!\nDiesem Programm muss der Name mit Pfad zu einer Filmdatei übergeben werden!')
        else:
            self.leFilmName.setText(self.fname) 
            if os.path.isfile(self.fname):
                self.teFilmDetails.setFont(QFont('Courier', 12))
                self.teFilmDetails.setTextColor(QColor('lightyellow'))
                vid = getFilmDetails(self.fname)
                ausg = txtAusgabe(vid) 
                self.teFilmDetails.setPlainText(ausg)
                self.teFilmDetails.setDisabled(False)
                self.teFilmDetails.setReadOnly(True)
            else:
                self.teFilmDetails.setTextColor(QColor('red'))
                self.teFilmDetails.setPlainText(f'Fatal!\nKonnte den Film \n({self.fname})\n nicht finden!')

        # connects
        self.pbDone.clicked.connect(self.progende)
        # self.leName.installEventFilter(self)
        self.pbDone.setFocus()

    def openFileNameDialog(self)->str:
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "einen Film aussuchen", "E:\\Filme\\", "All Files (*);;Filme (*.mkv *.mpg *.mp4 *.ts *.avi)", options=options)
        if fileName:
            return fileName
        else:
            return None

    def mess(self, txt):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(txt)
        msgBox.setWindowTitle("Film Details")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    
    # Slots
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key == Qt.Key_Enter or event.key == Qt.Key_Return:            
            self.progende()
        
    # def eventFilter(self, source, event):
    #     if (event.type() == QEvent.FocusOut an
    #         source is self.leName):
    #         # print('eventFilter: focus out')
    #         if self.grpLaden(self.leName.text()) > 0:
    #             self.leName.setFocus()
    #             return True
    #     return super(QMainWindow, self).eventFilter(source, event)

    # Funktionen
    def progende(self):     # Ende Proc mit Nachfrage
        self.close()
   
    def Hinweis(self, nachricht ):        
        self.statusbar.showMessage(nachricht)        


def getFilmDetails(filmname):
    basename = os.path.basename(filmname)
    vid = videoFile(filmname)
    qlen = formatSize(os.stat(filmname).st_size)    
  
    dura = str(datetime.timedelta(seconds=vid.duration/1000))
    # Init der Datenstruktur
    vInfo = FilmInfo(filmname, vid.typ, dura, qlen)
    # Vorbesetzen der Überschriften
    vInfo.videoStreams.append(vStream("Auflösung", "Anz.Frames", "BitRate", "FrameRate"))
    vInfo.audioStreams.append(aStream("Nr", "Sprache", "Format", "Anz.Kanäle", "Sampl.Rate", "BitRate"))
    vInfo.uTitel.append(utStream("Nr", "Sprache", "Format", "Lib"))

    # Video-Streams    
    vInfo.videoStreams.append(vStream(str(vid.weite) + "x" + str(vid.hoehe), form(vid.frameCount), form(vid.bitRate), form(vid.fps)))

    for track in vid.a_tracks:   
        # 
        vInfo.audioStreams.append(aStream(
            track.stream_identifier,
            form(track.language),
            track.format,
            track.channel_s,
            form(track.sampling_rate),
            form(track.bit_depth) )
            )   

    for track in vid.t_tracks:   # Untertitel
        vInfo.uTitel.append(utStream(
            track.track_id,
            form(track.language),
            track.format,
            track.writing_library)
        )       
    return vInfo
    
    return vInfo



def txtAusgabe(videoInfo: FilmInfo) -> str:
    pt = PrettyTable()
    ausg = ""
    
    # FilmName & Spieldauer & Größe
    pt.clear()
    
    pt.field_names = ["Typ", "Spielzeit", "Dateilänge" ]
    pt.align["Typ"] = "c"
    pt.align["Spielzeit"] = "r"
    pt.align["Dateilänge"] = "r"
    pt.add_row( [videoInfo.filmTyp,
                videoInfo.Dauer,
                videoInfo.Groesse] )
    ausg += pt.get_string(title=videoInfo.filmName) + "\n\n"

    # Video-Streams
    pt.clear()
    slen = len(videoInfo.videoStreams)
    if slen < 2:     # nur Überschriften
        ausg += "Keine Video-Streams enthalten!"
    else:
        # Überschrift
        vstream = videoInfo.videoStreams[0]        
        pt.field_names = [vstream.Aufloesung, vstream.frameCnt, vstream.BitRate, vstream.FrameRate]
        for i in range(1, slen):
            vstream = videoInfo.videoStreams[i]
            pt.add_row([vstream.Aufloesung, vstream.frameCnt, vstream.BitRate, vstream.FrameRate])
        ausg += pt.get_string(title="Video-Streams") + "\n\n"

    # Audio-Streams
    pt.clear()
    slen = len(videoInfo.audioStreams)
    if slen < 2:     # nur Überschriften
        ausg += "Keine Audio-Streams enthalten!"
    else:
        # Überschrift
        astream = videoInfo.audioStreams[0]
        pt.field_names = [astream.Nr, astream.Sprache, astream.Format, astream.Kanaele, astream.SRate, astream.BitRate]        
        for i in range(1, slen):
            astream = videoInfo.audioStreams[i]
            pt.add_row([astream.Nr, astream.Sprache, astream.Format, astream.Kanaele, astream.SRate, astream.BitRate])
        ausg += pt.get_string(title="Audio-Streams") + "\n\n"
    
    # UT-Streams
    pt.clear()
    slen = len(videoInfo.uTitel)
    if slen < 2:     # nur Überschriften
        ausg += "Keine Untertitel enthalten!"
    else:
        # Überschrift
        ustream = videoInfo.uTitel[0]
        pt.field_names = [ustream.Nr, ustream.Sprache, ustream.Format, ustream.Lib]
        for i in range(1, slen):
            ustream = videoInfo.uTitel[i]
            pt.add_row([ustream.Nr, ustream.Sprache, ustream.Format, ustream.Lib])
        ausg += pt.get_string(title="Untertitel") + "\n"
    return ausg

            



def form(txt: object):
    if txt is None:
        s = "-"
    else:
        s = str(txt)
    return s



def main(fname):        
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = mainApp(fname)              # We set the form to be our App (design)
    form.show()                   # Show the form
    app.exec_()                   # and execute the app


if __name__ == '__main__':        # if we're running file directly and not importing it
    if len(sys.argv) == 2:        
        fname = sys.argv[1]       
    else:
        fname = None     
    main(fname)                        # run the main function