from PyQt5 import QtCore, QtGui, QtWidgets
import piirrettysijainnit as ps
import class_piirretyt as cp

MITAT = [535, 365] # ikkunan mitat
KATSONEET = []

class Ui_Katsojaikkuna(object):
    def setupUi(self, Katsojaikkuna, Isantaikkuna, sarja):
    # def setupUi(self, Etsinikkuna):
        font = QtGui.QFont()
        font.setPointSize(12)

        self.isanta = Isantaikkuna
        self.katsoneet = []
        self.sarja = sarja

        Katsojaikkuna.setObjectName("Katsoneet")
        Katsojaikkuna.resize(MITAT[0], MITAT[1])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Katsojaikkuna.sizePolicy().hasHeightForWidth())
        Katsojaikkuna.setSizePolicy(sizePolicy)
        Katsojaikkuna.setMinimumSize(QtCore.QSize(MITAT[0], MITAT[1]))
        Katsojaikkuna.setMaximumSize(QtCore.QSize(MITAT[0], MITAT[1]))
        Katsojaikkuna.setFont(font)
        Katsojaikkuna.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        self.centralwidget = QtWidgets.QWidget(Katsojaikkuna)
        self.centralwidget.setObjectName("centralwidget")

        # Nappulat (näitä on aika monta niin käärin)
        if True:
            self.txt_eikatsonut = QtWidgets.QLabel(self.centralwidget)
            self.txt_eikatsonut.setGeometry(QtCore.QRect(20, 10, 301, 201))
            self.txt_eikatsonut.setFont(font)
            self.txt_eikatsonut.setFrameShape(QtWidgets.QFrame.Box)
            self.txt_eikatsonut.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.txt_eikatsonut.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.txt_eikatsonut.setObjectName("txt_eikatsonut")

            self.nappi_pilperi = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_pilperi.setGeometry(QtCore.QRect(20, 10, 100, 100))
            self.nappi_pilperi.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
            self.nappi_pilperi.setIconSize(QtCore.QSize(100,100))
            self.nappi_pilperi.clicked.connect(lambda: self.tyyppihaku("Pilperi"))
            # self.nappi_pilperi.setCheckable(True)
            # self.nappi_pilperi.setObjectName("nappi_pilperi")

            self.nappi_haider = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_haider.setGeometry(QtCore.QRect(120, 10, 100, 100))
            self.nappi_haider.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
            self.nappi_haider.setIconSize(QtCore.QSize(100,100))
            self.nappi_haider.clicked.connect(lambda: self.tyyppihaku("Haider"))

            self.nappi_lihakunkari = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_lihakunkari.setGeometry(QtCore.QRect(220, 10, 100, 100))
            self.nappi_lihakunkari.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
            self.nappi_lihakunkari.setIconSize(QtCore.QSize(100,100))
            self.nappi_lihakunkari.clicked.connect(lambda: self.tyyppihaku("Lihakunkari"))

            self.nappi_nailo = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_nailo.setGeometry(QtCore.QRect(20, 110, 100, 100))
            self.nappi_nailo.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
            self.nappi_nailo.setIconSize(QtCore.QSize(100,100))
            self.nappi_nailo.clicked.connect(lambda: self.tyyppihaku("Nailo"))

            self.nappi_tursake = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_tursake.setGeometry(QtCore.QRect(120, 110, 100, 100))
            self.nappi_tursake.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
            self.nappi_tursake.setIconSize(QtCore.QSize(100,100))
            self.nappi_tursake.clicked.connect(lambda: self.tyyppihaku("Tursake"))

            self.nappi_null = QtWidgets.QPushButton(self.centralwidget)
            self.nappi_null.setGeometry(QtCore.QRect(220, 110, 100, 100))
            self.nappi_null.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_null.clicked.connect(lambda: self.tyyppihaku("Null"))
            # self.nappi_null.setIcon(QtGui.QIcon(ps.KUVA_NULL_0))
            # self.nappi_null.setIconSize(QtCore.QSize(100,100))

        self.Aseta = QtWidgets.QPushButton(self.centralwidget)
        self.Aseta.setGeometry(QtCore.QRect(18, 210, 305, 35))
        self.Aseta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Aseta.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Aseta.setText("Aseta")
        self.Aseta.setShortcut("Return")     # normi
        # self.Etsi.setShortcut("Enter")    # kp
        # self.Etsi.setObjectName("pushButton")
        self.Aseta.clicked.connect(self.aseta)

        self.Peru = QtWidgets.QPushButton(self.centralwidget)
        self.Peru.setGeometry(QtCore.QRect(18, 250, 305, 35))
        self.Peru.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Peru.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Peru.setText("Peru")
        self.Peru.setShortcut("Esc")     # normi
        self.Peru.clicked.connect(self.peru)

        Katsojaikkuna.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Katsojaikkuna)
        self.statusbar.setObjectName("statusbar")
        Katsojaikkuna.setStatusBar(self.statusbar)

        self.retranslateUi(Katsojaikkuna)
        QtCore.QMetaObject.connectSlotsByName(Katsojaikkuna)

        # self.txt_eikatsonut.raise_()

    def retranslateUi(self, Katsojaikkuna):
        _translate = QtCore.QCoreApplication.translate
        Katsojaikkuna.setWindowTitle(_translate("Katsojaikkuna", "Hakukriteerit"))


    def aseta(self):
        pass

    def peru(self):
        pass

    def tyyppihaku(self,katsoja):
        '''
        Vaihtaa jäbän kuvaketta ja muokkaa hakuparametrejä asiaankuuluvasti
        '''
        KATSONEET = self.katsoneet
        print(KATSONEET)
        if katsoja == "Pilperi":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Pilperi" in KATSONEET:
                KATSONEET.remove("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
            # Lisää kriteereihin
            else:
                KATSONEET.append("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))

        elif katsoja == "Haider":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Haider" in KATSONEET:
                KATSONEET.remove("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
            # Lisää kriteereihin
            else:
                KATSONEET.append("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_1))

        elif katsoja == "Lihakunkari":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Lihakunkari" in KATSONEET:
                KATSONEET.remove("Lihakunkari")
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
            # Lisää kriteereihin
            else:
                KATSONEET.append("Lihakunkari")
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_1))

        elif katsoja == "Nailo":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Nailo" in KATSONEET:
                KATSONEET.remove("Nailo")
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
            # Lisää kriteereihin
            else:
                KATSONEET.append("Nailo")
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_1))

        elif katsoja == "Tursake":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Tursake" in KATSONEET:
                KATSONEET.remove("Tursake")
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
            # Lisää kriteereihin
            else:
                KATSONEET.append("Tursake")
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_1))

        # Kaikki päälle/pois
        else:
            # Poista kriteereistä ja aseta kuva harmaaksi
            if KATSONEET:
                KATSONEET = []
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
            # Lisää kaikki hakukriteereihin (kattaa myös NULL-tapauksen ou jes)
            else:
                KATSONEET = ["Pilperi", "Haider", "Lihakunkari", "Nailo", "Tursake"]
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_1))
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_1))
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_1))
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Katsojaikkuna = QtWidgets.QMainWindow()
    ui = Ui_Katsojaikkuna()
    ui.setupUi(Katsojaikkuna, 0, cp.Piirretty())
    Katsojaikkuna.show()
    sys.exit(app.exec_())

