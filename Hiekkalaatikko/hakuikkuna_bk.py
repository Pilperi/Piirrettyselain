from PyQt5 import QtCore, QtGui, QtWidgets
import class_piirretyt as cp
import piirrettysijainnit as ps

HAKUKRITEERIT = cp.Hakuparametrit()
NULL = cp.NULL

class Ui_Etsinikkuna(object):
    def setupUi(self, Etsinikkuna):
        font = QtGui.QFont()
        font.setPointSize(12)

        Etsinikkuna.setObjectName("Etsinikkuna")
        Etsinikkuna.resize(535, 325)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Etsinikkuna.sizePolicy().hasHeightForWidth())
        Etsinikkuna.setSizePolicy(sizePolicy)
        Etsinikkuna.setMinimumSize(QtCore.QSize(535, 325))
        Etsinikkuna.setMaximumSize(QtCore.QSize(535, 325))
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

        self.nappi_pilperi = QtWidgets.QPushButton(self.centralwidget)
        self.nappi_pilperi.setGeometry(QtCore.QRect(220, 50, 100, 100))
        self.nappi_pilperi.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
        self.nappi_pilperi.setIconSize(QtCore.QSize(100,100))
        self.nappi_pilperi.clicked.connect(lambda: self.vaihdakuva("Pilperi"))
        # self.nappi_pilperi.setCheckable(True)
        # self.nappi_pilperi.setObjectName("nappi_pilperi")

        self.nappi_haider = QtWidgets.QPushButton(self.centralwidget)
        self.nappi_haider.setGeometry(QtCore.QRect(320, 50, 100, 100))
        self.nappi_haider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
        self.nappi_haider.setIconSize(QtCore.QSize(100,100))
        self.nappi_haider.clicked.connect(lambda: self.vaihdakuva("Haider"))

        self.nappi_lihakunkari = QtWidgets.QPushButton(self.centralwidget)
        self.nappi_lihakunkari.setGeometry(QtCore.QRect(420, 50, 100, 100))
        self.nappi_lihakunkari.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
        self.nappi_lihakunkari.setIconSize(QtCore.QSize(100,100))
        self.nappi_lihakunkari.clicked.connect(lambda: self.vaihdakuva("Lihakunkari"))

        self.nappi_nailo = QtWidgets.QPushButton(self.centralwidget)
        self.nappi_nailo.setGeometry(QtCore.QRect(220, 150, 100, 100))
        self.nappi_nailo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
        self.nappi_nailo.setIconSize(QtCore.QSize(100,100))
        self.nappi_nailo.clicked.connect(lambda: self.vaihdakuva("Nailo"))

        self.nappi_tursake = QtWidgets.QPushButton(self.centralwidget)
        self.nappi_tursake.setGeometry(QtCore.QRect(320, 150, 100, 100))
        self.nappi_tursake.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
        self.nappi_tursake.setIconSize(QtCore.QSize(100,100))
        self.nappi_tursake.clicked.connect(lambda: self.vaihdakuva("Tursake"))

        self.nappi_null = QtWidgets.QPushButton(self.centralwidget)
        self.nappi_null.setGeometry(QtCore.QRect(420, 150, 100, 100))
        self.nappi_null.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.nappi_null.setIcon(QtGui.QIcon(ps.KUVA_NULL_0))
        # self.nappi_null.setIconSize(QtCore.QSize(100,100))
        # self.nappi_null.clicked.connect(lambda: self.vaihdakuva("Null"))

        # Jaksomäärävalitsin
        self.txt_jaksoja = QtWidgets.QLabel(self.centralwidget)
        self.txt_jaksoja.setGeometry(QtCore.QRect(10, 50, 201, 201))
        self.txt_jaksoja.setFont(font)
        self.txt_jaksoja.setFrameShape(QtWidgets.QFrame.Box)
        self.txt_jaksoja.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.txt_jaksoja.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.txt_jaksoja.setObjectName("txt_jaksoja")

        # Jaksoja yli n
        self.txt_yli = QtWidgets.QLabel(self.centralwidget)
        self.txt_yli.setGeometry(QtCore.QRect(20, 100, 21, 31))
        self.txt_yli.setFont(font)
        self.txt_yli.setObjectName("txt_yli")
        self.jaksoja_yli = QtWidgets.QSpinBox(self.centralwidget)
        self.jaksoja_yli.setGeometry(QtCore.QRect(40, 100, 51, 31))
        self.jaksoja_yli.setFont(font)
        self.jaksoja_yli.setMinimum(-1)
        self.jaksoja_yli.setMaximum(127)
        self.jaksoja_yli.setProperty("value", -1)
        self.jaksoja_yli.setObjectName("jaksoja_yli")

        # Jaksoja ali n
        self.txt_ali = QtWidgets.QLabel(self.centralwidget)
        self.txt_ali.setGeometry(QtCore.QRect(120, 100, 31, 31))
        self.txt_ali.setFont(font)
        self.txt_ali.setObjectName("txt_ali")
        self.jaksoja_ali = QtWidgets.QSpinBox(self.centralwidget)
        self.jaksoja_ali.setGeometry(QtCore.QRect(150, 100, 51, 31))
        self.jaksoja_ali.setFont(font)
        self.jaksoja_ali.setMinimum(-1)
        self.jaksoja_ali.setMaximum(127)
        self.jaksoja_ali.setProperty("value", -1)
        self.jaksoja_ali.setObjectName("jaksoja_ali")

        self.txt_eikatsonut = QtWidgets.QLabel(self.centralwidget)
        self.txt_eikatsonut.setGeometry(QtCore.QRect(220, 10, 301, 241))
        self.txt_eikatsonut.setFont(font)
        self.txt_eikatsonut.setFrameShape(QtWidgets.QFrame.Box)
        self.txt_eikatsonut.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.txt_eikatsonut.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.txt_eikatsonut.setObjectName("txt_eikatsonut")

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

        self.txt_tyyppi = QtWidgets.QLabel(self.centralwidget)
        self.txt_tyyppi.setGeometry(QtCore.QRect(10, 150, 201, 101))
        self.txt_tyyppi.setFont(font)
        self.txt_tyyppi.setFrameShape(QtWidgets.QFrame.Box)
        self.txt_tyyppi.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.txt_tyyppi.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.txt_tyyppi.setObjectName("txt_tyyppi")

        self.Etsi = QtWidgets.QPushButton(self.centralwidget)
        self.Etsi.setGeometry(QtCore.QRect(10, 260, 511, 35))
        self.Etsi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Etsi.setText("Etsi")
        self.Etsi.setShortcut("Return")     # normi
        # self.Etsi.setShortcut("Enter")    # kp
        self.Etsi.setObjectName("pushButton")

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

        Etsinikkuna.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Etsinikkuna)
        self.statusbar.setObjectName("statusbar")
        Etsinikkuna.setStatusBar(self.statusbar)

        self.retranslateUi(Etsinikkuna)
        QtCore.QMetaObject.connectSlotsByName(Etsinikkuna)

        self.nimihaku.selectAll()

    def retranslateUi(self, Etsinikkuna):
        _translate = QtCore.QCoreApplication.translate
        Etsinikkuna.setWindowTitle(_translate("Etsinikkuna", "Hakukriteerit"))
        self.txt_yli.setText(_translate("Etsinikkuna", "Yli"))
        self.txt_ali.setText(_translate("Etsinikkuna", "Alle"))
        self.txt_jaksoja.setText(_translate("Etsinikkuna", "Jaksoja"))
        self.txt_eikatsonut.setText(_translate("Etsinikkuna", "Ei ole vielä katsonut"))
        self.txt_tyyppi.setText(_translate("Etsinikkuna", "Tyyppi"))
        self.nimihaku.setText(_translate("Etsinikkuna", "Nimi"))

    def vaihdakuva(self,tyyppi):
        '''
        Vaihtaa jäbän kuvaketta ja muokkaa hakuparametrejä asiaankuuluvasti
        '''
        if tyyppi == "Pilperi":
            print("tyyppi = Pilperi")
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.tyyppi is NULL:
                print("NULLI")
                HAKUKRITEERIT.tyyppi = ["Pilperi"]
                print(HAKUKRITEERIT.tyyppi)
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))
                print(ps.KUVA_PILPERI_1)
            
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Pilperi" in HAKUKRITEERIT.tyyppi:
                HAKUKRITEERIT.tyyppi.remove("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
            
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.tyyppi.append("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))

        elif tyyppi == "Haider":
            print("tyyppi = Haider")
            # Alustamaton tyyppilista
            if HAKUKRITEERIT.tyyppi is NULL:
                print("NULLI")
                HAKUKRITEERIT.tyyppi = ["Haider"]
                print(HAKUKRITEERIT.tyyppi)
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))
                print(ps.KUVA_PILPERI_1)
            
            # Poista kriteereistä ja aseta kuva harmaaksi
            elif "Haider" in HAKUKRITEERIT.tyyppi:
                HAKUKRITEERIT.tyyppi.remove("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
            
            # Lisää kriteereihin
            else:
                HAKUKRITEERIT.tyyppi.append("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Etsinikkuna = QtWidgets.QMainWindow()
    ui = Ui_Etsinikkuna()
    ui.setupUi(Etsinikkuna)
    Etsinikkuna.show()
    sys.exit(app.exec_())
