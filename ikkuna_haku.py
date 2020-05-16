from PyQt5 import QtCore, QtGui, QtWidgets
import class_piirretyt as cp
import vakiot_kansiovakiot as kvak
import main_piirrettyselain as piirrettyselain

HAKUKRITEERIT = cp.Hakuparametrit()
NULL = kvak.NULL

MITAT = [535, 365] # ikkunan mitat

class Ui_Etsinikkuna(object):
    def setupUi(self, Etsinikkuna, Isantaikkuna):
    # def setupUi(self, Etsinikkuna):
        font = QtGui.QFont()
        font.setPointSize(12)

        self.isanta = Isantaikkuna

        Etsinikkuna.setObjectName("Etsinikkuna")
        Etsinikkuna.resize(MITAT[0], MITAT[1])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Etsinikkuna.sizePolicy().hasHeightForWidth())
        Etsinikkuna.setSizePolicy(sizePolicy)
        Etsinikkuna.setMinimumSize(QtCore.QSize(MITAT[0], MITAT[1]))
        Etsinikkuna.setMaximumSize(QtCore.QSize(MITAT[0], MITAT[1]))
        Etsinikkuna.setFont(font)
        Etsinikkuna.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Etsinikkuna.setToolTip("")
        Etsinikkuna.setStatusTip("")
        Etsinikkuna.setAccessibleName("")
        Etsinikkuna.setAccessibleDescription("")
        self.centralwidget = QtWidgets.QWidget(Etsinikkuna)
        self.centralwidget.setObjectName("centralwidget")

        self.nimihaku = QtWidgets.QLineEdit(self.centralwidget)
        self.nimihaku.setGeometry(QtCore.QRect(10, 10, 205, 35))
        self.nimihaku.setObjectName("nimihaku")
        self.nimihaku.setClearButtonEnabled(True)

        # Nappulat (näitä on aika monta niin käärin)
        if True:
            self.txt_eikatsonut = QtWidgets.QLabel(self.centralwidget)
            self.txt_eikatsonut.setGeometry(QtCore.QRect(220, 10, 301, 241))
            self.txt_eikatsonut.setFont(font)
            self.txt_eikatsonut.setFrameShape(QtWidgets.QFrame.Box)
            self.txt_eikatsonut.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.txt_eikatsonut.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.txt_eikatsonut.setObjectName("txt_eikatsonut")

            self.nappi_pilperi = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_pilperi.setGeometry(QtCore.QRect(220, 50, 100, 100))
            self.nappi_pilperi.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_pilperi.setIcon(QtGui.QIcon(kvak.KUVA_PILPERI_0))
            self.nappi_pilperi.setIconSize(QtCore.QSize(100,100))
            self.nappi_pilperi.clicked.connect(lambda: self.tyyppihaku("Pilperi"))
            # self.nappi_pilperi.setCheckable(True)
            # self.nappi_pilperi.setObjectName("nappi_pilperi")

            self.nappi_haider = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_haider.setGeometry(QtCore.QRect(320, 50, 100, 100))
            self.nappi_haider.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_haider.setIcon(QtGui.QIcon(kvak.KUVA_HAIDER_0))
            self.nappi_haider.setIconSize(QtCore.QSize(100,100))
            self.nappi_haider.clicked.connect(lambda: self.tyyppihaku("Haider"))

            self.nappi_lihakunkari = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_lihakunkari.setGeometry(QtCore.QRect(420, 50, 100, 100))
            self.nappi_lihakunkari.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_lihakunkari.setIcon(QtGui.QIcon(kvak.KUVA_LIHAKUNKARI_0))
            self.nappi_lihakunkari.setIconSize(QtCore.QSize(100,100))
            self.nappi_lihakunkari.clicked.connect(lambda: self.tyyppihaku("Lihakunkari"))

            self.nappi_nailo = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_nailo.setGeometry(QtCore.QRect(220, 150, 100, 100))
            self.nappi_nailo.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_nailo.setIcon(QtGui.QIcon(kvak.KUVA_NAILO_0))
            self.nappi_nailo.setIconSize(QtCore.QSize(100,100))
            self.nappi_nailo.clicked.connect(lambda: self.tyyppihaku("Nailo"))

            self.nappi_tursake = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_tursake.setGeometry(QtCore.QRect(320, 150, 100, 100))
            self.nappi_tursake.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_tursake.setIcon(QtGui.QIcon(kvak.KUVA_TURSAKE_0))
            self.nappi_tursake.setIconSize(QtCore.QSize(100,100))
            self.nappi_tursake.clicked.connect(lambda: self.tyyppihaku("Tursake"))

            self.nappi_null = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_null.setGeometry(QtCore.QRect(420, 150, 100, 100))
            self.nappi_null.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_null.clicked.connect(lambda: self.tyyppihaku("Null"))
            # self.nappi_null.setIcon(QtGui.QIcon(kvak.KUVA_NULL_0))
            # self.nappi_null.setIconSize(QtCore.QSize(100,100))

        # Teostyypit
        if True:
            self.txt_tyyppi = QtWidgets.QLabel(self.centralwidget)
            self.txt_tyyppi.setGeometry(QtCore.QRect(10, 150, 201, 101))
            self.txt_tyyppi.setFont(font)
            self.txt_tyyppi.setFrameShape(QtWidgets.QFrame.Box)
            self.txt_tyyppi.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.txt_tyyppi.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.txt_tyyppi.setObjectName("txt_tyyppi")

            self.check_TV = QtWidgets.QCheckBox(self.centralwidget)
            self.check_TV.setGeometry(QtCore.QRect(20, 190, 61, 21))
            self.check_TV.setFont(font)
            self.check_TV.setToolTip("")
            self.check_TV.setStatusTip("")
            self.check_TV.setAccessibleName("")
            self.check_TV.setAccessibleDescription("")
            self.check_TV.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.check_TV.setText("TV")
            self.check_TV.setShortcut("")
            self.check_TV.setChecked(True)
            self.check_TV.setObjectName("check_TV")

            self.check_MOV = QtWidgets.QCheckBox(self.centralwidget)
            self.check_MOV.setGeometry(QtCore.QRect(120, 190, 61, 21))
            self.check_MOV.setFont(font)
            self.check_MOV.setToolTip("")
            self.check_MOV.setStatusTip("")
            self.check_MOV.setAccessibleName("")
            self.check_MOV.setAccessibleDescription("")
            self.check_MOV.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.check_MOV.setText("MOV")
            self.check_MOV.setShortcut("")
            self.check_MOV.setChecked(True)
            self.check_MOV.setObjectName("check_MOV")

            self.check_OVA = QtWidgets.QCheckBox(self.centralwidget)
            self.check_OVA.setGeometry(QtCore.QRect(20, 220, 61, 21))
            self.check_OVA.setFont(font)
            self.check_OVA.setToolTip("")
            self.check_OVA.setStatusTip("")
            self.check_OVA.setAccessibleName("")
            self.check_OVA.setAccessibleDescription("")
            self.check_OVA.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.check_OVA.setText("OVA")
            self.check_OVA.setShortcut("")
            self.check_OVA.setChecked(True)
            self.check_OVA.setObjectName("check_TV_3")
     
            self.check_SP = QtWidgets.QCheckBox(self.centralwidget)
            self.check_SP.setGeometry(QtCore.QRect(120, 220, 61, 21))
            self.check_SP.setFont(font)
            self.check_SP.setToolTip("")
            self.check_SP.setStatusTip("")
            self.check_SP.setAccessibleName("")
            self.check_SP.setAccessibleDescription("")
            self.check_SP.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.check_SP.setText("SP")
            self.check_SP.setShortcut("")
            self.check_SP.setChecked(True)
            self.check_SP.setObjectName("check_SP")

        # Jaksomäärävalitsin
        if True:
            self.txt_jaksoja = QtWidgets.QLabel(self.centralwidget)
            self.txt_jaksoja.setGeometry(QtCore.QRect(10, 50, 201, 201))
            self.txt_jaksoja.setFont(font)
            self.txt_jaksoja.setFrameShape(QtWidgets.QFrame.Box)
            self.txt_jaksoja.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.txt_jaksoja.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.txt_jaksoja.setObjectName("txt_jaksoja")

            # Jaksoja yli n
            self.txt_yli = QtWidgets.QLabel(self.centralwidget)
            self.txt_yli.setGeometry(QtCore.QRect(20, 100, 50, 31))
            self.txt_yli.setFont(font)
            self.txt_yli.setObjectName("txt_yli")
            self.jaksoja_yli = QtWidgets.QSpinBox(self.centralwidget)
            self.jaksoja_yli.setGeometry(QtCore.QRect(50, 100, 51, 31))
            self.jaksoja_yli.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.jaksoja_yli.setFont(font)
            self.jaksoja_yli.setMinimum(0)
            self.jaksoja_yli.setMaximum(127)
            self.jaksoja_yli.setProperty("value", 0)
            self.jaksoja_yli.setObjectName("jaksoja_yli")

            # Jaksoja ali n
            self.txt_ali = QtWidgets.QLabel(self.centralwidget)
            self.txt_ali.setGeometry(QtCore.QRect(110, 100, 50, 31))
            self.txt_ali.setFont(font)
            self.txt_ali.setObjectName("txt_ali")
            self.jaksoja_ali = QtWidgets.QSpinBox(self.centralwidget)
            self.jaksoja_ali.setGeometry(QtCore.QRect(150, 100, 51, 31))
            self.jaksoja_ali.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.jaksoja_ali.setFont(font)
            self.jaksoja_ali.setMinimum(0)
            self.jaksoja_ali.setMaximum(127)
            self.jaksoja_ali.setProperty("value", 0)
            self.jaksoja_ali.setObjectName("jaksoja_ali")

        self.Etsi = QtWidgets.QPushButton(self.centralwidget)
        self.Etsi.setGeometry(QtCore.QRect(10, 260, 511, 35))
        self.Etsi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Etsi.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Etsi.setText("Etsi")
        self.Etsi.setShortcut("Return")     # normi
        # self.Etsi.setShortcut("Enter")    # kp
        # self.Etsi.setObjectName("pushButton")
        self.Etsi.clicked.connect(self.hae)

        self.Nollaa = QtWidgets.QPushButton(self.centralwidget)
        self.Nollaa.setGeometry(QtCore.QRect(10, 300, 511, 35))
        self.Nollaa.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Nollaa.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Nollaa.setText("Nollaa")
        self.Nollaa.setShortcut("Esc")     # normi
        self.Nollaa.clicked.connect(self.nollaa)
        # self.Etsi.setShortcut("Enter")    # kp
        # self.Etsi.setObjectName("pushButton")

        # ?
        self.txt_tyyppi.raise_()
        self.txt_jaksoja.raise_()
        self.txt_eikatsonut.raise_()
        self.nappi_lihakunkari.raise_()
        self.nappi_haider.raise_()
        self.nappi_pilperi.raise_()
        self.nappi_tursake.raise_()
        self.nappi_nailo.raise_()
        self.jaksoja_yli.raise_()
        self.txt_yli.raise_()
        self.jaksoja_ali.raise_()
        self.txt_ali.raise_()
        self.check_TV.raise_()
        self.check_OVA.raise_()
        self.check_MOV.raise_()
        self.check_SP.raise_()
        self.nimihaku.raise_()
        self.Etsi.raise_()
        self.nappi_null.raise_()
        self.Nollaa.raise_()

        Etsinikkuna.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Etsinikkuna)
        self.statusbar.setObjectName("statusbar")
        Etsinikkuna.setStatusBar(self.statusbar)

        self.retranslateUi(Etsinikkuna)
        QtCore.QMetaObject.connectSlotsByName(Etsinikkuna)

        self.nimihaku.selectAll()

    def retranslateUi(self, Etsinikkuna):
        _translate = QtCore.QCoreApplication.translate
        Etsinikkuna.setWindowTitle(_translate("Etsinikkuna", "Hae sarjoja"))
        self.txt_yli.setText(_translate("Etsinikkuna", "Väh."))
        self.txt_ali.setText(_translate("Etsinikkuna", "Kork."))
        self.txt_jaksoja.setText(_translate("Etsinikkuna", "Jaksoja"))
        self.txt_eikatsonut.setText(_translate("Etsinikkuna", "Ei ole vielä katsonut"))
        self.txt_tyyppi.setText(_translate("Etsinikkuna", "Tyyppi"))
        self.nimihaku.setText(_translate("Etsinikkuna", "Nimi"))

    def tyyppihaku(self,katsoja):
        '''
        Vaihtaa jäbän kuvaketta ja muokkaa hakuparametrejä asiaankuuluvasti
        '''
        if katsoja == "Pilperi":
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.katsomatta is NULL:
                HAKUKRITEERIT.katsomatta = ["Pilperi"]
                self.nappi_pilperi.setIcon(QtGui.QIcon(kvak.KUVA_PILPERI_1))
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Pilperi" in HAKUKRITEERIT.katsomatta:
                HAKUKRITEERIT.katsomatta.remove("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(kvak.KUVA_PILPERI_0))
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.katsomatta.append("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(kvak.KUVA_PILPERI_1))

        elif katsoja == "Haider":
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.katsomatta is NULL:
                HAKUKRITEERIT.katsomatta = ["Haider"]
                self.nappi_haider.setIcon(QtGui.QIcon(kvak.KUVA_HAIDER_1))
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Haider" in HAKUKRITEERIT.katsomatta:
                HAKUKRITEERIT.katsomatta.remove("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(kvak.KUVA_HAIDER_0))
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.katsomatta.append("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(kvak.KUVA_HAIDER_1))

        elif katsoja == "Lihakunkari":
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.katsomatta is NULL:
                HAKUKRITEERIT.katsomatta = ["Lihakunkari"]
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(kvak.KUVA_LIHAKUNKARI_1))
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Lihakunkari" in HAKUKRITEERIT.katsomatta:
                HAKUKRITEERIT.katsomatta.remove("Lihakunkari")
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(kvak.KUVA_LIHAKUNKARI_0))
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.katsomatta.append("Lihakunkari")
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(kvak.KUVA_LIHAKUNKARI_1))

        elif katsoja == "Nailo":
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.katsomatta is NULL:
                HAKUKRITEERIT.katsomatta = ["Nailo"]
                self.nappi_nailo.setIcon(QtGui.QIcon(kvak.KUVA_NAILO_1))
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Nailo" in HAKUKRITEERIT.katsomatta:
                HAKUKRITEERIT.katsomatta.remove("Nailo")
                self.nappi_nailo.setIcon(QtGui.QIcon(kvak.KUVA_NAILO_0))
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.katsomatta.append("Nailo")
                self.nappi_nailo.setIcon(QtGui.QIcon(kvak.KUVA_NAILO_1))

        elif katsoja == "Tursake":
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.katsomatta is NULL:
                HAKUKRITEERIT.katsomatta = ["Tursake"]
                self.nappi_tursake.setIcon(QtGui.QIcon(kvak.KUVA_TURSAKE_1))
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Tursake" in HAKUKRITEERIT.katsomatta:
                HAKUKRITEERIT.katsomatta.remove("Tursake")
                self.nappi_tursake.setIcon(QtGui.QIcon(kvak.KUVA_TURSAKE_0))
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.katsomatta.append("Tursake")
                self.nappi_tursake.setIcon(QtGui.QIcon(kvak.KUVA_TURSAKE_1))

        # Kaikki päälle/pois
        else:
            # Poista kriteereistä ja aseta kuva harmaaksi
            if HAKUKRITEERIT.katsomatta:
                HAKUKRITEERIT.katsomatta = NULL
                self.nappi_pilperi.setIcon(QtGui.QIcon(kvak.KUVA_PILPERI_0))
                self.nappi_haider.setIcon(QtGui.QIcon(kvak.KUVA_HAIDER_0))
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(kvak.KUVA_LIHAKUNKARI_0))
                self.nappi_nailo.setIcon(QtGui.QIcon(kvak.KUVA_NAILO_0))
                self.nappi_tursake.setIcon(QtGui.QIcon(kvak.KUVA_TURSAKE_0))
            # Lisää kaikki hakukriteereihin (kattaa myös NULL-tapauksen ou jes)
            else:
                HAKUKRITEERIT.katsomatta = ["Pilperi", "Haider", "Lihakunkari", "Nailo", "Tursake"]
                self.nappi_pilperi.setIcon(QtGui.QIcon(kvak.KUVA_PILPERI_1))
                self.nappi_haider.setIcon(QtGui.QIcon(kvak.KUVA_HAIDER_1))
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(kvak.KUVA_LIHAKUNKARI_1))
                self.nappi_nailo.setIcon(QtGui.QIcon(kvak.KUVA_NAILO_1))
                self.nappi_tursake.setIcon(QtGui.QIcon(kvak.KUVA_TURSAKE_1))

    def hae(self):
        '''
        Suorittaa hakutoiminnon
        '''
        global HAKUKRITEERIT

        # Täytä hakukriteerit, tyypit onkin jo hoidettu ruksimisen kautta
        hakudikti = {}
        # Sarjan nimi
        if self.nimihaku.text() and self.nimihaku.text() != "Nimi":
            hakudikti["nimessa"] = self.nimihaku.text()

        # Jaksomäärä
        if self.jaksoja_yli.value() or self.jaksoja_ali.value():
            hakudikti["jaksoja"] = (self.jaksoja_yli.value(), self.jaksoja_ali.value())
        # Teostyyppi
        tyypit = []
        if self.check_TV.isChecked():
            tyypit.append("TV")
        if self.check_OVA.isChecked():
            tyypit.append("OVA")
        if self.check_MOV.isChecked():
            tyypit.append("MOV")
        if self.check_SP.isChecked():
            tyypit.append("SP")
        if tyypit and len(tyypit) < 4:
            hakudikti["tyyppi"] = tyypit

        # Katsoneet: kirjattu jo kliksuttelun yhteydessä
        # (vähän hölmöä takaisinpoimiskelua mut ihsm)
        hakudikti["katsomatta"] = HAKUKRITEERIT.katsomatta
        HAKUKRITEERIT = cp.Hakuparametrit(hakudikti)
        # print(HAKUKRITEERIT)

        # Hae sarjat:
        hakutulos, indeksit = HAKUKRITEERIT.hae_kriteereilla(piirrettyselain.SARJAT)
        print("Löydettiin {} sarjaa".format(len(indeksit)))
        self.isanta.sarjalista.clearSelection()
        self.isanta.KARTOITIN   = indeksit
        self.isanta.sarjannimet(hakutulos)
        if len(indeksit):
            print("Valitse rivi 0")
            self.isanta.sarjalista.setCurrentRow(0)
        self.isanta.nayta_tiedot()

    def nollaa(self):
        '''
        Nollaa hakukriteerit, eli palauttaa listan täydeksi
        '''
        self.isanta.KARTOITIN   = [i for i in range(len(piirrettyselain.SARJAT))]
        self.isanta.sarjannimet(piirrettyselain.SARJAT)
