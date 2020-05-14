# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'piirretyt.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import piirrettysijainnit as ps
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebKitWidgets

MANUAALIDIKTI = ps.MANUAALIDIKTI
PIIRRETTYDIKTI = ps.PIIRRETTYDIKTI
SARJAT = []
for kansio in MANUAALIDIKTI:
    for sarja in MANUAALIDIKTI[kansio]:
        SARJAT.append(sarja)
SARJOJA = len(SARJAT)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 645)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.webView = QtWebKitWidgets.QWebView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(439, 10, 351, 291))
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")

        self.sarjalista = QtWidgets.QListWidget(self.centralwidget)
        self.sarjalista.setGeometry(QtCore.QRect(20, 10, 381, 291))
        self.sarjalista.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sarjalista.setObjectName("sarjalista")
        self.sarjalista.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sarjalista.clicked.connect(self.etsi)

        self.sarjatiedot = QtWidgets.QTableWidget(self.centralwidget)
        self.sarjatiedot.setGeometry(QtCore.QRect(20, 320, 381, 281))
        self.sarjatiedot.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.sarjatiedot.setObjectName("sarjatiedot")
        self.sarjatiedot.setColumnCount(0)
        self.sarjatiedot.setRowCount(0)

        self.tallenna = QtWidgets.QPushButton(self.centralwidget)
        self.tallenna.setGeometry(QtCore.QRect(440, 370, 191, 101))
        self.tallenna.setObjectName("tallenna")
        self.tallenna.clicked.connect(self.paivita_kokolista)

        self.sarjaid = QtWidgets.QLineEdit(self.centralwidget)
        self.sarjaid.setGeometry(QtCore.QRect(530, 320, 230, 32))
        self.sarjaid.setObjectName("sarjaid")

        self.nappaaurl = QtWidgets.QPushButton(self.centralwidget)
        self.nappaaurl.setGeometry(QtCore.QRect(440, 320, 88, 34))
        self.nappaaurl.setObjectName("nappaaurl")
        self.nappaaurl.clicked.connect(self.id_urlista)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def sarjannimet(self, lista):
        '''
        Lisää sarjojen nimet listaan
        '''
        nimet = []
        self.sarjalista.clear()
        for sarja in lista:
            nimet.append(sarja.nimi)
        self.sarjalista.addItems(nimet)
        self.sarjalista.show()

    def etsi(self):
        valittu = self.sarjalista.currentRow()
        if valittu != -1 and valittu < SARJOJA:
            print(f"valittu {valittu}")
            sarja = SARJAT[valittu]
            print(sarja)
            print(sarja.nimi)
            print(sarja.mal)
            self.webView.setUrl(QtCore.QUrl(sarja.mal))

    def id_urlista(self):
        '''
        Nappaa sarjan ID MAL-urlista
        '''
        kokourli = self.webView.url().toString()
        # urlin rakenne
        # https://myanimelist.net/anime/658/sarjannimi/ eli ID on
        sarja_id = kokourli.split("/")[-2]
        print(sarja_id)
        sarja_nimi = kokourli.split("/")[-1].replace("_", " ")
        print(sarja_nimi)
        self.sarjaid.setText("{}: {:7s}".format(sarja_id, sarja_nimi))
        sarja = SARJAT[self.sarjalista.currentRow()]
        sarja.mal      = "https://myanimelist.net/anime/{}".format(sarja_id)
        sarja.kuvake   = "{}".format(sarja_id)
        if sarja_nimi != sarja.nimi and sarja_nimi not in sarja.aliakset:
            sarja.aliakset.append(sarja_nimi.replace("\"", "\\\""))

    def paivita_kokolista(self):
        poistettavat = [] # lista sarjoista joille on saatu tiedot (sarjaindeksejä)
        for i,sarja in enumerate(SARJAT):
            for kansio in PIIRRETTYDIKTI:
                for j,sarjaehdokas in enumerate(PIIRRETTYDIKTI[kansio]):
                    # jos sarjat sijaitsevat samassa kansiossa, ne ovat sama sarja
                    if sarjaehdokas.tiedostosijainti == sarja.tiedostosijainti:
                        # Sarjan tietämisen tunnistaa mm. siitä että sen kuvake on "oikea"
                        if sarja.kuvake != "oletus":
                            poistettavat.append(i)
                            PIIRRETTYDIKTI[kansio][j] = sarja
                            # Poista myös manuaalidiktistä
                            for k,manuaalisarja in enumerate(MANUAALIDIKTI[kansio]):
                                if manuaalisarja.tiedostosijainti == sarja.tiedostosijainti:
                                    del MANUAALIDIKTI[kansio][k]
                                    break
                        break
        # Kirjoita tietokantaan
        ps.kirjoita_dikti(PIIRRETTYDIKTI, ps.TIETOKANTATIEDOSTO)
        ps.kirjoita_dikti(MANUAALIDIKTI, ps.MANUAALISARJAT)
        print("poistettavia: {}".format(len(poistettavat)))
        poistettavat.reverse()
        for indeksi in poistettavat:
            del SARJAT[indeksi]
        self.sarjannimet(SARJAT)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Päivitä manuaalisesti"))
        self.tallenna.setText(_translate("MainWindow", "Tallenna"))
        self.nappaaurl.setText(_translate("MainWindow", "Nappaa ID"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.sarjannimet(SARJAT)
    MainWindow.show()
    sys.exit(app.exec_())
