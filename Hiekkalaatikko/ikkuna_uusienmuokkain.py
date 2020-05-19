# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uusienmuokkain.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Uusienmuokkain(object):
    def setupUi(self, Uusienmuokkain):
        Uusienmuokkain.setObjectName("Uusienmuokkain")
        Uusienmuokkain.resize(758, 229)
        self.Lista_uudet = QtWidgets.QListWidget(Uusienmuokkain)
        self.Lista_uudet.setGeometry(QtCore.QRect(20, 10, 256, 201))
        self.Lista_uudet.setObjectName("Lista_uudet")
        self.kansiopolku = QtWidgets.QLineEdit(Uusienmuokkain)
        self.kansiopolku.setGeometry(QtCore.QRect(290, 10, 311, 31))
        self.kansiopolku.setObjectName("kansiopolku")
        self.Hakutulokset = QtWidgets.QComboBox(Uusienmuokkain)
        self.Hakutulokset.setGeometry(QtCore.QRect(290, 130, 451, 31))
        self.Hakutulokset.setObjectName("Hakutulokset")
        self.MAL_linkki = QtWidgets.QLineEdit(Uusienmuokkain)
        self.MAL_linkki.setGeometry(QtCore.QRect(290, 50, 311, 31))
        self.MAL_linkki.setObjectName("MAL_linkki")
        self.buttonBox = QtWidgets.QDialogButtonBox(Uusienmuokkain)
        self.buttonBox.setGeometry(QtCore.QRect(290, 180, 174, 33))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.Nappi_kansio = QtWidgets.QPushButton(Uusienmuokkain)
        self.Nappi_kansio.setGeometry(QtCore.QRect(600, 10, 141, 33))
        self.Nappi_kansio.setObjectName("Nappi_kansio")
        self.Nappi_MAL = QtWidgets.QPushButton(Uusienmuokkain)
        self.Nappi_MAL.setGeometry(QtCore.QRect(600, 50, 141, 33))
        self.Nappi_MAL.setObjectName("Nappi_MAL")
        self.MAL_linkki_2 = QtWidgets.QLineEdit(Uusienmuokkain)
        self.MAL_linkki_2.setGeometry(QtCore.QRect(290, 90, 311, 31))
        self.MAL_linkki_2.setObjectName("MAL_linkki_2")
        self.Nappi_Aseta = QtWidgets.QPushButton(Uusienmuokkain)
        self.Nappi_Aseta.setGeometry(QtCore.QRect(600, 90, 141, 33))
        self.Nappi_Aseta.setObjectName("Nappi_Aseta")
        self.pushButton = QtWidgets.QPushButton(Uusienmuokkain)
        self.pushButton.setGeometry(QtCore.QRect(470, 180, 271, 33))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Uusienmuokkain)
        QtCore.QMetaObject.connectSlotsByName(Uusienmuokkain)

    def retranslateUi(self, Uusienmuokkain):
        _translate = QtCore.QCoreApplication.translate
        Uusienmuokkain.setWindowTitle(_translate("Uusienmuokkain", "Löytyi uusia sarjoja"))
        self.Nappi_kansio.setText(_translate("Uusienmuokkain", "Kansio"))
        self.Nappi_MAL.setText(_translate("Uusienmuokkain", "MAL"))
        self.Nappi_Aseta.setText(_translate("Uusienmuokkain", "Aseta"))
        self.pushButton.setText(_translate("Uusienmuokkain", "Tämä ei ole sarja"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Uusienmuokkain = QtWidgets.QWidget()
    ui = Ui_Uusienmuokkain()
    ui.setupUi(Uusienmuokkain)
    Uusienmuokkain.show()
    sys.exit(app.exec_())
