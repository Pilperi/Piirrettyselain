import os
import time
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
import funktiot_piirrettyfunktiot as pfun
import funktiot_anilist as anifun
import class_piirretyt as cp


class Ikkuna_uusienmuokkain(QtWidgets.QDialog):
    def __init__(self, Isantaikkuna):
        super().__init__()

        self.Isantaikkuna = Isantaikkuna
        self.MARGINAALIT    = [10,10]
        # self.MITAT          = [self.MARGINAALIT[0]*3+255+310+140,self.MARGINAALIT[1]*8+30*4+23+30]
        self.MITAT          = [self.MARGINAALIT[0]*3+255+310+140,self.MARGINAALIT[1]*4+30*4+23+30]
        self.resize(self.MITAT[0], self.MITAT[1])
        self.setMinimumSize(QtCore.QSize(self.MITAT[0], self.MITAT[1]))
        self.setMaximumSize(QtCore.QSize(self.MITAT[0], self.MITAT[1]))

        self.setWindowTitle("Löytyi uusia sarjoja")

        self.siivotutnimet = []
        self.sarjahaut = [] # anilist-hakutulokset, listaindeksien mukaan (2D lista)
        # testikansiot = ["/mnt/Suzuya/Suzuyajako/Anime/[OVA]Aikatsu! Nerawareta mahou no aikatsu card",
                        # "/mnt/Suzuya/Suzuyajako/Anime/Genshiken",
                        # "/mnt/Suzuya/Suzuyajako/Anime/[RAW] [OVA] Majimoji Rurumo kanketsuhen",
                        # "/mnt/Suzuya/Suzuyajako/Anime/Aikatsu! [RAW]"]
        # self.uudetsarjat = testikansiot
        self.uudetsarjat = Isantaikkuna.uudetkansiot
        print(self.uudetsarjat)
        self.maaritetyt = []

        self.Lista_uudet = QtWidgets.QListWidget(self)
        # self.Lista_uudet.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1], 255, self.MARGINAALIT[1]*5+30*4+23))
        self.Lista_uudet.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1], 255, self.MARGINAALIT[1]*4+30*3+20))
        self.Lista_uudet.setObjectName("Lista_uudet")
        self.Lista_uudet.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.Lista_uudet.selectionModel().selectionChanged.connect(self.nayta_tiedot_lista)

        self.kansiopolku = QtWidgets.QLineEdit(self)
        self.kansiopolku.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255, self.MARGINAALIT[1], 310, 30))
        self.kansiopolku.setObjectName("kansiopolku")
        self.kansiopolku.setReadOnly(True)

        self.Nappi_kansio = QtWidgets.QPushButton(self)
        self.Nappi_kansio.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255+310, self.MARGINAALIT[1], 140, 30))
        self.Nappi_kansio.setObjectName("Nappi_kansio")
        self.Nappi_kansio.setText("Avaa kansio")
        self.Nappi_kansio.clicked.connect(self.avaakansio)
        self.Nappi_kansio.setStyleSheet("background-color: #232629")
        self.Nappi_kansio.setCheckable(False)
        self.Nappi_kansio.setFocusPolicy(QtCore.Qt.NoFocus)

        self.MAL_linkki = QtWidgets.QLineEdit(self)
        self.MAL_linkki.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255, self.MARGINAALIT[1]*2+30, 310, 30))
        self.MAL_linkki.setObjectName("MAL_linkki")
        self.MAL_linkki.textChanged.connect(self.lisaamal)

        self.Nappi_MAL = QtWidgets.QPushButton(self)
        self.Nappi_MAL.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255+310, self.MARGINAALIT[1]*2+30, 140, 30))
        self.Nappi_MAL.setObjectName("Nappi_MAL")
        self.Nappi_MAL.setText("MAL")
        self.Nappi_MAL.clicked.connect(self.avamal)
        self.Nappi_MAL.setStyleSheet("background-color: #2e51a2; color: white; font-weight: bold") # MAL-värit
        self.Nappi_MAL.setCheckable(False)
        self.Nappi_MAL.setFocusPolicy(QtCore.Qt.NoFocus)

        self.Sarjan_tiedot = QtWidgets.QLineEdit(self)
        self.Sarjan_tiedot.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255, self.MARGINAALIT[1]*3+30*2, 310, 30))
        self.Sarjan_tiedot.setObjectName("Sarjan tiedot")
        self.Sarjan_tiedot.setText("")
        self.Sarjan_tiedot.setReadOnly(True)

        self.Nappi_Aseta = QtWidgets.QPushButton(self)
        # self.Nappi_Aseta.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255+310, self.MARGINAALIT[1]*3+30*2, 140, 30)) # Tietojen vieressä
        self.Nappi_Aseta.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255, self.MARGINAALIT[1]*5+30*4, 175, 35)) # pudotusvalikon alla
        self.Nappi_Aseta.setObjectName("Nappi_Aseta")
        self.Nappi_Aseta.setText("Aseta")
        self.Nappi_Aseta.clicked.connect(self.aseta)
        self.Nappi_Aseta.setCheckable(False)
        self.Nappi_Aseta.setFocusPolicy(QtCore.Qt.NoFocus)

        self.Hakutulokset = QtWidgets.QComboBox(self)
        self.Hakutulokset.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255, self.MARGINAALIT[1]*4+30*3, 310, 30))
        self.Hakutulokset.setObjectName("Hakutulokset")
        self.Hakutulokset.currentIndexChanged.connect(self.nayta_tiedot_hakutiedot)
        # self.Hakutulokset.setFocusPolicy(QtCore.Qt.NoFocus)

        self.Nappi_Peruuta = QtWidgets.QPushButton(self)
        self.Nappi_Peruuta.setGeometry(QtCore.QRect(self.MARGINAALIT[0]+120+7, self.MARGINAALIT[1]*5+30*4, 128, 35)) # pudotusvalikon alla
        self.Nappi_Peruuta.setObjectName("Nappi_Peruuta")
        self.Nappi_Peruuta.setText("Peruuta")
        self.Nappi_Peruuta.clicked.connect(self.peruuta)
        self.Nappi_Peruuta.setCheckable(False)
        self.Nappi_Peruuta.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.Nappi_Peruuta.setStyleSheet("background-color: #e189a8; color: black") # punainen ruutu

        self.Nappi_Tallenna = QtWidgets.QPushButton(self)
        self.Nappi_Tallenna.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1]*5+30*4, 120, 35)) # pudotusvalikon alla
        self.Nappi_Tallenna.setObjectName("Nappi_Tallenna")
        self.Nappi_Tallenna.setText("Valmis")
        self.Nappi_Tallenna.clicked.connect(self.hyvaksytty)
        self.Nappi_Tallenna.setCheckable(False)
        self.Nappi_Tallenna.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.Nappi_Tallenna.setStyleSheet("background-color: #3eaf18; color: black") # vihreä ruutu

        self.Nappi_Eisarja = QtWidgets.QPushButton(self)
        self.Nappi_Eisarja.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+255+180, self.MARGINAALIT[1]*5+30*4, 310-175-5, 35))
        self.Nappi_Eisarja.setObjectName("Nappi_Eisarja")
        self.Nappi_Eisarja.setText("Tämä ei ole sarja")
        self.Nappi_Eisarja.clicked.connect(self.tamaeiolesarja)
        self.Nappi_Eisarja.setCheckable(False)
        self.Nappi_Eisarja.setFocusPolicy(QtCore.Qt.NoFocus)

        self.kansioita_lista()


    def peruuta(self):
        '''
        Signaloidaan että lisäysprosessi peruutettiin ja suljetaan ikkuna
        '''
        print("peruutettiin")
        self.Isantaikkuna.peruutettiin = True
        self.close()

    def hyvaksytty(self):
        '''
        Signaloidaan että lisäysprosessi on valmis ja suljetaan ikkuna
        '''
        print("hyväksyttiin")
        print(self.maaritetyt)
        self.Isantaikkuna.uudetteokset = self.maaritetyt
        self.Isantaikkuna.peruutettiin = False
        self.close()

    def kansioita_lista(self):
        '''
        Ottaa sisään listan kansioita, jotka tulleet funktiosta
        funktiot_piirrettyfunktiot.tarkasta_uudet()
        ja läimii kansioiden nimet listaan.
        Muodostaa samalla siivotut versiot sarjojen nimistä (karsii [OVA] [RAW] ymv pois)
        '''
        nimet = []
        lista = self.uudetsarjat
        self.siivotutnimet = []
        self.Lista_uudet.clear()
        for sarja in lista:
            nimet.append(os.path.basename(sarja))
            self.siivotutnimet.append(pfun.siisti_nimi(os.path.basename(sarja)))
        # Jos anilist-hakuja ei ole vielä pohjustettu, tehdään se nyt.
        # alustetaan tyhjillä listoilla
        if not self.sarjahaut:
            self.sarjahaut = [[] for a in range(len(self.siivotutnimet))]
            # for sarja in self.siivotutnimet:
                # self.sarjahaut.append(anifun.etsi_sarjoja(sarja))
        self.Lista_uudet.addItems(nimet)
        self.Lista_uudet.show()


    def nayta_tiedot_lista(self):
        '''
        Länttää sarjan tiedot oleellisiin kenttiin
        '''
        valittu = self.Lista_uudet.currentRow()
        if valittu != -1 and valittu < len(self.sarjahaut):
            self.kansiopolku.setText(self.uudetsarjat[valittu])
            self.Hakutulokset.clear()
            # Jos sarjaehdokkaita ei ole vielä etsitty, tee haku nyt
            if not self.sarjahaut[valittu]:
                self.setWindowTitle("Etsitään Anilistista ehdokkaita...")
                self.sarjahaut[valittu] = anifun.etsi_sarjoja(self.siivotutnimet[valittu], isanta=self, lukumaara=5)
                self.setWindowTitle("Löytyi uusia sarjoja")
            # Hakutulokset muodossa
            # (sarjannimi, MAL-ID, tyyppi, jaksomäärä)
            nimilista = [a[0] for a in self.sarjahaut[valittu]] # hakutulosten sarjannimet
            self.Hakutulokset.addItems(nimilista)
            if nimilista:
                self.Hakutulokset.setCurrentIndex(0)

    def nayta_tiedot_hakutiedot(self):
        '''
        Näyttää hakutuloksen tiedot, jotta käyttäjä voi ne validoida
        '''
        valittu = self.Lista_uudet.currentRow() # kansio
        valittuehdotus = self.Hakutulokset.currentIndex()
        if valittu != -1 and valittuehdotus != -1:
            sarjan_kansio = self.uudetsarjat[valittu]
            sarjan_nimi   = self.sarjahaut[valittu][valittuehdotus][0]
            sarjan_mal    = self.sarjahaut[valittu][valittuehdotus][1]
            sarjan_tyyppi = self.sarjahaut[valittu][valittuehdotus][2][0]
            sarjan_jaksot = self.sarjahaut[valittu][valittuehdotus][3]

            self.kansiopolku.setText(sarjan_kansio)
            self.MAL_linkki.setText("https://myanimelist.net/anime/{}".format(sarjan_mal))
            self.Sarjan_tiedot.setText("{}, {} jakso{}".format(sarjan_tyyppi, sarjan_jaksot, 'a'*(sarjan_jaksot>1)))

    def lisaamal(self):
        '''
        Käyttäjä lisää oman MAL-linkin tietokenttään.
        Vähän pakko, kun joskus on kansioita joiden nimi on "SP"
        eikä AL-haku semmoisia hevin löydä.
        '''
        valittu = self.Lista_uudet.currentRow()
        if valittu != -1 and self.MAL_linkki.text():
            # Tarkistetaan linkin validius, as in muuntuu kokonaisluvuksi
            malid = self.MAL_linkki.text().split("https://myanimelist.net/anime/")[-1].split("/")[0]
            if all([a.isnumeric() for a in malid]):
                malid = int(malid)
                # Tarkistetaan, ettei ID:n alla ole jotain ehdotetuista sarjoista
                onjolistalla = False
                for e,ehdotus in enumerate(self.sarjahaut[valittu]):
                    if ehdotus[1] == malid:
                        self.Hakutulokset.setCurrentIndex(e)
                        self.nayta_tiedot_hakutiedot()
                        onjolistalla = True
                        break
                if not onjolistalla:
                    uudettiedot = anifun.hae_malidilla(malid)
                    # Jos paluuarvo on järkevä, lisätään listaan
                    # ja asetetaan näkyväksi
                    if uudettiedot[0]:
                        self.sarjahaut[valittu].append(uudettiedot)
                        self.Hakutulokset.addItem(uudettiedot[0])
                        self.Hakutulokset.setCurrentIndex(len(self.sarjahaut[valittu])-1)

    def avaakansio(self):
        '''
        Avaa sarjan kansio jotta käyttäjä voi tiedostoista katsoa
        mikä ihmeen sarja on kyseessä
        '''
        if self.kansiopolku.text():
            subprocess.run(["dolphin", self.kansiopolku.text()], stdin=None, stdout=None, stderr=None)

    def avamal(self):
        '''
        Avaa ehdotetun sarjan MAL-sivu jotta käyttäjä voi katsoa
        näyttääkö se siltä mikä oli mielessä (läh. promokuva)
        '''
        if self.MAL_linkki.text():
            subprocess.run(["firefox", self.MAL_linkki.text()], stdin=None, stdout=None, stderr=None)

    def tamaeiolesarja(self):
        '''
        Poistaa sarjan listalta koska se ei itse asiassa ole kansio piirrossarjalle.
        (näille pitäisi keksiä joku lokaali helvetti ts. tietokanta)
        '''
        valittu = self.Lista_uudet.currentRow()
        if valittu != -1:
            self.Lista_uudet.clearSelection()
            self.Hakutulokset.clear()
            self.kansiopolku.setText("")
            self.MAL_linkki.setText("")
            self.Sarjan_tiedot.setText("")

            # Poistetaan sarjat listoilta
            self.sarjahaut.pop(valittu)
            self.siivotutnimet.pop(valittu)
            self.uudetsarjat.pop(valittu)

            # Signaloi isäntäikkunan suuntaan että tällaisia ei saisi olla
            # todo

            self.kansioita_lista()
            if self.siivotutnimet:
                self.Lista_uudet.setCurrentRow(0)

    def aseta(self):
        '''
        Luo uuden sarjan annettujen tietojen perusteella.
        '''
        valittu = self.Lista_uudet.currentRow()
        valittuehdotus = self.Hakutulokset.currentIndex()
        if valittu != -1 and valittuehdotus != -1:
            # Sarjan tiedot
            sarjan_kansio = self.uudetsarjat[valittu]
            sarjan_nimi   = self.sarjahaut[valittu][valittuehdotus][0]
            sarjan_mal    = self.sarjahaut[valittu][valittuehdotus][1]
            sarjan_tyyppi = self.sarjahaut[valittu][valittuehdotus][2]
            sarjan_jaksot = self.sarjahaut[valittu][valittuehdotus][3]

            sarjatietodikti =  {
                                "nimi":             sarjan_nimi,
                                "tyyppi":           sarjan_tyyppi,
                                "jaksoja":          sarjan_jaksot,
                                "tiedostosijainti": sarjan_kansio,
                                "mal":              "https://myanimelist.net/anime/{}".format(sarjan_mal),
                                "kuvake":           sarjan_mal,
                                "tagit":            []
                                }
            # Jos kansiossa oleva nimi on eri kuin AL-nimi, lisätään aliaksiin
            if self.siivotutnimet[valittu] != sarjan_nimi:
                sarjatietodikti["aliakset"] = [self.siivotutnimet[valittu]]

            # Jos sarjan kansionimessä [RAW], lisää tageihin RAW
            if "[RAW]" in sarjan_kansio:
                sarjatietodikti["tagit"].append("RAW")
            # Jos sarja sijaitsee Aurinkokalalla, se on mitä todennäköisimmin bakaBT-sarja
            # (implementoidaan parempi tarkastusmenettely myöhemmin)
            if "/Aurinkokala/" in sarjan_kansio:
                sarjatietodikti["tagit"].append("bakaBT")

            piirrossarja = cp.Piirretty(sarjatietodikti)
            print(piirrossarja)
            self.maaritetyt.append(piirrossarja)

            # Hoidettu, joten poistetaan listalta ja päivitetään näkymä
            # Kentät ja valinnat veks
            self.Lista_uudet.clearSelection()
            self.Hakutulokset.clear()
            self.kansiopolku.setText("")
            self.MAL_linkki.setText("")
            self.Sarjan_tiedot.setText("")

            # Poistetaan sarjat listoilta
            self.sarjahaut.pop(valittu)
            self.siivotutnimet.pop(valittu)
            self.uudetsarjat.pop(valittu)

            # Listan uusiksitäyttö
            self.kansioita_lista()
            if self.siivotutnimet:
                self.Lista_uudet.setCurrentRow(0)
