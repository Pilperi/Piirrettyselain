import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Sijaintitarkistin(object):
    def setupUi(self, Sijaintitarkistin):
        self.MITAT          = [400,330]
        self.MARGINAALIT    = [10,10]

        Sijaintitarkistin.setObjectName("Sijaintitarkistin")
        Sijaintitarkistin.resize(self.MITAT[0], self.MITAT[1])
        Sijaintitarkistin.setMinimumSize(QtCore.QSize(self.MITAT[0], self.MITAT[1]))
        Sijaintitarkistin.setMaximumSize(QtCore.QSize(self.MITAT[0], self.MITAT[1]))
        # Sijaintitarkistin.setCancelButton(None)
        # Sijaintitarkistin.setAutoClose(True)
        # Sijaintitarkistin.setModal(True)
        # Sijaintitarkistin.setMinimum(0)
        # Sijaintitarkistin.setMaximum(100)

        self.Sijaintitarkistin = Sijaintitarkistin

        self.progressBar = QtWidgets.QProgressBar(Sijaintitarkistin)
        self.progressBar.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1], self.MITAT[0]-2*self.MARGINAALIT[0], self.MARGINAALIT[1]))
        self.progressBar.setValue(0)
        self.progressBar.setObjectName("progressBar")
        # self.Sijaintitarkistin.setBar(self.progressBar)

        self.tarkastettava = QtWidgets.QLineEdit(Sijaintitarkistin)
        self.tarkastettava.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1]*3, self.MITAT[0]-2*self.MARGINAALIT[0], 30))
        self.tarkastettava.setAutoFillBackground(False)
        self.tarkastettava.setObjectName("tarkastettava")
        self.tarkastettava.setReadOnly(True)

        self.kansiossa = QtWidgets.QLineEdit(Sijaintitarkistin)
        self.kansiossa.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1]*4+30, self.MITAT[0]-2*self.MARGINAALIT[0], 30))
        self.kansiossa.setObjectName("kansiossa")
        self.kansiossa.setReadOnly(True)

        # self.mene = QtWidgets.QPushButton(Sijaintitarkistin)
        # self.mene.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1]*5+2*30, self.MITAT[0]-2*self.MARGINAALIT[0], 30))
        # self.mene.setObjectName("kuva")
        # self.mene.setText("Mene")
        # self.mene.clicked.connect(self.edista)

        self.retranslateUi(Sijaintitarkistin)
        QtCore.QMetaObject.connectSlotsByName(Sijaintitarkistin)

        self.edista()
        # Sijaintitarkistin.exec()
        
        # for i in range(100):
        #     # self.progressBar.setValue(i)
        #     self.Sijaintitarkistin.setValue(i)
        #     print(i)
        #     time.sleep(0.01)
        # self.Sijaintitarkistin.close()


    def edista(self):
        # self.progressBar.setValue(0)
        # self.Sijaintitarkistin.setValue(0)
        # self.Sijaintitarkistin.show()
        # time.sleep(5)
        for i in range(101):
            self.progressBar.setValue(i)
            # self.Sijaintitarkistin.setValue(i)
            print(i)
            time.sleep(0.01)
        # self.Sijaintitarkistin.close()

    def retranslateUi(self, Sijaintitarkistin):
        _translate = QtCore.QCoreApplication.translate
        Sijaintitarkistin.setWindowTitle(_translate("Sijaintitarkistin", "Tarkistetaan kansioita..."))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    Sijaintitarkistin = QtWidgets.QDialog()
    # Sijaintitarkistin = QtWidgets.QProgressDialog()
    ui = Ui_Sijaintitarkistin()
    ui.setupUi(Sijaintitarkistin)

    Sijaintitarkistin.exec()
    # Sijaintitarkistin.show()
    time.sleep(2)
    # app.exec_()
    # ui.edista()
    # Sijaintitarkistin.show()
    # time.sleep(5)
    # ui.edista(Sijaintitarkistin)
    # sys.exit(app.exec_())
