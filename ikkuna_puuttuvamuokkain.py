import os
import subprocess
import time
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Puuttuvatsarjat(object):
    def setupUi(self, Puuttuvatsarjat, Paaikkuna):
        Puuttuvatsarjat.setObjectName("Puuttuvatsarjat")
        Puuttuvatsarjat.resize(850, 285)

        # font = QtGui.QFont()
        # font.setPointSize(12)

        self.buttonBox = QtWidgets.QDialogButtonBox(Puuttuvatsarjat)
        self.buttonBox.setGeometry(QtCore.QRect(50, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")

        self.sarjalista = QtWidgets.QListWidget(Puuttuvatsarjat)
        self.sarjalista.setGeometry(QtCore.QRect(10, 20, 211, 201))
        self.sarjalista.setObjectName("sarjalista")
        self.sarjalista.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sarjalista.selectionModel().selectionChanged.connect(self.nayta_tiedot)

        self.Paaikkuna  = Paaikkuna
        self.sarjat     = Paaikkuna.SARJAT                  # lista kaikista sarjoista
        self.indeksit   = Paaikkuna.muuttuneetindeksit      # puuttuvien indeksit
        self.ehdotukset = Paaikkuna.ehdotukset              # kansioehdotukset

        self.teksti_vanhapolku = QtWidgets.QLineEdit(Puuttuvatsarjat)
        self.teksti_vanhapolku.setGeometry(QtCore.QRect(230, 40, 600, 31))
        # self.teksti_vanhapolku.setFont(font)
        self.teksti_vanhapolku.setText("")
        self.teksti_vanhapolku.setReadOnly(True)
        self.teksti_vanhapolku.setObjectName("teksti_vanhapolku")

        self.label_vanhapolku = QtWidgets.QLabel(Puuttuvatsarjat)
        self.label_vanhapolku.setGeometry(QtCore.QRect(240, 20, 201, 20))
        self.label_vanhapolku.setObjectName("label_vanhapolku")
        self.label_uusipolku = QtWidgets.QLabel(Puuttuvatsarjat)
        self.label_uusipolku.setGeometry(QtCore.QRect(240, 100, 201, 20))
        self.label_uusipolku.setObjectName("label_uusipolku")

        self.teksti_uusipolku = QtWidgets.QLineEdit(Puuttuvatsarjat)
        self.teksti_uusipolku.setGeometry(QtCore.QRect(230, 120, 600, 31))
        # self.teksti_uusipolku.setFont(font)
        self.teksti_uusipolku.setText("")
        self.teksti_uusipolku.setObjectName("teksti_uusipolku")
        self.teksti_uusipolku.textChanged.connect(self.tarkistakansio)
        completer = QtWidgets.QCompleter()
        completer.setModel(QtWidgets.QDirModel(completer))
        self.teksti_uusipolku.setCompleter(completer)

        self.Aseta = QtWidgets.QPushButton(Puuttuvatsarjat)
        self.Aseta.setGeometry(QtCore.QRect(230, 170, 51, 41))
        self.Aseta.setObjectName("Aseta")
        self.Aseta.clicked.connect(self.aseta_uusikansio)

        self.Poista = QtWidgets.QPushButton(Puuttuvatsarjat)
        self.Poista.setGeometry(QtCore.QRect(290, 170, 51, 41))
        self.Poista.setObjectName("Poista")
        self.Poista.clicked.connect(self.poistasarja)

        self.Kansio = QtWidgets.QPushButton(Puuttuvatsarjat)
        self.Kansio.setGeometry(QtCore.QRect(400, 170, 51, 41))
        self.Kansio.setObjectName("Kansio")
        self.Kansio.clicked.connect(self.avaa_ehdotuskansio)

        self.retranslateUi(Puuttuvatsarjat)
        self.buttonBox.accepted.connect(Puuttuvatsarjat.accept)
        self.buttonBox.rejected.connect(Puuttuvatsarjat.reject)
        QtCore.QMetaObject.connectSlotsByName(Puuttuvatsarjat)

    def retranslateUi(self, Puuttuvatsarjat):
        _translate = QtCore.QCoreApplication.translate
        Puuttuvatsarjat.setWindowTitle(_translate("Puuttuvatsarjat", "Puuttuvia sarjoja"))
        self.label_vanhapolku.setText(_translate("Puuttuvatsarjat", "Vanha polku"))
        self.label_uusipolku.setText(_translate("Puuttuvatsarjat", "Uusi polku"))
        self.Aseta.setText(_translate("Puuttuvatsarjat", "Aseta"))
        self.Poista.setText(_translate("Puuttuvatsarjat", "Poista"))
        self.Kansio.setText(_translate("Puuttuvatsarjat", "Kansio"))

    def sarjannimet(self):
        '''
        Lisää sarjojen nimet listaan, mikäli sarjalle
        ei ole vielä asetettu uutta kansiota
        '''
        nimet = []
        self.sarjalista.clear()
        for indeksi in self.indeksit:
            nimet.append(self.sarjat[indeksi].nimi)
        self.sarjalista.addItems(nimet)
        self.sarjalista.show()

    def nayta_tiedot(self):
        '''
        Asettaa valitun sarjan tiedot (vanhan kansion ja ehdotuksen) näkyville
        '''
        if self.indeksit:
            valittu = self.sarjalista.currentRow()
            if valittu != -1:
                sarja = self.sarjat[self.indeksit[valittu]]
                self.teksti_vanhapolku.setText(sarja.tiedostosijainti)
                self.teksti_uusipolku.setText(self.ehdotukset[valittu])

    def tarkistakansio(self):
        '''
        Tarkistaa, onko ehdotettu uusi kansio olemassa vai ei
        '''
        if self.teksti_uusipolku.text():
            if os.path.exists(self.teksti_uusipolku.text()):
                self.teksti_uusipolku.setStyleSheet("background-color: #3eaf18; color: black") # vihreä ruutu
            else:
                self.teksti_uusipolku.setStyleSheet("background-color: #e189a8; color: black") # punainen ruutu
        else:
            self.teksti_uusipolku.setStyleSheet("background-color: grey") # normiruutu
    
    def aseta_uusikansio(self):
        '''
        Asettaa uuden kansion sarjan tietoihin
        '''
        valittu = self.sarjalista.currentRow()
        if valittu != -1 and self.teksti_uusipolku.text():
            sarja = self.sarjat[self.indeksit[valittu]]
            uusisijainti = self.teksti_uusipolku.text()
            # Ei kautta- tai kenoviivaan päättyviä polkuja
            if uusisijainti[-1] in ["/", "\\"]:
                uusisijainti = uusisijainti[:-1]
            sarja.tiedostosijainti = uusisijainti
            # sarja.tiedostosijainti = self.ehdotukset[valittu]
            self.indeksit.pop(valittu)
            self.ehdotukset.pop(valittu)
            self.sarjannimet()
            if self.indeksit:
                self.sarjalista.setCurrentRow(0)

    def poistasarja(self):
        '''
        Poistetaan sarja tietokannasta, koska se on poistettu kovalevyltä
        '''
        valittu = self.sarjalista.currentRow()
        if self.indeksit and valittu != -1:
            self.Paaikkuna.poistetutsarjat.append(self.indeksit[valittu])
            self.indeksit.pop(valittu)
            self.ehdotukset.pop(valittu)
            self.sarjannimet()
            if self.indeksit:
                self.sarjalista.setCurrentRow(0)

    def avaa_ehdotuskansio(self):
        '''
        Avaa ehdotetun kansion jotta käyttäjä voi katsoa näyttääkö oikealta
        '''
        valittu = self.sarjalista.currentRow()
        if valittu != -1:
            uusisijainti = self.teksti_uusipolku.text()
            if os.path.exists(uusisijainti):
                subprocess.run(["dolphin", uusisijainti], stdin=None, stdout=None, stderr=None)
