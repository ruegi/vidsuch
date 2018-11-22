# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VidSuchUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1274, 714)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("VidSuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("#QMainWindow {\n"
"background-color: rgb(170, 255, 127)\n"
"}\n"
"\n"
"#QFormLayout {\n"
"border: 3px solid gray;\n"
"border-radius: 40px;\n"
"background: white;\n"
"}\n"
"\n"
"#lbl_ergebnis {\n"
"color: rgb(255, 255, 127);\n"
"border: 3px solid gray;\n"
"border-radius: 20px;\n"
"background: rgb(110, 104, 113)\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 110, 1251, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_ergebnis = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_ergebnis.setFont(font)
        self.lbl_ergebnis.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_ergebnis.setStyleSheet("")
        self.lbl_ergebnis.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_ergebnis.setObjectName("lbl_ergebnis")
        self.verticalLayout.addWidget(self.lbl_ergebnis)
        self.lst_erg = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_erg.sizePolicy().hasHeightForWidth())
        self.lst_erg.setSizePolicy(sizePolicy)
        self.lst_erg.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lst_erg.setFont(font)
        self.lst_erg.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lst_erg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lst_erg.setAutoFillBackground(True)
        self.lst_erg.setStyleSheet("background-color:   qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));\n"
"")
        self.lst_erg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lst_erg.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.lst_erg.setAutoScrollMargin(16)
        self.lst_erg.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.lst_erg.setAlternatingRowColors(True)
        self.lst_erg.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lst_erg.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.lst_erg.setTextElideMode(QtCore.Qt.ElideRight)
        self.lst_erg.setRowCount(5)
        self.lst_erg.setColumnCount(3)
        self.lst_erg.setObjectName("lst_erg")
        item = QtWidgets.QTableWidgetItem()
        self.lst_erg.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.lst_erg.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.lst_erg.setHorizontalHeaderItem(2, item)
        self.lst_erg.horizontalHeader().setCascadingSectionResizes(True)
        self.lst_erg.horizontalHeader().setDefaultSectionSize(200)
        self.lst_erg.horizontalHeader().setMinimumSectionSize(50)
        self.lst_erg.horizontalHeader().setStretchLastSection(False)
        self.lst_erg.verticalHeader().setVisible(True)
        self.lst_erg.verticalHeader().setCascadingSectionResizes(False)
        self.lst_erg.verticalHeader().setDefaultSectionSize(20)
        self.lst_erg.verticalHeader().setMinimumSectionSize(20)
        self.lst_erg.verticalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.lst_erg)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 5, 1251, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lbl_such1 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_such1.sizePolicy().hasHeightForWidth())
        self.lbl_such1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_such1.setFont(font)
        self.lbl_such1.setObjectName("lbl_such1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_such1)
        self.le_such1 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_such1.setFont(font)
        self.le_such1.setObjectName("le_such1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_such1)
        self.lbl_such2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_such2.setFont(font)
        self.lbl_such2.setObjectName("lbl_such2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_such2)
        self.le_such2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_such2.setFont(font)
        self.le_such2.setObjectName("le_such2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_such2)
        self.proBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.proBar.setMinimumSize(QtCore.QSize(0, 25))
        self.proBar.setAutoFillBackground(False)
        self.proBar.setProperty("value", 24)
        self.proBar.setTextVisible(False)
        self.proBar.setObjectName("proBar")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.proBar)
        self.btn_suchen = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_suchen.setFont(font)
        self.btn_suchen.setStyleSheet("#btn_suchen{\n"
"color: white;\n"
"background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c);\n"
"border-width: 1px;\n"
"border-color: #339;\n"
"border-style: solid;\n"
"border-radius: 7;\n"
"padding: 3 px;\n"
"font-size: 14 px;\n"
"padding-left: 5 px;\n"
"padding-right: 5 px;\n"
"}")
        self.btn_suchen.setAutoDefault(True)
        self.btn_suchen.setDefault(True)
        self.btn_suchen.setObjectName("btn_suchen")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.btn_suchen)
        self.btnRen = QtWidgets.QPushButton(self.centralwidget)
        self.btnRen.setGeometry(QtCore.QRect(110, 640, 150, 23))
        self.btnRen.setObjectName("btnRen")
        self.btnPlay = QtWidgets.QPushButton(self.centralwidget)
        self.btnPlay.setGeometry(QtCore.QRect(530, 640, 150, 23))
        self.btnPlay.setObjectName("btnPlay")
        self.btnDel = QtWidgets.QPushButton(self.centralwidget)
        self.btnDel.setGeometry(QtCore.QRect(974, 640, 150, 23))
        self.btnDel.setObjectName("btnDel")
        self.btnEnde = QtWidgets.QPushButton(self.centralwidget)
        self.btnEnde.setGeometry(QtCore.QRect(1204, 630, 51, 51))
        self.btnEnde.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("EndBut_neutral.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("EndBut_focus.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("EndBut_pushed.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.btnEnde.setIcon(icon1)
        self.btnEnde.setIconSize(QtCore.QSize(48, 48))
        self.btnEnde.setObjectName("btnEnde")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VidSuch - Suche von Videos im Archiv"))
        self.lbl_ergebnis.setText(_translate("MainWindow", "Such-Ergebnis"))
        self.lst_erg.setSortingEnabled(True)
        item = self.lst_erg.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Video"))
        item = self.lst_erg.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Länge"))
        item = self.lst_erg.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Datum"))
        self.lbl_such1.setText(_translate("MainWindow", "Suchbegriff 1"))
        self.lbl_such2.setText(_translate("MainWindow", "Suchbegriff 2"))
        self.btn_suchen.setText(_translate("MainWindow", "Suchen"))
        self.btnRen.setText(_translate("MainWindow", "Umbenennen (F6)"))
        self.btnPlay.setText(_translate("MainWindow", "Film abspielen (Enter)"))
        self.btnDel.setText(_translate("MainWindow", "Film löschen (Entf)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

