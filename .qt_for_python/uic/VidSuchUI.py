# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\DEV\Py\vidsuch\VidSuchUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1274, 755)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\DEV\\Py\\vidsuch\\VidSuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.lst_erg.setStyleSheet("")
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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 1251, 152))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 5)
        self.formLayout.setSpacing(8)
        self.formLayout.setObjectName("formLayout")
        self.btnLeer = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLeer.sizePolicy().hasHeightForWidth())
        self.btnLeer.setSizePolicy(sizePolicy)
        self.btnLeer.setMinimumSize(QtCore.QSize(110, 0))
        self.btnLeer.setObjectName("btnLeer")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.btnLeer)
        self.le_such1 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_such1.sizePolicy().hasHeightForWidth())
        self.le_such1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_such1.setFont(font)
        self.le_such1.setObjectName("le_such1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_such1)
        self.btnLeer2 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLeer2.sizePolicy().hasHeightForWidth())
        self.btnLeer2.setSizePolicy(sizePolicy)
        self.btnLeer2.setMinimumSize(QtCore.QSize(110, 0))
        self.btnLeer2.setObjectName("btnLeer2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.btnLeer2)
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
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.proBar)
        self.btn_suchen = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_suchen.setFont(font)
        self.btn_suchen.setStyleSheet("")
        self.btn_suchen.setAutoDefault(True)
        self.btn_suchen.setDefault(True)
        self.btn_suchen.setObjectName("btn_suchen")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.btn_suchen)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.btnRen = QtWidgets.QPushButton(self.centralwidget)
        self.btnRen.setGeometry(QtCore.QRect(370, 670, 150, 23))
        self.btnRen.setObjectName("btnRen")
        self.btnPlay = QtWidgets.QPushButton(self.centralwidget)
        self.btnPlay.setGeometry(QtCore.QRect(640, 670, 150, 23))
        self.btnPlay.setObjectName("btnPlay")
        self.btnDel = QtWidgets.QPushButton(self.centralwidget)
        self.btnDel.setGeometry(QtCore.QRect(974, 670, 150, 23))
        self.btnDel.setObjectName("btnDel")
        self.btnEnde = QtWidgets.QPushButton(self.centralwidget)
        self.btnEnde.setGeometry(QtCore.QRect(1204, 660, 51, 51))
        self.btnEnde.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("d:\\DEV\\Py\\vidsuch\\EndBut_neutral.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("d:\\DEV\\Py\\vidsuch\\EndBut_focus.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("d:\\DEV\\Py\\vidsuch\\EndBut_pushed.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.btnEnde.setIcon(icon1)
        self.btnEnde.setIconSize(QtCore.QSize(48, 48))
        self.btnEnde.setObjectName("btnEnde")
        self.btnInfo = QtWidgets.QPushButton(self.centralwidget)
        self.btnInfo.setGeometry(QtCore.QRect(210, 670, 150, 23))
        self.btnInfo.setObjectName("btnInfo")
        self.lbl_db = QtWidgets.QLabel(self.centralwidget)
        self.lbl_db.setEnabled(True)
        self.lbl_db.setGeometry(QtCore.QRect(1066, 640, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_db.setFont(font)
        self.lbl_db.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lbl_db.setAutoFillBackground(False)
        self.lbl_db.setInputMethodHints(QtCore.Qt.ImhNoAutoUppercase)
        self.lbl_db.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_db.setObjectName("lbl_db")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuDatei = QtWidgets.QMenu(self.menuBar)
        self.menuDatei.setObjectName("menuDatei")
        self.menuBearbeiten = QtWidgets.QMenu(self.menuBar)
        self.menuBearbeiten.setObjectName("menuBearbeiten")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.actionEnde = QtWidgets.QAction(MainWindow)
        self.actionEnde.setObjectName("actionEnde")
        self.actionEinfuegen = QtWidgets.QAction(MainWindow)
        self.actionEinfuegen.setObjectName("actionEinfuegen")
        self.actionSplit = QtWidgets.QAction(MainWindow)
        self.actionSplit.setObjectName("actionSplit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSync = QtWidgets.QAction(MainWindow)
        self.actionSync.setObjectName("actionSync")
        self.menuDatei.addAction(self.actionSync)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionEnde)
        self.menuBearbeiten.addAction(self.actionEinfuegen)
        self.menuBearbeiten.addAction(self.actionSplit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuBearbeiten.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.le_such1, self.le_such2)
        MainWindow.setTabOrder(self.le_such2, self.btn_suchen)
        MainWindow.setTabOrder(self.btn_suchen, self.btnLeer)
        MainWindow.setTabOrder(self.btnLeer, self.btnInfo)
        MainWindow.setTabOrder(self.btnInfo, self.btnRen)
        MainWindow.setTabOrder(self.btnRen, self.btnPlay)
        MainWindow.setTabOrder(self.btnPlay, self.btnDel)
        MainWindow.setTabOrder(self.btnDel, self.btnEnde)

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
        self.btnLeer.setText(_translate("MainWindow", "Leer / Suche1"))
        self.btnLeer2.setText(_translate("MainWindow", "Paste / Suche 2"))
        self.btn_suchen.setText(_translate("MainWindow", "Suchen"))
        self.btnRen.setText(_translate("MainWindow", "Umbenennen (F6)"))
        self.btnPlay.setText(_translate("MainWindow", "Film abspielen (Enter)"))
        self.btnDel.setText(_translate("MainWindow", "Film löschen (Entf)"))
        self.btnInfo.setText(_translate("MainWindow", "DateiInfo (F2)"))
        self.lbl_db.setText(_translate("MainWindow", "DB: "))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.menuBearbeiten.setTitle(_translate("MainWindow", "Bearbeiten"))
        self.menuAbout.setTitle(_translate("MainWindow", "Info"))
        self.actionEnde.setText(_translate("MainWindow", "Ende  - (Alt-F4)"))
        self.actionEinfuegen.setText(_translate("MainWindow", "Einfügen - (F5 ; strg+m)"))
        self.actionSplit.setText(_translate("MainWindow", "Split Suchfeld1 @ Cursor Pos - (F4 ;strg+s)"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSync.setText(_translate("MainWindow", "Sync DB mit Archiv"))
