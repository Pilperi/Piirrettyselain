import time
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import funktiot_piirrettyfunktiot as pfun
import funktiot_kansiofunktiot as kfun

# class Example(QtWidgets.QMainWindow):
class Tarkistuksen_edistyminen(QtWidgets.QDialog):
    def __init__(self, Isantaikkuna):
        super().__init__()
        self.MITAT          = [400,110]
        self.MARGINAALIT    = [10,10]

        # self.reject()
        # Paaikkuna

        self.Isantaikkuna = Isantaikkuna
        self.value = 0

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1], self.MITAT[0]-2*self.MARGINAALIT[0], self.MARGINAALIT[1]))
        self.progressBar.setValue(0)
        self.progressBar.setObjectName("progressBar")

        self.tarkastettava = QtWidgets.QLineEdit(self)
        self.tarkastettava.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1]*3, self.MITAT[0]-2*self.MARGINAALIT[0], 30))
        self.tarkastettava.setAutoFillBackground(False)
        self.tarkastettava.setObjectName("tarkastettava")
        self.tarkastettava.setReadOnly(True)

        self.kansiossa = QtWidgets.QLineEdit(self)
        self.kansiossa.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1]*4+30, self.MITAT[0]-2*self.MARGINAALIT[0], 30))
        self.kansiossa.setObjectName("kansiossa")
        self.kansiossa.setReadOnly(True)

        self.setWindowTitle("Tarkastetaan sarjojen sijainteja...")
        self.resize(self.MITAT[0],self.MITAT[1])
        self.show()

        # Vähän purkkaa vetää ajastimella, mutta tämä on se tapa jolla sain
        # edistysjutun rullaamaan niin että itse ikkunakin on näkyvillä
        self.timer = QtCore.QTimer()
        # self.timer.setInterval(300000)
        self.timer.setInterval(100)
        # self.timer.timeout.connect(self.handleTimer)
        self.timer.timeout.connect(self.tarkasta_puuttuvat)
        self.timer.start(100)
        # self.tarkasta_puuttuvat()
        self.rejected.connect(self.sulje)

    def sulje(self):
        '''
        Mitä tapahtuu kun käyttäjä painaa punaista ruksia (sulkemisen lisäksi)
        '''
        self.timer.stop()
        if self.Isantaikkuna.peruutettiin:
            print("Käyttäjä sulkee ikkunan, päästiin arvoon {}".format(self.value))
        else:
            print("Prosessi saatiin loppuun")


    def tarkasta_puuttuvat(self):
        '''
        Tarkastaa kustakin piirretystä, onko määritelty kansiopolku vielä olemassa.
        '''

        # Katsotaan, olisiko sarjat siirretty jonnekin muualle:
        # yleensä tämä on tehty niin, että kansion nimi pysyy samana mutta sen sijainti on muuttunut
        indeksit = []
        ehdotukset = []
        sarjoja = len(self.Isantaikkuna.SARJAT)
        print(sarjoja)
        self.progressBar.setMaximum(sarjoja)
        for indeksi,sarja in enumerate(self.Isantaikkuna.SARJAT):
            # print(sarja.nimi)
            # print(sarja.tiedostosijainti)
            self.tarkastettava.setText(sarja.nimi)
            self.kansiossa.setText(sarja.tiedostosijainti)
            if not os.path.exists(sarja.tiedostosijainti):
                self.kansiossa.setStyleSheet("background-color: #ff9bbd; color: black; font-weight: bold")
                kansionimi = os.path.basename(sarja.tiedostosijainti)
                ehdokas = ""

                # Käydään tunnetut piirrettykansiot läpi ja katsotaan
                # olisiko siellä kansioita joilla puuttuvan nimi ja jotka eivät ole tietokannassa
                for piirrettykansio in pfun.PIIRRETTYDIKTI:
                    for kansioehdokas in [alikansio for alikansio in kfun.kansion_sisalto(piirrettykansio)[1] if kansionimi in alikansio]:
                        # tarkastetaan, onko sarjalistalla jo kansio jolla saman niminen kansio ja joka ei ole sarja itse
                        # (tavallaan vähän huolestuttavaa jos on sama sarja moneen kertaan)
                        if not any([muusarja.tiedostosijainti == sarja.tiedostosijainti for muusarja in self.Isantaikkuna.SARJAT if muusarja is not sarja]):
                            ehdokas = os.path.join(piirrettykansio, kansioehdokas)
                            break
                    if ehdokas:
                        break
                ehdotukset.append(ehdokas)
                indeksit.append(indeksi)
                print(f"puuttuva: {sarja.tiedostosijainti}")
                print(f"ehdotus:  {ehdokas}")
            else:
                self.kansiossa.setStyleSheet("background-color: #5aff23; color: black")
            self.progressBar.setValue(indeksi)
            self.value = f"{indeksi+1}/{sarjoja}"
        self.Isantaikkuna.muuttuneetindeksit      = indeksit
        self.Isantaikkuna.ehdotukset              = ehdotukset
        self.Isantaikkuna.peruutettiin            = False
        self.close()


    def handleTimer(self):
        '''
        Demo tasaisella eteenpäinrullauksella
        '''
        if self.value < 100:
            time.sleep(0.1)
            self.value += 1
            self.progressBar.setValue(self.value)
            self.tarkastettava.setText(str(self.value))
            self.kansiossa.setText(self.Isantaikkuna)
        else:
            self.value = 100
            self.tarkastettava.setText("Valmis")
            self.kansiossa.setText("Valmis!")
            # self.close()
        
# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication([])
#     Isantaikkuna = "Olen isäntäikkuna"
#     ex = Tarkistuksen_edistyminen(Isantaikkuna)
#     app.exec()
    # sys.exit(app.exec_())