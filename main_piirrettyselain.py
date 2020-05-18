import os
import subprocess
import funktiot_piirrettyfunktiot as pfun
import vakiot_kansiovakiot as kvak
import class_piirretyt as cp
import ikkuna_haku
import ikkuna_katsoneet
import ikkuna_puuttuvahaku
import ikkuna_puuttuvamuokkain
import ikkuna_uusienmuokkain
import funktiot_kansiofunktiot as kfun
import funktiot_anilist as anifun
from PyQt5 import QtCore, QtGui, QtWidgets

KUVAKANSIO = kvak.KUVAKANSIO
KUVAT = kfun.kansion_sisalto(KUVAKANSIO)[0]
OLETUSKUVA = os.path.join(KUVAKANSIO, "oletus.png")
PIIRRETTYDIKTI = pfun.PIIRRETTYDIKTI
SARJAT = []
for kansio in PIIRRETTYDIKTI:
    for sarja in PIIRRETTYDIKTI[kansio]:
        SARJAT.append(sarja)
# Sarjat aakkosjärjestykseen
SARJAT = pfun.jarjesta(SARJAT)

# Mitä näytetään listassa
NAYTETTAVAT = SARJAT                           # Mitä listalla näytetään (osajoukko SARJAT-listasta)
KARTOITIN   = [i for i in range(len(SARJAT))]  # mäppää näytettävien listan koko listaan (osajoukko)
SARJOJA     = len(KARTOITIN)                   # Kuinka monta sarjaa listalla on

KUVAMITAT       = (230, 336)
LISTAMITAT      = (440, KUVAMITAT[1])
TAULUKKOMITAT   = (LISTAMITAT[0], 178)
NAPPIMITAT      = (KUVAMITAT[0], 80)
MARGINAALIT     = (20,10)
MITAT           = (3*MARGINAALIT[0]+LISTAMITAT[0]+KUVAMITAT[0], 3*MARGINAALIT[1]+LISTAMITAT[1]+TAULUKKOMITAT[1])

class Paaikkuna(object):
    def setupUi(self, MainWindow):
        self.PIIRRETTYDIKTI = PIIRRETTYDIKTI
        self.SARJAT = SARJAT
        self.SARJOJA = SARJOJA
        self.KARTOITIN   = [i for i in range(len(self.SARJAT))]
        self.KUVAT = KUVAT

        # Tarkista puuttuvat sarjat
        self.muuttuneetindeksit = []        # Lista sarjoista (indekseistä) joille on käynyt hassusti
        self.ehdotukset         = []        # Lista ehdotetuista tiedostosijainneista
        self.peruutettiin       = True      # Jos käyttäjä peruutti toimenpiteen
        # self.indeksit, self.ehdotukset = pfun.tarkasta_puuttuvat(self.SARJAT)
        puuttuvien_tarkistusikkuna = ikkuna_puuttuvahaku.Tarkistuksen_edistyminen(self)
        puuttuvien_tarkistusikkuna.exec()
        self.poistetutsarjat = []
        # Jos jotain on muuttunut eikä käyttäjä peruuttanut hommaa
        if not self.peruutettiin and self.muuttuneetindeksit:
            Dialog = QtWidgets.QDialog()
            ui = ikkuna_puuttuvamuokkain.Ui_Puuttuvatsarjat()
            ui.setupUi(Dialog, self)
            ui.sarjannimet()
            paluuarvo = Dialog.exec()
            if paluuarvo:
                print("Muuttunut")
                if self.poistetutsarjat:
                    print("Poistetaan sarjat:")
                    i = len(self.poistetutsarjat)-1
                    while i >= 0:
                        print(self.SARJAT[self.poistetutsarjat[i]].nimi)
                        pfun.poista_diktista(self.PIIRRETTYDIKTI, self.SARJAT[self.poistetutsarjat[i]])
                        self.SARJAT.pop(self.poistetutsarjat[i])
                        i -= 1
                pfun.kirjoita_dikti(self.PIIRRETTYDIKTI, kvak.TIETOKANTATIEDOSTO) # kirjoita päivitys tiedostoon
                self.SARJOJA = len(self.SARJAT)
                self.KARTOITIN = [a for a in range(self.SARJOJA)]
            else:
                print("Peruttu")

        # Katsotaan, onko koneelle ilmaantunut uusia tai "uusia" piirrettyjä
        self.peruutettiin    = True
        self.uudetkansiot    = pfun.tarkasta_uudet(self.SARJAT)
        self.poistetutsarjat = []
        self.uudetteokset    = []
        if self.uudetkansiot:
            uusienmuokkain = ikkuna_uusienmuokkain.Ikkuna_uusienmuokkain(self)
            uusienmuokkain.exec()
            # Ei peruutettu ja jotain uutta löytyi:
            # uudet sarjat Piirrettyinä listassa
            if not(self.peruutettiin) and self.uudetteokset:
                for teos in self.uudetteokset:
                    print(teos.nimi)
                    self.SARJAT.append(teos)
                    # Laitetaan diktissä oikeaan kohtaan:
                    for kansio in self.PIIRRETTYDIKTI:
                        if kansio in teos.tiedostosijainti:
                            print(kansio)
                            self.PIIRRETTYDIKTI[kansio].append(teos)
                            break
                # Kirjataan tietokantaan
                pfun.kirjoita_dikti(self.PIIRRETTYDIKTI, kvak.TIETOKANTATIEDOSTO)
                # Aakkosjärjestykseen
                print("Järjestä taas")
                self.SARJAT = pfun.jarjesta(self.SARJAT)
                self.SARJOJA = len(self.SARJAT)
                self.KARTOITIN = [a for a in range(self.SARJOJA)]

        # Katsotaan, onko ihmiset katsonu viime aikoina piirrettyjä,
        # jos on tai on tullut uusia lokaaleja sarjoja, vertaillaan koneen
        # piirrettyjä ihmisten katsottujen listoihin
        uudetkatsotut = anifun.paivita_anilist_tietokannat()
        if uudetkatsotut:
            muuttunut = anifun.vertaa_katsoneita(uudetkatsotut, self.SARJAT)
            # Jos joku on katsonut sarjan joka on koneen kovalevyllä, päivitetään tämä
            # tieto sarjan tietoihin
            if muuttunut:
                pfun.kirjoita_dikti(self.PIIRRETTYDIKTI, kvak.TIETOKANTATIEDOSTO)
        if self.uudetteokset:
            muuttunut = anifun.vertaa_katsoneita(lokaalisarjat=self.uudetteokset)
            # Jos joku on katsonut sarjan joka on koneen kovalevyllä, päivitetään tämä
            # tieto sarjan tietoihin
            if muuttunut:
                pfun.kirjoita_dikti(self.PIIRRETTYDIKTI, kvak.TIETOKANTATIEDOSTO)
        
        # Lataa sarjojen kuvat
        pfun.lataa_kuvat_urleista(self.PIIRRETTYDIKTI)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MITAT[0], MITAT[1])
        MainWindow.setMinimumSize(QtCore.QSize(MITAT[0], MITAT[1]))
        MainWindow.setMaximumSize(QtCore.QSize(MITAT[0], MITAT[1]))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # self.kuva = QtWidgets.QGraphicsView(self.centralwidget)
        self.kuva = QtWidgets.QPushButton(self.centralwidget)
        self.kuva.setGeometry(QtCore.QRect(2*MARGINAALIT[0] + LISTAMITAT[0], MARGINAALIT[1], KUVAMITAT[0], KUVAMITAT[1]))
        self.kuva.setObjectName("kuva")
        # self.kuva.setScaledContents(True)
        self.kuva.setIcon(QtGui.QIcon(OLETUSKUVA))
        self.kuva.setIconSize(QtCore.QSize(KUVAMITAT[0]-5,KUVAMITAT[1]-5))
        self.kuva.clicked.connect(self.avaamal)
        # self.kuva.clicked.connect(self.etsi_sarjaa)

        self.sarjalista = QtWidgets.QListWidget(self.centralwidget)
        self.sarjalista.setGeometry(QtCore.QRect(MARGINAALIT[0], MARGINAALIT[1], LISTAMITAT[0], LISTAMITAT[1]))
        self.sarjalista.setObjectName("sarjalista")
        self.sarjalista.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # self.selModel = self.sarjalista.selectionModel()
        self.sarjalista.selectionModel().selectionChanged.connect(self.nayta_tiedot)
        # self.sarjalista.clicked.connect(self.nayta_tiedot)

        self.taulukko = QtWidgets.QTableWidget(self.centralwidget)
        self.taulukko.setGeometry(QtCore.QRect(MARGINAALIT[0], 2*MARGINAALIT[1]+LISTAMITAT[1], TAULUKKOMITAT[0], TAULUKKOMITAT[1]))
        self.taulukko.setObjectName("taulukko")
        self.taulukko.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.taulukko.setColumnCount(1)
        self.taulukko.setColumnWidth(0,340)
        self.taulukko.horizontalHeader().setVisible(False)

        self.taulukko.setRowCount(6)
        for row in range(6):
            self.taulukko.setRowHeight(row,20)
        self.taulukko.cellDoubleClicked.connect(self.taulukkomuokkaus)
        self.taulukko.verticalHeader().setVisible(True)
        self.taulukko.verticalHeader().setMaximumWidth(100)
        self.taulukko.verticalHeader().setMinimumWidth(100)
        self.taulukko.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.taulukko.setVerticalHeaderLabels(["Nimi", "Aliakset", "Jaksoja", "Tyyppi", "Tagit", "Katsoneet"])

        # self.taulukko.cellDoubleClicked.connect(self.taulukkomuokkaus)

        self.kansionappi = QtWidgets.QPushButton(self.centralwidget)
        self.kansionappi.setGeometry(QtCore.QRect(2*MARGINAALIT[0] + LISTAMITAT[0], 2*MARGINAALIT[1]+KUVAMITAT[1], NAPPIMITAT[0], NAPPIMITAT[1]))
        self.kansionappi.setObjectName("avaakansio")
        self.kansionappi.clicked.connect(self.avaakansio)

        self.etsimisnappi = QtWidgets.QPushButton(self.centralwidget)
        self.etsimisnappi.setGeometry(QtCore.QRect(2*MARGINAALIT[0] + LISTAMITAT[0], MITAT[1]-MARGINAALIT[1]-NAPPIMITAT[1], NAPPIMITAT[0], NAPPIMITAT[1]))
        self.etsimisnappi.setObjectName("etsisarjaa")
        self.etsimisnappi.clicked.connect(self.etsi_sarjaa)

        MainWindow.setCentralWidget(self.centralwidget)

        self.sarjannimet(self.SARJAT)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def etsi_sarjaa(self):
        self.NewWindow = QtWidgets.QMainWindow()
        uusiui = ikkuna_haku.Ui_Etsinikkuna()
        uusiui.setupUi(self.NewWindow, self)
        # uusiui.setupUi(self.NewWindow)
        self.NewWindow.show()


    def avaakansio(self):
        valittu = self.sarjalista.currentRow()
        if valittu != -1 and valittu < self.SARJOJA and os.path.exists(self.SARJAT[self.KARTOITIN[valittu]].tiedostosijainti):
            sarja = self.SARJAT[self.KARTOITIN[valittu]]
            print("Valittu sarja: {}\nKansiossa: {}".format(sarja.nimi, sarja.tiedostosijainti))
            subprocess.run(["dolphin", sarja.tiedostosijainti], stdin=None, stdout=None, stderr=None)


    def avaamal(self):
        valittu = self.sarjalista.currentRow()
        if valittu != -1 and valittu < self.SARJOJA:
            sarja = self.SARJAT[self.KARTOITIN[valittu]]
            print(sarja)
            subprocess.run(["firefox", sarja.mal], stdin=None, stdout=None, stderr=None)


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


    def nayta_tiedot(self):
        valittu = self.sarjalista.currentRow()
        if valittu != -1 and valittu < self.SARJOJA:
            sarja = self.SARJAT[self.KARTOITIN[valittu]]
            print(sarja)
            print(sarja.nimi)
            print(sarja.mal)
            sarjaid = sarja.kuvake
            print(sarjaid)
            # Etsi sarjaid:tä vastaava kuvatiedosto
            kuvake = OLETUSKUVA
            self.KUVAT = kfun.kansion_sisalto(KUVAKANSIO)[0]
            for k in self.KUVAT:
                # print(kfun.paate(k)[0])
                if kfun.paate(k)[0] == sarjaid:
                    kuvake = os.path.join(KUVAKANSIO, k)
                    break
            print(kuvake)
            if os.path.exists(kuvake):
                self.kuva.setIcon(QtGui.QIcon(kuvake))
            self.tietotaulukko(sarja)
            if not os.path.exists(sarja.tiedostosijainti):
                self.kansionappi.setStyleSheet("background-color: #e189a8; color: black") # punainen ruutu
            else:
                self.kansionappi.setStyleSheet("") # punainen ruutu
        else:
        	# tyhjä sarja
        	self.tietotaulukko(cp.Piirretty())
        	self.kuva.setIcon(QtGui.QIcon(OLETUSKUVA))


    def tietotaulukko(self, sarja):
        self.taulukko.setItem(0, 0, QtWidgets.QTableWidgetItem(sarja.nimi))

        aliakset = ""
        aliaksia = len(sarja.aliakset)-1
        for a,alias in enumerate(sarja.aliakset):
            aliakset += "\"{}\"{}".format(alias, ", "*(a<aliaksia))
        self.taulukko.setItem(1, 0, QtWidgets.QTableWidgetItem(aliakset))

        self.taulukko.setItem(2, 0, QtWidgets.QTableWidgetItem(str(sarja.jaksoja)))

        tyypit = ""
        tyyppeja = len(sarja.tyyppi)-1
        for a,tyyppi in enumerate(sarja.tyyppi):
            tyypit += "{}{}".format(tyyppi, ", "*(a<tyyppeja))
        self.taulukko.setItem(3, 0, QtWidgets.QTableWidgetItem(tyypit))

        tagit = ""
        tageja = len(sarja.tagit)-1
        for a,tagi in enumerate(sarja.tagit):
            tagit += "{}{}".format(tagi, ", "*(a<tageja))
        self.taulukko.setItem(4, 0, QtWidgets.QTableWidgetItem(tagit))

        katsoneet = ""
        katsoneita = len(sarja.katsoneet)-1
        for a,katsoja in enumerate(sarja.katsoneet):
            katsoneet += "{}{}".format(katsoja, ", "*(a<katsoneita))
        self.taulukko.setItem(5, 0, QtWidgets.QTableWidgetItem(katsoneet))


    def taulukkomuokkaus(self, rivi, sarake):
        muuttunut = False
        valittu = self.sarjalista.currentRow()
        if valittu != -1 and valittu < self.SARJOJA:
            # print(self.KARTOITIN[valittu])
            sarja = self.SARJAT[self.KARTOITIN[valittu]]

            # Sarjan nimen muokkaus
            if (rivi, sarake) == (0,0):
                uusinimi, ok = QtWidgets.QInputDialog.getText(self.centralwidget, 'Nimi', 'Sarjan nimi:', text=sarja.nimi)
                if ok and uusinimi != sarja.nimi:
                    sarja.nimi = uusinimi
                    muuttunut = True

            # Aliasten lisääminen tai poistaminen
            elif (rivi, sarake) == (1,0):
                box = QtWidgets.QMessageBox()
                # box.setIcon(QtWidgets.QMessageBox.Question)
                box.width = 500
                box.height = 500
                box.setWindowTitle('Muokkaa aliaksia')
                box.setText('Lisää vai poista alias?')
                box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Cancel)
                lisaa = box.button(QtWidgets.QMessageBox.Yes)
                lisaa.setText('Lisää')
                poista = box.button(QtWidgets.QMessageBox.No)
                poista.setText('Poista')
                peru = box.button(QtWidgets.QMessageBox.Cancel)
                peru.setText('Peru')
                box.exec_()
                muuttunut = False

                # Lisää uusi alias
                if box.clickedButton() == lisaa:
                    dialogi = QtWidgets.QInputDialog()
                    uusinimi, ok = dialogi.getText(self.centralwidget, 'Uusi alias', 'Alias:')
                    if ok and uusinimi and any([not(a.isspace()) for a in uusinimi]):
                        alias = uusinimi.replace("\"", "\\\"")
                        print(f"Lisätään alias {alias}")
                        sarja.aliakset.append(alias)
                        muuttunut = True

                # Poista alias sarjan aliaslistasta
                elif box.clickedButton() == poista and sarja.aliakset:
                    dialogi = QtWidgets.QInputDialog()
                    alias, ok = dialogi.getItem(self.centralwidget, "Poista alias", "Aliakset", sarja.aliakset, 0, False)
                    if ok:
                        sarja.aliakset.remove(alias)
                        muuttunut = True

            # Jaksomäärän muokkaus
            elif (rivi, sarake) == (2,0):
                uusimaara, ok = QtWidgets.QInputDialog.getInt(self.centralwidget, "Jaksoja","Jaksoja:", sarja.jaksoja, 1, 0xFFFF, 1)
                if ok and uusimaara != sarja.jaksoja:
                    sarja.jaksoja = uusimaara
                    muuttunut = True

            # Katsoneiden muokkaaminen
            elif (rivi, sarake) == (5,0):
                valittu = self.sarjalista.currentRow()
                if valittu != -1 and valittu < self.SARJOJA:
                    sarja = self.SARJAT[self.KARTOITIN[valittu]]
                    Dialog = QtWidgets.QDialog()
                    ui = ikkuna_katsoneet.Ui_Dialog()
                    ui.setupUi(Dialog, sarja)
                    paluuarvo = Dialog.exec()
                    if paluuarvo:
                        print("Muuttunut")
                        sarja.katsoneet = ui.katsoneet
                        muuttunut = True
                    else:
                        print("Peruttu")


        if muuttunut:
            self.nayta_tiedot()
            self.sarjannimet([self.SARJAT[a] for a in self.KARTOITIN])
            pfun.kirjoita_dikti(self.PIIRRETTYDIKTI, kvak.TIETOKANTATIEDOSTO) # kirjoita päivitys tiedostoon
            self.sarjalista.setCurrentRow(valittu) # palaa sarjalistalla sarjan kohdalle


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Piirrettyselain"))
        self.kansionappi.setText(_translate("MainWindow", "Avaa kansio"))
        self.etsimisnappi.setText(_translate("MainWindow", "Etsi"))
        self.etsimisnappi.setShortcut(_translate("MainWindow", "Ctrl+F"))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Paaikkuna()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec()
