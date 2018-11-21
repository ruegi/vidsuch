# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VidSuchUI3.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(745, 603)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("VidSuch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 721, 105))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lbl_such1 = QtWidgets.QLabel(self.formLayoutWidget)
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
        self.le_such1 = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_such1.setFont(font)
        self.le_such1.setObjectName("le_such1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_such1)
        self.lbl_such2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_such2.setFont(font)
        self.lbl_such2.setObjectName("lbl_such2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_such2)
        self.le_such2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_such2.setFont(font)
        self.le_such2.setObjectName("le_such2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_such2)
        self.btn_suchen = QtWidgets.QPushButton(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_suchen.setFont(font)
        self.btn_suchen.setDefault(True)
        self.btn_suchen.setObjectName("btn_suchen")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.btn_suchen)
        self.proBar = QtWidgets.QProgressBar(self.formLayoutWidget)
        self.proBar.setAutoFillBackground(False)
        self.proBar.setProperty("value", 24)
        self.proBar.setTextVisible(False)
        self.proBar.setObjectName("proBar")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.proBar)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 120, 721, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_ergebnis = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_ergebnis.setFont(font)
        self.lbl_ergebnis.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_ergebnis.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_ergebnis.setObjectName("lbl_ergebnis")
        self.verticalLayout.addWidget(self.lbl_ergebnis)
        self.lst_erg = QtWidgets.QListWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lst_erg.setFont(font)
        self.lst_erg.setObjectName("lst_erg")
        self.verticalLayout.addWidget(self.lst_erg)
        self.btnDel = QtWidgets.QPushButton(self.centralwidget)
        self.btnDel.setGeometry(QtCore.QRect(110, 540, 131, 23))
        self.btnDel.setObjectName("btnDel")
        self.btnRen = QtWidgets.QPushButton(self.centralwidget)
        self.btnRen.setGeometry(QtCore.QRect(410, 540, 141, 23))
        self.btnRen.setObjectName("btnRen")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 745, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_such1.setText(_translate("MainWindow", "Suchbegriff 1"))
        self.lbl_such2.setText(_translate("MainWindow", "Suchbegriff 2"))
        self.btn_suchen.setText(_translate("MainWindow", "Suchen"))
        self.lbl_ergebnis.setText(_translate("MainWindow", "Such-Ergebnis"))
        self.btnDel.setText(_translate("MainWindow", "Löschen (Entf)"))
        self.btnRen.setText(_translate("MainWindow", "Umbenennen (F6)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

