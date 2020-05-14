# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'piirretyt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.kuva = QtWidgets.QGraphicsView(self.centralwidget)
        self.kuva.setGeometry(QtCore.QRect(505, 10, 230, 336))
        self.kuva.setObjectName("kuva")
        self.sarjalista = QtWidgets.QListWidget(self.centralwidget)
        self.sarjalista.setGeometry(QtCore.QRect(20, 10, 441, 331))
        self.sarjalista.setObjectName("sarjalista")
        self.avaakansio = QtWidgets.QPushButton(self.centralwidget)
        self.avaakansio.setGeometry(QtCore.QRect(505, 350, 230, 81))
        self.avaakansio.setObjectName("avaakansio")
 
        self.taulukko = QtWidgets.QTableWidget(self.centralwidget)
        self.taulukko.setGeometry(QtCore.QRect(20, 350, 441, 241))
        self.taulukko.setMinimumSize(QtCore.QSize(441, 0))
        self.taulukko.setObjectName("taulukko")
        self.taulukko.setColumnCount(1)
        self.taulukko.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Nimi")
        self.taulukko.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.taulukko.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.taulukko.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.taulukko.setVerticalHeaderItem(3, item)
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Arvot")
        self.taulukko.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable)
        self.taulukko.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        self.taulukko.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable)
        self.taulukko.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        self.taulukko.setItem(3, 0, item)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.avaakansio.setText(_translate("MainWindow", "Avaa kansio"))
        item = self.taulukko.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Aliakset"))
        item = self.taulukko.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Jaksoja"))
        item = self.taulukko.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Katsoneet"))
        __sortingEnabled = self.taulukko.isSortingEnabled()
        self.taulukko.setSortingEnabled(False)
        self.taulukko.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
